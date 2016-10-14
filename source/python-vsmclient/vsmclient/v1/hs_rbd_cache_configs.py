
import urllib

from vsmclient import base

class HsRbdCacheConfig(base.Resource):
    """"""
    def __repr__(self):
        return "<HS_RBD_CACHE_CONFIG: %s>" % self.id

    def delete(self):
        """Delete this hyperstash rbd cache config."""
        self.manager.delete(self)

class HsRbdCacheConfigManager(base.ManagerWithFind):
    """
    Manage :class:`HS_RBD_CACHE_CONFIG` resources.
    """

    resource_class = HsRbdCacheConfig

    def get(self, id):
        return self._get("/hs_rbd_cache_configs/%s" % id, "hs_rbd_cache_config")

    def list(self):
        ret = self._list("/hs_rbd_cache_configs", "hs_rbd_cache_configs")
        return ret

    def get_by_rbd_id(self, rbd_id):
        qparams = {}
        if rbd_id:
            qparams['rbd_id'] = rbd_id

        query_string = "?%s" % urllib.urlencode(qparams) if qparams else ""

        return self._get("/hs_rbd_cache_configs/get_by_rbd_id%s" %
                         query_string, "hs_rbd_cache_config")

    def update(self, hs_rbd_cache_config, info):
        if not info:
            return

        body = {"hs_rbd_cache_config": info}
        self._update("/hs_rbd_cache_configs/%s" % base.getid(hs_rbd_cache_config), body)
