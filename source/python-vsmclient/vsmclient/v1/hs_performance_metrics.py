
import urllib

from vsmclient import base

class HsPerformanceMetric(base.Resource):
    """"""
    def __repr__(self):
        return "<HS_PERFORMANCE_METRIC: %s>" % self.id

    def delete(self):
        """Delete this hyperstash performance metric."""
        self.manager.delete(self)

class HsPerformanceMetricManager(base.ManagerWithFind):
    """
    Manage :class:`HS_PERFORMANCE_METRIC` resources.
    """

    resource_class = HsPerformanceMetric

    def get_value(self, rbd_id, type):
        qparams = {}
        if rbd_id:
            qparams['rbd_id'] = rbd_id
        if type:
            qparams['type'] = type

        query_string = "?%s" % urllib.urlencode(qparams) if qparams else ""

        return self._get("/hs_performance_metrics/get_value%s" %
                         query_string, "hs_performance_metrics")
