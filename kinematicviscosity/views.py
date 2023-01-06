# все стандратно кроме поиска по полям, импорта моделей и констант
from django.core.exceptions import ObjectDoesNotExist

from exelbase import export_protocolbase_xls, export_base_kinematicviscosity_xls, style_plain

"""
Модуль проекта LabJournal, приложения kinematicviscosity.
Приложение kinematicviscosity это журнал фиксации 
лабораторных записей по измерению кинематической вязкости нефтепродуктов
(Лабортаорный журнал измерения кинематической вязкости).

Данный модуль admin.py выводит таблицы приложения в административной части сайта. 
"""


from django.shortcuts import render

# этот блок нужен для всех журналов
from .forms import *
from formstandart import*
from .models import *

from .constants import *
from viewstandart import *

MODEL = ViscosityKinematic
COMMENTMODEL = Comments


class Constants:
    URL = URL
    JOURNAL = JOURNAL
    MODEL = MODEL
    COMMENTMODEL = COMMENTMODEL
    NAME = NAME
    journal = journal
    SearchForm = SearchForm
    SearchDateForm = SearchDateForm
# конец блока для всех журналов

# блок стандартных 'View' но с индивидуальностями, возможно унаследованных от стандартных классов из модуля viewstandart


class RegView(RegView):
    """ Представление, которое выводит форму регистрации в журнале. """
    """ метод форм валид перегружен для заполнения полей """
    template_name = URL + '/registration.html'
    form_class = StrJournalCreationForm
    success_message = "Запись внесена, подтвердите АЗ!"

    def form_valid(self, form):
        order = form.save(commit=False)
        """вставка начало"""
        konstant1 = Viscosimeters.objects.get(equipmentSM__equipment__lot=order.ViscosimeterNumber1.
                                              equipmentSM.equipment.lot)
        konstant2 = Viscosimeters.objects.get(equipmentSM__equipment__lot=order.ViscosimeterNumber2.
                                              equipmentSM.equipment.lot)
        order.Konstant1 = konstant1.konstant
        order.Konstant2 = konstant2.konstant
        try:
            oldvalue = ViscosityKinematicResult.objects.get(name=order.name, lot=order.lot, cipher=order.cipher)
            if order.temperature == 20:
                order.oldresult = oldvalue.cvt20

            if order.temperature == 25:
                order.oldresult = oldvalue.cvt25

            if order.temperature == 40:
                order.oldresult = oldvalue.cvt40

            if order.temperature == 50:
                order.oldresult = oldvalue.cvt50

            if order.temperature == 60:
                order.oldresult = oldvalue.cvt60

            if order.temperature == 80:
                order.oldresult = oldvalue.cvt80

            if order.temperature == 100:
                order.oldresult = oldvalue.cvt100

            if order.temperature == 150:
                order.oldresult = oldvalue.cvt150

            if order.temperature == -20:
                order.oldresult = oldvalue.cvtminus20
        except ObjectDoesNotExist:
            pass
        """вставка окончание"""
        order.save()
        return super().form_valid(form)
# конец блока стандартных 'View' но с индивидуальностями

# блок стандартных 'View' унаследованных от стандартных классов из модуля utils
# основные


class HeadView(Constants, HeadView):
    """ Представление, которое выводит заглавную страницу журнала """
    """ Стандартное """
    template_name = URL + '/head.html'


class StrJournalView(Constants, StrJournalView):
    """ выводит отдельную запись и форму добавления в ЖАЗ """
    form_class = StrJournalUdateForm
    template_name = URL + '/str.html'


class CommentsView(Constants, CommentsView):
    """ выводит комментарии к записи в журнале и форму для добавления комментариев """
    """Стандартное"""
    form_class = CommentCreationForm


class AllStrView(Constants, AllStrView):
    """ Представление, которое выводит все записи в журнале. """
    """стандартное"""
    template_name = URL + '/journal.html'
    model = MODEL


# блок View для формирования протокола
class RoomsUpdateView(Constants, RoomsUpdateView):
    """ выводит форму добавления помещения к измерению """
    form_class = StrJournalProtocolRoomUdateForm
    template_name = 'main/reg.html'
    success_message = "Помещение успешно добавлено"


class ProtocolbuttonView(Constants, ProtocolbuttonView):
    """ Выводит кнопку для формирования протокола """
    template_name = URL + '/buttonprotocol.html'


class ProtocolHeadView(Constants, ProtocolHeadView):
    """ выводит форму внесения для внесения допинформации для формирования протокола и кнопку для протокола """
    template_name = 'main/reg.html'
    form_class = StrJournalProtocolUdateForm


# блок  'View' для различных поисков - унаследованные
class DateSearchResultView(Constants, DateSearchResultView):
    """ Представление, которое выводит результаты поиска по датам на странице со всеми записями журнала. """
    """стандартное"""
    template_name = URL + '/journal.html'


