# """
# Модуль проекта LabJournal, приложения equipment.
# Приложение equipment это обширное приложение, включает все про лабораторное оборудование и лабораторные помещения
# Данный модуль forms.py выводит классы, создающие формы для внесения данных в базу данных со стороны пользователя и
# формы для внесения поисковых запросов - далее: формы.
# Список блоков:
# блок 1 - формы для поисков и распечатки этикеток
# блок 2 - формы для комментариев и примечаний, особенностей - внесение и обновление
# блок 3 - формы для первичного внесения ЛО; СИ, ИО, ВО и их характеристик. Под каждой формой - форма обновления если есть
# блок 4 - формы для внесения производителей, поверителей, комнат, принадлежностей, контактов поверителей
# блок 5 - формы для внесения внесения сведений о поверке, аттестации, проверке характеристик плюс формы изменения
# блок 6 - смена ответственного и помещения, изменение названия комнат
# блок 7 - формы для микроклимата
# блок 8 - формы для ТОИР
# """


from datetime import datetime, date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from django import forms
from django.forms import ModelForm

from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField
from .lookups import*

from equipment.models import*


# блок 1 - формы для поисков и распечатки этикеток

class SearchMEForm(forms.Form):
    """форма для поиска по полям списка СИ и ИО и ВО"""
    name = forms.CharField(label='Название', required=False,
                           help_text='введите название частично или полностью',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    exnumber = forms.CharField(label='Внут. №', required=False,
                               help_text='вн. № полн.',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    lot = forms.CharField(label='Заводской №', required=False,
                          help_text='заводской № полностью',
                          widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('exnumber', css_class='form-group col-md-2 mb-0'),
                Column('lot', css_class='form-group col-md-2 mb-0'),
                Row(Submit('submit', 'Найти', css_class='btn  btn-prima col-md-9 mb-3 mt-4 ml-4'))))


class Searchreestrform(forms.Form):
    """форма для поиска по полям списка госреестров"""
    name = forms.CharField(label='Название', required=False,
                           help_text='введите название частично или полностью',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    reestr = forms.CharField(label='Номер в госреестре', required=False,
                             help_text='введите номер частично или полностью',
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('reestr', css_class='form-group col-md-4 mb-0'),
                Submit('submit', 'Найти', css_class='btn  btn-prima col-md-4 mb-4 mt-4 ml-0')))


class Searchtestingform(forms.Form):
    """форма для поиска по полям списка свойств ИО"""
    name = forms.CharField(label='Название', required=False,
                           help_text='введите название частично или полностью',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-8 mb-0'),
                Submit('submit', 'Найти', css_class='btn  btn-prima col-md-4 mb-4 mt-4 ml-0')))


