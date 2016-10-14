
import webob

from vsm.api.openstack import wsgi
from vsm import conductor

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
        return

    def get_by_rbd_id(self, req):

        context = req.environ['vsm.context']

        search_opts = {}
        search_opts.update(req.GET)
        rbd_id = search_opts.pop('rbd_id')

        hs_rbd_cache_config = \
            self.conductor_api.hs_rbd_cache_config_get_by_rbd_id(context,
                                                                 rbd_id)

        return {'hs_rbd_cache_config': hs_rbd_cache_config}


def create_resource(ext_mgr):
    return wsgi.Resource(HsRbdCacheConfig(ext_mgr))
