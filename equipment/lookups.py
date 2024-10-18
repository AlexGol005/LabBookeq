from ajax_select import register, LookupChannel
from .models import *

@register('verificator_tag')
class VerificatorsLookup(LookupChannel):
    model = Verificators

    def get_query(self, q, request):
        return self.model.objects.filter(companyName__icontains=q).order_by('companyName')[:50]

    def format_item_display(self, item):
        return u"<span class='verificator_tag'>%s</span>" % item.companyName

    def format_item_display(self, item):
        return """
            <span class='product'>{}</span> 
            <a 
            id='change_id_order_product_{}'
            class='related-widget-wrapper-link change-related' 
            data-href-template='/admin/products/product/__fk__/change/?_to_field=id&_popup=1'
            href='/admin/products/product/{}/change/?_to_field=id&_popup=1'
            >
            <img src="/static/admin/img/icon-changelink.svg" alt="Change">
            </a>""".format(item.name, item.id, item.id)


