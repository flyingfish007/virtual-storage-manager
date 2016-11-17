# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 Intel Inc.
# All Rights Reserved.
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

"""
WSGI middleware for OpenStack Hardware API.
"""

from vsm.api import extensions
import vsm.api.openstack
from vsm.api import versions
from vsm.api.v1 import storage_pool
from vsm.api.v1 import clusters
from vsm.api.v1 import servers
from vsm.api.v1 import zones
from vsm.api.v1 import agents
from vsm.api.v1 import rbd_pools
from vsm.api.v1 import vsms
from vsm.api.v1 import hs_instances
from vsm.api.v1 import hs_rbd_cache_configs
from vsm.api.v1 import hs_performance_metrics

from vsm.openstack.common import log as logging

LOG = logging.getLogger(__name__)

class APIRouter(vsm.api.openstack.APIRouter):
    """
    Routes requests on the OpenStack API to the appropriate controller
    and method.
    """
    ExtensionManager = extensions.ExtensionManager

    def _setup_routes(self, mapper, ext_mgr):
        self.resources['versions'] = versions.create_resource()
        mapper.connect("versions", "/",
                       controller=self.resources['versions'],
                       action='show')

        mapper.redirect("", "/")


        self.resources['storage_pool'] = storage_pool.create_resource(ext_mgr)
        mapper.resource("storage_pool", "storage_pool",
                        controller=self.resources['storage_pool'],
                        collection={'detail': 'get',
                                    'test_scheduler': 'post',
                                    'resource_info':'post',
                                    'create': 'post',
                                    'get_storage_group_list': 'get',
                                    'get_pool_size_list': 'get',
                                    'list_storage_pool': 'get'},
                        member={'action': 'post'})

        # change name from storage_pool to storage_pools
        self.resources['storage_pools'] = storage_pool.create_resource(ext_mgr)
        mapper.resource("storage_pools", "storage_pools",
                        controller=self.resources['storage_pools'],
                        collection={'detail': 'get',
                                    'test_scheduler': 'post',
                                    'resource_info':'post',
                                    'create': 'post',
                                    'get_storage_group_list': 'get',
                                    'get_pool_size_list': 'get',
                                    'get_ec_profile_list': 'get',
                                    'add_cache_tier': 'post',
                                    'remove_cache_tier': 'post',
                                    'list_storage_pool': 'get'},
                        member={'action': 'post'})

        self.resources['clusters'] = clusters.create_resource(ext_mgr)
        mapper.resource("clusters", "clusters",
                        controller=self.resources['clusters'],
                        collection={'summary': 'get',
                                    'refresh': 'post',
                                    'import_ceph_conf': 'post',
                                    'integrate': 'post',
                                    'start_cluster': 'post',
                                    'stop_cluster': 'post',
                                    'get_ceph_health_list':'get',
                                    'check_pre_existing_cluster':'post',
                                    'import_cluster':'post',
                                    'detect_cephconf':'post',
                                    'detect_crushmap':'post',
                                    'get_crushmap_tree_data':'post',
                                    'get_service_list':'get'
                                    },
                        member={'action': 'post'})

        self.resources['servers'] = servers.create_resource(ext_mgr)
        mapper.resource("servers", "servers",
                        controller=self.resources['servers'],
                        collection={"add": "post",
                                    "remove": "post",
                                    "reset_status": "post",
                                    "start": "post",
                                    "stop": "post",
                                    "ceph_upgrade": "post"},
                        member={'action':'post'})

        self.resources['agents'] = agents.create_resource(ext_mgr)
        mapper.resource("agents", "agents",
                        controller=self.resources['agents'],
                        collection={'detail': 'get'},
                        member={'action':'post'})

        self.resources['zones'] = zones.create_resource(ext_mgr)
        mapper.resource("zones", "zones",
                        controller=self.resources['zones'],
                        collection={'osd_locations_choices': 'get',
                                    'get_zone_not_in_crush_list': 'get',
                                    'add_zone_to_crushmap_and_db': 'post',},
                        member={'action':'POST'})


        self.resources['vsms'] = vsms.create_resource(ext_mgr)
        mapper.resource("vsms", "vsms",
                        controller=self.resources['vsms'],
                        collection={"summary": "get"},
                        member={'action':'POST'})


        self.resources['rbd_pools'] = rbd_pools.create_resource(ext_mgr)
        mapper.resource("rbd_pools", "rbd_pools",
                        controller=self.resources['rbd_pools'],
                        collection={"summary": "get",
                                    "detail": "get"},
                        member={'action':'POST'})


        self.resources['hs_instances'] = hs_instances.create_resource(ext_mgr)
        mapper.resource("hs_instances", "hs_instances",
                        controller=self.resources['hs_instances'],
                        collection={
                            'list_rbds': "post"
                        },
                        member={'action': 'post'})

        self.resources['hs_rbd_cache_configs'] = hs_rbd_cache_configs.create_resource(ext_mgr)
        mapper.resource("hs_rbd_cache_configs", "hs_rbd_cache_configs",
                        controller=self.resources['hs_rbd_cache_configs'],
                        collection={
                            'get_by_rbd_id': 'get'
                        },
                        member={'action': 'post'})

        self.resources['hs_performance_metrics'] = hs_performance_metrics.create_resource(ext_mgr)
        mapper.resource("hs_performance_metrics", "hs_performance_metrics",
                        controller=self.resources['hs_performance_metrics'],
                        collection={
                            'get_value': 'get'
                        },
                        member={})
