
import logging
from oslo.config import cfg

from vsm.openstack.common import rpc
import vsm.openstack.common.rpc.proxy

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


class AgentAPI(vsm.openstack.common.rpc.proxy.RpcProxy):
    """Client side of the agent RPC API"""

    BASE_RPC_API_VERSION = '1.0'

    def __init__(self, topic=None):
        super(AgentAPI, self).__init__(
            topic = topic or CONF.agent_topic,
            default_version=self.BASE_RPC_API_VERSION)

    def update_keyring_admin_from_db(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                    self.make_msg('update_keyring_admin_from_db'),
                    topic)

    def upload_keyring_admin_into_db(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                    self.make_msg('upload_keyring_admin_into_db'),
                topic, version='1.0', timeout=6000)

    def add_osd(self, context, host_id, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                         self.make_msg('add_osd',
                                       host_id=host_id),
                         topic,
                         version='1.0', timeout=6000)

    def add_monitor(self, context, host_id, mon_id, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                         self.make_msg('add_monitor',
                                       mon_id=mon_id,
                                       host_id=host_id),
                         topic,
                         version='1.0', timeout=6000)

    def remove_osd(self, context, host_id, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                         self.make_msg('remove_osd',
                                       host_id=host_id),
                         topic,
                         version='1.0', timeout=6000)

    def remove_monitor(self, context, host_id, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                         self.make_msg('remove_monitor',
                                       host_id=host_id),
                         topic,
                         version='1.0', timeout=6000)

    def remove_mds(self, context, host_id, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                         self.make_msg('remove_mds',
                                       host_id=host_id),
                         topic,
                         version='1.0', timeout=6000)

    def add_mds(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                         self.make_msg('add_mds'),
                         topic,
                         version='1.0', timeout=6000)

    def get_ceph_disk_list(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                         self.make_msg('get_ceph_disk_list',),
                         topic, version='1.0', timeout=6000)

    def get_ceph_config(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                        self.make_msg('get_ceph_config',),
                        topic, version='1.0', timeout=6000)

    def clean_ceph_data(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                         self.make_msg('clean_ceph_data'),
                         topic,
                         version='1.0', timeout=6000)

    def mount_disks(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                         self.make_msg('mount_disks'),
                         topic,
                         version='1.0', timeout=6000)

    def get_ceph_health(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                         self.make_msg('get_ceph_health'),
                         topic, version='1.0', timeout=6000)

    def get_ceph_health_list(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                         self.make_msg('get_ceph_health_list'),
                         topic, version='1.0', timeout=6000)

    def get_osds_total_num(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context, self.make_msg('get_osds_total_num'), topic,
                version='1.0', timeout=6000)
 
    def create_storage_pool(self, ctxt, body=None):
        return self.call(ctxt, self.make_msg('create_storage_pool', body=body))

    def set_crushmap(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('set_crushmap'),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def update_ssh_keys(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('update_ssh_keys'),
                        topic, version='1.0', timeout=6000)
        return res

    def create_crushmap(self, context, server_list, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('create_crushmap',
                                      server_list=server_list),
                        topic, version='1.0', timeout=6000)
        return res

    def add_new_zone(self, context, zone_name, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('add_new_zone',
                                        zone_name=zone_name),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def start_server(self, context, node_id, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('start_server',
                                       node_id=node_id),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def stop_server(self, context, node_id, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('stop_server',
                                       node_id=node_id),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def cluster_refresh(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('cluster_refresh'),
                        topic, version='1.0', timeout=6000)
        return res

    def integrate_cluster_update_status(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('integrate_cluster_update_status'),
                        topic, version='1.0', timeout=6000)
        return res

    def integrate_cluster_sync_osd_states(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('integrate_cluster_sync_osd_states'),
                        topic, version='1.0', timeout=6000)
        return res

    def cluster_id(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                      self.make_msg('cluster_id'),
                  topic, version='1.0', timeout=6000)
        return res

    def update_osd_state(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        self.cast(context, self.make_msg('update_osd_state'), topic)

    def update_pool_state(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context, self.make_msg('update_pool_state'), topic)

    def update_mon_state(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        self.cast(context, self.make_msg('update_mon_health'), topic)

    def set_pool_pg_pgp_num(self, context, host, pool, pg_num, pgp_num):
        topic = rpc.queue_get_for(context, self.topic, host)
        self.cast(context, self.make_msg('set_pool_pg_pgp_num',
                  pool=pool, pg_num=pg_num, pgp_num=pgp_num), topic)

    def update_all_status(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        self.cast(context, self.make_msg('update_all_status'), topic)

    def update_ceph_conf(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        self.cast(context, self.make_msg('update_ceph_conf'), topic)

    def start_osd(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context, self.make_msg('start_osd'), topic,
                        version='1.0', timeout=6000)

    def inital_ceph_osd_db_conf(self, context, server_list,ceph_conf_in_cluster_manifest,host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                         self.make_msg('inital_ceph_osd_db_conf',
                                       server_list=server_list,
                                       ceph_conf_in_cluster_manifest=ceph_conf_in_cluster_manifest),
                         topic,
                         version='1.0',
                         timeout=6000)

    def stop_mds(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context, self.make_msg('stop_mds'), topic,
                        version='1.0', timeout=6000)

    def write_monitor_keyring(self, context, monitor_keyring, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        return self.call(context,
                         self.make_msg('write_monitor_keyring',
                                        monitor_keyring=monitor_keyring),
                         topic,
                         version='1.0', timeout=6000)

    def track_monitors(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('track_monitors'),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def create_keyring(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('create_keyring'),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def prepare_osds(self, context, server_list, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('prepare_osds',
                        server_list=server_list),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def add_cache_tier(self, context, body, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('add_cache_tier',
                                      body=body),
                        topic,
                        version='1.0', timeout=6000)

    def remove_cache_tier(self, context, body, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('remove_cache_tier',
                                      body=body),
                        topic,
                        version='1.0', timeout=6000)

    def start_cluster(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('start_cluster'),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def stop_cluster(self, context, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('stop_cluster'),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def add_new_disks_to_cluster(self, context, body, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('add_new_disks_to_cluster',
                                      body=body),
                        topic,
                        version='1.0', timeout=6000)

    def check_pre_existing_cluster(self, context, body, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('check_pre_existing_cluster',
                                      body=body),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def import_cluster(self, context, body, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('import_cluster',
                                      body=body),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def detect_cephconf(self, context, keyring, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('detect_cephconf',
                                      keyring=keyring),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def detect_crushmap(self, context, keyring, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('detect_crushmap',
                                      keyring=keyring),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def update_zones_from_crushmap_to_db(self, context, body, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('update_zones_from_crushmap_to_db',
                                      body=body),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def update_storage_groups_from_crushmap_to_db(self, context, body, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('update_storage_groups_from_crushmap_to_db',
                                      body=body),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def add_zone_to_crushmap_and_db(self, context, body, host):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context,
                        self.make_msg('add_zone_to_crushmap_and_db',
                                      body=body),
                        topic,
                        version='1.0', timeout=6000)
        return res

    def rgw_create(self, context, name, host, keyring, log_file, rgw_frontends,
                   is_ssl, s3_user_uid, s3_user_display_name, s3_user_email,
                   swift_user_subuser, swift_user_access, swift_user_key_type,
                   multiple_hosts=[]):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context, self.make_msg('rgw_create',
                                               name=name,
                                               host=host,
                                               keyring=keyring,
                                               log_file=log_file,
                                               rgw_frontends=rgw_frontends,
                                               is_ssl=is_ssl,
                                               s3_user_uid=s3_user_uid,
                                               s3_user_display_name=s3_user_display_name,
                                               s3_user_email=s3_user_email,
                                               swift_user_subuser=swift_user_subuser,
                                               swift_user_access=swift_user_access,
                                               swift_user_key_type=swift_user_key_type,
                                               multiple_hosts=multiple_hosts),
                        topic, version='1.0', timeout=6000)
        return res

    def rbd_get_by_rbd_name(self, context, host, rbd_name, pool_name):
        topic = rpc.queue_get_for(context, self.topic, host)
        res = self.call(context, self.make_msg('rbd_get_by_rbd_name',
                                               rbd_name=rbd_name,
                                               pool_name=pool_name),
                        topic, version='1.0', timeout=6000)
        return res
