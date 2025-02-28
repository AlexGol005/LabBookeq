"""
Модуль проекта LabJournal, приложения equipment.
Приложение equipment это обширное приложение, включает все про лабораторное оборудование и лабораторные помещения
Данный модуль models.py выводит классы, создающие таблицы в базе данных - далее: модели.
Список блоков:
блок 1 - константы
блок 2 -  производители и поверители, комнаты лаборатории
блок 3 - оборудование в целом, характеристики СИ ИО ВО, сами СИ ИО ВО
блок 4 - смена комнаты, ответственного, добавление принадлежностей к оборудованию
блок 5 - поверка СИ, аттестация ИО, проверка характеристик ВО
блок 6 - комментарии
блок 7 - микроклимат в помещении
блок 8 - техобслуживание
блок 9 - отправка в поверку
"""
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from decimal import *
from django.urls import reverse
from django_currentuser.db.models import CurrentUserField

from users.models import  Company
from functstandart import get_dateformat

# блок 1 - константы неизменяемые непользовательские константы для полей с выбором значений в моделях

CHOICES = (
        ('Э', 'Экс.'),
        ('РЕ', 'Рем.'),
        ('С', 'Сп.'),
        ('Р', 'Рез.'),
        ('Д', 'Др.'),
    )

KATEGORY = (
        ('СИ', 'Средство измерения'),
        ('ИО', 'Испытательное оборудование'),
        ('ВО', 'Вспомогательное оборудование'),
    )

NOTETYPE = (
        ('Техническое обслуживание', 'Техническое обслуживание'),
        ('Неисправность', 'Неисправность'),
        ('Ремонт', 'Ремонт'),
        ('Другое', 'Другое'),
    )

CHOICESVERIFIC = (
        ('Поверен', 'Поверен'),
        ('Признан непригодным', 'Признан непригодным'),
        ('Спорный', 'Спорный'),
    )

CHOICESCAL = (
        ('Калиброван', 'Калиброван'),
        ('Признан непригодным', 'Признан непригодным'),
        ('Спорный', 'Спорный'),
    )

CHOICESATT = (
        ('Аттестован', 'Аттестован'),
        ('Признан непригодным', 'Признан непригодным'),
        ('Спорный', 'Спорный'),
    )

CHOICESPLACE = (
        ('У поверителя', 'У поверителя'),
        ('На месте эксплуатации', 'На месте эксплуатации'),
    )

HAVE = (('собственность', 'собственность'),
                                     ('аренда', 'аренда'))


# блок 2 -  производители и поверители

