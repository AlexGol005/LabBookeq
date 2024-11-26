r"""
Модуль проекта LabJournal, приложения equipment.
Приложение equipment это обширное приложение, включает все про лабораторное оборудование и лабораторные помещения
Данный модуль views.py выводит представления для вывода форм и информации.
Список блоков:
блок 1 - заглавные страницы с кнопками, структурирующие разделы. (Самая верхняя страница - записана в приложении main)
блок 2 - списки и обновление: комнаты, поверители, персоны поверители, производители
блок 3 - списки: Все оборудование, СИ, ИО, ВО, госреестры, характеристики ИО, характеристики ВО
блок 4 - формы регистрации и обновления: комнаты, поверители, персоны поверители, производители, контакты поверителей
блок 5 - микроклимат: журналы, формы регистрации
блок 6 - регистрация госреестры, характеристики, ЛО - внесение, обновление
блок 7 - все поисковики
блок 8 - принадлежности к оборудованию
блок 9 - внесение и обновление поверка и аттестация
блок 10 - индивидуальные страницы СИ ИО ВО их поверок и аттестаций
блок 11 - все комментарии ко всему
блок 12 - вывод списков и форм  для метрологического  обеспечения
блок 13 - ТОиР
"""


import xlwt
import pytils.translit
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, request
from django.db.models import Max, Q, Value, CharField, Count, Sum
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from xlwt import Alignment, Borders

from equipment.constants import servicedesc0
from equipment.forms import*
from equipment.models import*
from formstandart import *
from functstandart import get_dateformat
from users.models import Profile, Company

URL = 'equipment'
now = date.today()


class OrderVerificationView(LoginRequiredMixin, ListView):
    template_name = URL + '/orderverification.html'
    context_object_name = 'list'
    model = Equipment



def OrderVerificationchange(request):
    if request.method == 'POST':
        if 'true' in request.POST:
            object_ids = request.POST.getlist('my_object')
            note = Equipment.objects.filter(id__in=object_ids) 
            for i in note:
                if i.kategory == 'СИ':               
                    i.measurequipment.newhaveorder = True
                    i.measurequipment.save()
                elif i.kategory == 'ИО':               
                    i.testingequipment.newhaveorder=True
                    i.testingequipment.save()
            slug = object_ids
            return redirect('export_orderverification_xls', {'slug': slug})
        if 'false' in request.POST:
            object_ids = request.POST.getlist('my_object')
            note = Equipment.objects.filter(id__in=object_ids) 
            for i in note:
                if i.kategory == 'СИ':               
                    i.measurequipment.newhaveorder=False
                    i.measurequipment.save()
                elif i.kategory == 'ИО':               
                    i.testingequipment.newhaveorder=False
                    i.testingequipment.save()
            return redirect('orderverification')
       






# блок 1 - заглавные страницы с кнопками, структурирующие разделы. Самая верхняя страница - в приложении main

class ManagerEquipmentView(LoginRequiredMixin, TemplateView):
    """выводит страницу для управляющего оборудованием"""
    template_name = URL + '/manager.html'

    def get_context_data(self, **kwargs):
        context = super(ManagerEquipmentView, self).get_context_data(**kwargs)
        try:
            user = User.objects.get(username=self.request.user)
            if user.is_staff:
                context['USER'] = True
            if not user.is_staff:
                context['USER'] = False
        except:
            context['USER'] = False
        return context

class MeteorologicalParametersView(LoginRequiredMixin, ListView):
    """Выводит страницу с кнопками для добавления помещений, микроклимата и вывода журнала микроклимата"""
    template_name = URL + '/meteo.html'
    context_object_name = 'objects'

    def get_queryset(self):
        queryset = Rooms.objects.filter(pointer=self.request.user.profile.userid)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MeteorologicalParametersView, self).get_context_data(**kwargs)
        try:
            user = User.objects.get(username=self.request.user)
            if user.is_staff:
                context['USER'] = True
            if not user.is_staff:
                context['USER'] = False
        except:
            context['USER'] = False
        context['form'] = DateForm()
        return context


class MetrologicalEnsuringView(LoginRequiredMixin, TemplateView):
    """Выводит заглавную страницу для Этикетки о поверке/аттестации и списки на поверку/аттестацию """
    template_name = URL + '/metro.html'

    def get_context_data(self, **kwargs):
        context = super(MetrologicalEnsuringView, self).get_context_data(**kwargs)
        context['form'] = DateForm()
        return context


class ReportsView(LoginRequiredMixin, TemplateView):
    """Выводит страницу с кнопками для вывода планов и отчётов по оборудованию"""
    template_name = URL + '/reports.html'

    def get_context_data(self, **kwargs):
        context = super(ReportsView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = YearForm()
        return context


# блок 2 - списки: комнаты, поверители, персоны поверители, производители


class VerificatorsView(ListView):
    """ Выводит список всех организаций поверителей """
    model = Verificators
    template_name = 'main/plainlist.html'
    context_object_name = 'objects'


class ManufacturerView(ListView):
    """ Выводит список всех производителей """
    model = Manufacturer
    template_name = URL + '/manufacturer_list.html'
    context_object_name = 'objects'
    ordering = ['companyName']
    paginate_by = 12


class RoomsView(LoginRequiredMixin, TemplateView):
    """выводит страницу комнат компании """
    template_name = 'equipment/rooms.html'
    def get_context_data(self, **kwargs):
        context = super(RoomsView, self).get_context_data(**kwargs)
        try:
            user = User.objects.get(username=self.request.user)
            if user.is_staff or user.is_superuser:
                context['USER'] = True
            else:
                context['USER'] = False
        except:
            context['USER'] = False
        rooms = Rooms.objects.filter(pointer=user.profile.userid)
        company = Company.objects.get(userid=user.profile.userid)
        context['rooms'] = rooms
        context['company'] = company 
        return context

@login_required
def RoomsUpdateView(request, str):
    """выводит форму для обновления данных о помещении"""
    ruser=request.user.profile.userid
    if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
        if request.method == "POST":
            form = RoomsUpdateForm(ruser, request.POST, instance=Rooms.objects.get(pk=str), initial={'ruser': ruser,})                                                       
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                return redirect('rooms')
        else:
            form = RoomsUpdateForm(ruser, instance=Rooms.objects.get(pk=str), initial={'ruser': ruser,})
        data = {'form': form,}                
        return render(request, 'equipment/reg.html', data)
    if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser:
        messages.success(request, 'Раздел недоступен')
        return redirect('rooms')




# блок 3 - списки: Все оборудование, СИ, ИО, ВО, госреестры, характеристики ИО, характеристики ВО

class EquipmentView(LoginRequiredMixin, ListView):
    """ Выводит список Всего ЛО """
    template_name = URL + '/EquipmentLIST.html'
    context_object_name = 'objects'
    ordering = ['exnumber']
    paginate_by = 12

    def get_queryset(self):
        queryset = Equipment.objects.filter(pointer=self.request.user.profile.userid)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EquipmentView, self).get_context_data(**kwargs)
        context['company'] =  Company.objects.get(userid=user.profile.userid).name
        return context


class MeasurEquipmentCharaktersView(LoginRequiredMixin, ListView):
    """ Выводит список госреестров """
    model = MeasurEquipmentCharakters
    template_name = URL + '/MEcharacterslist.html'
    context_object_name = 'objects'
    ordering = ['reestr']
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MeasurEquipmentCharaktersView, self).get_context_data(**kwargs)
        context['form'] = Searchreestrform()
        context['title'] = 'Госреестры, типы, модификации средств измерений'
        context['POINTER'] = self.request.user.profile.userid
        user = User.objects.get(username=self.request.user)
        return context


