# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
# Copyright 2014 Intel Corporation, All Rights Reserved.
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


from __future__ import absolute_import

from django.conf import settings

from vsmclient.v1 import client as vsm_client


def vsmclient(request):
    key_vsm_pass = getattr(settings,'KEYSTONE_VSM_SERVICE_PASSWORD')
    key_url = getattr(settings, 'OPENSTACK_KEYSTONE_URL')
    c = vsm_client.Client('vsm',
                          key_vsm_pass,
                          'service',
                          key_url,
                          extensions=[])
    return c


def create_storage_pool(request, body):
    return vsmclient(request).vsms.create_storage_pool(body)


def get_server_list(request):
    return vsmclient(request).servers.list()


def get_server(request, id):
    return vsmclient(request).servers.get(id)


def get_zone_list(request):
    return vsmclient(request).zones.list()


def get_cluster_list(request, opts=None):
    return vsmclient(request).vsms.get_cluster_list()


def create_cluster(request, servers=[]):
    return vsmclient(request).clusters.create(servers=servers)


def vsm_summary(request):
    return vsmclient(request).vsms.summary()


def pool_status(request):
    return vsmclient(request).storage_pools.list(detailed=True)


def list_rbds(request):
    return vsmclient(request).rbd_pools.list()


def list_hs_instances(request):
    return vsmclient(request).hs_instances.list()


def delete_hs_instance(request, hs_instance):
    return vsmclient(request).hs_instances.delete(hs_instance)


def create_hs_instance(request, body):
    return vsmclient(request).hs_instances.create(body)


def list_rbds_on_hs_instance(request, hs_instance_id):
    return vsmclient(request).hs_instances.list_rbds(hs_instance_id)


def list_hs_rbd_cache_configs(request):
    return vsmclient(request).hs_rbd_cache_configs.list()


def get_hs_rbd_cache_config(request, id):
    return vsmclient(request).hs_rbd_cache_configs.get(id)


def get_hs_rbd_cache_config_by_rbd_id(request, rbd_id):
    return vsmclient(request).hs_rbd_cache_configs.get_by_rbd_id(rbd_id)


def update_hs_rbd_cache_config(request, id, info):
    return vsmclient(request).hs_rbd_cache_configs.update(id, info)


def get_hs_performance_metric_value_by_rbd_id_and_type(request, rbd_id, type):
    return vsmclient(request).hs_performance_metrics.get_value(rbd_id, type)
