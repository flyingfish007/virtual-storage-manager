
import webob

from vsm.api.openstack import wsgi
from vsm import conductor
from vsm.openstack.common import log as logging
from vsm import utils

LOG = logging.getLogger(__name__)


class HyperstashController(wsgi.Controller):
    """The Hyperstash API controller for VSM API."""

    def __init__(self, ext_mgr):
        self.conductor_api = conductor.API()
        self.ext_mgr = ext_mgr
        super(HyperstashController, self).__init__()

    def show(self, req, id):

        context = req.environ['vsm.context']

        hs_instance = self.conductor_api.hyperstash_get(context, id)

        return {'hs_instance': hs_instance}

    def index(self, req):

        context = req.environ['vsm.context']

        hyperstash_instances = self.conductor_api.hyperstash_get_all(context)

        return {'hs_instances': hyperstash_instances}

    def create(self, req, body):

        context = req.environ['vsm.context']

        hyperstash_instance = body['hs_instance']
        hs_instance_name = hyperstash_instance['hs_instance_name']
        ip_address = hyperstash_instance['ip_address']
        description = hyperstash_instance['description']

        hostname = utils.execute('su', '-s', '/bin/bash', '-c',
                                 'exec ssh root@%s hostname' % ip_address,
                                 'root', run_as_root=True)[0].strip("\n")
        instance_info = {'hs_instance_name': hs_instance_name,
                         'ip_address': ip_address,
                         'hostname': hostname,
                         'description': description}
        self.conductor_api.hyperstash_create(context, instance_info)
        return webob.Response(status_int=201)

    def delete(self, req, id):

        context = req.environ['vsm.context']

        hs_instance = self.conductor_api.hyperstash_get(context, id)
        self.conductor_api.hyperstash_delete(context, hs_instance['id'])
        return webob.Response(status_int=201)

    def list_rbds(self, req, body):

        context = req.environ['vsm.context']

        hs_instance_id = body.get("hs_instance_id")
        LOG.info("==================hs_instance_id: %s" % hs_instance_id)

        hs_instance = self.conductor_api.hyperstash_get(context, hs_instance_id)
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
            LOG.info("==================rbd image name: %s" % rbd['image'])
            if rbd['image'] in rbds:
                rbd['rbd_name'] = rbd['image']
                rbd['hs_instance_id'] = hs_instance_id
                rbd.pop('image')
                new_rbds.append(rbd)
        return {'rbds': new_rbds}


def create_resource(ext_mgr):
    return wsgi.Resource(HyperstashController(ext_mgr))
