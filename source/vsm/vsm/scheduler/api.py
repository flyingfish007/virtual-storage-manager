
from oslo.config import cfg

from vsm.openstack.common import log as logging
from vsm.scheduler import rpcapi

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


class API(object):
    """Scheduler API that does updates via RPC to the SchedulerManager."""

    def __init__(self):
        self.scheduler_rpcapi = rpcapi.SchedulerAPI()

    def create_storage_pool(self, context, body=None):
        return self.scheduler_rpcapi.create_storage_pool(context, body)

    def list_storage_pool(self, context):
        return self.scheduler_rpcapi.list_storage_pool(context)

    def get_storage_group_list(self, context):
        return self.scheduler_rpcapi.get_storage_group_list(context)

    def get_server_list(self, context):
        return self.scheduler_rpcapi.get_server_list(context)

    def add_servers(self, context, body=None):
        return self.scheduler_rpcapi.add_servers(context, body)

    def remove_servers(self, context, body=None):
        return self.scheduler_rpcapi.remove_servers(context, body)

    def get_cluster_list(self, context):
        return self.scheduler_rpcapi.get_server_list(context)

    def create_cluster(self, context, server_list):
        return self.scheduler_rpcapi.create_cluster(context, server_list)

    def integrate_cluster(self, context, server_list=[]):
        return self.scheduler_rpcapi.integrate_cluster(context, server_list)

    def import_cluster(self, context, server_list=[]):
        return self.scheduler_rpcapi.import_cluster(context, server_list)

    def get_zone_list(self, context):
        return self.scheduler_rpcapi.get_server_list(context)

    def add_new_zone(self, context, values):
        return self.scheduler_rpcapi.add_new_zone(context, values)

    def cluster_refresh(self, context):
        return self.scheduler_rpcapi.cluster_refresh(context)

    def add_cache_tier(self, context, body=None):
        return self.scheduler_rpcapi.add_cache_tier(context, body)

    def remove_cache_tier(self, context, body=None):
        return self.scheduler_rpcapi.remove_cache_tier(context, body)

    def import_ceph_conf(self, context, cluster_id, ceph_conf_path):
        return self.scheduler_rpcapi.import_ceph_conf(context, cluster_id, ceph_conf_path)

    def start_cluster(self, context, body=None):
        return self.scheduler_rpcapi.start_cluster(context, body)

    def stop_cluster(self, context, body=None):
        return self.scheduler_rpcapi.stop_cluster(context, body)

    def get_ceph_health_list(self, context, body=None):
        return self.scheduler_rpcapi.get_ceph_health_list(context, body)

    def check_pre_existing_cluster(self,context,body):
        return self.scheduler_rpcapi.check_pre_existing_cluster(context,body)

    def detect_cephconf(self,context,body):
        return self.scheduler_rpcapi.detect_cephconf(context,body)

    def detect_crushmap(self,context,body):
        return self.scheduler_rpcapi.detect_crushmap(context,body)

    def get_crushmap_tree_data(self,context,body):
        return self.scheduler_rpcapi.get_crushmap_tree_data(context,body)

    def add_zone_to_crushmap_and_db(self,context,body):
        return self.scheduler_rpcapi.add_zone_to_crushmap_and_db(context,body)

    def rbd_get_by_rbd_name(self, context, rbd_name, pool_name):
        return self.scheduler_rpcapi.rbd_get_by_rbd_name(context, rbd_name, pool_name)
