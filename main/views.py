from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from .forms import AttestationJForm
from .models import AttestationJ, ResultValueJ


class About(View):
    """выводит страницу О сайте"""
    def get(self, request):
        return render(request, 'main/about.html')


class IndexView(View):
    """выводит страницу главная страница по основному адресу"""
    def get(self, request):
        return render(request, 'main/main.html')


# @login_required
class AttestationJView(View):
    """выводит страницу Журналы измерений"""
    def get(self, request):
        objects = AttestationJ.objects.all()
        return render(request, 'main/attestationJ.html', {'objects': objects})


class CertifiedValueJView(View):
    """выводит страницу Журналы результатов измерений"""
    def get(self, request):
        objects = ResultValueJ.objects.all()
        return render(request, 'main/certifiedvalueJ.html', {'objects': objects})


class EquipmentView(TemplateView):
    """выводит страницу Инфраструктура лаборатории"""
    template_name = 'main/equipment.html'

    def get_context_data(self, **kwargs):
        context = super(EquipmentView, self).get_context_data(**kwargs)
        try:
            user = User.objects.get(username=self.request.user)
            if user.is_staff:
                context['USER'] = True
            if not user.is_staff:
                context['USER'] = False
        except:
            context['USER'] = False
        return context


@login_required
def attestationJRegView(request):
    """ выводит форму внесения журнала """
    if request.method == "POST":
        form = AttestationJForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            order.save()
            messages.success(request,
                             f'Заявка принята. Сообщите о заявке разработчику по a.golovkina@petroanalytica.ru')
            return redirect('/attestationJ/')
    else:
        form = AttestationJForm()

    return render(
        request,
        'main/registrationAtt.html',
        {
            'form': form
        })
