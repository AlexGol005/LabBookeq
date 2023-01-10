from datetime import date, timedelta

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import *

from equipment.models import MeasurEquipment, Rooms
from jouViscosity.models import ViscosityDinamicResult
from functstandart import get_avg, get_acc_measurement, get_round_signif_digit

from viscosimeters.models import Viscosimeters
from .constants import *


class Dinamicviscosity(models.Model):
    # поля которые будут во всех подобных моделях
    # идентификационная информация о пробе
    performer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    performerdensity = models.ForeignKey(User, verbose_name='Плотность измерил', on_delete=models.CASCADE, null=True,
                                         related_name='performerdensity', blank=True)
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    name = models.CharField('Наименование', max_length=100,   blank=True, null=True)
    lot = models.CharField('Партия', max_length=100,  blank=True, null=True)
    cipher = models.CharField('Шифр', max_length=100, blank=True, null=True)
    sowner = models.CharField('Владелец пробы', max_length=500, blank=True, null=True)
    constit = models.CharField(max_length=300, choices=CHOICES, default='Прочие нефтепродукты', null=True)

    # методика и ее метрологические характеристики
    ndocument = models.CharField('Метод испытаний', max_length=100, choices=ndocumentoptional,
                                 default=ndocumentoptional[0][1],
                                 blank=True, null=True)
    equipment = models.CharField('Способ измерения плотности', max_length=300, choices=DENSITYE, default='денсиметром',
                                 null=True, blank=True)
    # фиксация результатов в журнале измерений
    fixation = models.BooleanField(verbose_name='Внесен ли результат в Журнал измерений?', default=False,
                                   null=True)
    exp = models.IntegerField('Срок годности, месяцев',  blank=True, null=True)
    date_exp = models.DateField('Годен до', blank=True, null=True)
    # дополнительно
    oldresult = models.CharField('Предыдущее измерение',  null=True, blank=True, max_length=300, default='')
    termostatition = models.BooleanField(verbose_name='Термостатировано не менее 20 минут', blank=True, null=True)
    temperatureCheck = models.BooleanField(verbose_name='Температура контролируется внешним поверенным термометром',
                                           blank=True, null=True)
    # условия и приборы
    temperature = models.DecimalField('Температура, ℃', max_digits=5, decimal_places=2, default='0', null=True)
    piknometer_volume = models.DecimalField('Объём пикнометра, мл', max_digits=7, decimal_places=4, null=True,
                                            blank=True)

    # результат наблюдений
    piknometer_mass1 = models.DecimalField('Масса пикнометра 1, г', max_digits=7, decimal_places=4, null=True,
                                           blank=True)
    piknometer_mass2 = models.DecimalField('Масса пикнометра 2, г', max_digits=7, decimal_places=4, null=True,
                                           blank=True)
    piknometer_plus_SM_mass1 = models.DecimalField('Масса пикнометра + пробы -  1, г', max_digits=7, decimal_places=4,
                                                   null=True, blank=True)
    piknometer_plus_SM_mass2 = models.DecimalField('Масса пикнометра + пробы -  2, г', max_digits=7, decimal_places=4,
                                                   null=True, blank=True)

    # расчёты
    SM_mass1 = models.DecimalField('Масса пробы -  1, г', max_digits=7, decimal_places=4, null=True, blank=True)
    SM_mass2 = models.DecimalField('Масса пробы -  2, г', max_digits=7, decimal_places=4, null=True, blank=True)
    density1 = models.DecimalField('плотность 1, г/мл', max_digits=7, decimal_places=5, null=True, blank=True)
    density2 = models.DecimalField('плотность 2, г/мл', max_digits=7, decimal_places=5, null=True, blank=True)
    density_avg = models.DecimalField('средняя плотность, г/мл', max_digits=7, decimal_places=4, null=True, blank=True)
    delta = models.CharField('Не превышает Δ', max_length=100, null=True, blank=True)
    kriteriy = models.DecimalField('Критерий приемлемости измерений', max_digits=7, decimal_places=4, null=True,
                                   blank=True)
    kinematicviscosity = models.CharField('Кинематическая вязкость при температуре измерений сСт', max_length=300,
                                          null=True, blank=True)
    dinamicviscosity_not_rouned = models.DecimalField('Динамическая вязкость неокругленная', max_digits=20,
                                                      decimal_places=6, null=True, blank=True)
    result = models.CharField('Результат измерений динамической вязкости', null=True,
                              blank=True, max_length=300)
    resultMeas = models.CharField('Результат измерений уд/неуд', max_length=100, default='неудовлетворительно',
                                  null=True, blank=True)
    cause = models.CharField('Причина', max_length=100, default='', null=True, blank=True)
    accMeasurement = models.DecimalField('Оценка приемлемости измерений плотности', max_digits=7, decimal_places=4,
                                         null=True, blank=True)
    olddensity = models.CharField('Предыдущее значение плотности', max_length=300, null=True, default='', blank=True)
    deltaolddensity = models.DecimalField('Оценка разницы с предыдущим значением плотности',
                                          max_digits=10, decimal_places=4, null=True, blank=True)
    resultWarning = models.CharField(max_length=300, default='', null=True, blank=True)
    resultWarningkinematic = models.CharField('Если нет кинематики', max_length=300, null=True,  blank=True)
    kinematicviscositydead = models.DateField('кинематика годна до:', blank=True, null=True)
    havedensity = models.BooleanField(verbose_name='Есть значение плотности, измеренное ранее',
                                      default=False, blank=True)
    densitydead = models.DateField('Плотность, измеренная ранее, годна до:', null=True, blank=True)

    #  дополнительно условия и приборы - для подготовки протокола анализа
    room = models.ForeignKey(Rooms, verbose_name='Номер комнаты', null=True,
                             on_delete=models.PROTECT, blank=True)
    equipment1 = models.ForeignKey(MeasurEquipment, verbose_name='Секундомер', null=True,
                                   on_delete=models.PROTECT, blank=True, related_name='equipment1dinamic')
    equipment2 = models.ForeignKey(MeasurEquipment, verbose_name='Вискозиметр1', null=True,
                                   on_delete=models.PROTECT, blank=True, related_name='equipment2dinamic')
    equipment3 = models.ForeignKey(MeasurEquipment, verbose_name='Вискозиметр2', null=True,
                                   on_delete=models.PROTECT, blank=True, related_name='equipment3dinamic')
    equipment4 = models.ForeignKey(MeasurEquipment, verbose_name='Термометр', null=True,
                                   on_delete=models.PROTECT, blank=True, related_name='equipment4dinamic')
    equipment5 = models.ForeignKey(MeasurEquipment, verbose_name='Весы', null=True,
                                   on_delete=models.PROTECT, blank=True, related_name='equipment5dinamic')

    def save(self, *args, **kwargs):
        self.kriteriy = Decimal(REPEATABILITY)
        if not self.exp:
            self.exp = 100
        if self.havedensity and self.density_avg and self.densitydead:
            self.resultMeas = 'плотность измерена ранее'
            if not self.kinematicviscosity:
                self.resultWarningkinematic = 'Нет актуального значения кинематической вязкости. ' \
                                              'Динамика не рассчитана. ' \
                                              'Измерьте динамику и заполните новую форму'
            if self.kinematicviscosity:
                self.dinamicviscosity_not_rouned = Decimal(self.kinematicviscosity) * self.density_avg
                self.result = get_round_signif_digit(self.dinamicviscosity_not_rouned, 4)
        if not self.havedensity and not self.density_avg and not self.densitydead:
            if not (self.density1 and self.density2):
                self.SM_mass1 = self.piknometer_plus_SM_mass1 - self.piknometer_mass1
                self.SM_mass2 = self.piknometer_plus_SM_mass2 - self.piknometer_mass2
                self.density1 = self.SM_mass1 / self.piknometer_volume
                self.density2 = self.SM_mass2 / self.piknometer_volume
                self.accMeasurement = ((self.density1 - self.density2).copy_abs()).\
                    quantize(Decimal(1.0000), ROUND_HALF_UP)
                if self.accMeasurement <= self.kriteriy:
                    self.resultMeas = 'удовлетворительно'
                    self.cause = ''
                    self.density_avg = get_avg(self.density1, self.density2, 4)
                    if not self.kinematicviscosity:
                        self.resultWarningkinematic = 'Нет актуального значения кинематической вязкости. ' \
                                                      'Динамика не рассчитана. ' \
                                                      'Измерьте динамику и заполните новую форму'
                    if self.kinematicviscosity:
                        self.dinamicviscosity_not_rouned = Decimal(self.kinematicviscosity) * self.density_avg
                        self.result = get_round_signif_digit(self.dinamicviscosity_not_rouned, 4)
                if self.accMeasurement > self.kriteriy:
                    self.resultMeas = 'неудовлетворительно'
                    self.cause = 'Δ > r'
            if self.density1 and self.density2:
                self.accMeasurement = (self.density1 - self.density2).copy_abs()
                if self.accMeasurement <= self.kriteriy:
                    self.resultMeas = 'удовлетворительно'
                    self.cause = ''
                    self.density_avg = get_avg(self.density1, self.density2, 4)
                    if not self.kinematicviscosity:
                        self.resultWarningkinematic = 'Нет актуального значения кинематической вязкости. ' \
                                                      'Динамика не рассчитана. ' \
                                                      'Измерьте динамику и заполните новую форму'
                    if self.kinematicviscosity:
                        self.dinamicviscosity_not_rouned = Decimal(self.kinematicviscosity) * self.density_avg
                        self.result = get_round_signif_digit(self.dinamicviscosity_not_rouned, 4)
                if self.accMeasurement > self.kriteriy:
                    self.resultMeas = 'неудовлетворительно'
                    self.cause = 'Δ > r'
        if self.olddensity and self.density_avg:
            self.olddensity = self.olddensity.replace(',', '.')
            self.deltaolddensity = get_acc_measurement(Decimal(self.olddensity), self.density_avg)
            if self.deltaolddensity > self.kriteriy:
                self.resultWarning = f'плотность отличается от предыдущей на {self.deltaolddensity}'
        if not self.havedensity:
            self.date_exp = date.today() + timedelta(days=30 * self.exp)

        # вносим измерение в журнал с результататами измерений
        if self.fixation:
            if not self.exp:
                self.exp = 100
            ViscosityDinamicResult.objects.get_or_create(name=self.name, lot=self.lot, cipher=self.cipher)
            note = ViscosityDinamicResult.objects.get(name=self.name, lot=self.lot, cipher=self.cipher)
            if self.temperature == 20:
                note.cvt20 = self.density_avg
                note.cvtdinamic20 = self.result
                if not self.havedensity:
                    note.cvt20date = self.date
                    note.cvt20exp = self.exp
                    note.cvt20dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt20dead = self.densitydead
                note.kinematicviscosityfordinamicdead20 = self.kinematicviscositydead
                note.save()
            if self.temperature == 25:
                note.cvt25 = self.density_avg
                note.cvtdinamic25 = self.result
                if not self.havedensity:
                    note.cvt25date = self.date
                    note.cvt25exp = self.exp
                    note.cvt25dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt250dead = self.densitydead
                note.kinematicviscosityfordinamicdead25 = self.kinematicviscositydead
                note.save()
            if self.temperature == 40:
                note.cvt40 = self.density_avg
                note.cvtdinamic40 = self.result
                if not self.havedensity:
                    note.cvt40date = self.date
                    note.cvt40exp = self.exp
                    note.cvt40dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt40dead = self.densitydead
                note.kinematicviscosityfordinamicdead40 = self.kinematicviscositydead
                note.save()
            if self.temperature == 50:
                note.cvt50 = self.density_avg
                note.cvtdinamic50 = self.result
                if not self.havedensity:
                    note.cvt50date = self.date
                    note.cvt50exp = self.exp
                    note.cvt50dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt50dead = self.densitydead
                note.kinematicviscosityfordinamicdead50 = self.kinematicviscositydead
                note.save()
            if self.temperature == 60:
                note.cvt60 = self.density_avg
                note.cvtdinamic60 = self.result
                if not self.havedensity:
                    note.cvt60date = self.date
                    note.cvt60exp = self.exp
                    note.cvt60dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt60dead = self.densitydead
                note.kinematicviscosityfordinamicdead60 = self.kinematicviscositydead
                note.save()
            if self.temperature == 80:
                note.cvt80 = self.density_avg
                note.cvtdinamic80 = self.result
                if not self.havedensity:
                    note.cvt80date = self.date
                    note.cvt80exp = self.exp
                    note.cvt80dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt80dead = self.densitydead
                note.kinematicviscosityfordinamicdead80 = self.kinematicviscositydead
                note.save()
            if self.temperature == 100:
                note.cvt100 = self.density_avg
                note.cvtdinamic100 = self.result
                if not self.havedensity:
                    note.cvt100date = self.date
                    note.cvt100exp = self.exp
                    note.cvt100dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt100dead = self.densitydead
                note.kinematicviscosityfordinamicdead100 = self.kinematicviscositydead
                note.save()
            if self.temperature == 150:
                note.cvt150 = self.density_avg
                note.cvtdinamic150 = self.result
                if not self.havedensity:
                    note.cvt150date = self.date
                    note.cvt150exp = self.exp
                    note.cvt150dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt150dead = self.densitydead
                note.kinematicviscosityfordinamicdead150 = self.kinematicviscositydead
                note.save()
            if self.temperature == -20:
                note.cvtminus20 = self.density_avg
                note.cvtdinamicminus20 = self.result
                if not self.havedensity:
                    note.cvtminus20date = self.date
                    note.cvtminus20exp = self.exp
                    note.cvtminus20dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvtminus20dead = self.densitydead
                note.kinematicviscosityfordinamicdeadminus20 = self.kinematicviscositydead
                note.save()
        super(Dinamicviscosity, self).save(*args, **kwargs)

    def __str__(self):
        return f' {self.name}  п.{self.lot};  {self.temperature} t ℃;  {self.date}'

    def get_absolute_url(self):
        return reverse('dinamicviscositystr', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Измерение плотности и расчёт динаммической вязкости'
        verbose_name_plural = 'Измерение плотности и расчёт динаммической вязкости'


class CommentsDinamicviscosity(models.Model):
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    name = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(Dinamicviscosity, verbose_name='К странице аттестации', on_delete=models.CASCADE,
                                related_name='comments')
    author = models.ForeignKey(User, verbose_name='Наименование', on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.author.username} , {self.forNote.name},  {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('dinamicviscositycomm', kwargs={'pk': self.forNote.pk})

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pk']
