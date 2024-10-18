from ajax_select import register, LookupChannel
from .models import *

@register('verificator_tag')
class VerificatorsLookup(LookupChannel):
    model = Verificators

    def get_query(self, q, request):
        return self.model.objects.filter(companyName__icontains=q).order_by('companyName')[:50]

    def get_result(self,obj):
        return obj.companyName
        
    def format_match(self,obj):
        return self.format_item_display(obj)
        
    def format_item_display(self,obj):
        return u"%s" % escape(obj.pk)




