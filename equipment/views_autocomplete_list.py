from dal import autocomplete

from equipment.models import*

class VerificatorsAutocomplete(autocomplete.Select2QuerySetView):
    """выводит список поверителей для формы"""
    """path(r'^verificators-autocomplete/$', views_autocomplete_list.VerificatorsAutocomplete.as_view(), name='verificators-autocomplete',),"""
    def get_queryset(self):
        qs = Verificators.objects.all()
        if self.q:
            query = Q(companyName__contains=self.q.lower()) | Q(companyName__contains=self.q.upper())
            qs = qs.filter(query)
        return qs


class ManufacturerAutocomplete(autocomplete.Select2QuerySetView):
    """выводит список производителей для формы"""
    """path(r'^manufacturer-autocomplete/$', views_autocomplete_list.ManufacturerAutocomplete.as_view(), name='manufacturer-autocomplete',),"""
    def get_queryset(self):
        qs = Manufacturer.objects.all()
        if self.q:
            query = Q(companyName__contains=self.q.lower()) | Q(companyName__contains=self.q.upper())
            qs = qs.filter(query)
        return qs

