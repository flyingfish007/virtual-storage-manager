
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

    def get_value(self, req):

        context = req.environ['vsm.context']

        rbd_id = req.GET['rbd_id']
        rbd = self.conductor_api.rbd_get(context, rbd_id)
        rbd_name = rbd['image']

        values = self.conductor_api.hs_performance_metric_get(context, rbd_name)
        new_values_list = []
        for value in values:
            if value not in new_values_list:
                new_values_list.append(value)
            else:
                break

        result = []
        type = req.GET['type']
        if type == "cache_size":
            new_value = {}
            cache_used_size = None
            cache_dirty_size = None
            for new_value in new_values_list:
                metric = new_value['metric']
                if metric == 'cache_used_size':
                    result.append(new_value)
                    cache_used_size = new_value['value']
                elif metric == 'cache_dirty_size':
                    result.append(new_value)
                    cache_dirty_size = new_value['value']
            hs_rbd_cache_config = \
                self.conductor_api.hs_rbd_cache_config_get_by_rbd_id(context, rbd_id)
            cache_free_size = int(hs_rbd_cache_config['cache_total_size']) - int(cache_used_size)
            cache_clean_size = int(cache_used_size) - int(cache_dirty_size)
            new_value['metric'] = 'cache_free_size'
            new_value['value'] = cache_free_size
            result.append(new_value)
            new_value['metric'] = 'cache_clean_size'
            new_value['value'] = cache_clean_size
            result.append(new_value)
        elif type == "cache_action":
            pass
        elif type == "cache_iops":
            pass
        elif type == "cache_bw":
            pass
        elif type == "cache_latency":
            pass
        return {'hs_performance_metrics': result}

def create_resource(ext_mgr):
    return wsgi.Resource(HsPerformanceMetric(ext_mgr))
