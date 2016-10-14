
import webob

from vsm.api.openstack import wsgi
from vsm import conductor
from vsm.openstack.common import log as logging
from vsm import utils

LOG = logging.getLogger(__name__)


class HsRbdCacheConfig(wsgi.Controller):
    """The Hyperstash Rbd Cache Config API controller for VSM API."""

    def __init__(self, ext_mgr):
        self.conductor_api = conductor.API()
        self.ext_mgr = ext_mgr
        super(HsRbdCacheConfig, self).__init__()

    def show(self, req, id):

        context = req.environ['vsm.context']

        hs_rbd_cache_config = self.conductor_api.hs_rbd_cache_config_get(context, id)

        return {'hs_rbd_cache_config': hs_rbd_cache_config}

    def index(self, req):

        context = req.environ['vsm.context']

        hs_rbd_cache_configs = self.conductor_api.hs_rbd_cache_config_get_all(context)

        return {'hs_rbd_cache_configs': hs_rbd_cache_configs}

    def create(self, req, body):

        context = req.environ['vsm.context']

        hs_rbd_cache_config = body['hs_rbd_cache_config']

        self.conductor_api.hs_rbd_cache_config_create(context, hs_rbd_cache_config)

        return webob.Response(status_int=201)

    def delete(self, req, id):
        return

    def update(self, req, id, body):

        context = req.environ['vsm.context']

        hs_rbd_cache_config = body['hs_rbd_cache_config']
        cache_dir = hs_rbd_cache_config['cache_dir']
        clean_start = hs_rbd_cache_config['clean_start']
        enable_memory_usage_tracker = hs_rbd_cache_config['enable_memory_usage_tracker']
        object_size = hs_rbd_cache_config['object_size']
        cache_total_size = hs_rbd_cache_config['cache_total_size']
        cache_dirty_ratio_min = hs_rbd_cache_config['cache_dirty_ratio_min']
        cache_dirty_ratio_max = hs_rbd_cache_config['cache_dirty_ratio_max']
        cache_ratio_health = hs_rbd_cache_config['cache_ratio_health']
        cache_ratio_max = hs_rbd_cache_config['cache_ratio_max']
        cache_flush_interval = hs_rbd_cache_config['cache_flush_interval']
        cache_evict_interval = hs_rbd_cache_config['cache_evict_interval']
        cache_flush_queue_depth = hs_rbd_cache_config['cache_flush_queue_depth']
        agent_threads_num = hs_rbd_cache_config['agent_threads_num']
        cache_service_threads_num = hs_rbd_cache_config['cache_service_threads_num']

        hs_rbd_cache_config_db = self.conductor_api.hs_rbd_cache_config_get(context, id)
        hs_instance_id = hs_rbd_cache_config_db['hs_instance_id']
        hs_instance = self.conductor_api.hs_instance_get(context, hs_instance_id)
        ip_address = hs_instance['ip_address']

        rbd_id = hs_rbd_cache_config_db['rbd_id']
        rbd = self.conductor_api.rbd_get(context, rbd_id)
        rbd_name = rbd['image']

        utils.execute('su', '-s', '/bin/bash', '-c',
                      'exec scp root@%s:/etc/rbc/%s.conf /tmp' % (ip_address, rbd_name),
                      'root', run_as_root=True)
        utils.execute('chown', 'vsm:vsm', '/tmp/%s.conf' % rbd_name,
                      run_as_root=True)

        rbd_conf = rbd_template_conf
        rbd_conf = rbd_conf.replace("%cache_dir%", cache_dir)
        rbd_conf = rbd_conf.replace("%clean_start%", clean_start)
        rbd_conf = rbd_conf.replace("%enable_MemoryUsageTracker%", enable_memory_usage_tracker)
        rbd_conf = rbd_conf.replace("%object_size%", object_size)
        rbd_conf = rbd_conf.replace("%cache_total_size%", cache_total_size)
        rbd_conf = rbd_conf.replace("%cache_dirty_ratio_min%", cache_dirty_ratio_min)
        rbd_conf = rbd_conf.replace("%cache_dirty_ratio_max%", cache_dirty_ratio_max)
        rbd_conf = rbd_conf.replace("%cache_ratio_health%", cache_ratio_health)
        rbd_conf = rbd_conf.replace("%cache_ratio_max%", cache_ratio_max)
        rbd_conf = rbd_conf.replace("%cache_flush_interval%", cache_flush_interval)
        rbd_conf = rbd_conf.replace("%cache_evict_interval%", cache_evict_interval)
        rbd_conf = rbd_conf.replace("%cache_flush_queue_depth%", cache_flush_queue_depth)
        rbd_conf = rbd_conf.replace("%agent_threads_num%", agent_threads_num)
        rbd_conf = rbd_conf.replace("%cacheservice_threads_num%", cache_service_threads_num)
        with open("/tmp/%s.conf" % rbd_name, "w") as file:
            file.write(rbd_conf)
            file.close()

        LOG.info("==================rbd_conf: %s" % str(rbd_conf))
        utils.execute('su', '-s', '/bin/bash', '-c',
                      'exec scp /tmp/%s.conf root@%s:/etc/rbc/' % (rbd_name, ip_address),
                      'root', run_as_root=True)

        if hs_rbd_cache_config['enable_memory_usage_tracker'] == "false":
            hs_rbd_cache_config['enable_memory_usage_tracker'] = False
        else:
            hs_rbd_cache_config['enable_memory_usage_tracker'] = True
        self.conductor_api.hs_rbd_cache_config_update(context, id, hs_rbd_cache_config)

    def get_by_rbd_id(self, req):

        context = req.environ['vsm.context']

        search_opts = {}
        search_opts.update(req.GET)
        rbd_id = search_opts.pop('rbd_id')

        hs_rbd_cache_config = \
            self.conductor_api.hs_rbd_cache_config_get_by_rbd_id(context, rbd_id)

        return {'hs_rbd_cache_config': hs_rbd_cache_config}


def create_resource(ext_mgr):
    return wsgi.Resource(HsRbdCacheConfig(ext_mgr))

rbd_template_conf = """
# Each RBD image has its own configuration file.
# e.g., RBD named testimage -> /etc/rbc/testimage.conf
[global]

cache_dir=%cache_dir%
# a blob file with cache_total_size would be created
# also there will be two directories created:
# meta: rocksdb contains the metadata
# run: rocksdb contains blob file usage
# you may want to mount your SSD to this dir

clean_start=%clean_start%
# if reload metadata from rocksdb then start

enable_MemoryUsageTracker=%enable_MemoryUsageTracker%
object_size=%object_size%
cache_total_size=%cache_total_size%
cache_dirty_ratio_min=%cache_dirty_ratio_min%
cache_dirty_ratio_max=%cache_dirty_ratio_max%
cache_ratio_health=%cache_ratio_health%
cache_ratio_max=%cache_ratio_max%
cache_flush_interval=%cache_flush_interval%
cache_evict_interval=%cache_evict_interval%
cache_flush_queue_depth=%cache_flush_queue_depth%
agent_threads_num=%agent_threads_num%
cacheservice_threads_num=%cacheservice_threads_num%

"""