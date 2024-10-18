from ajax_select import register, LookupChannel
from .models import *

@register('verificator_tag')
class VerificatorsLookup(LookupChannel):
    model = Verificators

    def get_query(self, q, request):
        return self.model.objects.filter(companyName__icontains=q).order_by('companyName')[:50]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.companyName
      
