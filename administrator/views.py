from django.views.generic import TemplateView
from django.db.models import Max
from .models import *

class RegstrView(TemplateView):
    """ выводит отдельный пост """
    template_name = 'administrator/about_registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj'] = Regstr.objects.latest('date')
        return context