class TestingEquipmentCharaktersView(LoginRequiredMixin, ListView):
    """ Выводит список характеристик ИО """
    model = TestingEquipmentCharakters
    template_name = URL + '/TEcharacterslist.html'
    context_object_name = 'objects'
    ordering = ['name']
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TestingEquipmentCharaktersView, self).get_context_data(**kwargs)
        context['form'] = Searchtestingform()
        context['title'] = 'Характеристики, типы, испытательного оборудования'
        return context


class HelpingEquipmentCharaktersView(LoginRequiredMixin, ListView):
    """ Выводит список характеристик ВО """
    model = HelpingEquipmentCharakters
    template_name = URL + '/HEcharacterslist.html'
    context_object_name = 'objects'
    ordering = ['name']
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HelpingEquipmentCharaktersView, self).get_context_data(**kwargs)
        context['form'] = Searchtestingform()
        context['title'] = 'Характеристики, типы, вспомогательного оборудования'
        return context


class MeasurEquipmentView(LoginRequiredMixin, ListView):
    """Выводит список средств измерений"""
    template_name = URL + '/MEequipmentLIST.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']
    paginate_by = 12

    def get_queryset(self):
        queryset = MeasurEquipment.objects.filter(pointer=self.request.user.profile.userid).exclude(equipment__status='С')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MeasurEquipmentView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context


class TestingEquipmentView(LoginRequiredMixin, ListView):
    """ Выводит список испытательного оборудования """
    template_name = URL + '/TEequipmentLIST.html'
    context_object_name = 'objects'
    ordering = ['charakters__name']
    paginate_by = 12

    def get_queryset(self):
        queryset = TestingEquipment.objects.filter(pointer=self.request.user.profile.userid).exclude(equipment__status='С')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TestingEquipmentView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context


class HelpingEquipmentView(LoginRequiredMixin, ListView):
    """ Выводит список вспомогательного оборудования """
    template_name = URL + '/HEequipmentLIST.html'
    context_object_name = 'objects'
    ordering = ['charakters__name']
    paginate_by = 12

    def get_queryset(self):
        queryset = HelpingEquipment.objects.filter(pointer=self.request.user.profile.userid).exclude(equipment__status='С')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HelpingEquipmentView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context


# блок 4 - формы регистрации и обновления: комнаты, поверители, производители

@login_required
def RoomsCreateView(request):
    """ выводит форму добавления помещения """
    template_name = URL + '/newroomreg.html'
    if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
        if request.method == "POST":
            form = RoomsCreateForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    order = form.save(commit=False)
                    order.pointer = request.user.profile.userid
                    order.save()
                    messages.success(request, "Помещение успешно добавлено")
                    return redirect('rooms')
                except: 
                    messages.success(request, 'Эта комната уже есть')
                    return redirect('roomreg')                  
            else:
                messages.success(request, 'Эта комната уже есть')
                return redirect('roomreg')
        else:
            form = RoomsCreateForm()
        data = {'form': form, }                   
        return render(request, template_name, data)
    if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser:
        messages.success(request, 'Раздел недоступен')
        return redirect('roomreg')


class VerificatorsCreationView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    """ выводит форму добавления компании поверителя и список поверителей """
    template_name = URL + '/verificatorsreglist.html'
    success_url = '/equipment/verificatorsreg/'
    success_message = "Организация поверитель успешно добавлена"
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super(VerificatorsCreationView, self).get_context_data(**kwargs)
        context['title'] = 'Внести организацию поверителя'
        context['serform'] = Searchtestingform
        context['form'] = VerificatorsCreationForm       
        return context

    def get_queryset(self):
        queryset = Verificators.objects.all()
        return queryset


class ManufacturerRegView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """ выводит форму добавления производителя """
    template_name = URL + '/reg.html'
    form_class = ManufacturerCreateForm
    success_url = '/equipment/manufacturerlist/'
    success_message = "Производитель успешно добавлен"

    def get_context_data(self, **kwargs):
        context = super(ManufacturerRegView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить производителя ЛО'
        return context


class PersonchangeFormView(LoginRequiredMixin, View):
    """вывод формы смены ответсвенного за прибор, URL=personchangereg/<str:str>/"""
    def get(self, request, str):
        ruser=request.user.profile.userid
        title = 'Смена ответственного за прибор'
        dop = Equipment.objects.get(exnumber=str)
        form =  PersonchangeForm(ruser, initial={'ruser': ruser,})
        context = {
            'title': title,
            'dop': dop,
            'form': form,
        }
        template_name = 'equipment/reg.html'
        return render(request, template_name, context)

    def post(self, request, str, *args, **kwargs):
        ruser=request.user.profile.userid
        form = PersonchangeForm(ruser, request.POST)
        if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.equipment = Equipment.objects.get(exnumber=str)
                order.save()
                if order.equipment.kategory == 'СИ':
                    return redirect(f'/equipment/measureequipment/{str}')
                if order.equipment.kategory == 'ИО':
                    return redirect(f'/equipment/testequipment/{self.kwargs["str"]}')
                if order.equipment.kategory == 'ВО':
                    return redirect(f'/equipment/helpequipment/{self.kwargs["str"]}')
        else:
            messages.success(request, f'Раздел недоступен')
            if order.equipment.kategory == 'СИ':
                return redirect(f'/equipment/measureequipment/{str}')
            if order.equipment.kategory == 'ИО':
                return redirect(f'/equipment/testequipment/{self.kwargs["str"]}')
            if order.equipment.kategory == 'ВО':
                return redirect(f'/equipment/helpequipment/{self.kwargs["str"]}')


class RoomschangeFormView(LoginRequiredMixin, View):
    """вывод формы смены помещения, URL=roomschangereg/<str:str>/"""
    def get(self, request, str):
        ruser=request.user.profile.userid
        title = 'Смена размещения прибора'
        dop = Equipment.objects.get(exnumber=str)
        form =  RoomschangeForm(ruser, initial={'ruser': ruser,})
        context = {
            'title': title,
            'dop': dop,
            'form': form,
        }
        template_name = 'equipment/roomreg.html'
        return render(request, template_name, context)

    def post(self, request, str, *args, **kwargs):
        ruser=request.user.profile.userid
        form = RoomschangeForm(ruser, request.POST)
        if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.equipment = Equipment.objects.get(exnumber=str)
                order.save()
                if order.equipment.kategory == 'СИ':
                    return redirect(f'/equipment/measureequipment/{str}')
                if order.equipment.kategory == 'ИО':
                    return redirect(f'/equipment/testequipment/{self.kwargs["str"]}')
                if order.equipment.kategory == 'ВО':
                    return redirect(f'/equipment/helpequipment/{self.kwargs["str"]}')
        else:
            messages.success(request, f'Раздел недоступен')
            if order.equipment.kategory == 'СИ':
                return redirect(f'/equipment/measureequipment/{str}')
            if order.equipment.kategory == 'ИО':
                return redirect(f'/equipment/testequipment/{self.kwargs["str"]}')
            if order.equipment.kategory == 'ВО':
                return redirect(f'/equipment/helpequipment/{self.kwargs["str"]}')


# блок 5 - микроклимат: журналы, формы регистрации

class MeteorologicalParametersCreateView(LoginRequiredMixin, SuccessMessageMixin, View):
    """ выводит форму добавления условий микроклимата """
    def get(self, request):
        ruser=request.user.profile.userid
        title = 'Добавить условия окружающей среды'
        dopin = 'equipment/meteo/'
        form =  MeteorologicalParametersRegForm(ruser, initial={'ruser': ruser,})
        context = {
            'title': title,
            'dopin': dopin,
            'form': form,
        }
        template_name = URL + '/reg.html'
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        ruser=request.user.profile.userid
        form = MeteorologicalParametersRegForm(ruser, request.POST, initial={'ruser': ruser,})
        if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                str = order.roomnumber.pk
                return redirect(f'/equipment/meteoroom/{str}/') 
            else:
                messages.success(request, f'Условия уже добавлены ранее')
                return redirect(f'/equipment/meteoreg/')
        else:
            messages.success(request, f'Раздел недоступен')
            return redirect(f'/equipment/meteoreg/')


class MeteorologicalParametersRoomView(LoginRequiredMixin, ListView):
    """ выводит условия микроклимата и кнопки для добавления и выгрузки для отдельного помещения """
    model = MeteorologicalParameters
    template_name = URL + '/meteoroom.html'
    context_object_name = 'objects'
    paginate_by = 22

    def get_queryset(self):
        queryset = MeteorologicalParameters.objects.filter(roomnumber_id=self.kwargs['pk']).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MeteorologicalParametersRoomView, self).get_context_data(**kwargs)
        try:
            user = User.objects.get(username=self.request.user)
            if user.is_staff:
                context['USER'] = True
            if not user.is_staff:
                context['USER'] = False
        except:
            context['USER'] = False
        get_eq = MeteorologicalParameters.objects.filter(roomnumber=Rooms.objects.get(id=self.kwargs['pk']).pk).last()
        try:
            context['me'] = get_eq.equipments 
        except:
            context['me'] = 'добавьте средства измерения для комнаты и  первую запись о условиях микроклимата'
        try:
            context['rp'] = get_eq.person 
        except:
            context['rp'] = 'добавьте ответственного для комнаты и  первую запись о условиях микроклимата'
        context['title'] = Rooms.objects.get(id=self.kwargs['pk']).roomnumber
        context['titlepk'] = Rooms.objects.get(id=self.kwargs['pk']).pk
        context['form'] = DateForm()
        context['form1'] = YearForm(initial={'date': now.year})
        return context


