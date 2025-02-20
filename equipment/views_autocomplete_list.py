from dal import autocomplete
from django.db.models import Q
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


class MeasurEquipmentCharaktersAutocomplete(autocomplete.Select2QuerySetView):
    """выводит список характеристик СИ (госреестров) для формы"""
    """path(r'^mecharakters-autocomplete/$', views_autocomplete_list.MeasurEquipmentCharaktersAutocomplete.as_view(), name='mecharakters-autocomplete',),"""
    def get_queryset(self):
        qs = MeasurEquipmentCharakters.objects.all()
        if self.q:
            query = Q(name__contains=self.q.lower()) | Q(name__contains=self.q.upper())| Q(reestr__contains=self.q) | Q(name__contains=self.q)
            qs = qs.filter(query)
        return qs


class TestingEquipmentCharaktersAutocomplete(autocomplete.Select2QuerySetView):
    """выводит список характеристик ИО для формы"""
    """path(r'^techarakters-autocomplete/$', views_autocomplete_list.TestingEquipmentCharaktersAutocomplete.as_view(), name='techarakters-autocomplete',),"""
    def get_queryset(self):
        qs = TestingEquipmentCharakters.objects.all()
        if self.q:
            query = Q(name__contains=self.q.lower()) | Q(name__contains=self.q.upper())| Q(name__contains=self.q)
            qs = qs.filter(query)
        return qs


class HelpingEquipmentCharaktersAutocomplete(autocomplete.Select2QuerySetView):
    """выводит список характеристик ИО для формы"""
    """path(r'^hecharakters-autocomplete/$', views_autocomplete_list.HelpingEquipmentCharaktersAutocomplete.as_view(), name='hecharakters-autocomplete',),"""
    def get_queryset(self):
        qs = HelpingEquipmentCharakters.objects.all()
        if self.q:
            query = Q(name__contains=self.q.lower()) | Q(name__contains=self.q.upper())| Q(name__contains=self.q)
            qs = qs.filter(query)
        return qs