class Manufacturer(models.Model):
    """Производители оборудования"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    companyName = models.CharField('Производитель', max_length=100, unique=True)
    companyAdress = models.CharField('Адрес', max_length=200, default='', blank=True)
    country = models.CharField('Страна', max_length=200, default='Россия', blank=True)
    telnumber = models.CharField('Телефон', max_length=200, default='', blank=True)
    telnumberhelp = models.CharField('Телефон техподдержки для вопросов по оборудованию',
                                     max_length=200, default='', blank=True)
    pointer =  models.CharField('ID добавившей организации', max_length=500, blank=True, null=True)

    def __str__(self):
        return self.companyName

    def save(self, *args, **kwargs):
        if not self.pointer:
                self.pointer = self.created_by.profile.userid
        super(Manufacturer, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

class Test(models.Model):
    """тест"""
    text = models.CharField('Поверитель', max_length=100)



class Verificators(models.Model):
    """Компании поверители оборудования"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    companyName = models.CharField('Поверитель', max_length=100, unique=True)
    companyAdress = models.CharField('Адрес', max_length=200, default='-', blank=True)
    telnumber = models.CharField('Телефон', max_length=200, default='-', blank=True)
    email = models.CharField('email', max_length=200, default='-', blank=True)
    note = models.CharField('Примечание', max_length=10000, default='-', blank=True)
    head_position = models.CharField('Кому: должность лица организации-поверителя', max_length=100, default=None, null=True, blank=True)
    head_name = models.CharField('Кому: имя лица организации-поверителя', max_length=100, default=None, null=True, blank=True)
    pointer =  models.CharField('ID добавившей организации', max_length=500, blank=True, null=True, default=None,)

    def __str__(self):
        return f'{self.companyName}'

    def save(self, *args, **kwargs):
            if not self.pointer:
                    self.pointer = self.created_by.profile.userid
            super(Verificators, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Поверитель организация'
        verbose_name_plural = 'Поверители организации'


# блок 3 - оборудование в целом, характеристики СИ ИО ВО, сами СИ ИО ВО

class Equipment(models.Model):
    """Лабораторное оборудование - базовая индивидуальная сущность"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    date = models.DateField('Дата внесения записи', auto_now_add=True, blank=True, null=True)
    exnumber = models.CharField('Внутренний номер', max_length=100, default='', blank=True, null=True)
    lot = models.CharField('Заводской номер', max_length=100, default='')
    yearmanuf = models.IntegerField('Год выпуска', default='', blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, verbose_name='Производитель')
    status = models.CharField(max_length=300, choices=CHOICES, default='В эксплуатации', null=True,
                              verbose_name='Статус')
    standard_number = models.CharField('номер в качестве эталона в ФИФ, разряд по ГПС, ЛПС, и т. п.',  default='', blank=True, null=True, max_length=90)
    yearintoservice = models.IntegerField('Год ввода в эксплуатацию', default='0', blank=True, null=True)
    new = models.CharField('Новый или б/у', max_length=100, default='новый')
    invnumber = models.CharField('Инвентарный номер', max_length=100, default='', blank=True, null=True)
    kategory = models.CharField(max_length=300, choices=KATEGORY, default='Средство измерения', null=True,
                                verbose_name='Категория')
    individuality = models.TextField('Индивидуальные особенности прибора',  blank=True, null=True)
    notemaster = models.TextField('Примечание (или временное предостережение для сотрудников)',  blank=True, null=True)
    notemetrology = models.TextField('Примечание о метрологическом обеспечении прибора',  blank=True, null=True)
    price = models.DecimalField('Стоимость', max_digits=100, decimal_places=2, null=True, blank=True)
    pasport = models.CharField('Ссылка на паспорт', max_length=1000,  blank=True, null=True)
    instruction = models.CharField('Инструкция по эксплуатации (ссылка)', max_length=1000,  blank=True, null=True)
    repair = models.CharField('Контакты для ремонта', max_length=1000,  blank=True, null=True)
    pravo = models.CharField('Право владения прибором (например, номер и дата накладной)', max_length=1000,  blank=True, null=True)
    pravo_have = models.CharField(max_length=300, choices=HAVE, default='cобственность', null=True,
                              verbose_name='Собственность или аренда')
    aim = models.CharField('Предназначение', max_length=500, blank=True, null=True)                           
    aim2 = models.CharField('Наименование испытуемых групп объектов', max_length=500, blank=True, null=True)
    pointer =  models.CharField('ID организации', max_length=500, blank=True, null=True)   

    newperson = models.CharField(verbose_name='Ответственный за оборудование', max_length=90, blank=True, null=True)
    newpersondate =  models.CharField('Дата изменения ответственного', blank=True, null=True, max_length=90 )
        
    newroomnumber = models.CharField('Номер комнаты', max_length=100, blank=True, null=True,)
    newroomnumberdate = models.CharField('Дата перемещения', blank=True, null=True, max_length=90)
    serviceneed = models.BooleanField('Включать в график ТО', default=True, blank=True)

    def __str__(self):
        return f'{self.pointer}: {self.exnumber} - зав№ {self.lot}, pk={self.pk}'

    def save(self, *args, **kwargs):
        super(Equipment, self).save(*args, **kwargs)
        try:
            ServiceEquipmentU.objects.filter(equipment=self).filter(year=str(self.yearintoservice))
        except:
            ServiceEquipmentU.objects.get_or_create(equipment=self, year=str(self.yearintoservice))

    class Meta:
        unique_together = ('exnumber', 'pointer',)
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование: список всего оборудования'


class MeasurEquipmentCharakters(models.Model):
    """Характеристики средств измерений (госреестры в связке с модификациями/типами/диапазонами)"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    name = models.CharField('Название прибора', max_length=100, default='')
    reestr = models.CharField('Номер в Госреестре', max_length=1000, default='', blank=True, null=True)
    calinterval = models.IntegerField('МежМетрологический интервал, месяцев', default=12, blank=True, null=True)
    modificname = models.CharField('Модификация прибора', max_length=100, default='', blank=True, null=True)
    typename = models.CharField('Тип прибора', max_length=100, default='', blank=True, null=True)
    measurydiapason = models.CharField('Диапазон измерений', max_length=1000, default='', blank=True, null=True)
    accuracity = models.CharField('Класс точности /(разряд/), погрешность и /(или/) неопределённость /(класс, разряд/)',
                                  max_length=1000, default='', blank=True, null=True)
    power = models.BooleanField('Работает от сети', default=False, blank=True)
    voltage = models.CharField('напряжение', max_length=100, default='', blank=True, null=True)
    frequency = models.CharField('частота', max_length=100, default='', blank=True, null=True)
    temperature = models.CharField('температура', max_length=100, default='', blank=True, null=True)
    humidicity = models.CharField('влажность', max_length=100, default='', blank=True, null=True)
    pressure = models.CharField('давление', max_length=100, default='', blank=True, null=True)
    setplace = models.CharField('описание мероприятий по установке', max_length=1000, default='', blank=True, null=True)
    needsetplace = models.BooleanField('установка не требуется', default=False, blank=True)
    complectlist = models.CharField('где в паспорте комплектация', max_length=100, default='', blank=True, null=True)
    expresstest = models.BooleanField('тестирование возможно? да/нет', default=False, blank=True)
    traceability = models.TextField('Информация о прослеживаемости (к какому эталону прослеживаются измерения на СИ)',
                                    default='', blank=True, null=True)
    aim = models.CharField('примечание', max_length=90, blank=True, null=True)
    cod = models.CharField('виды измерений, тип (группа) средств измерений по МИ 2314' , max_length=200, blank=True, null=True)
    pointer =  models.CharField('ID добавившей организации', max_length=500, blank=True, null=True) 
                           
    def __str__(self):
        return f'госреестр: {self.reestr},  {self.name} {self.typename} {self.modificname}'

    class Meta:
        verbose_name = 'Средство измерения: описание типа'
        verbose_name_plural = 'Средства измерения: описания типов'
        unique_together = ('reestr', 'modificname', 'typename', 'name')
        

class TestingEquipmentCharakters(models.Model):
    """Характеристики ИО"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    name = models.CharField('Название прибора', max_length=100, default='')
    calinterval = models.IntegerField('МежМетрологический интервал, месяцев', default=12, blank=True, null=True)
    modificname = models.CharField('Модификация прибора', max_length=100, default='', blank=True, null=True)
    typename = models.CharField('Тип прибора', max_length=100, default='', blank=True, null=True)
    measurydiapason = models.CharField('Основные технические характеристики', max_length=1000,  blank=True, null=True)
    aim = models.CharField('Наименование видов испытаний и/или определяемых характеристик (параметров) продукции',
                           max_length=500, blank=True, null=True)
    aim2 = models.CharField('Наименование испытуемых групп объектов',
                            max_length=500, blank=True, null=True)
    ndoc = models.CharField('Методики испытаний', max_length=500, blank=True, null=True)
    power = models.BooleanField('Работает от сети', default=False, blank=True)
    voltage = models.CharField('напряжение', max_length=100, default='', blank=True, null=True)
    frequency = models.CharField('частота', max_length=100, default='', blank=True, null=True)
    temperature = models.CharField('температура', max_length=100, default='', blank=True, null=True)
    humidicity = models.CharField('влажность', max_length=100, default='', blank=True, null=True)
    pressure = models.CharField('давление', max_length=100, default='', blank=True, null=True)
    setplace = models.CharField('описание мероприятий по установке', max_length=1000, default='', blank=True, null=True)
    needsetplace = models.BooleanField('Установка не требуется', default=False, blank=True)
    complectlist = models.CharField('Где в паспорте комплектация', max_length=100, default='', blank=True, null=True)
    expresstest = models.BooleanField('Тестирование возможно? да/нет', default=False, blank=True)
    pointer =  models.CharField('ID добавившей организации', max_length=500, blank=True, null=True) 

    def __str__(self):
        return f'{self.name}  {self.modificname}'

    class Meta:
        verbose_name = 'Испытательное оборудование, характеристики'
        verbose_name_plural = 'Испытательное оборудование, характеристики'
        unique_together = ('name', 'modificname', 'typename')


class HelpingEquipmentCharakters(models.Model):
    """Характеристики ВО"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    name = models.CharField('Название прибора', max_length=100, default='')
    modificname = models.CharField('Модификация прибора', max_length=100, default='', blank=True, null=True)
    typename = models.CharField('Тип прибора', max_length=100, default='', blank=True, null=True)
    measurydiapason = models.CharField('Основные технические характеристики', max_length=1000,  blank=True, null=True)
    aim = models.CharField('Назначение',
                           max_length=500, blank=True, null=True)
    ndoc = models.CharField('Методики испытаний', max_length=500, blank=True, null=True)
    power = models.BooleanField('Работает от сети', default=False, blank=True)
    voltage = models.CharField('напряжение', max_length=100, default='', blank=True, null=True)
    frequency = models.CharField('частота', max_length=100, default='', blank=True, null=True)
    temperature = models.CharField('температура', max_length=100, default='', blank=True, null=True)
    humidicity = models.CharField('влажность', max_length=100, default='', blank=True, null=True)
    pressure = models.CharField('давление', max_length=100, default='', blank=True, null=True)
    setplace = models.CharField('описание мероприятий по установке', max_length=1000, default='', blank=True, null=True)
    needsetplace = models.BooleanField('Установка не требуется', default=False, blank=True)
    complectlist = models.CharField('Где в паспорте комплектация', max_length=100, default='', blank=True, null=True)
    expresstest = models.BooleanField('Тестирование возможно? да/нет', default=False, blank=True)
    kvasyattestation = models.CharField('...', max_length=100, default='', blank=True, null=True)
    pointer =  models.CharField('ID добавившей организации', max_length=500, blank=True, null=True) 

    def __str__(self):
        return f'{self.name}  {self.modificname}'

    class Meta:
        verbose_name = 'Вспомогательное оборудование, характеристики'
        verbose_name_plural = 'Вспомогательное оборудование, характеристики'
        unique_together = ('name', 'modificname', 'typename')


class MeasurEquipment(models.Model):
    """СИ: составлено из ЛО и характеристик СИ"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    pointer =  models.CharField('ID организации', max_length=500, blank=True, null=True) 
    charakters = models.ForeignKey(MeasurEquipmentCharakters,  on_delete=models.PROTECT,
                                   verbose_name='Характеристики СИ', blank=True, null=True)
    equipment = models.OneToOneField(Equipment, on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name='Оборудование')
    aim = models.CharField('Наименование определяемых (измеряемых) характеристик (параметров) продукции',
                           max_length=90, blank=True, null=True)
                                    
    newdate = models.CharField('Дата последней поверки', blank=True, null=True, max_length=90)
    newdatedead = models.CharField('Дата окончания последней поверки', blank=True, null=True, max_length=90)
    newdatedead_date = models.DateField('Дата окончания поверки в формате даты', blank=True, null=True)
    newdateorder = models.CharField('Дата заказа следующей поверки', blank=True, null=True, max_length=90, default='-')
    newdateorder_date = models.DateField('Дата заказа следующей поверки в формате даты', blank=True, null=True)
    newarshin = models.TextField('Ссылка на сведения о поверке в Аршин', blank=True, null=True)
    newcertnumber = models.CharField('Номер последнего свидетельства о поверке', max_length=90, blank=True, null=True)
    newcertnumbershort = models.CharField('Краткий номер свидетельства о поверке', max_length=90, blank=True, null=True)
    newprice = models.DecimalField('Стоимость данной поверки', max_digits=100, decimal_places=2, null=True, blank=True)
    newstatusver = models.CharField(max_length=300, default='Поверен', null=True,
                                 verbose_name='Статус')
    newverificator = models.CharField(verbose_name='Поверитель поверка', blank=True, null=True, max_length=200)
    newplace = models.CharField(max_length=300, choices=CHOICESPLACE, default='У поверителя', null=True,
                             verbose_name='Место поверки')
    newnote = models.CharField('Примечание', max_length=900, blank=True, null=True)
    newyear = models.CharField('Год поверки (если нет точных дат)', max_length=900, blank=True, null=True)
    newdateordernew = models.CharField('Дата заказа нового оборудования (если поверять не выгодно)', max_length=90, default='-') 
    newdateordernew_date = models.DateField('Дата заказа нового оборудования в формате даты', blank=True, null=True)
    newhaveorder = models.BooleanField(verbose_name='Заказана следующая поверка (или новое СИ)', default=False,  blank=True)                                 
    newcust = models.BooleanField(verbose_name='Поверку организует Поставщик', default=False, blank=True)                            
    newextra = models.TextField('Дополнительная информация', blank=True, null=True)

    calnewdate = models.CharField('Дата калибровки', blank=True, null=True, max_length=90)
    calnewdatedead = models.CharField('Дата окончания калибровки', blank=True, null=True, max_length=90)
    calnewdateorder = models.CharField('Дата заказа следующей калибровки', blank=True, null=True, max_length=90, default='-')
    calnewarshin = models.TextField('Ссылка на скан сертификата', blank=True, null=True)
    calnewcertnumber = models.CharField('Номер сертификата калибровки', max_length=90, blank=True, null=True)
    calnewcertnumbershort = models.CharField('Краткий номер свидетельства о поверке', max_length=90, blank=True, null=True)
    calnewprice = models.DecimalField('Стоимость данной калибровки', max_digits=100, decimal_places=2, null=True, blank=True)
    calnewstatusver = models.CharField(max_length=300,  default='Калиброван', null=True,
                                 verbose_name='Статус')
    calnewverificator = models.CharField(verbose_name='Поверитель калибровка', blank=True, null=True, max_length=200)
    calnewplace = models.CharField(max_length=300, choices=CHOICESPLACE, default='У поверителя', null=True,
                             verbose_name='Место калибровки')
    calnewnote = models.CharField('Примечание', max_length=900, blank=True, null=True)
    calnewyear = models.CharField('Год калибровки (если нет точных дат)', max_length=900, blank=True, null=True)
    calnewdateordernew = models.CharField('Дата заказа нового оборудования (если калибровать не выгодно)', max_length=90, default='-')
    calnewhaveorder = models.BooleanField(verbose_name='Заказана следующая калибровка (или новое СИ)', default=False, blank=True)                                   
    calnewcust = models.BooleanField(verbose_name='Калибровку организует Поставщик', default=False,
                               blank=True)
    calnewextra = models.TextField('Дополнительная информация', blank=True, null=True)

    def __str__(self):
        return f'Вн № {self.equipment.exnumber[:5]}  {self.charakters.name}  Зав № {self.equipment.lot} ' \
               f' № реестр {self.charakters.reestr} - pk {self.pk}'

    def save(self, *args, **kwargs):
        super().save()
        self.pointer = self.equipment.pointer
        return super(MeasurEquipment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Средство измерения'
        verbose_name_plural = 'Средства измерения: список'
        unique_together = ('charakters', 'equipment')
        ordering = ['charakters__name']


class TestingEquipment(models.Model):
    """ИО: составлено из ЛО и характеристик ИО"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    charakters = models.ForeignKey(TestingEquipmentCharakters,  on_delete=models.PROTECT,
                                   verbose_name='Характеристики ИО', blank=True, null=True)
    equipment = models.OneToOneField(Equipment, on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name='Оборудование')
    pointer =  models.CharField('ID организации', max_length=500, blank=True, null=True)  
        
    newdate = models.CharField('Дата последней аттестации', blank=True, null=True, max_length=90)
    newdatedead = models.CharField('Дата окончания последней аттестации', blank=True, null=True, max_length=90)
    newdatedead_date = models.DateField('Дата окончания аттестации в формате даты', blank=True, null=True)
    newdateorder = models.CharField('Дата заказа следующей аттестации', blank=True, null=True, max_length=90, default='-')
    newdateorder_date = models.DateField('Дата заказа следующей аттестации в формате даты', blank=True, null=True)
    newarshin = models.TextField('Ссылка на скан аттестата', blank=True, null=True)
    newcertnumber = models.CharField('Номер последнего аттестата', max_length=90, blank=True, null=True)
    newcertnumbershort = models.CharField('Краткий номер последнего аттестата', max_length=90, blank=True, null=True)
    newprice = models.DecimalField('Стоимость данной аттестации', max_digits=100, decimal_places=2, null=True, blank=True)
    newstatusver = models.CharField(max_length=300, default='Поверен', null=True,
                                 verbose_name='Статус')
    newverificator = models.CharField(verbose_name='Поверитель аттестации', blank=True, null=True, max_length=200)
    newplace = models.CharField(max_length=300, choices=CHOICESPLACE, default='У поверителя', null=True,
                             verbose_name='Место аттестации')
    newnote = models.CharField('Примечание', max_length=900, blank=True, null=True)
    newyear = models.CharField('Год аттестации (если нет точных дат)', max_length=900, blank=True, null=True)
    newdateordernew = models.CharField('Дата заказа нового оборудования (если аттестация не выгодна)', max_length=90, default='-')  
    newdateordernew_date = models.DateField('Дата заказа нового оборудования в формате даты', blank=True, null=True)
    newhaveorder = models.BooleanField(verbose_name='Заказана следующая аттестация (или новое ИО)', default=False,  blank=True)                                 
    newcust = models.BooleanField(verbose_name='Аттестацию организует Поставщик', default=False, blank=True)                            
    newextra = models.TextField('Дополнительная информация', blank=True, null=True)


    def __str__(self):
        return f'Вн № {self.equipment.exnumber[:5]}  {self.charakters.name}  Зав № {self.equipment.lot} ' \
               f' - pk {self.pk}'

    def save(self, *args, **kwargs):
        super().save()
        self.pointer = self.equipment.pointer
        return super(TestingEquipment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Испытательное оборудование'
        verbose_name_plural = 'Испытательное оборудование: список'
        unique_together = ('charakters', 'equipment')
        ordering = ['charakters__name']


class HelpingEquipment(models.Model):
    """ВО: составлено из ЛО и характеристик ВО"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    charakters = models.ForeignKey(HelpingEquipmentCharakters,  on_delete=models.PROTECT,
                                   verbose_name='Характеристики ВО', blank=True, null=True)
    equipment = models.OneToOneField(Equipment, on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name='Оборудование')
    pointer =  models.CharField('ID организации', max_length=500, blank=True, null=True)  

    def __str__(self):
        return f'Вн № {self.equipment.exnumber[:5]}  {self.charakters.name}  Зав № {self.equipment.lot}   - pk {self.pk}'
               

    def save(self, *args, **kwargs):
        super().save()
        self.pointer = self.equipment.pointer
        return super(HelpingEquipment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Вспомогательное оборудование'
        verbose_name_plural = 'Вспомогательное оборудование: список'
        unique_together = ('charakters', 'equipment')
        ordering = ['charakters__name']


# блок 4 - смена комнаты, ответственного, добавление принадлежностей к оборудованию
class Rooms(models.Model):
    """Комнаты лаборатории/производства"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    roomnumber = models.CharField('Номер комнаты', max_length=100, default='')
    person = models.ForeignKey(User, verbose_name='Ответственный за комнату', on_delete=models.PROTECT, blank=True, null=True)
    pointer =  models.CharField('ID организации', max_length=500, blank=True, null=True) 
    equipment1 = models.ForeignKey(MeasurEquipment, verbose_name='Барометр', null=True,
                                   on_delete=models.PROTECT, blank=True, related_name='equipment1rooms')
    equipment2 = models.ForeignKey(MeasurEquipment, verbose_name='Гигрометр', null=True, related_name='equipment2rooms',
                                   on_delete=models.PROTECT, blank=True)
        

    def __str__(self):
        return self.roomnumber

    class Meta:
        unique_together = ('roomnumber', 'pointer',)
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты: список'
            

class Personchange(models.Model):
    person = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Ответственный за оборудование')
    date = models.DateField('Дата изменения ответственного', auto_now_add=True, db_index=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        try:
            return f'{self.equipment.exnumber} Изменён ответственный {self.date}'
        except:
            return '&'             

    def save(self, *args, **kwargs):
        super().save()
        # добавляем последнего ответственого к СИ
        try:
            note = Equipment.objects.get(pk=self.equipment.pk)
        except:
            pass
        if note:
            note.newperson = self.person.profile.name
            newpersondate = get_dateformat(self.date)
            note.newpersondate = newpersondate        
            note.save()

    class Meta:
        verbose_name = 'Оборудование: дата изменения ответственного'
        verbose_name_plural = 'Оборудование: даты изменения ответственных'


class Roomschange(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    roomnumber = models.ForeignKey(Rooms, on_delete=models.PROTECT)
    date = models.DateField('Дата перемещения', auto_now_add=True, db_index=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, blank=True, null=True,
                                  verbose_name='Оборудование')

    def __str__(self):
        return f'{self.equipment} Перемещено {self.date} '

    def save(self, *args, **kwargs):
        super().save()
            # добавляем последнего ответственого к СИ
        try:
            note = Equipment.objects.get(pk=self.equipment.pk)
            note.newroomnumber = self.roomnumber.roomnumber
            newroomnumberdate = get_dateformat(self.date)
            note.newroomnumberdate = newroomnumberdate  
            note.save()
        except:
            pass

    class Meta:
        verbose_name = 'Оборудование: Дата перемещения прибора'
        verbose_name_plural = 'Оборудование: Даты перемещения приборов'


class DocsCons(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    date = models.CharField('Дата появления',  max_length=1000, default='', blank=True, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, blank=True, null=True,
                                  verbose_name='Оборудование')
    docs = models.CharField('Документ или принадлежность (1 или несколько)', max_length=100, default='', blank=True,
                            null=True)
    source = models.CharField('Откуда появился', max_length=1000, default='От поставщика', blank=True, null=True)
    note = models.CharField('Примечание', max_length=1000, blank=True, null=True)

    def __str__(self):
        return f'{self.equipment.exnumber} '

    class Meta:
        verbose_name = 'Оборудование: комплект к прибору'
        verbose_name_plural = 'Оборудование: комплекты к приборам'


# блок 5 - проверка СИ, аттестация ИО, проверка характеристик ВО


class Verificationequipment(models.Model):
    """Поверка СИ"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    equipmentSM = models.ForeignKey(MeasurEquipment, verbose_name='СИ',
                                    on_delete=models.PROTECT, related_name='equipmentSM_ver', blank=True, null=True)
    date = models.DateField('Дата поверки', blank=True, null=True)
    datedead = models.DateField('Дата окончания поверки', blank=True, null=True)
    dateorder = models.DateField('Дата заказа следующей поверки', blank=True, null=True)
    arshin = models.TextField('Ссылка на сведения о поверке в Аршин', blank=True, null=True)
    certnumber = models.CharField('Номер свидетельства о поверке', max_length=90, blank=True, null=True)
    certnumbershort = models.CharField('Краткий номер свидетельства о поверке', max_length=90, blank=True, null=True)
    price = models.DecimalField('Стоимость данной поверки', max_digits=100, decimal_places=2, null=True, blank=True)
    img = models.ImageField('Сертификат', upload_to='user_images', blank=True, null=True)
    statusver = models.CharField(max_length=300, choices=CHOICESVERIFIC, default='Поверен', null=True,
                                 verbose_name='Статус')
    verificator = models.ForeignKey(Verificators, on_delete=models.PROTECT,
                                    verbose_name='Поверитель', blank=True, null=True)
    place = models.CharField(max_length=300, choices=CHOICESPLACE, default='У поверителя', null=True,
                             verbose_name='Место поверки')
    note = models.CharField('Примечание', max_length=900, blank=True, null=True)
    year = models.CharField('Год поверки (если нет точных дат)', max_length=900, blank=True, null=True)
    dateordernew = models.DateField('Дата заказа нового оборудования (если поверять не выгодно)',
                                    blank=True, null=True)
    haveorder = models.BooleanField(verbose_name='Заказана следующая поверка (или новое СИ)', default=False,
                                    blank=True)
    cust = models.BooleanField(verbose_name='Поверку организует Поставщик', default=False,
                               blank=True)
    extra = models.TextField('Дополнительная информация', blank=True, null=True)

    def __str__(self):
        try:
            return f'Поверка  вн № ' \
               f'  {self.equipmentSM.equipment.exnumber} {self.equipmentSM.charakters.name} от {self.date} ' \
                   f'до {self.datedead} {self.year}'
        except:
            return '&'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('measureequipmentver', kwargs={'str': self.equipmentSM.equipment.exnumber})



    def save(self, *args, **kwargs):
        super().save()
        # добавляем последнюю поверку к оборудованию
        try:
            note = MeasurEquipment.objects.get(pk=self.equipmentSM.pk)
        except:
            pass
        if note:       
            note.newcertnumber = self.certnumber
            note.newarshin = self.arshin
            note.newcertnumbershort = self.certnumbershort
            note.newprice = self.price
            note.newstatusver = self.statusver
            note.newverificator = self.verificator.companyName
            note.newplace = self.place
            note.newnote = self.note
            note.newyear = self.year
            note.newhaveorder = self.haveorder
            note.newcust = self.cust
            note.newextra = self.extra 
            newdatedead = get_dateformat(self.datedead)
            note.newdatedead = newdatedead 
            note.newdatedead_date = self.datedead
            if self.dateorder:
                newdateorder = get_dateformat(self.dateorder)
                note.newdateorder = newdateorder
                note.newdateorder_date = self.dateorder
            else:
                note.newdateorder = '-' 
            if self.dateordernew:
                newdateordernew = get_dateformat(self.dateordernew)
                note.newdateordernew = newdateordernew  
                note.newdateordernew_date = self.dateordernew
            else:
                note.newdateordernew = '-' 
            note.save()

    class Meta:
        verbose_name = 'Средство измерения: поверка'
        verbose_name_plural = 'Средства измерения: поверки'


class Calibrationequipment(models.Model):
    """Калибровка СИ"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    equipmentSM = models.ForeignKey(MeasurEquipment, verbose_name='СИ',
                                    on_delete=models.PROTECT, related_name='equipmentSM_cal', blank=True, null=True)
    date = models.DateField('Дата калибровки', blank=True, null=True)
    datedead = models.DateField('Дата окончания калибровки', blank=True, null=True)
    dateorder = models.DateField('Дата заказа следующей калибровки', blank=True, null=True)
    arshin = models.TextField('Ссылка на скан сертификата', blank=True, null=True)
    certnumber = models.CharField('Номер сертификата калибровки', max_length=90, blank=True, null=True)
    certnumbershort = models.CharField('Краткий номер свидетельства о поверке', max_length=90, blank=True, null=True)
    price = models.DecimalField('Стоимость данной калибровки', max_digits=100, decimal_places=2, null=True, blank=True)
    statusver = models.CharField(max_length=300, choices=CHOICESCAL, default='Калиброван', null=True,
                                 verbose_name='Статус')
    verificator = models.ForeignKey(Verificators, on_delete=models.PROTECT,
                                    verbose_name='Поверитель', blank=True, null=True)
    place = models.CharField(max_length=300, choices=CHOICESPLACE, default='У поверителя', null=True,
                             verbose_name='Место калибровки')
    note = models.CharField('Примечание', max_length=900, blank=True, null=True)
    year = models.CharField('Год калибровки (если нет точных дат)', max_length=900, blank=True, null=True)
    dateordernew = models.DateField('Дата заказа нового оборудования (если калибровать не выгодно)',
                                    blank=True, null=True)
    haveorder = models.BooleanField(verbose_name='Заказана следующая калибровка (или новое СИ)', default=False,
                                    blank=True)
    cust = models.BooleanField(verbose_name='Калибровку организует Поставщик', default=False,
                               blank=True)
    extra = models.TextField('Дополнительная информация', blank=True, null=True)

    def __str__(self):
        try:
            return f'Калибровка  вн № ' \
               f'  {self.equipmentSM.equipment.exnumber} {self.equipmentSM.charakters.name} от {self.date} ' \
                   f'до {self.datedead} {self.year}'
        except:
            return '&'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('measureequipmentcal', kwargs={'str': self.equipmentSM.equipment.exnumber})


    def save(self, *args, **kwargs):
        super().save()
        # добавляем последнюю калибровку к оборудованию
        try:
            note = MeasurEquipment.objects.get(pk=self.equipmentSM.pk)
        except:
            pass
        if note:
            note = MeasurEquipment.objects.get(pk=self.equipmentSM.pk)
            note.calnewcertnumber = self.certnumber
            note.calnewarshin = self.arshin
            note.calnewcertnumbershort = self.certnumbershort
            note.calnewprice = self.price
            note.calnewstatusver = self.statusver
            note.calnewverificator = self.verificator.companyName
            note.calnewplace = self.place
            note.calnewnote = self.note
            note.calnewyear = self.year
            note.calnewhaveorder = self.haveorder
            note.calnewcust = self.cust
            note.calnewextra = self.extra      
            calnewdate = get_dateformat(self.date)
            note.calnewdate = calnewdate
            calnewdatedead = get_dateformat(self.datedead)
            note.calnewdatedead = calnewdatedead
            if self.dateorder:
                calnewdateorder = get_dateformat(self.dateorder)
                note.calnewdateorder = calnewdateorder
            else:
                note.calnewdateorder = '-' 
            if self.dateordernew:
                calnewdateordernew = get_dateformat(self.dateordernew)
                note.calnewdateordernew = calnewdateordernew  
            else:
                note.calnewdateordernew = '-'            
            note.save()

    class Meta:
        verbose_name = 'Средство измерения: калибровка'
        verbose_name_plural = 'Средства измерения: калибровка'


class Attestationequipment(models.Model):
    """Аттестация ИО"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    arshin = models.TextField('Ссылка на скан аттестата', blank=True, null=True)
    equipmentSM = models.ForeignKey(TestingEquipment, verbose_name='ИО',
                                    on_delete=models.PROTECT, related_name='equipmentSM_att', blank=True, null=True)
    date = models.DateField('Дата аттестации', blank=True, null=True)
    datedead = models.DateField('Дата окончания аттестации', blank=True, null=True)
    dateorder = models.DateField('Дата заказа следующей аттестации', blank=True, null=True)
    certnumber = models.CharField('Номер аттестата', max_length=90, blank=True, null=True)
    certnumbershort = models.CharField('Краткий номер свидетельства о аттестата', max_length=90, blank=True, null=True)
    price = models.DecimalField('Стоимость данной аттестации', max_digits=100, decimal_places=2, null=True, blank=True)
    img = models.ImageField('Аттестат', upload_to='user_images', blank=True, null=True)
    statusver = models.CharField(max_length=300, choices=CHOICESATT, default='Аттестован', null=True,
                                 verbose_name='Статус')
    verificator = models.ForeignKey(Verificators, on_delete=models.PROTECT,
                                    verbose_name='Поверитель', blank=True, null=True)
    place = models.CharField(max_length=300, choices=CHOICESPLACE, default='У поверителя', null=True,
                             verbose_name='Место аттестации')
    note = models.CharField('Примечание', max_length=900, blank=True, null=True)
    year = models.CharField('Год аттестации (если нет точных дат)', max_length=900, blank=True, null=True)
    dateordernew = models.DateField('Дата заказа нового оборудования (если аттестовывать не выгодно)',
                                    blank=True, null=True)
    haveorder = models.BooleanField(verbose_name='Заказана следующая аттестация (или новое СИ)', default=False,
                                    blank=True)
    cust = models.BooleanField(verbose_name='Аттестацию организует Поставщик', default=False,
                               blank=True)
    extra = models.TextField('Дополнительная информация', blank=True, null=True)

    def __str__(self):
        try:
            return f'Аттестация  вн № ' \
                   f'  {self.equipmentSM.equipment.exnumber} {self.equipmentSM.charakters.name} от {self.date} до' \
                   f' {self.datedead} {self.year}'
        except:
            return '&'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('testingequipmentatt', kwargs={'str': self.equipmentSM.equipment.exnumber})

    def save(self, *args, **kwargs):
        super().save()
        # добавляем последнюю аттестацию к оборудованию
        try:
            note = TestingEquipment.objects.get(pk=self.equipmentSM.pk)
        except:
            pass
        if note:       
            note.newcertnumber = self.certnumber
            note.newarshin = self.arshin
            note.newcertnumbershort = self.certnumbershort
            note.newprice = self.price
            note.newstatusver = self.statusver
            note.newverificator = self.verificator.companyName
            note.newplace = self.place
            note.newnote = self.note
            note.newyear = self.year
            note.newhaveorder = self.haveorder
            note.newcust = self.cust
            note.newextra = self.extra 
            newdatedead = get_dateformat(self.datedead)
            note.newdatedead = newdatedead 
            note.newdatedead_date = self.datedead
            if self.dateorder:
                newdateorder = get_dateformat(self.dateorder)
                note.newdateorder = newdateorder
                note.newdateorder_date = self.dateorder
            else:
                note.newdateorder = '-' 
            if self.dateordernew:
                newdateordernew = get_dateformat(self.dateordernew)
                note.newdateordernew = newdateordernew  
                note.newdateordernew_date = self.dateordernew
            else:
                note.newdateordernew = '-' 
            note.save()



    def save(self, *args, **kwargs):
        super().save()
        # добавляем последнюю аттестацию к оборудованию
        try:
            note = TestingEquipment.objects.get(pk=self.equipmentSM.pk)
        except:
            pass
        if note:       
            note.newcertnumber = self.certnumber
            note.newarshin = self.arshin
            note.newcertnumbershort = self.certnumbershort
            note.newprice = self.price
            note.newstatusver = self.statusver
            note.newverificator = self.verificator.companyName
            note.newplace = self.place
            note.newnote = self.note
            note.newyear = self.year
            note.newhaveorder = self.haveorder
            note.newcust = self.cust
            note.newextra = self.extra 
            newdatedead = get_dateformat(self.datedead)
            note.newdatedead = newdatedead 
            note.newdatedead_date = self.datedead
            if self.dateorder:
                newdateorder = get_dateformat(self.dateorder)
                note.newdateorder = newdateorder
                note.newdateorder_date = self.dateorder
            else:
                note.newdateorder = '-' 
            if self.dateordernew:
                newdateordernew = get_dateformat(self.dateordernew)
                note.newdateordernew = newdateordernew  
                note.newdateordernew_date = self.dateordernew
            else:
                note.newdateordernew = '-' 
            note.save()    
    class Meta:
        verbose_name = 'Испытательное оборудование: аттестация'
        verbose_name_plural = 'Испытательное оборудование: аттестации'



# блок 6 - комментарии

class CommentsEquipment(models.Model):
    """стандартнрый класс для комментариев"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    date = models.DateField('Дата',  db_index=True)
    note = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(Equipment, verbose_name='К прибору', on_delete=models.CASCADE)
    author = models.CharField('Автор', max_length=90, blank=True, null=True)
    type = models.CharField('Тип записи', max_length=90, blank=True, null=True, choices=NOTETYPE)
    img = models.ImageField('Фото', upload_to='user_images', blank=True, null=True)

    def __str__(self):
        return f' {self.author} , {self.forNote.exnumber},  {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('measureequipmentcomm', kwargs={'str': self.forNote.exnumber})

    def save(self, *args, **kwargs):
        super().save()
        if self.img:
                image = Image.open(self.img.path)
                if image.height > 1000 or image.width > 1000:
                    resize = (1000, 1000)
                    image.thumbnail(resize)
                    image.save(self.img.path)

    class Meta:
        verbose_name = 'Оборудование: запись о приборе'
        verbose_name_plural = 'Оборудование: записи о приборах'


class CommentsVerificationequipment(models.Model):
    """комментарии к поверке """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    note = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(Equipment, verbose_name='К прибору', on_delete=models.CASCADE)
    author = models.CharField('Автор', max_length=90, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('measureequipmentver', kwargs={'str': self.forNote.exnumber})

    class Meta:
        verbose_name = 'Средства измерения: Поверка: Комментарий к поверке'
        verbose_name_plural = 'Средства измерения: Поверка: Комментарии к поверкам'


class CommentsAttestationequipment(models.Model):
    """комментарии к аттестации """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    note = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(Equipment, verbose_name='К прибору', on_delete=models.CASCADE)
    author = models.CharField('Автор', max_length=90, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('testingequipmentatt', kwargs={'str': self.forNote.exnumber})

    class Meta:
        verbose_name = 'Испытательное оборудование: Аттестация: Комментарий к аттестации'
        verbose_name_plural = 'Испытательное оборудование: Аттестация: Комментарии к аттестациям'


# блок 7 - микроклимат в помещении

class MeteorologicalParameters(models.Model):
    """микроклимат в помещении"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    date = models.DateField('Дата')
    roomnumber = models.ForeignKey(Rooms, on_delete=models.PROTECT)
    pressure = models.CharField('Давление, кПа', max_length=90, blank=True, null=True)
    temperature = models.CharField('Температура, °С', max_length=90, blank=True, null=True)
    humidity = models.CharField('Влажность, %', max_length=90, blank=True, null=True)
    equipments = models.CharField('СИ', max_length=190, blank=True, null=True)
    person = models.CharField('Исполнитель ФИО', max_length=190, blank=True, null=True)
    

    def __str__(self):
        return f' {self.date} , {self.roomnumber.roomnumber}'
            
    def save(self, *args, **kwargs):
        self.equipments = f'{self.roomnumber.equipment1.charakters.name} тип {self.roomnumber.equipment1.charakters.typename}, заводской номер {self.roomnumber.equipment1.equipment.lot}, '\
        f'свидетельство о поверке № {self.roomnumber.equipment1.newcertnumber}, действительно до {self.roomnumber.equipment1.newdatedead}; '\
        f'{self.roomnumber.equipment2.charakters.name} тип {self.roomnumber.equipment2.charakters.typename}, заводской номер {self.roomnumber.equipment2.equipment.lot}, '\
        f'свидетельство о поверке № {self.roomnumber.equipment2.newcertnumber}, действительно до {self.roomnumber.equipment2.newdatedead};'
        self.person = self.roomnumber.person.name
        return super(MeteorologicalParameters, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Комнаты: Микроклимат в помещении'
        verbose_name_plural = 'Комнаты: Микроклимат в помещениях'
        unique_together = ('date', 'roomnumber',)


# блок 8 - техобслуживание

class ServiceEquipmentME(models.Model):
    """Техобслуживание СИ - постоянная информация из паспортов и инструкций"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    pointer =  models.CharField('ID организации кто вносил запись', max_length=500, blank=True, null=True) 
    charakters = models.OneToOneField(MeasurEquipmentCharakters,  on_delete=models.PROTECT,
                                   verbose_name='Характеристики СИ')
    # ТО 0
    descriptiont0 = models.TextField('Объем технического обслуживания ТО 0',  default='', blank=True)

    # ТО 1
    descriptiont1 = models.TextField('Объем технического обслуживания ТО 1',  default='', blank=True)

    # ТО 2
    descriptiont2 = models.TextField('Объем технического обслуживания ТО 2',  default='', blank=True)

    comment = models.TextField('Комментарий к постоянным особенностям ТО',  default='', blank=True)

    def __str__(self):
        return f'{self.charakters.name}, pk = {self.pk}'

    class Meta:
        verbose_name = 'Средство измерения: Техобслуживание постоянная информация'
        verbose_name_plural = 'Средства измерения: Техобслуживание постоянная информация'


class ServiceEquipmentTE(models.Model):
    """Техобслуживание ИО"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    pointer =  models.CharField('ID организации кто вносил запись', max_length=500, blank=True, null=True) 
    charakters = models.OneToOneField(TestingEquipmentCharakters, on_delete=models.PROTECT,
                                   verbose_name='Характеристики ИО')

    # ТО 0
    descriptiont0 = models.TextField('Объем технического обслуживания ТО 0',  default='', blank=True)

    # ТО 1
    descriptiont1 = models.TextField('Объем технического обслуживания ТО 1',  default='', blank=True)

    # ТО 2
    descriptiont2 = models.TextField('Объем технического обслуживания ТО 2',  default='', blank=True)

    comment = models.TextField('Комментарий к постоянным особенностям ТО',  default='', blank=True)

    def __str__(self):
        return self.charakters.name

    class Meta:
        verbose_name = 'Испытательное оборудование: Техобслуживание постоянная информация'
        verbose_name_plural = 'Испытательное оборудование: Техобслуживание постоянная информация'


class ServiceEquipmentHE(models.Model):
    """Техобслуживание ВО"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    pointer =  models.CharField('ID организации кто вносил запись', max_length=500, blank=True, null=True) 
    charakters = models.OneToOneField(HelpingEquipmentCharakters, on_delete=models.PROTECT,
                                   verbose_name='Характеристики ВО')
    
    # ТО 0
    descriptiont0 = models.TextField('Объем технического обслуживания ТО 0',  default='', blank=True)

    # ТО 1
    descriptiont1 = models.TextField('Объем технического обслуживания ТО 1',  default='', blank=True)

    # ТО 2
    descriptiont2 = models.TextField('Объем технического обслуживания ТО 2',  default='', blank=True)
        
    comment = models.TextField('Комментарий к постоянным особенностям ТО',  default='', blank=True)


    def __str__(self):
        return self.charakters.name

    class Meta:
        verbose_name = 'Вспомогательное оборудование: Техобслуживание постоянная информация'
        verbose_name_plural = 'Вспомогательное оборудование: Техобслуживание постоянная информация'


class ServiceEquipmentU(models.Model):
    """Техобслуживание всего лабораторного оборудования индивидуальная информация ПЛАН"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    pointer =  models.CharField('ID организации', max_length=500, blank=True, null=True)
    year =  models.CharField('Год ТО-2 план', max_length=4, blank=True, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name='Оборудование')
    commentservice = models.TextField('Примечание к ТОиР', default='', blank=True, null=True)
    # ТО 2
    t2month1 = models.BooleanField('ТО 2 в месяце 1', default=True)
    t2month2 = models.BooleanField('ТО 2 в месяце 2', default=False)
    t2month3 = models.BooleanField('ТО 2 в месяце 3', default=False)
    t2month4 = models.BooleanField('ТО 2 в месяце 4', default=True)
    t2month5 = models.BooleanField('ТО 2 в месяце 5', default=False)
    t2month6 = models.BooleanField('ТО 2 в месяце 6', default=False)
    t2month7 = models.BooleanField('ТО 2 в месяце 7', default=True)
    t2month8 = models.BooleanField('ТО 2 в месяце 8', default=False)
    t2month9 = models.BooleanField('ТО 2 в месяце 9', default=False)
    t2month10 = models.BooleanField('ТО 2 в месяце 10', default=True)
    t2month11 = models.BooleanField('ТО 2 в месяце 11', default=False)
    t2month12 = models.BooleanField('ТО 2 в месяце 12', default=False)

    def __str__(self):
        return f'pk = {self.pk}'
            
    def save(self, *args, **kwargs):
        self.pointer = self.equipment.pointer
        super(ServiceEquipmentU, self).save(*args, **kwargs)
        ServiceEquipmentUFact.objects.get_or_create(equipment=self.equipment, pk_pointer=self.pk, year=self.year)
                    
    class Meta:
        verbose_name = 'Оборудование: ТО-2 план'
        verbose_name_plural = 'Оборудование: ТО-2 план'




class ServiceEquipmentUFact(models.Model):
    """Техобслуживание всего лабораторного оборудования индивидуальная информация факт"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    pointer =  models.CharField('ID организации', max_length=500, blank=True, null=True)
    year =  models.CharField('Год ТО-2 факт', max_length=4, blank=True, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name='Оборудование')
    pk_pointer=models.CharField('указатель на pk соответствующего ТО-2 план', max_length=20, blank=True, null=True)
    # ТО 2
    t2month1 = models.BooleanField('ТО 2 в месяце 1', default=True)
    t2month2 = models.BooleanField('ТО 2 в месяце 2', default=False)
    t2month3 = models.BooleanField('ТО 2 в месяце 3', default=False)
    t2month4 = models.BooleanField('ТО 2 в месяце 4', default=True)
    t2month5 = models.BooleanField('ТО 2 в месяце 5', default=False)
    t2month6 = models.BooleanField('ТО 2 в месяце 6', default=False)
    t2month7 = models.BooleanField('ТО 2 в месяце 7', default=True)
    t2month8 = models.BooleanField('ТО 2 в месяце 8', default=False)
    t2month9 = models.BooleanField('ТО 2 в месяце 9', default=False)
    t2month10 = models.BooleanField('ТО 2 в месяце 10', default=True)
    t2month11 = models.BooleanField('ТО 2 в месяце 11', default=False)
    t2month12 = models.BooleanField('ТО 2 в месяце 12', default=False)

    def __str__(self):
        return f'pk = {self.pk}'
            
    def save(self, *args, **kwargs):
        self.pointer = self.equipment.pointer
        return super(ServiceEquipmentUFact, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Оборудование: ТО-2 факт'
        verbose_name_plural = 'Оборудование: ТО-2 факт'





# блок 9 - отправка в поверку
class Agreementverification(models.Model):
    """Договоры организации с поверителями"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    verificator = models.ForeignKey(Verificators, on_delete=models.PROTECT, verbose_name='Поверитель')    
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='Компания')  
    ver_agreement_number = models.CharField('Номер договора с организацией-поверителем', max_length=100, default=None, null=True, blank=True)
    ver_agreement_date = models.CharField('Дата договора с организацией-поверителем', max_length=100, default=None, null=True, blank=True)
    ver_agreement_card = models.CharField('Номер учетной карточки у организации-поверителя', max_length=100, default=None, null=True, blank=True)
    pointer =  models.CharField('ID организации', max_length=500, blank=True, null=True)
    active = models.BooleanField('Активный', default=False, blank=True)
    public_agree = models.BooleanField('Согласие на передачу данных в Аршин', default=True, blank=True)

    def save(self, *args, **kwargs):
        super().save()        
        self.pointer = self.company.userid
        try:
            Activeveraqq.objects.get(company=self.company)
        except:
            Activeveraqq.objects.get_or_create(aqq=self, company=self.company)

        
    def __str__(self):
        return self.verificator.companyName
    class Meta:
        verbose_name = 'Договоры организаций с поверителями'
        verbose_name_plural = 'Договоры организаций с поверителями'


class Activeveraqq(models.Model):
    """Активный договор с поверителем"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField()
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='Компания')  
    aqq = models.ForeignKey(Agreementverification, on_delete=models.PROTECT, verbose_name='Договор с поверителем', unique=True, null=True) 
    pointer =  models.CharField('ID организации', max_length=500, blank=True, null=True)
         
    def save(self, *args, **kwargs):
        self.pointer = self.company.userid
            
        return super(Activeveraqq, self).save(*args, **kwargs)
        
    def __str__(self):
        try:
            return self.aqq.verificator.companyName
        except: 
            return ''

            
    class Meta:
        verbose_name = 'Активный договор с поверителем'
        verbose_name_plural = 'Активный договор с поверителем'