class MeteorologicalParametersRoomSearchResultView(ListView):
    model = MeteorologicalParameters
    template_name = URL + '/meteoroom.html'
    context_object_name = 'objects'
    paginate_by = 22

    def get_queryset(self):
        serdate = self.request.GET['date']
        queryset1 = MeteorologicalParameters.objects.filter(roomnumber_id=self.kwargs['pk'])
        queryset = queryset1.filter(date=serdate)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MeteorologicalParametersRoomSearchResultView, self).get_context_data(**kwargs)
        serdate = self.request.GET['date']
        context['title'] = Rooms.objects.get(id=self.kwargs['pk']).roomnumber
        context['titlepk'] = Rooms.objects.get(id=self.kwargs['pk']).pk
        context['form'] = DateForm(initial={'date': serdate})
        context['form1'] = YearForm(initial={'date': now.year})
        return context


# блок 6 - регистрация госреестры, характеристики, ЛО - внесение, обновление

@login_required
def EquipmentReg(request):
    """выводит форму для регистрации  ЛО"""
    if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
        if request.method == "POST":
            form = EquipmentCreateForm(request.POST, request.FILES)
            if form.is_valid():
                order = form.save(commit=False)
                order.pointer = request.user.profile.userid
                try:
                    a = Equipment.objects.filter(exnumber__startswith=order.exnumber).filter(pointer=request.user.profile.userid).last().exnumber
                    b = int(str(a)[1:5]) + 1
                    c = str(b).rjust(4, '0')
                    d = str(order.exnumber) + c + '_' + str(order.pointer)
                    order.exnumber = d
                except:
                    order.exnumber =  str(order.exnumber) + '0001' + '_' + str(order.pointer)
                order.save()
                if order.kategory == 'СИ':
                    return redirect(f'/equipment/measureequipmentreg/{order.exnumber}/')
                if order.kategory == 'ИО':
                    return redirect(f'/equipment/testequipmentreg/{order.exnumber}/')
                if order.kategory == 'ВО':
                    return redirect(f'/equipment/helpequipmentreg/{order.exnumber}/')
                else:
                    return redirect('equipmentlist') 
            else:
                messages.success(request, 'Заполните поле "Производитель прибора"')
                return redirect('/equipment/equipmentreg/')
        else:
            form = EquipmentCreateForm()
            content = {
                'form': form,
                    }
            return render(request, 'equipment/Equipmentreg.html', content)
    if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect('/equipment/')


@login_required
def EquipmentDeleteView(request, str):
    """для кнопки удаления ЛО"""
    if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
        try:
            ruser=request.user.profile.userid
            note = Equipment.objects.filter(pointer=ruser).get(pk=str)
            note.delete()
            return redirect('/equipment/lasttenequipment/')
            messages.success(request, 'Оборудование удалено!')
        except:
            messages.success(request, 'Оборудование невозможно удалить, так как она зарегистрировано в качестве СИ, ИО или ВО. Вы можете поменять статус оборудования на "Списано"')
            return redirect('/equipment/lasttenequipment/')


