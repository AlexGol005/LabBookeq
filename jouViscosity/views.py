from datetime import timedelta, date

from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, TemplateView

from dinamicviscosity.models import Dinamicviscosity
from jouViscosity.forms import SearchKinematicaForm
from jouViscosity.models import ViscosityKinematicResult, ViscosityDinamicResult
from kinematicviscosity.models import ViscosityKinematic

NAME = 'Вязкость'
NAME2 = 'Плотность и динамика'

TABLENAME = 'Кинематическая вязкость (мм<sup>2</sup>/с)'
TABLENAME2 = 'Плотность/Динамическая вязкость (г/мл)/(Па*с)'
MODEL = ViscosityKinematicResult
MODEL2 = ViscosityDinamicResult


class AllKinematicviscosityView(ListView):
    """ Представление, которое выводит все значения кинматической вязкости из Журнала аттестованных значений"""
    """полустандартное"""
    template_name = 'jouViscosity/kinematicviscosityvalues.html'
    context_object_name = 'objects'

    def get_queryset(self):
        queryset = MODEL.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllKinematicviscosityView, self).get_context_data(**kwargs)
        objects2 = MODEL2.objects.all()
        context['objects2'] = objects2
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        context['TABLENAME2'] = TABLENAME2
        context['now'] = date.today()
        context['now_date_plusmonth'] = date.today() + timedelta(days=30)
        context['form'] = SearchKinematicaForm()
        return context


class SearchKinematicResultView(TemplateView):
    """ Представление, которое выводит результаты поиска на странице со всеми записями журнала результатов
    кинематической вязкости. """
    """нестандартное"""

    template_name = 'jouViscosity/kinematicviscosityvalues.html'

    def get_context_data(self, **kwargs):
        name = self.request.GET['name']
        lot = self.request.GET['lot']
        context = super(SearchKinematicResultView, self).get_context_data(**kwargs)
        if name and lot:
            objects = MODEL.objects.filter(name=name, lot=lot)
            objects2 = MODEL2.objects.filter(name=name, lot=lot)
            context['objects'] = objects
            context['objects2'] = objects2
        if name and not lot:
            objects = MODEL.objects.filter(name=name)
            objects2 = MODEL2.objects.filter(name=name)
            context['objects'] = objects
            context['objects2'] = objects2
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        context['TABLENAME2'] = TABLENAME2
        context['now'] = date.today()
        context['now_date_plusmonth'] = date.today() + timedelta(days=30)
        context['form'] = SearchKinematicaForm(initial={'name': name, 'lot': lot})
        return context


class DetailKinematicView(View):
    """ выводит историю измерений кинематической вязкости для партии """
    def get(self, request, path, int, str, *args, **kwargs):
        objects = ViscosityKinematic.objects.filter(fixation=True).filter(name=path).\
            filter(lot=int).filter(temperature=str)
        name = ViscosityKinematic.objects.filter(fixation=True, name=path, lot=int, temperature=str)[0]
        template = 'jouViscosity/detailkinematicviscosity.html'
        context = {
            'objects': objects,
            'name': name
        }
        return render(request, template, context)


class AllDinamicviscosityView(ListView):
    """ Представление, которое выводит все значения динамической вязкости и плотности
    из Журнала аттестованных значений"""
    """полустандартное"""
    template_name = 'jouViscosity/dinamicviscosityvalues.html'
    context_object_name = 'objects'

    def get_queryset(self):
        queryset = MODEL.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllDinamicviscosityView, self).get_context_data(**kwargs)
        objects2 = MODEL2.objects.all()
        context['objects2'] = objects2
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        context['TABLENAME2'] = TABLENAME2
        context['now'] = date.today()
        context['now_date_plusmonth'] = date.today() + timedelta(days=30)
        context['form'] = SearchKinematicaForm()
        return context


class DetailDinamicView(View):
    """ выводит историю измерений плотности и динамической  вязкости для партии"""
    def get(self, request, path, int, str, *args, **kwargs):
        objects = Dinamicviscosity.objects.filter(fixation=True).filter(name=path).filter(lot=int).\
            filter(temperature=str)
        name = Dinamicviscosity.objects.filter(fixation=True, name=path, lot=int, temperature=str)[0]
        template = 'jouViscosity/detaildinamicviscosity.html'
        context = {
            'objects': objects,
            'name': name
        }
        return render(request, template, context)

