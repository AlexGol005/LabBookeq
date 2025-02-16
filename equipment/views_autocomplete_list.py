from dal import autocomplete

from equipment.models import*

class VerificatorsAutocomplete(autocomplete.Select2QuerySetView):
  "выводит список поверителей для формы"
  """path(r'^verificators-autocomplete/$', views.VerificatorsAutocomplete.as_view(), name='verificators-autocomplete',),"""
    def get_queryset(self):
        qs = Verificators.objects.all()
        if self.q:
            query = Q(companyName__contains=self.q.lower()) | Q(companyName__contains=self.q.upper())
            qs = qs.filter(query)
        return qs

