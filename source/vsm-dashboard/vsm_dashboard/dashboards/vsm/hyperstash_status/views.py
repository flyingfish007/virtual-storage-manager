
import json
import logging
import time

from vsm_dashboard.api import vsm as vsmapi

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from horizon import forms
from horizon import tables

from .forms import ConfigRbdForm
from .tables import ListHyperstashInstanceTable
from .tables import ListRbdTable

LOG = logging.getLogger(__name__)


class IndexView(tables.DataTableView):
    table_class = ListHyperstashInstanceTable
    template_name = 'vsm/hyperstash_status/index.html'

    def get_data(self):
        hs_instance_list = vsmapi.list_hs_instances(self.request)
        return hs_instance_list

class CreateView(TemplateView):
    template_name = 'vsm/hyperstash_status/create.html'
    success_url = reverse_lazy('horizon:vsm:hyperstash_status:index')

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        return context

def create_hs_instance(request):
    body = json.loads(request.body)
    hs_instance = body['hs_instance']
    vsmapi.create_hs_instance(request, hs_instance)
    status = "OK"
    msg = "succeed to create hs instance"
    resp = dict(message=msg, status=status)
    resp = json.dumps(resp)
    return HttpResponse(resp)

class RbdListView(tables.DataTableView):
    table_class = ListRbdTable
    verbose_name = "List RBD"
    template_name = 'vsm/hyperstash_status/list_rbd.html'

    def get_data(self):
        LOG.info("=========================RBD LIST VIEW: %s" % self.kwargs)
        hs_instance_id = self.kwargs["hs_instance_id"]
        rbd_list = vsmapi.list_rbds_on_hs_instance(self.request, hs_instance_id)
        for rbd in rbd_list:
            rbd.size = rbd.size / 1024 / 1024
        return rbd_list

class ConfigRbdView(forms.ModalFormView):
    form_class = ConfigRbdForm
    template_name = 'vsm/hyperstash_status/config_rbd.html'

    def get_object(self):
        LOG.info("=========================OBJECT CONFIG RBD VIEW: %s" % self.kwargs)
        rbd_config = vsmapi.get_hs_rbd_cache_config_by_rbd_id(self.request,
                                                              self.kwargs['rbd_id'])
        LOG.info("=========================rbd_config: %s" % str(rbd_config))
        rbd_config = {
            'id': rbd_config.id,
            'cache_dir': rbd_config.cache_dir,
            'clean_start': rbd_config.clean_start,
            'enable_memory_usage_tracker': rbd_config.enable_memory_usage_tracker,
            'object_size': rbd_config.object_size,
            'cache_total_size': rbd_config.cache_total_size,
            'cache_dirty_ratio_min': rbd_config.cache_dirty_ratio_min,
            "cache_dirty_ratio_max": rbd_config.cache_dirty_ratio_max,
            "cache_ratio_health": rbd_config.cache_ratio_health,
            "cache_ratio_max": rbd_config.cache_ratio_max,
            "cache_flush_interval": rbd_config.cache_flush_interval,
            "cache_evict_interval": rbd_config.cache_evict_interval,
            "cache_flush_queue_depth": rbd_config.cache_flush_queue_depth,
            "agent_threads_num": rbd_config.agent_threads_num,
            "cache_service_threads_num": rbd_config.cache_service_threads_num,
            "hs_instance_id": rbd_config.hs_instance_id
        }
        return rbd_config

    def get_context_data(self, **kwargs):
        context = super(ConfigRbdView, self).get_context_data(**kwargs)
        context['rbd_config'] = self.get_object()
        return context

    def get_initial(self):
        LOG.info("=========================INITIAL CONFIG RBD VIEW: %s" % self.kwargs)
        rbd_config = self.get_object()
        return rbd_config

def update_action(request):
    data = json.loads(request.body)
    try:
        id = data.pop('id')
        vsmapi.update_hs_rbd_cache_config(request, id, data)
        status = "OK"
        msg = "Update Hyperstash Rbd Cache Config Successfully!"
    except:
        status = "Failed"
        msg = "Update Hyperstash Rbd Cache Config Failed!"

    resp = dict(message=msg, status=status)
    resp = json.dumps(resp)
    return HttpResponse(resp)

