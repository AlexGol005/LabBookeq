from ajax_select import register, LookupChannel
from .models import *

@register('verificator_tag')
class VerificatorsLookup(LookupChannel):
    model = Verificators

    def get_query(self, q, request):
        return self.model.objects.filter(companyName__icontains=q).order_by('companyName')[:50]

    # def format_item_display(self, item):
    #     return u"<span class='verificator_tag'>%s</span>" % item.companyName



    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.companyName
        
    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s<div><i>%s</i></div>" % (escape(obj.companyName))

    def get_objects(self, ids):
        return model.objects.filter(pk__in=ids)





