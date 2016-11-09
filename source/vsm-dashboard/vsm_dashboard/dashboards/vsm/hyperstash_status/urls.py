
from django.conf.urls import patterns, url

from .views import IndexView
from .views import CreateView
from .views import RbdListView
from .views import ConfigRbdView
from .views import monitor
from .views import cache_ratio
from .views import create_hs_instance
from .views import update_action
from .views import cache_action
from .views import cache_io_workload


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create/$', CreateView.as_view(), name='create'),
    url(r'^create_hs_instance/$', create_hs_instance, name='create_hs_instance'),
    url(r'^(?P<hs_instance_id>[^/]+)/list_rbd/$', RbdListView.as_view(), name='list_rbd'),
    url(r'^(?P<rbd_id>[^/]+)/config_rbd/$', ConfigRbdView.as_view(), name='config_rbd'),
    url(r'^(?P<rbd_id>[^/]+)/monitor/$', monitor, name='monitor'),
    url(r'^(?P<rbd_id>[^/]+)/cache_ratio/$', cache_ratio, name='cache_ratio'),
    url(r'^(?P<rbd_id>[^/]+)/cache_action/$', cache_action, name='cache_action'),
    url(r'^(?P<rbd_id>[^/]+)/cache_io_workload/$', cache_io_workload, name='cache_io_workload'),
    url(r'^update_action/$', update_action, name='update_action'),
)
