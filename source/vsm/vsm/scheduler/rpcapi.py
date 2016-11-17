
import logging
from oslo.config import cfg

import vsm.openstack.common.rpc.proxy

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


class SchedulerAPI(vsm.openstack.common.rpc.proxy.RpcProxy):
    """Client side of the scheduler RPC API"""

    BASE_RPC_API_VERSION = '1.0'

    def __init__(self, topic=None):
        super(SchedulerAPI, self).__init__(
            topic = topic or CONF.scheduler_topic,
            default_version=self.BASE_RPC_API_VERSION)

    def create_storage_pool(self, ctxt, body=None):
        return self.call(ctxt, self.make_msg('create_storage_pool', body=body))

    def add_cache_tier(self, ctxt, body=None):
        return self.call(ctxt, self.make_msg('add_cache_tier', body=body))

    def remove_cache_tier(self, ctxt, body=None):
        return self.call(ctxt, self.make_msg('remove_cache_tier', body=body))

    def list_storage_pool(self, ctxt):
        ret = self.call(ctxt, self.make_msg('list_storage_pool'))
        return ret

    def get_storage_group_list(self, ctxt):
        ret = self.call(ctxt, self.make_msg('get_storage_group_list'))
        return ret

    def get_server_list(self, ctxt):
        ret = self.call(ctxt, self.make_msg('get_server_list'))
        return ret

    def add_servers(self, ctxt, body=None):
        ret = self.cast(ctxt, self.make_msg('add_servers', body=body))
        return ret

    def remove_servers(self, ctxt, body=None):
        ret = self.cast(ctxt, self.make_msg('remove_servers', body=body))
        return ret

    def create_cluster(self, context, server_list):
        ret = self.cast(context,
                        self.make_msg('create_cluster',
                                      server_list=server_list))
        return ret

    def integrate_cluster(self, context, server_list):
        ret = self.cast(context,
                        self.make_msg('integrate_cluster',
                                      server_list=server_list))
        return ret

    def add_new_zone(self, ctxt, values):
        ret = self.call(ctxt, self.make_msg('add_new_zone', values=values))
        return ret

    def cluster_refresh(self, ctxt):
        ret = self.call(ctxt, self.make_msg('cluster_refresh'),
                        version='1.0', timeout=6000)
        return ret

    def import_ceph_conf(self, context, cluster_id, ceph_conf_path):
        ret = self.call(context,
                        self.make_msg('import_ceph_conf',
                                      cluster_id=cluster_id, ceph_conf_path=ceph_conf_path))
        return ret

    def start_server(self, context, body=None):
        ret = self.call(context,
                        self.make_msg('start_server',
                                      body=body))
        return ret

    def stop_server(self, context, body=None):
        ret = self.call(context,
                        self.make_msg('stop_server',
                                      body=body))
        return ret

    def start_cluster(self, context, body=None):
        ret = self.call(context,
                        self.make_msg('start_cluster',
                                      body=body))
        return ret

    def stop_cluster(self, context, body=None):
        ret = self.call(context,
                        self.make_msg('stop_cluster',
                                      body=body))
        return ret

    def get_ceph_health_list(self, ctxt, body=None):
        return self.call(ctxt, self.make_msg('get_ceph_health_list', body=body))

    def check_pre_existing_cluster(self,ctxt,body):
        return self.call(ctxt, self.make_msg('check_pre_existing_cluster', body=body))

    def import_cluster(self,ctxt,body):
        return self.call(ctxt, self.make_msg('import_cluster', body=body),timeout=6000)

    def detect_cephconf(self,ctxt,body):
        return self.call(ctxt, self.make_msg('detect_cephconf', body=body))

    def detect_crushmap(self,ctxt,body):
        return self.call(ctxt, self.make_msg('detect_crushmap', body=body))

    def get_crushmap_tree_data(self,ctxt,body):
        return self.call(ctxt, self.make_msg('get_crushmap_tree_data', body=body))

    def add_zone_to_crushmap_and_db(self,ctxt,body):
        return self.call(ctxt, self.make_msg('add_zone_to_crushmap_and_db', body=body))

    def rbd_get_by_rbd_name(self, ctxt, rbd_name, pool_name):
        return self.call(ctxt, self.make_msg('rbd_get_by_rbd_name',
                                             rbd_name=rbd_name,
                                             pool_name=pool_name))
