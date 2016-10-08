
import horizon

from django.utils.translation import ugettext_lazy as _

from vsm_dashboard.dashboards.vsm import dashboard


class HyperstashStatus(horizon.Panel):
    name = _("Hyperstash Status")
    slug = 'hyperstash_status'

dashboard.VizDash.register(HyperstashStatus)
