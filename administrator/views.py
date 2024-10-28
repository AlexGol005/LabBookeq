from django.views.generic import TemplateView
from django.db.models import Max
from .models import *

class RegstrView(TemplateView):
    """ выводит отдельный пост """
    model = Regstr
    template_name = 'administrator/about_registration.html'
    context_object_name = 'obj'

    def get_object(self, queryset=None):
        return Regstr.objects.get(pk=1)

