"""
Модуль проекта LabJournal, приложения kinematicviscosity.
Приложение kinematicviscosity это журнал фиксации
лабораторных записей по измерению кинематической вязкости нефтепродуктов
(Лабораторный журнал измерения кинематической вязкости).

Данный модуль model.py содержит классы для формирования таблиц в базе данных sqlite.
"""

from datetime import timedelta, date

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import *

from equipment.models import MeasurEquipment, Rooms
from jouViscosity.models import ViscosityKinematicResult
from viscosimeters.models import Viscosimeters
# from jouViscosity.models import ViscosityKinematicResult
from functstandart import mrerrow, numberDigits, get_avg, get_acc_measurement, get_sec, get_round_signif_digit

from .constants import CHOICES, REPEATABILITY, RELEERROR, ndocumentoptional


class ViscosityKinematic(models.Model):
    """уникальный класс, хранит первичные данные измерения и вычисляет результаты"""
    # поля которые будут во всех подобных моделях
    # идентификационная информация о пробе
    performer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
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
    relerror = models.DecimalField('Относительная  погрешность', max_digits=3, decimal_places=1, null=True)
    repeatability = models.CharField('Повторяемость', max_length=100, choices=REPEATABILITY,
                                     default=REPEATABILITY[0][1],
                                     blank=True, null=True)
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
    ViscosimeterNumber1 = models.ForeignKey(Viscosimeters, verbose_name='Заводской номер вискозиметра № 1',
                                            on_delete=models.PROTECT, related_name='k1', blank=True)
    Konstant1 = models.DecimalField('Константа вискозиметра № 1', max_digits=20, decimal_places=6, default='0',
                                    null=True, blank=True)
    ViscosimeterNumber2 = models.ForeignKey(Viscosimeters, verbose_name='Заводской номер вискозиметра № 2',
                                            on_delete=models.PROTECT, related_name='k2', blank=True)
    Konstant2 = models.DecimalField('Константа вискозиметра № 2', max_digits=20, decimal_places=6, default='0',
                                    null=True, blank=True)
    # результат наблюдений
    plustimeminK1T1 = models.DecimalField('Время истечения K1T1, + мин', max_digits=3, decimal_places=0, null=True)
    plustimesekK1T1 = models.DecimalField('Время истечения K1T1, + cек', max_digits=5, decimal_places=2, null=True)
    plustimeminK1T2 = models.DecimalField('Время истечения K1T2, + мин', max_digits=3, decimal_places=0, null=True)
    plustimesekK1T2 = models.DecimalField('Время истечения K1T2, + cек', max_digits=5, decimal_places=2, null=True)
    plustimeminK2T1 = models.DecimalField('Время истечения K2T1, + мин', max_digits=3, decimal_places=0, null=True)
    plustimesekK2T1 = models.DecimalField('Время истечения K2T1, + cек', max_digits=5, decimal_places=2, null=True)
    plustimeminK2T2 = models.DecimalField('Время истечения K2T2, + мин', max_digits=3, decimal_places=0, null=True)
    plustimesekK2T2 = models.DecimalField('Время истечения K2T2, + cек', max_digits=5, decimal_places=2, null=True)

    # расчёты
    timeK1T1_sec = models.DecimalField('Время истечения K1T1, в секундах', max_digits=7, decimal_places=2, default=0.00,
                                       null=True)
    timeK1T2_sec = models.DecimalField('Время истечения K1T2, в секундах', max_digits=7, decimal_places=2, default=0.00,
                                       null=True)
    timeK2T1_sec = models.DecimalField('Время истечения K2T1, в секундах', max_digits=7, decimal_places=2, default=0.00,
                                       null=True)
    timeK2T2_sec = models.DecimalField('Время истечения K2T2, в секундах', max_digits=7, decimal_places=2, default=0.0,
                                       null=True)
    timeK1_avg = models.DecimalField('Время истечения среднее 1, в секундах', max_digits=7, decimal_places=2,
                                     default=0.00, null=True)
    timeK2_avg = models.DecimalField('Время истечения среднее 2, в секундах', max_digits=7, decimal_places=2,
                                     default=0.00, null=True)
    viscosity1 = models.DecimalField('Вязкость кинематическая X1', max_digits=20, decimal_places=5, default=0.0000000,
                                     null=True)
    viscosity2 = models.DecimalField('Вязкость кинематическая X2', max_digits=20, decimal_places=5, default=0.0000000,
                                     null=True)
    viscosityAVG = models.DecimalField('Вязкость кинематическая Xсреднее', max_digits=20, decimal_places=5,
                                       default=0.0000000, null=True)
    deltaoldresult = models.DecimalField('Оценка разницы с предыдущим значением',
                                         max_digits=10, decimal_places=2, null=True, blank=True)
    resultWarning = models.CharField(max_length=300, default='', null=True,  blank=True)
    kriteriy = models.DecimalField('Критерий приемлемости измерений', max_digits=2, decimal_places=2, null=True)
    accMeasurement = models.DecimalField('Оценка приемлемости измерений', max_digits=5, decimal_places=2, null=True)
    resultMeas = models.CharField('Результат измерений уд/неуд', max_length=100, default='неудовлетворительно',
                                  null=True)
    cause = models.CharField('Причина', max_length=100, default='', null=True, blank=True)
    abserror = models.CharField('Абсолютная  погрешность',  max_length=100, null=True)
    result = models.CharField('Результат измерений, вязкость с округлением',
                              max_length=300, default='', null=True,  blank=True)

    #  дополнительно условия и приборы - для подготовки протокола анализа
    room = models.ForeignKey(Rooms, verbose_name='Номер комнаты', null=True,
                             on_delete=models.PROTECT,  blank=True)
    equipment1 = models.ForeignKey(MeasurEquipment, verbose_name='Секундомер', null=True,
                                   on_delete=models.PROTECT, blank=True, related_name='equipment1kinematic')
    equipment2 = models.ForeignKey(MeasurEquipment, verbose_name='Вискозиметр1', null=True,
                                   on_delete=models.PROTECT, blank=True, related_name='equipment2kinematic')
    equipment3 = models.ForeignKey(MeasurEquipment, verbose_name='Вискозиметр2', null=True,
                                   on_delete=models.PROTECT, blank=True, related_name='equipment3kinematic')
    equipment4 = models.ForeignKey(MeasurEquipment, verbose_name='Термометр', null=True,
                                   on_delete=models.PROTECT, blank=True, related_name='equipment4kinematic')

    def save(self, *args, **kwargs):
        # в блоке ниже находим средний результат для разного количества измерений (1, 2, 4 измерения)
        # переводим минуты в секунды, усредняем секунды, округляем результат (по 2 измерения на 2 вискозиметрах)
        if (self.plustimeminK1T2 and self.plustimeminK2T1
                and self.plustimeminK2T2 and self.plustimeminK1T1):
            self.timeK1T1_sec = get_sec(self.plustimeminK1T1, self.plustimesekK1T1)
            self.timeK1T2_sec = get_sec(self.plustimeminK1T2, self.plustimesekK1T2)
            self.timeK2T1_sec = get_sec(self.plustimeminK2T1, self.plustimesekK2T1)
            self.timeK2T2_sec = get_sec(self.plustimeminK2T2, self.plustimesekK2T2)
            self.timeK1_avg = get_avg(self.timeK1T1_sec, self.timeK1T2_sec, 3)
            self.timeK2_avg = get_avg(self.timeK2T1_sec, self.timeK2T2_sec, 3)
            # рассчитываем кинематическую вязкость Х1 и Х2
            self.viscosity1 = (self.Konstant1 * self.timeK1_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
            self.viscosity2 = (self.Konstant2 * self.timeK2_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
            # вычисляем среднее измеренное значение кинематической вязкости
            self.viscosityAVG = get_avg(self.viscosity1, self.viscosity2, 5)
        # переводим минуты в секунды, усредняем секунды, округляем результат (1 измерение на 1 вискозиметре)
        if self.plustimeminK1T1 and not (self.plustimeminK1T2 and self.plustimeminK2T2 and self.plustimeminK2T2):
            self.timeK1T1_sec = get_sec(self.plustimeminK1T1, self.plustimesekK1T1)
            self.timeK1_avg = self.timeK1T1_sec
            self.viscosity1 = (self.Konstant1 * self.timeK1_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
            self.viscosityAVG = self.viscosity1
            self.resultMeas = 'экспрес оценка вязкости'
            self.cause = 'не в условиях повторяемости'
        # переводим минуты в секунды, усредняем секунды, округляем результат (по 1 измерению на 2 вискозиметрах)
        if (self.plustimeminK1T1 and self.plustimeminK2T1) \
                and not (self.plustimeminK1T2 and self.plustimeminK2T2):
            self.timeK1T1_sec = get_sec(self.plustimeminK1T1, self.plustimesekK1T1)
            self.timeK2T1_sec = get_sec(self.plustimeminK2T1, self.plustimesekK2T1)
            self.timeK1_avg = self.timeK1T1_sec
            self.timeK2_avg = self.timeK2T1_sec
            self.viscosity1 = (self.Konstant1 * self.timeK1_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
            self.viscosity2 = (self.Konstant2 * self.timeK2_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
            self.viscosityAVG = get_avg(self.viscosity1, self.viscosity2, 5)

        # оценка повторяемости измерений между вискозиметрами (по нормативному документу)
        # находим повторяемость, она зависит от состава пробы
        self.accMeasurement = get_acc_measurement(Decimal(self.viscosity1), Decimal(self.viscosity2))
        self.kriteriy = REPEATABILITY[int(self.constit) - 1][1]

        # сравниваем среднее с повторяемостью и делаем выводы
        if self.accMeasurement <= Decimal(self.kriteriy):
            self.resultMeas = 'удовлетворительно'
            self.cause = ''
        if self.accMeasurement > Decimal(self.kriteriy):
            self.resultMeas = 'неудовлетворительно'
            self.cause = ':  Δ > r'

        # если результаты удовлетворительны, то полученное среднее значение округляем и выдаем результат измерений
        if self.resultMeas == 'удовлетворительно':
            # способ округления зависит от выбранного нормативного документа
            if self.ndocument == 'ГОСТ 33-2016':
                self.result = get_round_signif_digit(self.viscosityAVG, 4)
            if self.ndocument == 'ГОСТ 33768-2015':
                self.relerror = Decimal(RELEERROR)
                self.abserror = mrerrow((Decimal(self.relerror) * self.viscosityAVG) / Decimal(100))
                self.result = numberDigits(self.viscosityAVG, self.abserror)

        # если есть с чем сравнить измеренное значение, то сравниваем
        if self.oldresult and self.result:
            self.oldresult = self.oldresult.replace(',', '.')
            self.deltaoldresult = \
                get_acc_measurement(Decimal(self.oldresult), self.result, 2)
            if self.deltaoldresult > Decimal(self.kriteriy):
                self.resultWarning = f'Результат отличается от предыдущего на {self.deltaoldresult} %'

        # срок годности измерения рассчитываем если указан срок годности (в месяцах)
        if self.exp:
            self.date_exp = date.today() + timedelta(days=30*self.exp)

        # вносим измерение в журнал с результататами измерений
        if self.fixation:
            if not self.exp:
                self.exp = 100
            ViscosityKinematicResult.objects.get_or_create(name=self.name, lot=self.lot, cipher=self.cipher)
            note = ViscosityKinematicResult.objects.get(name=self.name, lot=self.lot, cipher=self.cipher)
            if self.temperature == 20:
                note.cvt20 = self.result
                note.cvt20date = self.date
                note.cvt20exp = self.exp
                note.cvt20dead = self.date + timedelta(days=30*self.exp)
                note.save()
            if self.temperature == 25:
                note.cvt25 = self.result
                note.cvt25date = self.date
                note.cvt25exp = self.exp
                note.cvt25dead = self.date + timedelta(days=30 * self.exp)
                note.save()
            if self.temperature == 40:
                note.cvt40 = self.result
                note.cvt40date = self.date
                note.cvt40exp = self.exp
                note.cvt40dead = self.date + timedelta(days=30 * self.exp)
                note.save()
            if self.temperature == 50:
                note.cvt50 = self.result
                note.cvt50date = self.date
                note.cvt50exp = self.exp
                note.cvt50dead = self.date + timedelta(days=30 * self.exp)
                note.save()
            if self.temperature == 60:
                note.cvt60 = self.result
                note.cvt60date = self.date
                note.cvt60exp = self.exp
                note.cvt60dead = self.date + timedelta(days=30 * self.exp)
                note.save()
            if self.temperature == 80:
                note.cvt80 = self.result
                note.cvt80date = self.date
                note.cvt80exp = self.exp
                note.cvt80dead = self.date + timedelta(days=30 * self.exp)
                note.save()
            if self.temperature == 100:
                note.cvt100 = self.result
                note.cvt100date = self.date
                note.cvt100exp = self.exp
                note.cvt100dead = self.date + timedelta(days=30 * self.exp)
                note.save()
            if self.temperature == 150:
                note.cvt150 = self.result
                note.cvt150date = self.date
                note.cvt150exp = self.exp
                note.cvt150dead = self.date + timedelta(days=30 * self.exp)
                note.save()
            if self.temperature == -20:
                note.cvtminus20 = self.result
                note.cvtminus20date = self.date
                note.cvtminus20exp = self.exp
                note.cvtminus20dead = self.date + timedelta(days=30 * self.exp)
                note.save()
        super(ViscosityKinematic, self).save(*args, **kwargs)

    def __str__(self):
        return f' {self.name}  п.{self.lot};  {self.temperature} t ℃;   {self.date}; pk={self.pk}'

    def get_absolute_url(self):
        return reverse('kinematicviscositystr', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Измерение кинематической вязкости'
        verbose_name_plural = 'Журнал измерений кинематической вязкости'


class Comments(models.Model):
    """стандартнрый класс для комментариев, поменять только get_absolute_url"""
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    name = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(ViscosityKinematic, verbose_name='К странице аттестации', on_delete=models.CASCADE,
                                related_name='comments')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.author.username} , {self.forNote.name},  {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('kinematicviscositycomm', kwargs={'pk': self.forNote.pk})

    class Meta:
        verbose_name = 'Комментарий к измерению кинематики'
        verbose_name_plural = 'Комментарии к измерениям кинематики'
        ordering = ['-pk']
