
import webob

from vsm.api.openstack import wsgi
from vsm import conductor
from vsm import utils

class HyperstashController(wsgi.Controller):
    """The Hyperstash API controller for VSM API."""

    def __init__(self, ext_mgr):
        self.conductor_api = conductor.API()
        self.ext_mgr = ext_mgr
        super(HyperstashController, self).__init__()

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

    def list_rbds(self, req, hs_instance_id):

        context = req.environ['vsm.context']

        hs_instance = self.conductor_api.hyperstash_get(context, hs_instance_id)

        rbds_all = self.conductor_api.rbd_get_all(context)

def create_resource(ext_mgr):
    return wsgi.Resource(HyperstashController(ext_mgr))
