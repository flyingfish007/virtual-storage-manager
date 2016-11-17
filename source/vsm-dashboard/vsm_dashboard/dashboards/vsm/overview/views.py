# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

from __future__ import division

import commands
import json
import logging

from django.http import HttpResponse
from django.shortcuts import render

from vsm_dashboard.api import vsm as vsmapi
from vsm_dashboard.utils import get_time_delta

LOG = logging.getLogger(__name__)


def index(request):
        return render(request, 'vsm/overview/index.html',{})


def version(request):
    return HttpResponse(get_version())


def get_vsm_version():
    try:
        (status, out) = commands.getstatusoutput('vsm --version')
    except:
        out = '2.0'
    return out


def get_version():
    ceph_version = ''
    up_time = ''
    try:
        vsm_summary = vsmapi.vsm_summary(None)
        if vsm_summary is not None:
            up_time = get_time_delta(vsm_summary.created_at)
            ceph_version = vsm_summary.ceph_version
    except:
        pass
    vsm_version = get_vsm_version()
    vsm_version = {
        "version": vsm_version,
        "update": up_time,
        "ceph_version": ceph_version,
    }
    version_data = json.dumps(vsm_version)
    return version_data
