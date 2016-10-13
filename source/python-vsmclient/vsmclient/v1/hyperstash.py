
from vsmclient import base

class Hyperstash(base.Resource):
    """"""
    def __repr__(self):
        return "<HYPERSTASH: %s>" % self.id

    def delete(self):
        """Delete this hyperstash."""
        self.manager.delete(self)

class HyperstashManager(base.ManagerWithFind):
    """
    Manage :class:`HYPERSTASH` resources.
    """

    resource_class = Hyperstash

    def get(self, id):
        return self._get("/hyperstashes/%s" % id, "hs_instance")

    def list(self):
        ret = self._list("/hyperstashes", "hs_instances")
        return ret

    def create(self, hyperstash_instance=None):
        body = {"hs_instance": hyperstash_instance}
        return self._create('/hyperstashes', body, 'hs_instance')

    def delete(self, hs_instance):
        self._delete("/hyperstashes/%s" % base.getid(hs_instance))

    def list_rbds(self, hs_instance_id):
        body = {"hs_instance_id": hs_instance_id}
        return self._list("/hyperstashes/list_rbds", "rbds", body=body)
