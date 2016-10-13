
import json
import logging

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
        hs_instance_list = vsmapi.list_hyperstash_instances(self.request)
        return hs_instance_list

        # hs_instance_str = open("/opt/hyperstash_instances.json").read()
        # hs_instance_json = json.loads(hs_instance_str)
        # hs_instance_list = hs_instance_json['hs_instances']
        # return hs_instance_list

class CreateView(TemplateView):
    template_name = 'vsm/hyperstash_status/create.html'
    success_url = reverse_lazy('horizon:vsm:hyperstash_status:index')

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        return context

def create_hs_instance(request):
    body = json.loads(request.body)
    hs_instance = body['hs_instance']
    vsmapi.create_hyperstash_instance(request, hs_instance)
    status = "OK"
    msg = "succeed to create hs instance"
    resp = dict(message=msg, status=status)
    resp = json.dumps(resp)
    return HttpResponse(resp)

    # hs_instance_str = open("/opt/hyperstash_instances.json").read()
    # hs_instance_json = json.loads(hs_instance_str)
    # hs_instance_list = hs_instance_json['hs_instances']
    # max = 0
    # hs_id = 0
    # for _hs_instance in hs_instance_list:
    #     hs_id = int(_hs_instance['id'])
    #     if hs_id > max:
    #         max = hs_id
    # hs_instance['id'] = hs_id + 1
    # hs_instance['hostname'] = "hs" + str(hs_id + 1)
    # hs_instance_json['hs_instances'].append(hs_instance)
    # hs_instance_str = json.dumps(hs_instance_json)
    # with open("/opt/hyperstash_instances.json", "w") as file:
    #     file.write(hs_instance_str)
    #     file.close()
    # status = "OK"
    # msg = "succeed to create hs instance"
    # resp = dict(message=msg, status=status)
    # resp = json.dumps(resp)
    # return HttpResponse(resp)


class RbdListView(tables.DataTableView):
    table_class = ListRbdTable
    verbose_name = "List RBD"
    template_name = 'vsm/hyperstash_status/list_rbd.html'

    def get_data(self):
        LOG.info("=========================RBD LIST VIEW: %s" % self.kwargs)
        if int(self.kwargs["hs_instance_id"]) == 1:
            rbd_list = [
                {
                    "id": 1,
                    "pool": "tp01",
                    "rbd_name": "testvol01",
                    "size": 1024,
                    "objects": 2,
                    "order": 22,
                    "format": 2,
                    "hs_instance_id": 1
                },
                {
                    "id": 2,
                    "pool": "tp01",
                    "rbd_name": "testvol02",
                    "size": 1024,
                    "objects": 2,
                    "order": 22,
                    "format": 2,
                    "hs_instance_id": 1
                },
                {
                    "id": 3,
                    "pool": "tp02",
                    "rbd_name": "testvol03",
                    "size": 1024,
                    "objects": 2,
                    "order": 22,
                    "format": 2,
                    "hs_instance_id": 1
                }
            ]
        else:
            rbd_list = [
                {
                    "id": 4,
                    "pool": "tp01",
                    "rbd_name": "testvol04",
                    "size": 1024,
                    "objects": 2,
                    "order": 22,
                    "format": 2,
                    "hs_instance_id": 2
                },
                {
                    "id": 5,
                    "pool": "tp01",
                    "rbd_name": "testvol05",
                    "size": 1024,
                    "objects": 2,
                    "order": 22,
                    "format": 2,
                    "hs_instance_id": 2
                },
                {
                    "id": 6,
                    "pool": "tp02",
                    "rbd_name": "testvol06",
                    "size": 1024,
                    "objects": 2,
                    "order": 22,
                    "format": 2,
                    "hs_instance_id": 2
                }
            ]
        return rbd_list

class ConfigRbdView(forms.ModalFormView):
    form_class = ConfigRbdForm
    template_name = 'vsm/hyperstash_status/config_rbd.html'
    success_url = reverse_lazy('horizon:vsm:openstackconnect:index')

    def get_object(self):
        LOG.info("=========================OBJECT CONFIG RBD VIEW: %s" % self.kwargs)
        if int(self.kwargs['rbd_id']) in [1, 2, 3]:
            rbd_config = {
                "id": 1,
                "cache_dir": "/hyperstorage",
                "clean_start": 0,
                "enable_memory_usage_tracker": False,
                "object_size": 4096,
                "cache_total_size": 10737418240,
                "cache_dirty_ratio_min": 0.1,
                "cache_dirty_ratio_max": 0.9,
                "cache_ratio_health": 0.5,
                "cache_ratio_max": 0.7,
                "cache_flush_interval": 1,
                "cache_evict_interval": 1,
                "cache_flush_queue_depth": 256,
                "agent_threads_num": 128,
                "cache_service_threads_num": 64,
                "hs_instance_id": 1
            }
        else:
            rbd_config = {
                "id": 4,
                "cache_dir": "/hyperstorage1111",
                "clean_start": 0,
                "enable_memory_usage_tracker": False,
                "object_size": 4096,
                "cache_total_size": 10737418240,
                "cache_dirty_ratio_min": 0.1,
                "cache_dirty_ratio_max": 0.9,
                "cache_ratio_health": 0.5,
                "cache_ratio_max": 0.7,
                "cache_flush_interval": 1,
                "cache_evict_interval": 1,
                "cache_flush_queue_depth": 256,
                "agent_threads_num": 128,
                "cache_service_threads_num": 64,
                "hs_instance_id": 2
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

def monitor(request, rbd_id):
    LOG.info("=========================rbd_id: %s" % str(rbd_id))
    if int(rbd_id) == 1:
        rbd_name = "testvol01"
    elif int(rbd_id) == 2:
        rbd_name = "testvol02"
    elif int(rbd_id) == 3:
        rbd_name = "testvol03"
    elif int(rbd_id) == 4:
        rbd_name = "testvol04"
    elif int(rbd_id) == 5:
        rbd_name = "testvol05"
    else:
        rbd_name = "testvol06"
    return render(request,
                  'vsm/hyperstash_status/monitor.html',
                  {"rbd_id": rbd_id,
                   "rbd_name": rbd_name})

def cache_ratio(request, rbd_id):
    LOG.info("=========================request: %s" % str(request))
    if int(rbd_id) == 1:
        cache_ratio =  {"free": 20,
                        "used": 80,
                        "clean": 60,
                        "dirty": 20}
    elif int(rbd_id) == 2:
        cache_ratio =  {"free": 10,
                        "used": 90,
                        "clean": 65,
                        "dirty": 25}
    elif int(rbd_id) == 3:
        cache_ratio =  {"free": 38,
                        "used": 62,
                        "clean": 2,
                        "dirty": 60}
    elif int(rbd_id) == 4:
        cache_ratio =  {"free": 53,
                        "used": 47,
                        "clean": 27,
                        "dirty": 20}
    elif int(rbd_id) == 5:
        cache_ratio =  {"free": 88,
                        "used": 12,
                        "clean": 10,
                        "dirty": 2}
    else:
        cache_ratio =  {"free": 71,
                        "used": 29,
                        "clean": 22,
                        "dirty": 7}
    cache_ratio = json.dumps(cache_ratio)
    return HttpResponse(cache_ratio)
