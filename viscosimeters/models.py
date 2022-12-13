from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from equipment.models import Manufacturer, Equipment, MeasurEquipment


class ViscosimeterType(models.Model):
    """Создает в бд таблицу базовых типов вискозиметров (по диапазонам измерений/диаметрам"""
    pairNumber = models.CharField('Номер пары', max_length=100)
    diameter = models.CharField('Диаметр', max_length=5, unique=True)
    viscosity1000 = models.CharField('Вязкость за 1000 сек, сСт', max_length=30)
    range = models.CharField('Область измерений, сСт', max_length=30)

    def __str__(self):
        return f'{self.diameter}'

    class Meta:
        verbose_name = 'Тип вискозиметра'
        verbose_name_plural = 'Типы вискозиметров'


class Viscosimeters(models.Model):
    """Создает в бд таблицу, которая связывает вискозиметр как приборную инвентарную единицу с его диаметром
     (областью измерений) и константой"""
    viscosimeterType = models.ForeignKey(ViscosimeterType, verbose_name='Диаметр',
                                         on_delete=models.PROTECT)
    equipmentSM = models.ForeignKey(MeasurEquipment, verbose_name='СИ',
                                    on_delete=models.PROTECT, related_name='equipmentSM', blank=True, null=True)
    konstant = models.DecimalField('Константа', max_digits=20, decimal_places=6,  blank=True, null=True)

    def __str__(self):
        return f'№ {self.equipmentSM.equipment.lot} ({self.viscosimeterType.viscosity1000} сСт)'

    def get_absolute_url(self):
        return reverse('Str', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Вискозиметр'
        verbose_name_plural = 'Вискозиметры'