class MeasurEquipmentCharaktersRegView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """ выводит форму внесения госреестра. """
    template_name = URL + '/Echaractersreg.html'
    form_class = MeasurEquipmentCharaktersCreateForm
    success_url = '/equipment/measurequipmentcharacterslist/'
    success_message = "Госреестр успешно добавлен. Для внесения изменений обратитесь к администрации сайта"
    error_message = "Раздел доступен только инженеру по оборудованию"

    def form_valid(self, form):
        order = form.save(commit=False)
        user = User.objects.get(username=self.request.user)
        if user.has_perm('equipment.add_equipment') or user.is_superuser:
            order.pointer = self.request.user.profile.userid
            order.save()
            return super().form_valid(form)
        else:
            messages.success(self.request, "Раздел доступен только инженеру по оборудованию")
            return redirect('/equipment/measurequipmentcharacterslist/')

    def get_context_data(self, **kwargs):
        context = super(MeasurEquipmentCharaktersRegView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить госреестр'
        context['dopin'] = 'equipment/measurequipmentcharacterslist'
        return context


@login_required
def MeasurEquipmentCharaktersUpdateView(request, str):
    """выводит форму для обновления данных о госреестре"""
    if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
        if request.method == "POST":
            form = MeasurEquipmentCharaktersCreateForm(request.POST,
                                                       instance=MeasurEquipmentCharakters.objects.get(pk=str))
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                return redirect('measurequipmentcharacterslist')
        else:
            form = MeasurEquipmentCharaktersCreateForm(instance=MeasurEquipmentCharakters.objects.get(pk=str))
        data = {'form': form,
                }
        return render(request, 'equipment/Echaractersreg.html', data)
    if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect('/equipment/measurequipmentcharacterslist/')


class TestingEquipmentCharaktersRegView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """ выводит форму внесения характеристик ИО. """
    template_name = URL + '/Echaractersreg.html'
    form_class = TestingEquipmentCharaktersCreateForm
    success_url = '/equipment/testingequipmentcharacterslist/'
    success_message = "Характеристики ИО успешно добавлены"
    error_message = "Раздел доступен только инженеру по оборудованию"

    def form_valid(self, form):
        order = form.save(commit=False)
        user = User.objects.get(username=self.request.user)
        if user.has_perm('equipment.add_equipment') or user.is_superuser:
            order.save()
            return super().form_valid(form)
        else:
            messages.success(self.request, "Раздел доступен только инженеру по оборудованию")
            return redirect('/equipment/testingequipmentcharacterslist/')

    def get_context_data(self, **kwargs):
        context = super(TestingEquipmentCharaktersRegView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить характеристики ИО'
        context['dopin'] = 'equipment/testingequipmentcharacterslist'
        return context

@login_required
def TestingEquipmentCharaktersUpdateView(request, str):
    """выводит форму для обновления данных о характеристиках ИО"""
    if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
        if request.method == "POST":
            form = TestingEquipmentCharaktersCreateForm(request.POST,
                                                       instance=TestingEquipmentCharakters.objects.get(pk=str))
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                return redirect('testingequipmentcharacterslist')
        else:
            form = TestingEquipmentCharaktersCreateForm(instance=TestingEquipmentCharakters.objects.get(pk=str))
        data = {'form': form,
                }
        return render(request, 'equipment/Echaractersreg.html', data)
    if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect('/equipment/testingequipmentcharacterslist/')


class HelpingEquipmentCharaktersRegView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """ выводит форму внесения характеристик ВО. """
    template_name = URL + '/Echaractersreg.html'
    form_class = HelpingEquipmentCharaktersCreateForm
    success_url = '/equipment/helpingequipmentcharacterslist/'
    success_message = "Характеристики ВО успешно добавлены"
    error_message = "Раздел доступен только инженеру по оборудованию"

    def form_valid(self, form):
        order = form.save(commit=False)
        user = User.objects.get(username=self.request.user)
        if user.has_perm('equipment.add_equipment') or user.is_superuser:
            order.save()
            return super().form_valid(form)
        else:
            messages.success(self.request, "Раздел доступен только инженеру по оборудованию")
            return redirect('/equipment/helpingequipmentcharacterslist/')

    def get_context_data(self, **kwargs):
        context = super(HelpingEquipmentCharaktersRegView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить характеристики ВО'
        context['dopin'] = 'equipment/helpingequipmentcharacterslist'
        return context

@login_required
def HelpingEquipmentCharaktersUpdateView(request, str):
    """выводит форму для обновления данных о характеристиках ВО"""
    if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
        if request.method == "POST":
            form = HelpingEquipmentCharaktersCreateForm(request.POST,
                                                       instance=HelpingEquipmentCharakters.objects.get(pk=str))
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                return redirect('helpingequipmentcharacterslist')
        else:
            form = HelpingEquipmentCharaktersCreateForm(instance=HelpingEquipmentCharakters.objects.get(pk=str))
        data = {'form': form,
                }
        return render(request, 'equipment/Echaractersreg.html', data)
    if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect('/equipment/helpingequipmentcharacterslist/')


class MeasureequipmentregView(LoginRequiredMixin, CreateView):
    """ выводит форму регистрации СИ на основе ЛО и Госреестра """
    form_class = MeasurEquipmentCreateForm
    template_name = 'equipment/crispy_reg.html'
    success_url = f'/equipment/measureequipment/{str}'

    def get_object(self, queryset=None):
        return get_object_or_404(Equipment, exnumber=self.kwargs['str'])

    def get_context_data(self, **kwargs):
        context = super(MeasureequipmentregView, self).get_context_data(**kwargs)
        context['title'] = 'Зарегистрировать СИ'
        context['dop'] = Equipment.objects.get(exnumber=self.kwargs['str'])
        return context

    def form_valid(self, form):
        if form.is_valid():
            order = form.save(commit=False)
            order.equipment = Equipment.objects.get(exnumber=self.kwargs['str'])
            order.save()
            return redirect(f'/equipment/measureequipment/{self.kwargs["str"]}')


class TestingequipmentregView(LoginRequiredMixin, CreateView):
    """ выводит форму регистрации ИО на основе ЛО и характеристик ИО """
    form_class = TestingEquipmentCreateForm
    template_name = 'equipment/reg.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Equipment, exnumber=self.kwargs['str'])

    def get_context_data(self, **kwargs):
        context = super(TestingequipmentregView, self).get_context_data(**kwargs)
        context['title'] = 'Зарегистрировать ИО'
        context['dop'] = Equipment.objects.get(exnumber=self.kwargs['str'])
        return context

    def form_valid(self, form):
        if form.is_valid():
            order = form.save(commit=False)
            order.equipment = Equipment.objects.get(exnumber=self.kwargs['str'])
            order.save()
            return redirect(f'/equipment/testequipment/{self.kwargs["str"]}')


class HelpingequipmentregView(LoginRequiredMixin, CreateView):
    """ выводит форму регистрации ВО на основе ЛО и характеристик ВО """
    form_class = HelpingEquipmentCreateForm
    template_name = 'equipment/reg.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Equipment, exnumber=self.kwargs['str'])

    def get_context_data(self, **kwargs):
        context = super(HelpingequipmentregView, self).get_context_data(**kwargs)
        context['title'] = 'Зарегистрировать ВО'
        context['dop'] = Equipment.objects.get(exnumber=self.kwargs['str'])
        return context

    def form_valid(self, form):
        if form.is_valid():
            order = form.save(commit=False)
            order.equipment = Equipment.objects.get(exnumber=self.kwargs['str'])
            order.save()
            return redirect(f'/equipment/helpingequipment/{self.kwargs["str"]}')


@login_required
def EquipmentUpdate(request, str):
    """выводит форму для обновления разрешенных полей оборудования ответственному за оборудование"""
    title = Equipment.objects.get(exnumber=str)
    try:
        get_pk = title.personchange_set.latest('pk').pk
        person = Personchange.objects.get(pk=get_pk).person
    except:
        person = 1
    if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser or request.user == person:
        if request.method == "POST":
            form = EquipmentUpdateForm(request.POST,  instance=Equipment.objects.get(exnumber=str))
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                if title.kategory == 'СИ':
                    return redirect(reverse('measureequipment', kwargs={'str': str}))
                if title.kategory == 'ИО':
                    return redirect(reverse('testequipment', kwargs={'str': str}))
                if title.kategory == 'ВО':
                    return redirect(reverse('supequipment', kwargs={'str': str}))
        else:
            form = EquipmentUpdateForm(request.POST, instance=Equipment.objects.get(exnumber=str))
        data = {'form': EquipmentUpdateForm(instance=Equipment.objects.get(exnumber=str)), 'title': title
                }
        return render(request, 'equipment/Eindividuality.html', data)
    if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser or not request.user == person:
        messages.success(request, f' Для внесения записей о приборе нажмите на кнопку'
                                  f' "Внести запись о приборе и смотреть записи (для всех пользователей)"'
                                  f'. Добавить особенности работы или поменять статус может только ответственный '
                                  f'за прибор или поверку.')
        if title.kategory == 'СИ':
            return redirect(reverse('measureequipment', kwargs={'str': str}))
        if title.kategory == 'ИО':
            return redirect(reverse('testequipment', kwargs={'str': str}))
        if title.kategory == 'ВО':
            return redirect(reverse('supequipment', kwargs={'str': str}))


# блок 7 - все поисковики

class SearchPersonverregView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    """ Представление, которое выводит результаты поиска по списку поверителей организаций """

    template_name = URL + '/verificatorsreglist.html'
    context_object_name = 'objects'
    success_url = '/equipment/verificatorsreg/'
    success_message = "Организация поверитель успешно добавлена"


    def get_context_data(self, **kwargs):
        context = super(SearchPersonverregView, self).get_context_data(**kwargs)
        context['serform'] = Searchtestingform
        context['form'] = VerificatorsCreationForm  
        return context

    def get_queryset(self):
        name = self.request.GET['name']
        queryset = Verificators.objects.filter(companyName__icontains=name)
        return queryset


class ReestrsearresView(LoginRequiredMixin, TemplateView):
    """ Представление, которое выводит результаты поиска по списку госреестров """

    template_name = URL + '/MEcharacterslist.html'

    def get_context_data(self, **kwargs):
        context = super(ReestrsearresView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        reestr = self.request.GET['reestr']
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        reestr = self.request.GET['reestr']
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        if name and not reestr:
            objects = MeasurEquipmentCharakters.objects.\
            filter(Q(name__icontains=name)|Q(name__icontains=name1)).order_by('name')
            context['objects'] = objects
        if reestr and not name:
            objects = MeasurEquipmentCharakters.objects.filter(reestr__icontains=reestr)
            context['objects'] = objects
        if reestr and  name:
            objects = MeasurEquipmentCharakters.objects.filter(reestr__icontains=reestr).\
                filter(Q(name__icontains=name)|Q(name__icontains=name1)).order_by('name')
            context['objects'] = objects
        context['form'] = Searchreestrform(initial={'name': name, 'reestr': reestr})
        context['URL'] = URL
        context['title'] = 'Госреестры, типы, модификации средств измерений'
        return context

class TEcharacterssearresView(LoginRequiredMixin, TemplateView):
    """ Представление, которое выводит результаты поиска по списку характеристик ИО """

    template_name = URL + '/TEcharacterslist.html'

    def get_context_data(self, **kwargs):
        context = super(TEcharacterssearresView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        if name:
            objects = TestingEquipmentCharakters.objects.\
            filter(Q(name__icontains=name)|Q(name__icontains=name1)).order_by('name')
            context['objects'] = objects
        context['form'] = Searchreestrform(initial={'name': name})
        context['URL'] = URL
        context['title'] = 'Характеристики, типы, испытательного оборудования'
        return context


class SearchResultMeasurEquipmentView(LoginRequiredMixin, TemplateView):
    """ Представление, которое выводит результаты поиска по списку средств измерений """

    template_name = URL + '/MEequipmentLIST.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultMeasurEquipmentView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        exnumber = self.request.GET['exnumber']
        lot = self.request.GET['lot']

        get_id_actual = Verificationequipment.objects.select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        list_ = list(get_id_actual)
        set = []
        for n in list_:
            set.append(n.get('id_actual'))
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        if name and not lot and not exnumber:
            objects = MeasurEquipment.objects.filter(pointer=self.request.user.profile.userid).\
            filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).order_by('charakters__name')
            context['objects'] = objects
        if lot and not name  and not exnumber:
            objects = MeasurEquipment.objects.filter(equipment__lot=lot).filter(pointer=self.request.user.profile.userid).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and not name and not lot:
            objects = MeasurEquipment.objects.filter(equipment__exnumber__startswith=exnumber).filter(pointer=self.request.user.profile.userid).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and name and lot:
            objects = MeasurEquipment.objects.filter(equipment__exnumber__startswith=exnumber).filter(pointer=self.request.user.profile.userid).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and name and not lot:
            objects = MeasurEquipment.objects.filter(equipment__exnumber__startswith=exnumber).filter(pointer=self.request.user.profile.userid).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                order_by('charakters__name')
            context['objects'] = objects
        if exnumber and not name and lot:
            objects = MeasurEquipment.objects.filter(equipment__exnumber__startswith=exnumber).filter(pointer=self.request.user.profile.userid).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if lot and name and not exnumber:
            objects = MeasurEquipment.objects.filter(pointer=self.request.user.profile.userid).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        context['form'] = SearchMEForm(initial={'name': name, 'lot': lot, 'exnumber': exnumber})
        context['URL'] = URL
        return context


class SearchResultTestingEquipmentView(LoginRequiredMixin, TemplateView):
    """ Представление, которое выводит результаты поиска по списку испытательного оборудования """
    
    template_name = URL + '/TEequipmentLIST.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultTestingEquipmentView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        exnumber = self.request.GET['exnumber']
        lot = self.request.GET['lot']
        get_id_actual = TestingEquipment.objects.select_related('equipmentSM_att').values('equipmentSM_att'). \
            annotate(id_actual=Max('id')).values('id_actual')
        list_ = list(get_id_actual)
        set = []
        for n in list_:
            set.append(n.get('id_actual'))

        if name and not lot and not exnumber:
            objects = TestingEquipment.objects.filter(pointer=self.request.user.profile.userid).\
            filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                order_by('charakters__name')
            context['objects'] = objects
        if lot and not name  and not exnumber:
            objects = TestingEquipment.objects.filter(pointer=self.request.user.profile.userid).filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and not name and not lot:
            objects = TestingEquipment.objects.filter(pointer=self.request.user.profile.userid).filter(equipment__exnumber=exnumber).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and name and lot:
            objects = TestingEquipment.objects.filter(pointer=self.request.user.profile.userid).filter(equipment__exnumber=exnumber).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and name and not lot:
            objects = TestingEquipment.objects.filter(pointer=self.request.user.profile.userid).filter(equipment__exnumber=exnumber).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                order_by('charakters__name')
            context['objects'] = objects
        if exnumber and not name and lot:
            objects = TestingEquipment.objects.filter(pointer=self.request.user.profile.userid).filter(equipment__exnumber=exnumber).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if lot and name and not exnumber:
            objects = TestingEquipment.objects.filter(pointer=self.request.user.profile.userid).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        context['form'] = SearchMEForm(initial={'name': name, 'lot': lot, 'exnumber': exnumber})
        context['URL'] = URL
        return context


# блок 8  принадлежности к оборудованию

class DocsConsView(LoginRequiredMixin, View, SuccessMessageMixin):
    """ выводит список принадлежностей прибора и форму для добавления принадлежности """
    def get(self, request, str):
        template_name = 'equipment/Edocsconslist.html'
        form = DocsConsCreateForm()
        title = Equipment.objects.get(exnumber=str)
        objects = DocsCons.objects.filter(equipment__exnumber=str).order_by('pk')
        context = {
                'title': title,
                'form': form,
                'objects': objects,
                }
        return render(request, template_name, context)

    def post(self, request, str, *args, **kwargs):
        form = DocsConsCreateForm(request.POST)
        if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.equipment = Equipment.objects.get(exnumber=str)
                order.save()
                return redirect(f'/equipment/docsreg/{str}')
        else:
            messages.add_message(request, messages.SUCCESS, 'Раздел доступен только инженеру по оборудованию')
            return redirect(f'/equipment/docsreg/{str}')


# блок 9 - внесение и обновление поверка и аттестация

@login_required
def VerificationReg(request, str):
    """выводит форму для внесения сведений о поверке"""
    title = Equipment.objects.get(exnumber=str)
    if request.user.is_superuser:
        if request.method == "POST":
            form = VerificationRegForm(request.POST, request.FILES)
            if form.is_valid():
                order = form.save(commit=False)
                order.equipmentSM = MeasurEquipment.objects.get(equipment__exnumber=str)
                order.save()
                return redirect(order)
    if not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect(reverse('measureequipmentver', kwargs={'str': str}))
    else:
        form = VerificationRegForm()
    data = {
        'form': form,
        'title': title
    }
    return render(request, 'equipment/verificationreg.html', data)


@login_required
def CalibrationReg(request, str):
    """выводит форму для внесения сведений о калибровке"""
    title = Equipment.objects.get(exnumber=str)
    if request.user.is_superuser:
        if request.method == "POST":
            form = CalibrationRegForm(request.POST, request.FILES)
            if form.is_valid():
                order = form.save(commit=False)
                order.equipmentSM = MeasurEquipment.objects.get(equipment__exnumber=str)
                order.save()
                return redirect(order)
    if not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect(reverse('measureequipmentcal', kwargs={'str': str}))
    else:
        form = CalibrationRegForm()
    data = {
        'form': form,
        'title': title
    }
    return render(request, 'equipment/calibrationreg.html', data)


@login_required
def AttestationReg(request, str):
    """выводит форму для внесения сведений об аттестации"""
    title = Equipment.objects.get(exnumber=str)
    if request.user.is_superuser:
        if request.method == "POST":
            form = AttestationRegForm(request.POST, request.FILES)
            if form.is_valid():
                order = form.save(commit=False)
                order.equipmentSM = TestingEquipment.objects.get(equipment__exnumber=str)
                order.save()
                return redirect(order)
    if not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect(reverse('testingequipmentatt', kwargs={'str': str}))
    else:
        form = AttestationRegForm()
    data = {
        'form': form,
        'title': title
    }
    return render(request, 'equipment/TEattestationreg.html', data)


@login_required
def EquipmentMetrologyUpdate(request, str):
    """выводит форму для обновления постоянных особенностей поверки"""
    title = Equipment.objects.get(exnumber=str)
    try:
        get_pk = title.personchange_set.latest('pk').pk
        person = Personchange.objects.get(pk=get_pk).person
    except:
        person = 1

    if person == request.user or request.user.is_superuser or request.user.has_perm('equipment.add_equipment'):
        if request.method == "POST":
            form = MetrologyUpdateForm(request.POST, instance=Equipment.objects.get(exnumber=str))
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                if title.kategory == 'СИ':
                    return redirect(reverse('measureequipmentver', kwargs={'str': str}))
                if title.kategory == 'ИО':
                    return redirect(reverse('testingequipmentatt', kwargs={'str': str}))
    if person != request.user or  not request.user.is_superuser or not request.user.has_perm('equipment.add_equipment'):
        messages.success(request, f'. поменять статус может только ответственный за поверку.')
        return redirect(reverse('measureequipmentver', kwargs={'str': str}))
    else:
        form = MetrologyUpdateForm(instance=Equipment.objects.get(exnumber=str))
    data = {'form': form, 'title': title
            }
    return render(request, 'equipment/metrologyindividuality.html', data)


class VerificationequipmentView(LoginRequiredMixin, View):
    """ выводит историю поверок и форму для добавления комментария к истории поверок """

    def get(self, request, str):
        note = Verificationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        try:
            strreg = note.latest('pk').equipmentSM.equipment.exnumber
        except:
            strreg = Equipment.objects.get(exnumber=str).exnumber
        try:
            calinterval = note.latest('pk').equipmentSM.charakters.calinterval
        except:
            calinterval = '-'
        title = Equipment.objects.get(exnumber=str)
        try:
            dateorder = Verificationequipment.objects.filter(equipmentSM__equipment__exnumber=str).last().dateorder
        except:
            dateorder = 'не поверен'
        now = date.today()
        try:
            comment = CommentsVerificationequipment.objects.filter(forNote__exnumber=str).last().note
        except:
            comment = ''
        form = CommentsVerificationCreationForm(initial={'comment': comment})
        data = {'note': note,
                'title': title,
                'calinterval': calinterval,
                'now': now,
                'dateorder': dateorder,
                'form': form,
                'comment': comment,
                'strreg': strreg,
                }
        return render(request, 'equipment/MEverification.html', data)

    def post(self, request, str, *args, **kwargs):
        form = CommentsVerificationCreationForm(request.POST)
        if request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.author = request.user
                order.forNote = Equipment.objects.get(exnumber=str)
                order.save()
                return redirect(order)
        else:
            messages.success(request, f'Комментировать может только ответственный за поверку приборов')
            return redirect(reverse('measureequipmentver', kwargs={'str': str}))


class CalibrationequipmentView(LoginRequiredMixin, View):
    """ выводит историю калибровок и форму для добавления комментария к истории калибровок """

    def get(self, request, str):
        note = Calibrationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        try:
            strreg = note.latest('pk').equipmentSM.equipment.exnumber
        except:
            strreg = Equipment.objects.get(exnumber=str).exnumber
        try:
            calinterval = note.latest('pk').equipmentSM.charakters.calinterval
        except:
            calinterval = '-'
        title = Equipment.objects.get(exnumber=str)
        try:
            dateorder = Calibrationequipment.objects.filter(equipmentSM__equipment__exnumber=str).last().dateorder
        except:
            dateorder = 'не поверен'
        now = date.today()
        try:
            comment = CommentsVerificationequipment.objects.filter(forNote__exnumber=str).last().note
        except:
            comment = ''
        form = CommentsVerificationCreationForm(initial={'comment': comment})
        data = {'note': note,
                'title': title,
                'calinterval': calinterval,
                'now': now,
                'dateorder': dateorder,
                'form': form,
                'comment': comment,
                'strreg': strreg,
                }
        return render(request, 'equipment/MEcalibration.html', data)

    def post(self, request, str, *args, **kwargs):
        form = CommentsVerificationCreationForm(request.POST)
        if request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.author = request.user
                order.forNote = Equipment.objects.get(exnumber=str)
                order.save()
                return redirect(order)
        else:
            messages.success(request, f'Комментировать может только ответственный за поверку приборов')
            return redirect(reverse('measureequipmentcal', kwargs={'str': str}))


class AttestationequipmentView(LoginRequiredMixin, View):
    """ выводит историю аттестаций и форму для добавления комментария к истории аттестаций """

    def get(self, request, str):
        note = Attestationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        try:
            strreg = note.latest('pk').equipmentSM.equipment.exnumber
        except:
            strreg = Equipment.objects.get(exnumber=str).exnumber
        try:
            calinterval = note.latest('pk').equipmentSM.charakters.calinterval
        except:
            calinterval = '-'
        title = Equipment.objects.get(exnumber=str)
        try:
            dateorder = Attestationequipment.objects.filter(equipmentSM__equipment__exnumber=str).last().dateorder
        except:
            dateorder = 'не аттестован'
        now = date.today()
        try:
            comment = CommentsAttestationequipment.objects.filter(forNote__exnumber=str).last().note
        except:
            comment = ''
        form = CommentsAttestationequipmentForm(initial={'comment': comment})
        data = {'note': note,
                'title': title,
                'calinterval': calinterval,
                'now': now,
                'dateorder': dateorder,
                'form': form,
                'comment': comment,
                'strreg': strreg,
                }
        return render(request, 'equipment/TEattestation.html', data)

    def post(self, request, str, *args, **kwargs):
        form = CommentsAttestationequipmentForm(request.POST)
        if request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.author = request.user
                order.forNote = Equipment.objects.get(exnumber=str)
                order.save()
                return redirect(order)
        else:
            messages.success(request, f'Комментировать может только ответственный за поверку приборов')
            return redirect(reverse('testingequipmentattestation', kwargs={'str': str}))


class HaveorderVerView(LoginRequiredMixin, UpdateView):
    """ выводит форму добавления инфо о заказе поверки """
    template_name = 'equipment/reg.html'
    form_class = OrderMEUdateForm

    def get_object(self, queryset=None):
        queryset_get = Verificationequipment.objects. \
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        q = Verificationequipment.objects.filter(id__in=set). \
            get(equipmentSM_id=self.kwargs['pk'])
        return q

    def form_valid(self, form):
        order = form.save(commit=False)
        user = User.objects.get(username=self.request.user)
        if user.has_perm('equipment.add_equipment') or user.is_superuser:
            order.save()
            return redirect('/equipment/measureequipmentall/')
        else:
            messages.success(self.request, "Раздел доступен только инженеру по оборудованию")
            return redirect('/equipment/measureequipmentall/')

    def get_context_data(self, **kwargs):
        context = super(HaveorderVerView, self).get_context_data(**kwargs)
        context['title'] = "Заказана поверка или новое СИ"
        return context


class HaveorderAttView(LoginRequiredMixin, UpdateView):
    """ выводит форму добавления инфо о заказе аттестации """
    template_name = 'equipment/reg.html'
    form_class = OrderMEUdateForm

    def get_object(self, queryset=None):
        queryset_get = Attestationequipment.objects. \
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        q = Attestationequipment.objects.filter(id__in=set). \
            get(equipmentSM_id=self.kwargs['pk'])
        return q

    def form_valid(self, form):
        order = form.save(commit=False)
        user = User.objects.get(username=self.request.user)
        if user.has_perm('equipment.add_equipment') or user.is_superuser:
            order.save()
            return redirect('/equipment/testingequipmentall/')
        else:
            messages.success(self.request, "Раздел доступен только инженеру по оборудованию")
            return redirect('/equipment/testingequipmentall/')

    def get_context_data(self, **kwargs):
        context = super(HaveorderAttView, self).get_context_data(**kwargs)
        context['title'] = "Заказана аттестация или новое ИО"
        return context


# блок 10 - индивидуальные страницы СИ ИО ВО их поверок и аттестаций

class StrMeasurEquipmentView(LoginRequiredMixin, View):
    """ выводит отдельную страницу СИ """
    def get(self, request, str):
        note = Verificationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        obj = get_object_or_404(MeasurEquipment, equipment__exnumber=str)
        context = {
            'obj': obj,
            'note': note,
        }
        return render(request, URL + '/MEequipmentSTR.html', context)


class StrTestEquipmentView(LoginRequiredMixin, View):
    """ выводит отдельную страницу ИО """
    def get(self, request, str):
        note = Attestationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        obj = get_object_or_404(TestingEquipment, equipment__exnumber=str)
        context = {
            'obj': obj,
            'note': note,
        }
        return render(request, URL + '/TEequipmentSTR.html', context)


class StrHelpEquipmentView(LoginRequiredMixin, View):
    """ выводит отдельную страницу ВО """
    def get(self, request, str):
        note = Checkequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        obj = get_object_or_404(HelpingEquipment, equipment__exnumber=str)
        context = {
            'obj': obj,
            'note': note,
        }
        return render(request, URL + '/HEequipmentSTR.html', context)


# блок 11 - все комментарии ко всему

class CommentsView(View):
    """ выводит комментарии к оборудованию и форму для добавления комментариев """
    form_class = NoteCreationForm
    initial = {'key': 'value'}
    template_name = 'equipment/comments.html'

    def get(self, request, str):
        note = CommentsEquipment.objects.filter(forNote__exnumber=str).order_by('-pk')
        title = Equipment.objects.get(exnumber=str)
        form = NoteCreationForm()
        return render(request, 'equipment/comments.html', {'note': note, 'title': title, 'form': form, 'URL': URL})

    def post(self, request, str, *args, **kwargs):
        form = NoteCreationForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user and not order.author:
                order.author = request.user
            if not request.user and order.author:
                order.author = order.author
            order.forNote = Equipment.objects.get(exnumber=str)
            order.save()
            messages.success(request, f'Запись добавлена!')
            return redirect(order)


# блок 12 - вывод списков и форм  для метрологического обеспечения

class SearchMustVerView(LoginRequiredMixin, ListView):
    """ выводит список СИ у которых дата заказа поверки совпадает с указанной либо раньше неё"""

    template_name = URL + '/MEequipmentLIST.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']

    def get_context_data(self, **kwargs):
        context = super(SearchMustVerView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context

    def get_queryset(self):
        serdate = self.request.GET['date']
        queryset_get = Verificationequipment.objects.filter(haveorder=False).\
            filter(equipment__pointer=self.request.user.profile.userid).\
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        queryset_get1 = Verificationequipment.objects.filter(id__in=set).\
            filter(dateorder__lte=serdate).values('equipmentSM__id')
        b = list(queryset_get1)
        set1 = []
        for i in b:
            a = i.get('equipmentSM__id')
            set1.append(a)
        queryset = MeasurEquipment.objects.filter(equipment__pointer=self.request.user.profile.userid).filter(id__in=set1).filter(equipment__status='Э')
        return queryset


class SearchMustAttView(LoginRequiredMixin, ListView):
    """ выводит список ИО у которых дата заказа аттестации совпадает с указанной либо раньше неё"""

    template_name = URL + '/TEequipmentLIST.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']

    def get_context_data(self, **kwargs):
        context = super(SearchMustAttView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context

    def get_queryset(self):
        serdate = self.request.GET['date']
        queryset_get = Attestationequipment.objects.filter(haveorder=False).\
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        queryset_get1 = Attestationequipment.objects.filter(id__in=set).\
            filter(dateorder__lte=serdate).values('equipmentSM__id')
        b = list(queryset_get1)
        set1 = []
        for i in b:
            a = i.get('equipmentSM__id')
            set1.append(a)
        queryset = TestingEquipment.objects.filter(equipment__pointer=self.request.user.profile.userid).filter(id__in=set1).filter(equipment__status='Э')
        return queryset


class SearchNotVerView(LoginRequiredMixin, ListView):
    """ выводит список СИ у которых дата окончания поверки совпадает с указанной либо раньше неё"""

    template_name = URL + '/MEequipmentLIST.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']

    def get_context_data(self, **kwargs):
        context = super(SearchNotVerView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context

    def get_queryset(self):
        serdate = self.request.GET['date']
        queryset_get = Verificationequipment.objects.\
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        queryset_get1 = Verificationequipment.objects.filter(id__in=set).\
            filter(datedead__lte=serdate).values('equipmentSM__id')
        b = list(queryset_get1)
        set1 = []
        for i in b:
            a = i.get('equipmentSM__id')
            set1.append(a)
        queryset = MeasurEquipment.objects.filter(equipment__pointer=self.request.user.profile.userid).filter(id__in=set1).exclude(equipment__status='C')
        return queryset


class SearchNotAttView(LoginRequiredMixin, ListView):
    """ выводит список ИО у которых дата окончания аттестации совпадает с указанной либо раньше неё"""

    template_name = URL + '/TEequipmentLIST.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']

    def get_context_data(self, **kwargs):
        context = super(SearchNotAttView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context

    def get_queryset(self):
        serdate = self.request.GET['date']
        queryset_get = Attestationequipment.objects.\
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        queryset_get1 = Attestationequipment.objects.filter(id__in=set).\
            filter(datedead__lte=serdate).values('equipmentSM__id')
        b = list(queryset_get1)
        set1 = []
        for i in b:
            a = i.get('equipmentSM__id')
            set1.append(a)
        queryset = TestingEquipment.objects.filter(equipment__pointer=self.request.user.profile.userid).filter(id__in=set1).exclude(equipment__status='C')
        return queryset


class LastNewEquipmentView(LoginRequiredMixin, ListView):
    """ выводит список добавленных приборов"""

    template_name = URL + '/EquipmentLIST.html'
    context_object_name = 'objects'  
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(LastNewEquipmentView, self).get_context_data(**kwargs)
        context['URL'] = URL
        return context

    def get_queryset(self):
        queryset = Equipment.objects.filter(pointer=self.request.user.profile.userid).order_by('-pk')
        return queryset

            
# .filter()[Total-10:Total]

class SearchMustOrderView(LoginRequiredMixin, ListView):
    """ выводит список СИ у которых месяц заказа новых совпадает с указанным либо раньше него"""

    template_name = URL + '/MEequipmentLIST.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']

    def get_context_data(self, **kwargs):
        context = super(SearchMustOrderView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context

    def get_queryset(self):
        serdate = self.request.GET['date']
        queryset_get = Verificationequipment.objects.filter(haveorder=False).\
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        queryset_get1 = Verificationequipment.objects.filter(id__in=set).\
            filter(dateordernew__lte=serdate).values('equipmentSM__id')
        b = list(queryset_get1)
        set1 = []
        for i in b:
            a = i.get('equipmentSM__id')
            set1.append(a)
        queryset = MeasurEquipment.objects.filter(equipment__pointer=self.request.user.profile.userid).filter(id__in=set1).filter(equipment__status='Э')
        return queryset


class VerificationLabelsView(LoginRequiredMixin, TemplateView):
    """выводит форму для ввода внутренних номеров для распечатки этикеток о метрологическом обслуживании приборов """
    template_name = URL + '/labels.html'

    def get_context_data(self, **kwargs):
        context = super(VerificationLabelsView, self).get_context_data(**kwargs)
        context['form'] = LabelEquipmentform()
        return context


# блок 13 - ТОиР

@login_required
def ServiceEquipmentregView(request, str):
    """выводит форму для добавления постоянного ТОИР"""
    charakters = MeasurEquipmentCharakters.objects.get(pk=str)    
    if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
        if request.method == "POST":
            try: 
                ServiceEquipmentME.objects.get(charakters=charakters)
                form = ServiceEquipmentregForm(request.POST, instance=ServiceEquipmentME.objects.get(charakters=charakters))  
            except:
                form = ServiceEquipmentregForm(request.POST)  
            if form.is_valid():
                order = form.save(commit=False)
                order.charakters = charakters
                order.save()
                return redirect('measurequipmentcharacterslist')
        else:
            try: 
                ServiceEquipmentME.objects.get(charakters=charakters)
                form = ServiceEquipmentregForm(instance=ServiceEquipmentME.objects.get(charakters=charakters))
            except:
                form = ServiceEquipmentregForm()
        data = {'form': form,}                
        return render(request, 'equipment/toreg.html', data)
    if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser:
        messages.success(request, 'Раздел недоступен')
        return redirect('measurequipmentcharacterslist')



class ServiceView(LoginRequiredMixin, ListView):
    """Выводит главную страницу просмотра и планирования ТОиР"""
    template_name = URL + '/service.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']
    paginate_by = 12

    def get_queryset(self):
        queryset = ServiceEquipmentU.objects.filter(pointer=self.request.user.profile.userid).filter(year=str(now.year))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ServiceView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SimpleSearchForm()
        context['year'] = now.year
        context['yearform'] = YearForm()
        return context


class ServiceStrView(LoginRequiredMixin, View):
    """ выводит отдельную страницу плана ТО2 """
    def get(self, request, str):
        obj = get_object_or_404(ServiceEquipmentU, pk=str)
        obj2 = get_object_or_404(ServiceEquipmentUFact, pk_pointer=str)
        year = now.year
        context = {
            'obj': obj, 'obj2': obj2, 'year': year,
            }
        return render(request, URL + '/serviceplan.html', context)


@login_required
def ServiceEquipmentUUpdateView(request, str):
    """выводит форму для обновления данных о ТО-2 план"""
    
    if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
        if request.method == "POST":
            form = ServiceEquipmentUUpdateForm(request.POST, instance=ServiceEquipmentU.objects.get(pk=str))                                                    
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                return redirect(reverse('serviceplan', kwargs={'str': str}))
        else:
            form = ServiceEquipmentUUpdateForm(instance=ServiceEquipmentU.objects.get(pk=str))
        data = {'form': form,
                }
        return render(request, 'equipment/reg.html', data)
    if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect(reverse('serviceplan', kwargs={'str': str}))



@login_required
def ServiceEquipmentUFactUpdateView(request, str):
    """выводит форму для обновления данных о ТО-2 факт"""
    if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
        if request.method == "POST":
            form = ServiceEquipmentUFactUpdateViewForm(request.POST, instance=ServiceEquipmentUFact.objects.get(pk_pointer=str))                                                    
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                return redirect(reverse('serviceplan', kwargs={'str': str}))
        else:
            form = ServiceEquipmentUFactUpdateViewForm(instance=ServiceEquipmentUFact.objects.get(pk_pointer=str))
        data = {'form': form,
                }
        return render(request, 'equipment/reg.html', data)
    if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect(reverse('serviceplan', kwargs={'str': str}))




class ServiceYearView(LoginRequiredMixin, View):
    """вывод страницы - ТОИР за год, год передан в форме поиска на предыдущей странице"""
    def get(self, request):
        date = self.request.GET['date']
        objects = ServiceEquipmentU.objects.filter(pointer=self.request.user.profile.userid).filter(year=date)
        form =  DubleSearchForm()
        URL = 'equipment'
        year= date
        yearform = YearForm()
        context = {
            'objects': objects,
            'URL': URL,
            'form': form,
            'yearform': yearform,
            'year': year,
        }
        template_name = 'equipment/serviceyear.html'
        return render(request, template_name, context)



@login_required
def ServiceCreateView(request):
    queryset = Equipment.objects.filter(pointer=request.user.profile.userid)
    if request.method == 'GET':
        year = request.GET.get('date')
    for i in queryset:
        ServiceEquipmentU.objects.get_or_create(equipment=i, year=year)
    return redirect('service')



class ServiceSearchResultView(LoginRequiredMixin, ListView):
    """ выводит результаты поиска по списку ТО-2 по номеру оборудования """

    template_name = URL + '/serviceyear.html'
    context_object_name = 'objects' 

    def get_context_data(self, **kwargs):
        context = super(ServiceSearchResultView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['year'] = self.request.GET.get('qwery1')
        context['form'] = DubleSearchForm()
        return context

    def get_queryset(self):
        qwery = self.request.GET.get('qwery')
        year = self.request.GET.get('qwery1')
        queryset = ServiceEquipmentU.objects.filter(pointer=self.request.user.profile.userid).filter(equipment__exnumber__startswith=qwery).filter(year=year)
        return queryset


class ToMEView(LoginRequiredMixin, View):
    """выводит описание ТО для СИ """
    template_name = URL + '/to.html'

    def get(self, request, str):
        obj = ServiceEquipmentME.objects.get(pk=str)
        return render(request, URL + '/to.html', {'obj': obj,})


