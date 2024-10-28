from django.views.generic import TemplateView
from django.db.models import Max
from blog.models import *

class RegstrView(TemplateView):
    """ выводит отдельный пост """
    model = Regstr
    template_name = 'administrator/about_registration.html'

    def get_object(self, queryset=None):
        return Regstr.objects.get(date=Max('date'))
