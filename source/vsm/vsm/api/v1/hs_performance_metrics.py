
from vsm.api.openstack import wsgi
from vsm import conductor
from vsm.openstack.common import log as logging
from vsm import utils

LOG = logging.getLogger(__name__)


class HsPerformanceMetric(wsgi.Controller):
    """"""

    def __init__(self, ext_mgr):
        self.conductor_api = conductor.API()
        self.ext_mgr = ext_mgr
        super(HsPerformanceMetric, self).__init__()

