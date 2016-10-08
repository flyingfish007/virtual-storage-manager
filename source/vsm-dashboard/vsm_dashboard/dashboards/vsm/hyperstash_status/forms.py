
from django.utils.translation import ugettext_lazy as _

from horizon import forms


class AddHSInstanceForm(forms.SelfHandlingForm):

    failure_url = 'horizon:vsm:hyperstash_status:index'

    hs_instance_name = forms.CharField(
        label = _("Hyperstash Instance Name"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    ip_address = forms.CharField(
        label = _("IP Address"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    description = forms.CharField(
        label = _("Description"),
        required=False
    )

    def handle(self, request, data):
        pass

class ConfigRbdForm(forms.SelfHandlingForm):

    failure_url = 'horizon:vsm:hyperstash_status:list_rbd'

    cache_dir = forms.CharField(
        label = _("Cache Dir"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    clean_start = forms.CharField(
        label = _("Clean Start"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    enable_memory_usage_tracker = forms.CharField(
        label = _("Enable Memory Usage Tracker"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    object_size = forms.CharField(
        label = _("Object Size"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    cache_total_size = forms.CharField(
        label = _("Cache Total Size"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    cache_dirty_ratio_min = forms.CharField(
        label = _("Cache Dirty Ratio Min"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    cache_dirty_ratio_max = forms.CharField(
        label = _("Cache Dirty Ratio Max"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    cache_ratio_health = forms.CharField(
        label = _("Cache Ratio Health"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    cache_ratio_max = forms.CharField(
        label = _("Cache Ratio Max"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    cache_flush_interval = forms.CharField(
        label = _("Cache Flush Interval"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    cache_evict_interval = forms.CharField(
        label = _("Cache Evict Interval"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    cache_flush_queue_depth = forms.CharField(
        label = _("Cache Flush Queue Depth"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    agent_threads_num = forms.CharField(
        label = _("Agent Thread Num"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )
    cache_service_threads_num = forms.CharField(
        label = _("Cache Service Threads Num"),
        max_length = 255,
        min_length = 1,
        error_messages = {
            'required': _('This field is required.')
        }
    )

    def handle(self, request, data):
        pass
