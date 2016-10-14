
import webob

from vsm.api.openstack import wsgi
from vsm import conductor
from vsm.openstack.common import log as logging
from vsm import utils

LOG = logging.getLogger(__name__)


class HsInstanceController(wsgi.Controller):
    """The Hyperstash Instance API controller for VSM API."""

    def __init__(self, ext_mgr):
        self.conductor_api = conductor.API()
        self.ext_mgr = ext_mgr
        super(HsInstanceController, self).__init__()

    def show(self, req, id):

        context = req.environ['vsm.context']

        hs_instance = self.conductor_api.hs_instance_get(context, id)

        return {'hs_instance': hs_instance}

    def index(self, req):

        context = req.environ['vsm.context']

        hs_instances = self.conductor_api.hs_instance_get_all(context)

        return {'hs_instances': hs_instances}

    def create(self, req, body):

        context = req.environ['vsm.context']

        hs_instance = body['hs_instance']
        hs_instance_name = hs_instance['hs_instance_name']
        ip_address = hs_instance['ip_address']
        description = hs_instance['description']

        hostname = utils.execute('su', '-s', '/bin/bash', '-c',
                                 'exec ssh root@%s hostname' % ip_address,
                                 'root', run_as_root=True)[0].strip("\n")
        hs_instance_info = {'hs_instance_name': hs_instance_name,
                            'ip_address': ip_address,
                            'hostname': hostname,
                            'description': description}
        self.conductor_api.hs_instance_create(context, hs_instance_info)
        return webob.Response(status_int=201)

    def delete(self, req, id):

        context = req.environ['vsm.context']

        hs_instance = self.conductor_api.hs_instance_get(context, id)
        self.conductor_api.hs_instance_delete(context, hs_instance['id'])
        return webob.Response(status_int=201)

    def list_rbds(self, req, body):

        context = req.environ['vsm.context']

        hs_instance_id = body.get("hs_instance_id")
        LOG.info("==================hs_instance_id: %s" % hs_instance_id)

        hs_instance = self.conductor_api.hs_instance_get(context, hs_instance_id)
        rbds_all = self.conductor_api.rbd_get_all(context, None, None, None, None)
        LOG.info("==================rbds from db: %s" % rbds_all)

        ip_address = hs_instance['ip_address']
        rbds_conf = utils.execute('su', '-s', '/bin/bash', '-c',
                                  'exec ssh root@%s ls /etc/rbc' % ip_address,
                                  'root', run_as_root=True)[0].strip("\n").split('\n')
        LOG.info("==================rbds_conf from hyperstash instance: %s" % rbds_conf)
        rbds = []
        for rbd_conf in rbds_conf:
            rbds.append(rbd_conf.split('.')[0])
        LOG.info("==================rbds from hyperstash instance: %s" % rbds)
        new_rbds = []
        for rbd in rbds_all:
            if rbd['image'] in rbds:
                rbd['rbd_name'] = rbd['image']
                rbd['hs_instance_id'] = hs_instance_id
                rbd.pop('image')
                new_rbds.append(rbd)
                utils.execute('su', '-s', '/bin/bash', '-c',
                              'exec scp root@%s:/etc/rbc/%s.conf /tmp' %
                              (ip_address, rbd['rbd_name']),
                              'root', run_as_root=True)
                utils.execute('chown', 'vsm:vsm', '/tmp/%s.conf' % rbd['rbd_name'],
                              run_as_root=True)
        for rbd in new_rbds:
            new_hs_rbd_cache_config = {}
            with open('/tmp/%s.conf' % rbd['rbd_name']) as file:
                for line in file.readlines():
                    try:
                        value = line.split('=')[1].strip('\n')
                    except:
                        value = None
                    if "cache_dir=" in line:
                        new_hs_rbd_cache_config['cache_dir'] = value
                    elif "clean_start=" in line:
                        new_hs_rbd_cache_config['clean_start'] = value
                    elif "enable_MemoryUsageTracker=" in line:
                        enable_memory_usage_tracker = value
                        if enable_memory_usage_tracker == "true":
                            new_hs_rbd_cache_config['enable_memory_usage_tracker'] = True
                        else:
                            new_hs_rbd_cache_config['enable_memory_usage_tracker'] = False
                    elif "object_size=" in line:
                        new_hs_rbd_cache_config['object_size'] = value
                    elif "cache_total_size=" in line:
                        new_hs_rbd_cache_config['cache_total_size'] = value
                    elif "cache_dirty_ratio_min=" in line:
                        new_hs_rbd_cache_config['cache_dirty_ratio_min'] = value
                    elif "cache_dirty_ratio_max=" in line:
                        new_hs_rbd_cache_config['cache_dirty_ratio_max'] = value
                    elif "cache_ratio_health=" in line:
                        new_hs_rbd_cache_config['cache_ratio_health'] = value
                    elif "cache_ratio_max=" in line:
                        new_hs_rbd_cache_config['cache_ratio_max'] = value
                    elif "cache_flush_interval=" in line:
                        new_hs_rbd_cache_config['cache_flush_interval'] = value
                    elif "cache_evict_interval=" in line:
                        new_hs_rbd_cache_config['cache_evict_interval'] = value
                    elif "cache_flush_queue_depth=" in line:
                        new_hs_rbd_cache_config['cache_flush_queue_depth'] = value
                    elif "agent_threads_num=" in line:
                        new_hs_rbd_cache_config['agent_threads_num'] = value
                    elif "cacheservice_threads_num=" in line:
                        new_hs_rbd_cache_config['cache_service_threads_num'] = value
                new_hs_rbd_cache_config['hs_instance_id'] = int(hs_instance_id)
                new_hs_rbd_cache_config['rbd_id'] = int(rbd['id'])
                hs_rbd_cache_config = \
                    self.conductor_api.hs_rbd_cache_config_get_by_rbd_id(context,
                                                                         int(rbd['id']))
                if hs_rbd_cache_config:
                    self.conductor_api.\
                        hs_rbd_cache_config_update(context,
                                                   hs_rbd_cache_config['id'],
                                                   new_hs_rbd_cache_config)
                else:
                    self.conductor_api.\
                        hs_rbd_cache_config_create(context, new_hs_rbd_cache_config)
                file.close()
        return {'rbds': new_rbds}


def create_resource(ext_mgr):
    return wsgi.Resource(HsInstanceController(ext_mgr))