# блок  'View' для различных поисков - НЕунаследованные
class SearchResultView(Constants, TemplateView):
    """ Представление, которое выводит результаты поиска на странице со всеми записями журнала. """
    """нестандартное"""
    template_name = URL + '/journal.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        lot = self.request.GET['lot']
        cipher = self.request.GET['cipher']
        temperature = self.request.GET['temperature']
        if name and lot and temperature and not cipher:
            objects = MODEL.objects.filter(name=name).filter(lot=lot).filter(temperature=temperature).\
                filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if name and lot and not temperature and not cipher:
            objects = MODEL.objects.filter(name=name).filter(lot=lot).filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if name and not lot and not temperature and not cipher:
            objects = MODEL.objects.filter(name=name).filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if name and temperature and not lot and not cipher:
            objects = MODEL.objects.filter(name=name).filter(temperature=temperature).\
                filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if name and temperature and lot and cipher:
            objects = MODEL.objects.filter(name=name).filter(temperature=temperature).filter(cipher=cipher).\
                        filter(lot=lot).filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if name and temperature and not lot and cipher:
            objects = MODEL.objects.filter(name=name).filter(temperature=temperature).filter(cipher=cipher).\
                        filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if name and not temperature and lot and cipher:
            objects = MODEL.objects.filter(name=name).filter(cipher=cipher).\
                        filter(lot=lot).filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if name and not temperature and not lot and cipher:
            objects = MODEL.objects.filter(name=name).filter(cipher=cipher).\
                        filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if not name and not temperature and not lot and cipher:
            objects = MODEL.objects.filter(cipher=cipher).\
                        filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if not name and not temperature and lot and not cipher:
            objects = MODEL.objects.\
                        filter(lot=lot).filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if not name and temperature and not lot and not cipher:
            objects = MODEL.objects.filter(temperature=temperature).\
                        filter(lot=lot).filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if name and temperature and lot and cipher:
            objects = MODEL.objects.filter(name=name).filter(temperature=temperature).filter(cipher=cipher).\
                        filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if not name and temperature and lot and cipher:
            objects = MODEL.objects.filter(temperature=temperature).filter(cipher=cipher).filter(lot=lot).\
                        filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if not name and not temperature and lot and cipher:
            objects = MODEL.objects.filter(cipher=cipher).\
                        filter(lot=lot).filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if not name and temperature and not lot and cipher:
            objects = MODEL.objects.filter(temperature=temperature).filter(cipher=cipher).\
                       filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        context['journal'] = JOURNAL.objects.filter(for_url=URL)
        context['formSM'] = SearchForm(initial={'name': name, 'lot': lot, 'temperature': temperature, 'cipher': cipher})
        context['formdate'] = SearchDateForm()
        context['URL'] = URL
        return context


def filterview(request, pk):
    """ Фильтры записей об измерениях по дате, АЗ, мои записи и пр """
    """Стандартная"""
    objects = MODEL.objects.all()
    formSM = SearchForm()
    formdate = SearchDateForm()
    if pk == 1:
        now = datetime.datetime.now() - timedelta(minutes=60 * 24 * 7)
        objects = objects.filter(date__gte=now).order_by('-pk')
    elif pk == 2:
        now = datetime.datetime.now()
        objects = objects.filter(date__gte=now).order_by('-pk')
    elif pk == 3:
        objects = objects.order_by('-pk')
    elif pk == 4:
        objects = objects.filter(fixation__exact=True).order_by('-pk')
    elif pk == 5:
        objects = objects.filter(performer=request.user).order_by('-pk')
    elif pk == 6:
        objects = objects.filter(performer=request.user).filter(fixation__exact=True).order_by('-pk')
    elif pk == 7:
        objects = objects.filter(performer=request.user).filter(fixation__exact=True).filter(
            date__gte=datetime.datetime.now()).order_by('-pk')
    return render(request, URL + "/journal.html", {'objects': objects, 'journal': journal, 'formSM': formSM, 'URL': URL,
                                                   'formdate': formdate})


# блок выгрузок данных в формате ексель (вызывают стандартизированные функции)

def export_me_xls(request, pk):
    return export_base_kinematicviscosity_xls(request, pk, MODEL)


def export_protocol_xls(request, pk):
    """представление для выгрузки протокола испытаний в ексель вызывает базовое представление"""
    note = MODEL.objects.get(pk=pk)
    columns1 = [
        'Измеряемый параметр',
        'Измеряемый параметр',
        'Т °C',
        'Измеренное значение Х1, мм2/с ',
        'Измеренное значение Х2, мм2/с ',
        'Измеренное значение Хср, мм2/с ',
        'Результат контрольной процедуры измерения, rk, % ',
        'Норматив контроля, r, % ',
    ]
    columns2 = [
        'Кинематическая вязкость',
        'Кинематическая вязкость',
        note.temperature,
        note.viscosity1,
        note.viscosity2,
        note.result,
        note.accMeasurement,
        note.kriteriy,
    ]

    def get_for_columns1(ws, row_num):
        for col_num in range(2):
            ws.write(row_num, col_num, columns1[col_num], style_plain)
            ws.merge(row_num, row_num, 0, 1, style_plain)
        for col_num in range(1, len(columns1)):
            ws.write(row_num, col_num, columns1[col_num], style_plain)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 1050

    def get_for_columns2(ws, row_num):
        for col_num in range(2):
            ws.write(row_num, col_num, columns2[col_num], style_plain)
            ws.merge(row_num, row_num, 0, 1, style_plain)
        for col_num in range(2, 3):
            ws.write(row_num, col_num, columns2[col_num], style_plain)
        for col_num in range(3, len(columns2)):
            ws.write(row_num, col_num, columns2[col_num], style_plain)
    extrainfo = ''
    return export_protocolbase_xls(request, pk, MODEL, parameter, extrainfo, get_for_columns1, get_for_columns2,
                                   conclusion,
                                   columns1, columns2
                                   )
