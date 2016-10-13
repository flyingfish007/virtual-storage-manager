
from vsmclient import base

class HsInstance(base.Resource):
    """"""
    def __repr__(self):
        return "<HS_INSTANCE: %s>" % self.id

    def delete(self):
        """Delete this hyperstash instance."""
        self.manager.delete(self)

class HsInstanceManager(base.ManagerWithFind):
    """
    Manage :class:`HS_INSTANCE` resources.
    """

    resource_class = HsInstance

    def get(self, id):
        return self._get("/hs_instances/%s" % id, "hs_instance")

    def list(self):
        ret = self._list("/hs_instances", "hs_instances")
        return ret

    def create(self, hs_instance=None):
        body = {"hs_instance": hs_instance}
        return self._create('/hs_instances', body, 'hs_instance')

    def delete(self, hs_instance):
        self._delete("/hs_instances/%s" % base.getid(hs_instance))

    def list_rbds(self, hs_instance_id):
        body = {"hs_instance_id": hs_instance_id}
        return self._list("/hs_instances/list_rbds", "rbds", body=body)
