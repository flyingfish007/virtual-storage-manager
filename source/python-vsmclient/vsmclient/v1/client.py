#  Copyright 2014 Intel Corporation, All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from vsmclient import client
from vsmclient.v1 import vsms
from vsmclient.v1 import clusters
from vsmclient.v1 import zones
from vsmclient.v1 import servers
from vsmclient.v1 import rbd_pools
from vsmclient.v1 import storage_pools
from vsmclient.v1 import hs_instances
from vsmclient.v1 import hs_rbd_cache_configs
from vsmclient.v1 import hs_performance_metrics

class Client(object):
    """
    Top-level object to access the OpenStack Volume API.

    Create an instance with your creds::

        >>> client = Client(USERNAME, PASSWORD, PROJECT_ID, AUTH_URL)

    Then call methods on its managers::

        >>> client.vsms.list()
        ...

    """

    def __init__(self, username, api_key, project_id=None, auth_url='',
                 insecure=False, timeout=None, tenant_id=None,
                 proxy_tenant_id=None, proxy_token=None, region_name=None,
                 endpoint_type='publicURL', extensions=None,
                 service_type='vsm', service_name=None,
                 vsm_service_name=None, retries=None,
                 http_log_debug=False,
                 cacert=None):
        # FIXME(comstud): Rename the api_key argument above when we
        # know it's not being used as keyword argument
        password = api_key

        self.vsms = vsms.VolumeManager(self)
        self.clusters = clusters.ClusterManager(self)
        self.zones = zones.ZoneManager(self)
        self.servers = servers.ServerManager(self)
        self.rbd_pools = rbd_pools.RBDPoolsManager(self)
        self.storage_pools = storage_pools.StoragePoolManager(self)
        self.hs_instances = hs_instances.HsInstanceManager(self)
        self.hs_rbd_cache_configs = hs_rbd_cache_configs.HsRbdCacheConfigManager(self)
        self.hs_performance_metrics = hs_performance_metrics.HsPerformanceMetricManager(self)

        # Add in any extensions...
        if extensions:
            for extension in extensions:
                if extension.manager_class:
                    setattr(self, extension.name,
                            extension.manager_class(self))

        self.client = client.HTTPClient(
            username,
            password,
            project_id,
            auth_url,
            insecure=insecure,
            timeout=timeout,
            tenant_id=tenant_id,
            proxy_token=proxy_token,
            proxy_tenant_id=proxy_tenant_id,
            region_name=region_name,
            endpoint_type=endpoint_type,
            service_type=service_type,
            service_name=service_name,
            vsm_service_name=vsm_service_name,
            retries=retries,
            http_log_debug=http_log_debug,
            cacert=cacert)

    def authenticate(self):
        """
        Authenticate against the server.

        Normally this is called automatically when you first access the API,
        but you can call this method to force authentication right now.

        Returns on success; raises :exc:`exceptions.Unauthorized` if the
        credentials are wrong.
        """
        self.client.authenticate()