def monitor(request, rbd_id):
    LOG.info("=========================rbd_id: %s" % str(rbd_id))
    rbds = vsmapi.list_rbds(request)
    rbd_name = None
    for rbd in rbds:
        if int(rbd.id) == int(rbd_id):
            rbd_name = rbd.image_name
            break
    return render(request,
                  'vsm/hyperstash_status/monitor.html',
                  {"rbd_id": rbd_id,
                   "rbd_name": rbd_name})

def cache_ratio(request, rbd_id):
    result = vsmapi.\
        get_hs_performance_metric_value_by_rbd_id_and_type(request, rbd_id, "cache_size")
    cache_ratio = {}
    for i in result:
        if i.metric == 'cache_free_size':
            cache_ratio['cache_free_size'] = i.value
        elif i.metric == 'cache_used_size':
            cache_ratio['cache_used_size'] = i.value
        elif i.metric == 'cache_clean_size':
            cache_ratio['cache_clean_size'] = i.value
        elif i.metric == 'cache_dirty_size':
            cache_ratio['cache_dirty_size'] = i.value
    cache_ratio = json.dumps(cache_ratio)
    return HttpResponse(cache_ratio)

def cache_action(request, rbd_id):
    result = vsmapi.\
        get_hs_performance_metric_value_by_rbd_id_and_type(request, rbd_id, "cache_action")
    cache_action = {}
    cache_action['date'] = []
    cache_action['cache_promote'] = []
    cache_action['cache_flush'] = []
    cache_action['cache_evict'] = []
    for i in result:
        value = i.value
        timestr = i.timestamp
        timearry = time.localtime(timestr)
        timestyle = time.strftime("%H:%M:%S", timearry)
        if timestyle not in cache_action['date']:
            cache_action['date'].append(timestyle)
        if i.metric == "cache_promote":
            cache_action['cache_promote'].append(value)
        elif i.metric == "cache_flush":
            cache_action['cache_flush'].append(value)
        elif i.metric == "cache_evict":
            cache_action['cache_evict'].append(value)
    cache_action = json.dumps(cache_action)
    return HttpResponse(cache_action)

def cache_io_workload(request, rbd_id):
    result = vsmapi.\
        get_hs_performance_metric_value_by_rbd_id_and_type(request, rbd_id, "cache_io_workload")

    cache_io_workload = {}
    for i in result:
        if i.metric == "cache_read":
            cache_io_workload['cache_read'] = i.value
        elif i.metric == "cache_read_miss":
            cache_io_workload['cache_read_miss'] = i.value
        elif i.metric == "cache_write":
            cache_io_workload['cache_write'] = i.value
        elif i.metric == "cache_write_miss":
            cache_io_workload['cache_write_miss'] = i.value
        elif i.metric == "cache_bw":
            cache_io_workload['cache_bw'] = i.value
        elif i.metric == "cache_latency":
            cache_io_workload['cache_latency'] = i.value

    cache_io_workload = json.dumps(cache_io_workload)
    return HttpResponse(cache_io_workload)

def get_rbd_basic_info(request, rbd_id):
    result = vsmapi.\
        get_hs_performance_metric_value_by_rbd_id_and_type(request, rbd_id, "rbd_basic_info")
    rbd = result[0]
    rbd_basic_info = {}
    rbd_basic_info['name'] = rbd.name
    rbd_basic_info['size'] = rbd.size
    rbd_basic_info['objects'] = rbd.objects
    rbd_basic_info['order'] = rbd.order
    rbd_basic_info['object_size'] = rbd.object_size
    rbd_basic_info['block_name_prefix'] = rbd.block_name_prefix
    rbd_basic_info['format'] = rbd.format
    feature = rbd.features
    f_str = ''
    for _feature in feature:
        if not f_str:
            f_str = _feature
        else:
            f_str = f_str + ',' + _feature
    rbd_basic_info['features'] = f_str
    flags = rbd.flags
    f_flag = ''
    for _flag in flags:
        if not f_flag:
            f_flag = _flag
        else:
            f_flag = f_flag + ',' + _flag
    rbd_basic_info['flags'] = f_flag
    rbd_basic_info = json.dumps(rbd_basic_info)
    return HttpResponse(rbd_basic_info)