class LabelEquipmentform(forms.Form):
    """форма для внесения номеров оборудования для распечатки этикеток о поверке/аттестации"""
    n1 = forms.CharField(label='№1', required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'А001'}))
    n2 = forms.CharField(label='№2', required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'В010'}))
    n3 = forms.CharField(label='№3', required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    n4 = forms.CharField(label='№4', required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    n5 = forms.CharField(label='№5', required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    n6 = forms.CharField(label='№6', required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    n7 = forms.CharField(label='№7', required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    n8 = forms.CharField(label='№8', required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    n9 = forms.CharField(label='№9', required=False,
                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    n10 = forms.CharField(label='№10', required=False,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    n11 = forms.CharField(label='№11', required=False,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    n12 = forms.CharField(label='№12', required=False,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    n13 = forms.CharField(label='№13', required=False,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    n14 = forms.CharField(label='№14', required=False,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('n1', css_class='form-group col-md-2 mb-0'),
                Column('n2', css_class='form-group col-md-2 mb-0'),
                Column('n3', css_class='form-group col-md-2 mb-0'),
                Column('n4', css_class='form-group col-md-2 mb-0')),
            Row(
                Column('n5', css_class='form-group col-md-2 mb-0'),
                Column('n6', css_class='form-group col-md-2 mb-0'),
                Column('n7', css_class='form-group col-md-2 mb-0'),
                Column('n8', css_class='form-group col-md-2 mb-0')),
            Row(
                Column('n9', css_class='form-group col-md-2 mb-0'),
                Column('n10', css_class='form-group col-md-2 mb-0'),
                Column('n11', css_class='form-group col-md-2 mb-0'),
                Column('n12', css_class='form-group col-md-2 mb-0')),
            Row(
                Column('n13', css_class='form-group col-md-2 mb-0'),
                Column('n14', css_class='form-group col-md-2 mb-0')),
            Row(Submit('submit', 'сформировать', css_class='btn  btn-prima col-md-6 mb-3 mt-4 ml-4')))


class DateForm(forms.Form):
    """форма для указания даты"""
    date = forms.DateField(label='Дата', initial = date.today(),
                           widget=forms.DateInput(
                               attrs={'class': 'form-control', 'placeholder': ''}),)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-4 mb-0 ml-2 mr-2'),
                Submit('submit', 'сформировать', css_class='btn  btn-prima col-md-6 mb-3 mt-4 ml-2 mr-2')))



# блок 2 - формы для комментариев и примечаний, особенностей - внесение и обновление

class NoteCreationForm(forms.ModelForm):
    """форма для  записей об оборудовании - запись событий для карточки на оборудование"""
    date = forms.DateField(label='Дата', required=False, initial=datetime.now(),
                           widget=forms.DateInput(
                               attrs={'class': 'form-control', 'placeholder': ''}),
                           input_formats=(
                               '%Y-%m-%d',
                               '%m/%d/%Y',
                               '%m/%d/%y',
                               '%d.%m.%Y',
                           ))
    type = forms.ChoiceField(label='Выберите тип события', required=True,
                             choices=NOTETYPE,
                             widget=forms.Select(attrs={'class': 'form-control'}))
    note = forms.CharField(label='Внести запись о приборе', max_length=10000,
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'placeholder': 'введите текст записи о приборе'}))
    img = forms.ImageField(label='Загрузить фото прибора или документа', required=False,
                           widget=forms.FileInput)
    author = forms.CharField(label='Автор записи', required=False,  max_length=100,
                             help_text='впишите автора если вы не авторизованы',
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CommentsEquipment
        fields = ['date', 'type', 'note', 'img', 'author']


class CommentsVerificationCreationForm(forms.ModelForm):
    """форма для комментария к истории поверки"""
    note = forms.CharField(label='Обновить комментарий отвественного', max_length=10000000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': ''}))

    class Meta:
        model = CommentsVerificationequipment
        fields = ['note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('note', css_class='form-group col-md-10 mb-0'),
                Row(Submit('submit', 'Обновить', css_class='btn  btn-info col-md-10 mb-3 mt-4 ml-4'))))


class CommentsAttestationequipmentForm(forms.ModelForm):
    """форма для комментария к истории аттестации"""
    note = forms.CharField(label='Обновить комментарий отвественного', max_length=10000000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': ''}))

    class Meta:
        model = CommentsAttestationequipment
        fields = ['note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('note', css_class='form-group col-md-10 mb-0'),
                Row(Submit('submit', 'Обновить', css_class='btn  btn-info col-md-10 mb-3 mt-4 ml-4'))))


class MetrologyUpdateForm(forms.ModelForm):
    """форма для обновления постоянные особенности метрологического обеспечения"""
    notemetrology = forms.CharField(label='Указать постоянные особенности метрологического обеспечения',
                                    max_length=10000,
                                    required=False,
                                    widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Equipment
        fields = [
            'notemetrology'
        ]


# блок 3 - формы для внесения ЛО; СИ, ИО, ВО и их характеристик. Под каждой формой - форма обновления если есть


class EquipmentCreateForm(forms.ModelForm):
    """форма для внесения ЛО"""
    exnumber = forms.CharField(label='Внутренний номер', max_length=10000, initial='А',
                               help_text='уникальный, придумайте первую букву номера по названию оборудования (заглавная кириллица, 1 буква)',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'А'}))
    lot = forms.CharField(label='Заводской номер', max_length=10000,
                          help_text='указан производителем на приборе и в документах',
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    yearmanuf = forms.CharField(label='Год выпуска прибора', max_length=10000, initial=datetime.now().year,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    manufacturer = AutoCompleteSelectField('manufacturer_tag', label='Производитель прибора', required=True, help_text='Начните вводить название строчными или заглавными буквами', show_help_text=False)
    status = forms.ChoiceField(label='Статус (эксплуатация, ремонт и тд)', initial='Эксплуатация',
                               choices=CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    new = forms.ChoiceField(label='Новый или б/у', initial='новый',
                            choices=(
                                     ('новый', 'новый'),
                                     ('б/у', 'б/у')),
                            widget=forms.Select(attrs={'class': 'form-control'}))
    invnumber = forms.CharField(label='Инвентарный номер', max_length=10000, initial='б/н',  required=False,
                                help_text='Присваивает бухгалтерия',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    kategory = forms.ChoiceField(label='Категория', initial='Средство измерения',
                                 choices=KATEGORY,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    pasport = forms.CharField(label='Паспорт (ссылка)', max_length=10000, required=False)
    instruction = forms.CharField(label='Внутренняя инструкция (ссылка)', max_length=10000, required=False)                                       
    individuality = forms.CharField(label='Индивидуальные особенности прибора', max_length=10000, required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    notemaster = forms.CharField(label='Примечание ответственного за прибор', max_length=10000, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label='Стоимость', max_digits=10, decimal_places=2, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': '0000.00'}))  
    pravo = forms.CharField(label='Право владения прибором (например, номер и дата накладной)',  required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    notemetrology = forms.CharField(label='Примечание о метрологическом обеспечении прибора',  required=False)
    repair = forms.CharField(label='Контакты для ремонта', max_length=1000,  required=False)    
    yearintoservice = forms.CharField(label='Год ввода в эксплуатацию', max_length=10000, initial=datetime.now().year,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    standard_number = forms.CharField(label='номер в качестве эталона в ФИФ, разряд по ГПС, ЛПС, и т. п', max_length=10000, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    pravo_have = forms.ChoiceField(label='Собственность или аренда', initial='собственность',
                            choices=( ('собственность', 'собственность'),
                                     ('аренда', 'аренда')), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Equipment
        fields = [
            'exnumber', 'lot', 'yearmanuf', 'manufacturer', 'status', 
            'new', 'invnumber', 'kategory', 'individuality', 'notemaster', 'price',
            'pasport', 'instruction',
             'notemetrology', 'repair', 'yearintoservice', 'pravo', 
            'standard_number', 'pravo_have',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('kategory', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('exnumber', css_class='form-group col-md-4 mb-0'),
                Column('lot', css_class='form-group col-md-4 mb-0'),
                Column('invnumber', css_class='form-group col-md-4 mb-0')),
            Row(
                Column('yearmanuf', css_class='form-group col-md-4 mb-0'),
                Column('manufacturer', css_class='form-group col-md-4 mb-0'),
                Column('new', css_class='form-group col-md-4 mb-0')),
            Row(
                Column('status', css_class='form-group col-md-6 mb-0'),
                Column('yearintoservice', css_class='form-group col-md-6 mb-0'),
                ),
            Row(
                Column('pasport', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('instruction', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('individuality', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('price', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('notemetrology', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('repair', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('standard_number', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('pravo', css_class='form-group col-md-6 mb-0'),
                Column('pravo_have', css_class='form-group col-md-6 mb-0'),
                ),
            Row(Submit('submit', 'Записать', css_class='btn btn-primary col-md-11 mb-3 mt-4 ml-4')))


class EquipmentUpdateForm(forms.ModelForm):
    """форма для обновления разрешенных полей ЛО ответственному за оборудование"""
    status = forms.ChoiceField(label='Выберите статус прибора (если требуется изменить статус)', required=False,
                               choices=CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    individuality = forms.CharField(label='Индивидуальные особенности прибора', max_length=10000, required=False,
                                    widget=forms.Textarea(attrs={'class': 'form-control'}))
    notemaster = forms.CharField(label='Примечание (или временное предостережение для сотрудников)', max_length=10000, required=False,
                                 widget=forms.Textarea(attrs={'class': 'form-control'}))
    notemetrology = forms.CharField(label='Примечание о метрологическом обеспечении прибора (для вывода на странице поверок: телефоны поверителей и т.п.)', max_length=10000, required=False,
                                 widget=forms.Textarea(attrs={'class': 'form-control'}))
    pasport = forms.CharField(label='Паспорт', max_length=10000, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'добавьте ссылку на паспорт'}))
    instruction = forms.CharField(label='Основная инструкция по эксплуатации', max_length=10000, required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'добавьте ссылку на инструкцию'}))
    invnumber = forms.CharField(label='Инвентарный номер', max_length=10000, initial='б/н', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    repair = forms.CharField(label='Контакты для ремонта', max_length=10000,  required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    standard_number = forms.CharField(label='номер в качестве эталона в ФИФ, разряд по ГПС, ЛПС, и т. п', max_length=10000, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    pravo = forms.CharField(label='Право владения прибором (например, номер и дата накладной)', max_length=10000,  required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    pravo_have = forms.ChoiceField(label='Собственность или аренда', initial='собственность',
                            choices=( ('собственность', 'собственность'),
                                     ('аренда', 'аренда')), widget=forms.Select(attrs={'class': 'form-control'}))
                                    

    class Meta:
        model = Equipment
        fields = [
            'status', 'individuality', 'notemaster',
            'pasport', 'instruction',
            'pravo',
             'invnumber',
            'repair', 'notemetrology',
            'standard_number', 'pravo_have',
                  ]


class MeasurEquipmentCharaktersCreateForm(forms.ModelForm):
    """форма для внесения характеристик СИ (госреестра)"""
    reestr = forms.CharField(label='Номер в Госреестре', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': ''}))
    name = forms.CharField(label='Название прибора', max_length=10000000, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': ''}))
    typename = forms.CharField(label='Тип', max_length=10000000, required=False, initial='нет типа',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': ''}))
    modificname = forms.CharField(label='Модификация', max_length=10000000, required=False, initial='нет модификации',
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': ''}))
    calinterval = forms.CharField(label='Межповерочный интервал, месяцев', max_length=10000000, required=True,
                                  initial='12',
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))
    measurydiapason = forms.CharField(label='Диапазон измерений', max_length=10000000, required=True,
                                      widget=forms.Textarea(attrs={'class': 'form-control',
                                                                   'placeholder': ''}))
    accuracity = forms.CharField(label='Класс точности /(разряд/), погрешность и /(или/) '
                                 'неопределённость /(класс, разряд/)', max_length=10000000, required=True,
                                 widget=forms.Textarea(attrs={'class': 'form-control',
                                                              'placeholder': ''}))
    power = forms.BooleanField(label='Работает от сети', required=False, initial=False)
    needsetplace = forms.BooleanField(label='Требуется установка', required=False, initial=False)
    voltage = forms.CharField(label='Напряжение требуемое', required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': ''}))
    frequency = forms.CharField(label='Частота требуемая', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': ''}))
    temperature = forms.CharField(label='Температура требуемая', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))
    humidicity = forms.CharField(label='Влажность требуемая', required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': ''}))
    pressure = forms.CharField(label='Давление требуемое', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': ''}))
    setplace = forms.CharField(label='Описание мероприятий по установке', required=False,
                               widget=forms.Textarea(attrs={'class': 'form-control',
                                                            'placeholder': ''}))
    complectlist = forms.CharField(label='Где указана комплектация', required=False,
                                   initial='Паспорт, страница 2',
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': ''}))
    expresstest = forms.BooleanField(label='Возможно тестирование', required=False, initial=False)
    traceability = forms.CharField(label='Информация о прослеживаемости (к какому '
                                   'эталону прослеживаются измерения)', required=False,
                                   widget=forms.Textarea(attrs={'class': 'form-control',
                                                                 'placeholder': ''}))
    cod = forms.CharField(label='виды измерений, тип (группа) средств измерений по МИ 2314', required=False,
                                   widget=forms.Textarea(attrs={'class': 'form-control',
                                                                 'placeholder': ''}))

    class Meta:
        model = MeasurEquipmentCharakters
        fields = [
            'reestr',
            'name',
            'typename',
            'modificname',
            'calinterval',
            'measurydiapason', 'accuracity',
            'aim',
            'power',
            'needsetplace',
            'voltage',
            'frequency',
            'temperature',
            'humidicity',
            'pressure',
            'setplace',
            'complectlist',
            'expresstest',
            'traceability',
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('reestr', css_class='form-group col-md-6 mb-0'),
                Column('calinterval', css_class='form-group col-md-6 mb-0')),
            Row(
                Column('name', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('typename', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('modificname', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('measurydiapason',  css_class='form-group col-md-12 mb-0')),
            Row(
                Column('accuracity', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('complectlist', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('power', css_class='form-group col-md-4 mb-0'),
                Column('needsetplace', css_class='form-group col-md-4 mb-0'),
                Column('expresstest', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('voltage', css_class='form-group col-md-6 mb-0'),
                Column('frequency', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('temperature', css_class='form-group col-md-4 mb-0'),
                Column('humidicity', css_class='form-group col-md-4 mb-0'),
                Column('pressure', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('setplace', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('traceability', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('cod', css_class='form-group col-md-12 mb-0'),
            ),
            Row(Submit('submit', 'Записать', css_class='btn  btn-info col-md-11 mb-3 mt-4 ml-4')))


class TestingEquipmentCharaktersCreateForm(forms.ModelForm):
    """форма для внесения характеристик ИО"""
    name = forms.CharField(label='Название прибора', max_length=10000000, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': ''}))
    typename = forms.CharField(label='Тип', max_length=10000000, required=False, initial='нет типа',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': ''}))
    modificname = forms.CharField(label='Модификация', max_length=10000000, required=False, initial='нет модификации',
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))
    calinterval = forms.CharField(label='Межаттестационный интервал, месяцев', max_length=10000000, required=True,
                                  initial='24',
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))
    measurydiapason = forms.CharField(label='Основные технические характеристики', max_length=10000000, required=True,
                                      widget=forms.Textarea(attrs={'class': 'form-control',
                                                                   'placeholder': ''}))
    power = forms.BooleanField(label='Работает от сети', required=False, initial=False)
    needsetplace = forms.BooleanField(label='Требуется установка', required=False, initial=False)
    voltage = forms.CharField(label='Напряжение требуемое', required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': ''}))
    frequency = forms.CharField(label='Частота требуемая', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': ''}))
    temperature = forms.CharField(label='Температура требуемая', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))
    humidicity = forms.CharField(label='Влажность требуемая', required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': ''}))
    pressure = forms.CharField(label='Давление требуемое', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': ''}))
    setplace = forms.CharField(label='Описание мероприятий по установке', required=False,
                               widget=forms.Textarea(attrs={'class': 'form-control',
                                                            'placeholder': ''}))
    complectlist = forms.CharField(label='Где указана комплектация', required=False,
                                   initial='Руководство по эксплуатации, страница 2',
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': ''}))
    expresstest = forms.BooleanField(label='Возможно тестирование', required=False, initial=False)

    class Meta:
        model = TestingEquipmentCharakters
        fields = [
                  'name',
                  'typename',
                  'modificname',
                  'calinterval',
                  'measurydiapason',
                  'aim',
                  'aim2',
                  'ndoc',
                  'power',
                  'needsetplace',
                  'voltage',
                  'frequency',
                  'temperature',
                  'humidicity',
                  'pressure',
                  'setplace',
                  'complectlist',
                  'expresstest',
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('calinterval', css_class='form-group col-md-6 mb-0')),
            Row(
                Column('name', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('typename', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('modificname', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('measurydiapason',  css_class='form-group col-md-12 mb-0')),
            Row(
                Column('accuracity', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('complectlist', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('power', css_class='form-group col-md-4 mb-0'),
                Column('needsetplace', css_class='form-group col-md-4 mb-0'),
                Column('expresstest', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('voltage', css_class='form-group col-md-6 mb-0'),
                Column('frequency', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('temperature', css_class='form-group col-md-4 mb-0'),
                Column('humidicity', css_class='form-group col-md-4 mb-0'),
                Column('pressure', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('setplace', css_class='form-group col-md-12 mb-0'),
            ),
            Row(Submit('submit', 'Записать', css_class='btn  btn-info col-md-11 mb-3 mt-4 ml-4')))


class HelpingEquipmentCharaktersCreateForm(forms.ModelForm):
    """форма для внесения характеристик ВО"""
    name = forms.CharField(label='Название прибора', max_length=10000000, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': ''}))
    typename = forms.CharField(label='Тип', max_length=10000000, required=False, initial='нет типа',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': ''}))
    modificname = forms.CharField(label='Модификация', max_length=10000000, required=False, initial='нет модификации',
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))
    measurydiapason = forms.CharField(label='Основные технические характеристики', max_length=10000000, required=False,
                                      widget=forms.Textarea(attrs={'class': 'form-control',
                                                                    'placeholder': ''}))
    power = forms.BooleanField(label='Работает от сети', required=False, initial=False)
    needsetplace = forms.BooleanField(label='Требуется установка', required=False, initial=False)
    voltage = forms.CharField(label='Напряжение требуемое', required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': ''}))
    frequency = forms.CharField(label='Частота требуемая', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': ''}))
    temperature = forms.CharField(label='Температура требуемая', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))
    humidicity = forms.CharField(label='Влажность требуемая', required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': ''}))
    pressure = forms.CharField(label='Давление требуемое', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': ''}))
    setplace = forms.CharField(label='Описание мероприятий по установке', required=False,
                               widget=forms.Textarea(attrs={'class': 'form-control',
                                                            'placeholder': ''}))
    complectlist = forms.CharField(label='Где указана комплектация', required=False,
                                   initial='Руководство по эксплуатации, страница 2',
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': ''}))
    expresstest = forms.BooleanField(label='Возможно тестирование', required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('typename', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('modificname', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('measurydiapason',  css_class='form-group col-md-12 mb-0')),
            Row(
                Column('complectlist', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('power', css_class='form-group col-md-4 mb-0'),
                Column('needsetplace', css_class='form-group col-md-4 mb-0'),
                Column('expresstest', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('voltage', css_class='form-group col-md-6 mb-0'),
                Column('frequency', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('temperature', css_class='form-group col-md-4 mb-0'),
                Column('humidicity', css_class='form-group col-md-4 mb-0'),
                Column('pressure', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('setplace', css_class='form-group col-md-12 mb-0'),
            ),

            Row(Submit('submit', 'Записать', css_class='btn  btn-info col-md-11 mb-3 mt-4 ml-4')))

    class Meta:
        model = HelpingEquipmentCharakters
        fields = [
            'name',
            'typename',
            'modificname',
            'measurydiapason',
            'aim',
            'ndoc',
            'power',
            'needsetplace',
            'voltage',
            'frequency',
            'temperature',
            'humidicity',
            'pressure',
            'setplace',
            'complectlist',
            'expresstest',
            'kvasyattestation',
                  ]


class MeasurEquipmentCreateForm(forms.ModelForm):
    """форма для внесения СИ"""
    charakters = AutoCompleteSelectField('mecharakters_tag', label='Госреестр', required=True, help_text='Начните вводить название прибора строчными или с заглавной буквы', show_help_text=False)

    class Meta:
        model = MeasurEquipment
        fields = [
            'charakters',
                  ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('charakters', css_class='form-group col-md-10 mb-0'),
                ),
            Submit('submit', 'Внести'))


class TestingEquipmentCreateForm(forms.ModelForm):
    """форма для внесения ИО"""
    charakters = forms.ModelChoiceField(label='Характеристики испытательного оборудования', required=False,
                                        queryset=TestingEquipmentCharakters.objects.all().order_by('name'),
                                        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = TestingEquipment
        fields = [
            'charakters',
                  ]


class HelpingEquipmentCreateForm(forms.ModelForm):
    """форма для внесения ВО"""
    charakters = forms.ModelChoiceField(label='Характеристики вспомогательного оборудования', required=False,
                                        queryset=HelpingEquipmentCharakters.objects.all().order_by('name'),
                                        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = HelpingEquipment
        fields = [
            'charakters',
                  ]


# блок 4 - формы для внесения производителей, поверителей, комнат, принадлежностей

class ManufacturerCreateForm(forms.ModelForm):
    """форма для внесения производителя"""
    companyName = forms.CharField(label='Название компании', max_length=10000,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(label='Страна', max_length=10000, initial='Россия',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    companyAdress = forms.CharField(label='Адрес', max_length=10000,
                                    required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    telnumber = forms.CharField(label='Телефон общий', max_length=10000, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    telnumberhelp = forms.CharField(label='Телефон техподдержки для вопросов по приборам', required=False,
                                    max_length=10000,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Manufacturer
        fields = [
            'companyName', 'country', 'companyAdress', 'telnumber',
            'telnumberhelp'
                  ]


class VerificatorsCreationForm(forms.ModelForm):
    """форма для внесения компании поверителя"""
    companyName = forms.CharField(label='Название организации', max_length=10000000,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))
    companyAdress = forms.CharField(label='Адрес организации', max_length=10000000,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))
    telnumber = forms.CharField(label='Телефон', max_length=10000000,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))
    email = forms.CharField(label='email', max_length=10000000,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))
    head_position = forms.CharField(label='Кому: должность лица организации-поверителя (для шапки заявки на поверку)', max_length=10000000,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))
    head_name  = forms.CharField(label='Кому: ФИО лица организации-поверителя (для шапки заявки на поверку)', max_length=10000000,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))


    class Meta:
        model = Verificators
        fields = [
            'companyName',
            'companyAdress',
            'telnumber',
            'email',
            'head_position',
            'head_name',
                  ]


class AgreementVerificatorsCreationForm(forms.ModelForm):
    """форма для внесения договора с компанией поверителем"""
    verificator = forms.ModelChoiceField(label='Организация-поверитель',
                                         queryset=Verificators.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    ver_agreement_number = forms.CharField(label='Номер договора с организацией-поверителем', max_length=10000000,  required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))
    ver_agreement_date = forms.CharField(label='Дата договора с организацией-поверителем', max_length=10000000, required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))

    ver_agreement_card = forms.CharField(label='Номер учетной карточки у с организации-поверителя', max_length=10000000, required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))

    class Meta:
        model = Agreementverification
        fields = [
            'verificator',
            'ver_agreement_number',
            'ver_agreement_date',
            'ver_agreement_card',
                  ]


class RoomsCreateForm(forms.ModelForm):
    """форма для внесения комнаты"""
    roomnumber = forms.CharField(label='Номер комнаты', widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = Rooms
        fields = [
            'roomnumber'
                  ]


class DocsConsCreateForm(forms.ModelForm):
    """форма для внесения документа или принадлежности"""
    date = forms.CharField(label='Дата',  initial=datetime.now().year,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    docs = forms.CharField(label='Наименование документа/принадлежности', initial='Паспорт', max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    source = forms.CharField(label='Источник', initial='От поставщика',
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    note = forms.CharField(label='Примечание', required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = DocsCons
        fields = [
            'date',
            'docs', 'source',
            'note'
                  ]

# блок 5 - формы для внесения внесения сведений о поверке, аттестации, проверке характеристик плюс формы изменения


   

class VerificationRegForm(forms.ModelForm):
    """форма для внесения сведений о поверке"""
    date = forms.DateField(label='Дата поверки',
                           widget=forms.DateInput(
                                                  attrs={'class': 'form-control', 'placeholder': ''}),
                           input_formats=(
                                          '%Y-%m-%d',  # '2006-10-25'
                                          '%m/%d/%Y',  # '10/25/2006'
                                          '%m/%d/%y',
                                          '%d.%m.%Y',
                                           ))
    datedead = forms.DateField(label='Дата окончания поверки',
                               widget=forms.DateInput(
                                                      attrs={'class': 'form-control', 'placeholder': ''}),
                               input_formats=(
                                              '%Y-%m-%d',  # '2006-10-25'
                                              '%m/%d/%Y',  # '10/25/2006'
                                              '%m/%d/%y',
                                              '%d.%m.%Y',
                                              ))
    dateorder = forms.DateField(label='Дата заказа поверки', required=False,
                                widget=forms.DateInput(
                                                       attrs={'class': 'form-control', 'placeholder': ''}),
                                input_formats=(
                                               '%Y-%m-%d',  # '2006-10-25'
                                               '%m/%d/%Y',  # '10/25/2006'
                                               '%m/%d/%y',
                                               '%d.%m.%Y',
                                                ))
    arshin = forms.CharField(label='Ссылка на сведения о поверке в Аршин', max_length=10000,
                             required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    certnumber = forms.CharField(label='№ свидетельства о поверке', max_length=10000,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label='Стоимость поверки', max_digits=10, decimal_places=2,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': '0000.00'}))
    statusver = forms.ChoiceField(label='Результат поверки',
                                  choices=CHOICESVERIFIC,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    verificator = AutoCompleteSelectField('verificator_tag', label='Организация-поверитель', required=True,  help_text='Начните вводить название, например: "ФБУ "ТЕСТ-С.-ПЕТЕРБУРГ""', show_help_text=False)
    place = forms.ChoiceField(label='Место поверки',
                              choices=CHOICESPLACE,
                              widget=forms.Select(attrs={'class': 'form-control'}))
    cust = forms.BooleanField(label='Не оплачивалась', required=False, help_text='Например, если поверку оплачивал производитель')
    dateordernew = forms.DateField(label='Дата заказа замены', required=False,
                                   help_text='Укажите, если поверка не выгодна и вы покупаете замену',
                                   widget=forms.DateInput(
                                                          attrs={'class': 'form-control', 'placeholder': ''}),
                                   input_formats=(
                                                  '%Y-%m-%d',
                                                  '%m/%d/%Y',
                                                  '%m/%d/%y',
                                                  '%d.%m.%Y',
                                                   ))
    extra = forms.CharField(label='Дополнительная информация/выписка из текущих сведений о поверке',
                                  widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Verificationequipment
        fields = ['date', 'datedead', 'dateorder', 'arshin', 'certnumber',
                  'price', 'statusver',  'verificator', 
                  'place', 'year',
                  'dateordernew',
                  'cust',
                  'extra',
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-4 mb-0'),
                Column('datedead', css_class='form-group col-md-4 mb-0'),
                Column('dateorder', css_class='form-group col-md-4 mb-0'),
                ),
            Row(
                Column('arshin', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('certnumber', css_class='form-group col-md-6 mb-0'),
                Column('statusver', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('verificator', css_class='form-group col-md-6 mb-0'),
                Column('place', css_class='form-group col-md-3 mb-0'),   
                Column('dateordernew', css_class='form-group col-md-3 mb-1'), 
            ),
            Row(
                Column('price', css_class='form-group col-md-3 mb-0'),                       
                Column('cust', css_class='form-group col-md-8 mb-0'), 
            ),
            Row(
                Column('extra', css_class='form-group col-md-12 mb-1')),
            Submit('submit', 'Внести'))




class CalibrationRegForm(forms.ModelForm):
    """форма для внесения сведений о калибровке"""
    date = forms.DateField(label='Дата калибровки',
                           widget=forms.DateInput(
                                                  attrs={'class': 'form-control', 'placeholder': ''}),
                           input_formats=(
                                          '%Y-%m-%d',  # '2006-10-25'
                                          '%m/%d/%Y',  # '10/25/2006'
                                          '%m/%d/%y',
                                          '%d.%m.%Y',
                                           ))
    datedead = forms.DateField(label='Дата окончания калибровки рекомендуемая',
                               widget=forms.DateInput(
                                                      attrs={'class': 'form-control', 'placeholder': ''}),
                               input_formats=(
                                              '%Y-%m-%d',  # '2006-10-25'
                                              '%m/%d/%Y',  # '10/25/2006'
                                              '%m/%d/%y',
                                              '%d.%m.%Y',
                                              ))
    dateorder = forms.DateField(label='Дата заказа калибровки', required=False,
                                widget=forms.DateInput(
                                                       attrs={'class': 'form-control', 'placeholder': ''}),
                                input_formats=(
                                               '%Y-%m-%d',  # '2006-10-25'
                                               '%m/%d/%Y',  # '10/25/2006'
                                               '%m/%d/%y',
                                               '%d.%m.%Y',
                                                ))
    arshin = forms.CharField(label='Ссылка на скан сертификата', max_length=10000,
                             required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    certnumber = forms.CharField(label='№ сертификата калибровки', max_length=10000,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label='Стоимость калибровки', max_digits=10, decimal_places=2,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': '0000.00'}))
    statusver = forms.ChoiceField(label='Результат калибровки',
                                  choices=CHOICESCAL,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    verificator = AutoCompleteSelectField('verificator_tag', label='Организация-поверитель', required=True,  help_text='Начните вводить название, например: "ФБУ "ТЕСТ-С.-ПЕТЕРБУРГ""', show_help_text=False)
    place = forms.ChoiceField(label='Место калибровки',
                              choices=CHOICESPLACE,
                              widget=forms.Select(attrs={'class': 'form-control'}))
    cust = forms.BooleanField(label='Не оплачивалась', required=False, help_text='Например, если калибровку оплачивал производитель')
    dateordernew = forms.DateField(label='Дата заказа замены', required=False,
                                   help_text='Укажите, если калибровкa не выгодна и вы покупаете замену',
                                   widget=forms.DateInput(
                                                          attrs={'class': 'form-control', 'placeholder': ''}),
                                   input_formats=(
                                                  '%Y-%m-%d',
                                                  '%m/%d/%Y',
                                                  '%m/%d/%y',
                                                  '%d.%m.%Y',
                                                   ))
    extra = forms.CharField(label='Дополнительная информация/выписка из текущих сведений о калибровкe',
                                  widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Calibrationequipment
        fields = ['date', 'datedead', 'dateorder', 'arshin', 'certnumber',
                  'price', 'statusver',  'verificator', 
                  'place', 'year',
                  'dateordernew',
                  'cust',
                  'extra',
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-4 mb-0'),
                Column('datedead', css_class='form-group col-md-4 mb-0'),
                Column('dateorder', css_class='form-group col-md-4 mb-0'),
                ),
            Row(
                Column('arshin', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('certnumber', css_class='form-group col-md-6 mb-0'),
                Column('statusver', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('verificator', css_class='form-group col-md-6 mb-0'),
                Column('place', css_class='form-group col-md-3 mb-0'),   
                Column('dateordernew', css_class='form-group col-md-3 mb-1'), 
            ),
            Row(
                Column('price', css_class='form-group col-md-3 mb-0'),                       
                Column('cust', css_class='form-group col-md-8 mb-0'), 
            ),
            Row(
                Column('extra', css_class='form-group col-md-12 mb-1')),
            Submit('submit', 'Внести'))


class AttestationRegForm(forms.ModelForm):
    """форма для  внесения сведений об аттестации"""
    date = forms.DateField(label='Дата аттестации', required=False,
                           widget=forms.DateInput(
                                                  attrs={'class': 'form-control', 'placeholder': ''}),
                           input_formats=(
                                          '%Y-%m-%d',  # '2006-10-25'
                                          '%m/%d/%Y',  # '10/25/2006'
                                          '%m/%d/%y',
                                          '%d.%m.%Y',
                                           ))
    datedead = forms.DateField(label='Дата окончания аттестации', required=False,
                               widget=forms.DateInput(
                                                      attrs={'class': 'form-control', 'placeholder': ''}),
                               input_formats=(
                                              '%Y-%m-%d',  # '2006-10-25'
                                              '%m/%d/%Y',  # '10/25/2006'
                                              '%m/%d/%y',
                                              '%d.%m.%Y',
                                               ))
    dateorder = forms.DateField(label='Дата заказа аттестации', required=False,
                                widget=forms.DateInput(
                                                       attrs={'class': 'form-control', 'placeholder': ''}),
                                input_formats=(
                                               '%Y-%m-%d',  # '2006-10-25'
                                               '%m/%d/%Y',  # '10/25/2006'
                                               '%m/%d/%y',
                                               '%d.%m.%Y',
                                                ))
    certnumber = forms.CharField(label='№ аттестата', max_length=10000, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label='Стоимость данной атт.', max_digits=10, decimal_places=2,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': '0000.00'}))
    statusver = forms.ChoiceField(label='Результат аттестации',
                                  choices=CHOICESATT,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    verificator = forms.ModelChoiceField(label='Организация-поверитель',
                                         queryset=Verificators.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    place = forms.ChoiceField(label='Место аттестации',
                              choices=CHOICESPLACE, initial='В ПА',
                              widget=forms.Select(attrs={'class': 'form-control'}))
    cust = forms.BooleanField(label='Аттестация заказана поставщиком', required=False)
    img = forms.ImageField(label='Аттестат', widget=forms.FileInput, required=False)
    dateordernew = forms.DateField(label='Дата заказа замены', required=False,
                                   help_text='Укажите, если аттестации не выгодна',
                                   widget=forms.DateInput(
                                                          attrs={'class': 'form-control', 'placeholder': ''}),
                                   input_formats=(
                                                  '%Y-%m-%d',
                                                  '%m/%d/%Y',
                                                  '%m/%d/%y',
                                                  '%d.%m.%Y',
                                                  ))
    year = forms.CharField(label='год аттестации', max_length=10000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    extra = forms.CharField(label='Дополнительная информация/выписка из аттестата',
                                  widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Attestationequipment
        fields = ['date', 'datedead', 'dateorder', 'certnumber',
                  'price', 'statusver',  'verificator', 
                  'place',
                  'year',
                  'dateordernew',
                  'cust',
                  'extra',
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-4 mb-0'),
                Column('datedead', css_class='form-group col-md-4 mb-0'),
                Column('dateorder', css_class='form-group col-md-4 mb-0'),
                ),
            Row(
                Column('certnumber', css_class='form-group col-md-4 mb-0'),
                Column('statusver', css_class='form-group col-md-4 mb-0'),
                Column('price', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('verificator', css_class='form-group col-md-4 mb-0'),
                Column('verificatorperson', css_class='form-group col-md-4 mb-0'),
                Column('place', css_class='form-group col-md-4 mb-0'),
                Column('cust', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('img', css_class='form-group col-md-6 mb-1'),
                Column('year', css_class='form-group col-md-6 mb-1'),
                Column('dateordernew', css_class='form-group col-md-6 mb-1')),
            Row(
                Column('extra', css_class='form-group col-md-12 mb-1')),
            Submit('submit', 'Внести'))


class OrderMEUdateForm(forms.ModelForm):
    """форма для обозначения того, что заказана поверка, или ЛО на замену"""
    haveorder = forms.BooleanField(label='', required=False)

    class Meta:
        model = Verificationequipment
        fields = ['haveorder']


class OrderTEUdateForm(forms.ModelForm):
    """форма для обозначения того, что заказана аттестация, или ЛО на замену"""
    haveorder = forms.BooleanField(label='', required=False)

    class Meta:
        model = Attestationequipment
        fields = ['haveorder']


# блок 6 - смена ответственного и помещения

class PersonchangeForm(forms.ModelForm):
    """форма для смены ответственного за ЛО"""
    def __init__(self, ruser, *args, **kwargs):
        super(PersonchangeForm, self).__init__(*args, **kwargs)
        self.fields['person'].queryset = Employees.objects.filter(userid__userid = ruser)
    
    class Meta:
        model = Personchange
        fields = [
            'person'
                  ]
        widgets = {'person':forms.Select(attrs={'class': 'form-control'}),}



class RoomschangeForm(forms.ModelForm):
    """форма для смены Размещения ЛО"""
    def __init__(self, ruser, *args, **kwargs):
        super(RoomschangeForm, self).__init__(*args, **kwargs)
        self.fields['roomnumber'].queryset = Rooms.objects.filter(pointer = ruser)

    class Meta:
        model = Roomschange
        fields = [
            'roomnumber'
                  ]
        widgets = {'roomnumber':forms.Select(attrs={'class': 'form-control'}),}
        labels = {'roomnumber': 'название или номер помещения'}



class RoomsUpdateForm(forms.ModelForm):
    """форма для создания обновления названия комнаты и оборудования"""
    def __init__(self, ruser, *args, **kwargs):
        super(RoomsUpdateForm, self).__init__(*args, **kwargs)
        self.fields['equipment1'].queryset = MeasurEquipment.objects.filter(equipment__pointer = ruser).filter(charakters__name__contains='Барометр')
        self.fields['equipment2'].queryset = MeasurEquipment.objects.filter(equipment__pointer = ruser).filter(charakters__name__contains='Гигрометр')
        self.fields['person'].queryset = Employees.objects.filter(userid__userid = ruser)
                                 
    class Meta:
        model = Rooms
        fields = [
                 'roomnumber', 
                 'equipment1', 
                 'equipment2', 
                'person'
                  ]
        widgets = {'equipment1':forms.Select(attrs={'class': 'form-control'}), 'equipment2':forms.Select(attrs={'class': 'form-control'}), 'roomnumber':forms.TextInput(attrs={'class': 'form-control'}),'person':forms.Select(attrs={'class': 'form-control'}),}
        labels = {'equipment1': 'Барометр', 'equipment2': 'Гигрометр', 'roomnumber': 'Название комнаты','person': 'Ответственный за комнату'}


# блок 7 - формы для микроклимата


class MeteorologicalParametersRegForm(ModelForm):
    """форма для внесения условий окружающей среды в помещении"""
    def __init__(self, ruser, *args, **kwargs):
        super(MeteorologicalParametersRegForm, self).__init__(*args, **kwargs)
        self.fields['roomnumber'].queryset = Rooms.objects.filter(pointer = ruser)
        
    date = forms.DateField(label='Дата', initial = f'{date.today().day}.{date.today().month}.{date.today().year}',
                           widget=forms.DateInput(
                               attrs={'class': 'form-control', 'placeholder': ''}),
                           input_formats=(
                               '%Y-%m-%d',
                               '%m/%d/%Y',
                               '%m/%d/%y',
                               '%d.%m.%Y',
                           ))
    pressure = forms.CharField(label='Давление, кПа', required=False, initial='102.0',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    temperature = forms.CharField(label='Температура, °С',  required=False, initial='20.0',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    humidity = forms.CharField(label='Влажность, %', required=False, initial='50',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = MeteorologicalParameters
        fields = [
            'date',
            'roomnumber', 'pressure',
            'temperature', 'humidity',

                  ]
        widgets = {'roomnumber':forms.Select(attrs={'class': 'form-control'}),}
        labels = {'roomnumber': 'название или номер помещения'}


# блок 8 - формы для ТОИР

class ServiceEquipmentregForm(forms.ModelForm):
    """форма для  внесения постоянного описания ТОИР к госреестрам"""
    descriptiont0 = forms.CharField(label='Объем технического обслуживания ТО 0', max_length=10000,
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'placeholder': 'введите текст записи о приборе'}))
    descriptiont1 = forms.CharField(label='Объем технического обслуживания ТО 1', max_length=10000,
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'placeholder': 'введите текст записи о приборе'}))
    descriptiont2 = forms.CharField(label='Объем технического обслуживания ТО 2', max_length=10000,
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'placeholder': 'введите текст записи о приборе'}))


    class Meta:
        model = ServiceEquipmentME
        fields = ['descriptiont0', 'descriptiont1', 'descriptiont2', ]



class ServiceEquipmentUUpdateForm(forms.ModelForm):
    """Техобслуживание всего лабораторного оборудования индивидуальная информация ПЛАН"""
    commentservice = forms.CharField(label='Примечание к ТОиР', max_length=10000,  required=False,
                           widget=forms.Textarea(attrs={'class': 'form-control', }))
                                                       
    t2month1 = forms.BooleanField(label='ТО 2 в месяце 1', required=False)    
    t2month2 = forms.BooleanField(label='ТО 2 в месяце 2', required=False)
    t2month3 = forms.BooleanField(label='ТО 2 в месяце 3', required=False )
    t2month4 = forms.BooleanField(label='ТО 2 в месяце 4', required=False)
    t2month5 = forms.BooleanField(label='ТО 2 в месяце 5', required=False)
    t2month6 = forms.BooleanField(label='ТО 2 в месяце 6', required=False)
    t2month7 = forms.BooleanField(label='ТО 2 в месяце 7', required=False)
    t2month8 = forms.BooleanField(label='ТО 2 в месяце 8', required=False)
    t2month9 = forms.BooleanField(label='ТО 2 в месяце 9', required=False)
    t2month10 = forms.BooleanField(label='ТО 2 в месяце 10',required=False)
    t2month11 = forms.BooleanField(label='ТО 2 в месяце 11', required=False)
    t2month12 = forms.BooleanField(label='ТО 2 в месяце 12', required=False)

    class Meta:
        model = ServiceEquipmentU
        fields = ['commentservice', 't2month1', 't2month2', 't2month3',
                  't2month4', 't2month5',  't2month6', 
                  't2month7',
                  't2month8',
                  't2month9',
                  't2month10',
                  't2month11',
                  't2month12',
                  ]


class ServiceEquipmentUFactUpdateViewForm(forms.ModelForm):
    """Техобслуживание всего лабораторного оборудования индивидуальная информация ПЛАН"""
    t2month1 = forms.BooleanField(label='ТО 2 в месяце 1', required=False)    
    t2month2 = forms.BooleanField(label='ТО 2 в месяце 2', required=False)
    t2month3 = forms.BooleanField(label='ТО 2 в месяце 3', required=False )
    t2month4 = forms.BooleanField(label='ТО 2 в месяце 4', required=False)
    t2month5 = forms.BooleanField(label='ТО 2 в месяце 5', required=False)
    t2month6 = forms.BooleanField(label='ТО 2 в месяце 6', required=False)
    t2month7 = forms.BooleanField(label='ТО 2 в месяце 7', required=False)
    t2month8 = forms.BooleanField(label='ТО 2 в месяце 8', required=False)
    t2month9 = forms.BooleanField(label='ТО 2 в месяце 9', required=False)
    t2month10 = forms.BooleanField(label='ТО 2 в месяце 10',required=False)
    t2month11 = forms.BooleanField(label='ТО 2 в месяце 11', required=False)
    t2month12 = forms.BooleanField(label='ТО 2 в месяце 12', required=False)

    class Meta:
        model = ServiceEquipmentUFact
        fields = [ 't2month1', 't2month2', 't2month3',
                  't2month4', 't2month5',  't2month6', 
                  't2month7',
                  't2month8',
                  't2month9',
                  't2month10',
                  't2month11',
                  't2month12',
                  ]
