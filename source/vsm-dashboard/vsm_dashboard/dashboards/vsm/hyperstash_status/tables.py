
import json

from vsm_dashboard.api import vsm as vsmapi

from django.utils.translation import ugettext_lazy as _
from horizon import tables


class AddHsInstanceAction(tables.LinkAction):
    name = "add hyperstash instance"
    verbose_name = _("Add HS Instance")
    url = "horizon:vsm:hyperstash_status:create"
    classes = ("ajax-modal", "btn-primary")

    def allowed(self, request, datum=None):
        return True

class ListRbdAction(tables.LinkAction):
    name = "list rbd"
    verbose_name = _("List RBD")
    url = "horizon:vsm:hyperstash_status:list_rbd"
    classes = ("ajax-modal", "btn-primary")

    def allowed(self, request, datum=None):
        return True

class DeleteAction(tables.DeleteAction):
    data_type_singular = ("hs instance")
    data_type_plural = ("hs instances")
    classes = ("btn-del-hs-instance", )

    def allowed(self, request, datum=None):
        return True

    def delete(self, request, obj_id):
        return vsmapi.delete_hyperstash_instance(request, obj_id)

        # hs_instance_str = open("/opt/hyperstash_instances.json").read()
        # hs_instance_json = json.loads(hs_instance_str)
        # hs_instance_list = hs_instance_json['hs_instances']
        # for hs_instance in hs_instance_list:
        #     if int(hs_instance['id']) == int(obj_id):
        #         hs_instance_list.remove(hs_instance)
        # hs_instance_json['hs_instances'] = hs_instance_list
        # hs_instance_str = json.dumps(hs_instance_json)
        # with open("/opt/hyperstash_instances.json", "w") as file:
        #     file.write(hs_instance_str)
        #     file.close()

class ListHyperstashInstanceTable(tables.DataTable):

    id = tables.Column("id", verbose_name=_("ID"), hidden=False)
    hs_instance_name = tables.Column("hs_instance_name",
                                     verbose_name=_("Hyperstash Instance Name"))
    ip_address = tables.Column("ip_address", verbose_name=_("IP Address"))
    hostname = tables.Column("hostname", verbose_name=_("Hostname"))

    class Meta:
        name = "hyperstash_instances_list"
        verbose_name = _("Hyperstash Instances List")
        table_actions = (AddHsInstanceAction, DeleteAction)
        row_actions = (ListRbdAction, )

    def get_object_id(self, datum):
        if hasattr(datum, "id"):
            return datum.id
        else:
            return datum["id"]

class MonitorAction(tables.LinkAction):
    name = "monitor"
    verbose_name = _("Monitor")
    url = "horizon:vsm:hyperstash_status:monitor"
    classes = ("ajax-modal", "btn-primary")

    def allowed(self, request, datum=None):
        return True

class RbdHSConfigAction(tables.LinkAction):
    name = "rbd hs config"
    verbose_name = _("Config RBD")
    url = "horizon:vsm:hyperstash_status:config_rbd"
    classes = ("ajax-modal", "btn-primary")

    def allowed(self, request, datum=None):
        return True

class ListRbdTable(tables.DataTable):

    id = tables.Column("id", verbose_name=_("ID"), hidden=False)
    pool = tables.Column("pool", verbose_name=_("Pool Name"))
    rbd_name = tables.Column("rbd_name", verbose_name=_("RBD Name"))
    size = tables.Column("size", verbose_name=_("Size(MB)"))
    objects = tables.Column("objects", verbose_name=_("Objects"))
    order = tables.Column("order", verbose_name=_("Order"))
    format = tables.Column("format", verbose_name=_("Format"))
    hs_instance_id = tables.Column("hs_instance_id", hidden=True)

    class Meta:
        name = "rbd_list"
        verbose_name = _("RBD List")
        row_actions = (MonitorAction, RbdHSConfigAction)

    def get_object_id(self, datum):
        if hasattr(datum, "id"):
            return datum.id
        else:
            return datum["id"]
