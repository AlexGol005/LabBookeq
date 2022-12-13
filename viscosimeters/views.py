from django.views.generic import ListView, TemplateView

from viscosimeters.models import*


class ViscosimetersView(ListView):
    """ Представление, которое выводит все вискозиметры в статусе 'в эксплуатации' с константами."""
    template_name = 'viscosimeters/viscosimetersKonstants.html'
    context_object_name = 'viscosimeters'
    ordering = ['charakters_name']

    def get_queryset(self):
        queryset = Viscosimeters.objects.filter(equipmentSM__equipment__status__exact='Э')
        return queryset


class ViscosimetersHeadView(TemplateView):
    """ выводит заглавную страницу вискозиметров """
    template_name = 'viscosimeters/head.html'





