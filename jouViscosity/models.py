from django.db import models
from django.contrib.auth.models import User


CHOICES = (
        ('6', '6'),
        ('12', '12'),
        ('24', '24'),
    )


class ViscosityKinematicResult(models.Model):
    name = models.CharField('Название пробы', max_length=100, blank=True, null=True)
    lot = models.CharField('Партия пробы', max_length=100, blank=True, null=True)
    cipher = models.CharField('Шифр пробы', max_length=100, blank=True, null=True)
    cvt20 = models.CharField('Кинематика при 20 - АЗ', max_length=30, blank=True, null=True)
    cvt20date = models.DateField('Кинематика при 20 - дата измерения', blank=True, null=True)
    cvt20exp = models.IntegerField('Кинематика при 20 - срок годности', blank=True, null=True)
    cvt20dead = models.DateField('20 годен до', blank=True, null=True)

    cvt25 = models.CharField('Кинематика при 25 - АЗ', max_length=30, blank=True, null=True)
    cvt25date = models.DateField('Кинематика при 25 - дата измерения', blank=True, null=True)
    cvt25exp = models.IntegerField('Кинематика при 25 - срок годности', blank=True, null=True)
    cvt25dead = models.DateField('25 годен до', blank=True, null=True)

    cvt40 = models.CharField('Кинематика при 40 - АЗ', max_length=30, blank=True, null=True)
    cvt40date = models.DateField('Кинематика при 40 - дата измерения', blank=True, null=True)
    cvt40exp = models.IntegerField('Кинематика при 40 - срок годности', blank=True, null=True)
    cvt40dead = models.DateField('40 годен до', blank=True, null=True)

    cvt50 = models.CharField('Кинематика при 50 - АЗ', max_length=30, blank=True, null=True)
    cvt50date = models.DateField('Кинематика при 50 - дата измерения', blank=True, null=True)
    cvt50exp = models.IntegerField('Кинематика при 50 - срок годности', blank=True, null=True)
    cvt50dead = models.DateField('50 годен до', blank=True, null=True)

    cvt60 = models.CharField('Кинематика при 60 - АЗ', max_length=30, blank=True, null=True)
    cvt60date = models.DateField('Кинематика при 60 - дата измерения', blank=True, null=True)
    cvt60exp = models.IntegerField('Кинематика при 60 - срок годности', blank=True, null=True)
    cvt60dead = models.DateField('60 годен до', blank=True, null=True)

    cvt80 = models.CharField('Кинематика при 80 - АЗ', max_length=30, blank=True, null=True)
    cvt80date = models.DateField('Кинематика при 80 - дата измерения', blank=True, null=True)
    cvt80exp = models.IntegerField('Кинематика при 80 - срок годности', blank=True, null=True)
    cvt80dead = models.DateField('80 годен до', blank=True, null=True)

    cvt100 = models.CharField('Кинематика при 100 - АЗ', max_length=30, blank=True, null=True)
    cvt100date = models.DateField('Кинематика при 100 - дата измерения', blank=True, null=True)
    cvt100exp = models.IntegerField('Кинематика при 100 - срок годности', blank=True, null=True)
    cvt100dead = models.DateField('100 годен до', blank=True, null=True)

    cvt150 = models.CharField('Кинематика при 150 - АЗ', max_length=30, blank=True, null=True)
    cvt150date = models.DateField('Кинематика при 150 - дата измерения', blank=True, null=True)
    cvt150exp = models.IntegerField('Кинематика при 150 - срок годности', blank=True, null=True)
    cvt150dead = models.DateField('150 годен до', blank=True, null=True)

    cvtminus20 = models.CharField('Кинематика при -20 - АЗ', max_length=30, blank=True, null=True)
    cvtminus20date = models.DateField('Кинематика при -20 - дата измерения', blank=True, null=True)
    cvtminus20exp = models.IntegerField('Кинематика при -20 - срок годности', blank=True, null=True)
    cvtminus20dead = models.DateField('-20 годен до', blank=True, null=True)

    def __str__(self):
        return f'кинематика результаты измерений для {self.name} партия {self.lot} шифр {self.cipher}'

    class Meta:
        verbose_name = 'проба, кинематика'
        verbose_name_plural = 'пробы, кинематика'


class ViscosityDinamicResult(models.Model):
    name = models.CharField('Название пробы', max_length=100, blank=True, null=True)
    lot = models.CharField('Партия пробы', max_length=100, blank=True, null=True)
    cipher = models.CharField('Шифр пробы', max_length=100, blank=True, null=True)
    cvt20 = models.CharField('Плотность при 20 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic20 = models.CharField('Динамика при 20 - АЗ', max_length=30, blank=True, null=True)
    cvt20date = models.DateField('Плотность при 20 - дата измерения', blank=True, null=True)
    cvt20exp = models.IntegerField('Плотность при 20 - срок годности', blank=True, null=True)
    cvt20dead = models.DateField('20 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead20 = models.DateField('кинематика 20 годен до', blank=True, null=True)
    cvt25 = models.CharField('Плотность при 25 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic25 = models.CharField('Динамика при 25 - АЗ', max_length=30, blank=True, null=True)
    cvt25date = models.DateField('Плотность при 25 - дата измерения', blank=True, null=True)
    cvt25exp = models.IntegerField('Плотность при 25 - срок годности', blank=True, null=True)
    cvt25dead = models.DateField('25 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead25 = models.DateField('кинематика 25 годен до', blank=True, null=True)
    cvt40 = models.CharField('Плотность при 40 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic40 = models.CharField('Динамика при 40 - АЗ', max_length=30, blank=True, null=True)
    cvt40date = models.DateField('Плотность при 40 - дата измерения', blank=True, null=True)
    cvt40exp = models.IntegerField('Плотность при 40 - срок годности', blank=True, null=True)
    cvt40dead = models.DateField('40 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead40 = models.DateField('кинематика 40 годен до', blank=True, null=True)
    cvt50 = models.CharField('Плотность при 50 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic50 = models.CharField('Динамика при 50 - АЗ', max_length=30, blank=True, null=True)
    cvt50date = models.DateField('Плотность при 50 - дата измерения', blank=True, null=True)
    cvt50exp = models.IntegerField('Плотность при 50 - срок годности', blank=True, null=True)
    cvt50dead = models.DateField('50 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead50 = models.DateField('кинематика 50 годен до', blank=True, null=True)
    cvt60 = models.CharField('Плотность при 60 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic60 = models.CharField('Динамика при 60 - АЗ', max_length=30, blank=True, null=True)
    cvt60date = models.DateField('Плотность при 60 - дата измерения', blank=True, null=True)
    cvt60exp = models.IntegerField('Плотность при 60 - срок годности', blank=True, null=True)
    cvt60dead = models.DateField('60 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead60 = models.DateField('кинематика 60 годен до', blank=True, null=True)
    cvt80 = models.CharField('Плотность при 80 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic80 = models.CharField('Динамика при 80 - АЗ', max_length=30, blank=True, null=True)
    cvt80date = models.DateField('Плотность при 80 - дата измерения', blank=True, null=True)
    cvt80exp = models.IntegerField('Плотность при 80 - срок годности', blank=True, null=True)
    cvt80dead = models.DateField('80 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead80 = models.DateField('кинематика 80 годен до', blank=True, null=True)
    cvt100 = models.CharField('Плотность при 100 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic100 = models.CharField('Динамика при 100 - АЗ', max_length=30, blank=True, null=True)
    cvt100date = models.DateField('Плотность при 100 - дата измерения', blank=True, null=True)
    cvt100exp = models.IntegerField('Плотность при 100 - срок годности', blank=True, null=True)
    cvt100dead = models.DateField('100 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead100 = models.DateField('кинематика 100 годен до', blank=True, null=True)
    cvt150 = models.CharField('Плотность при 150 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic150 = models.CharField('Динамика при 150 - АЗ', max_length=30, blank=True, null=True)
    cvt150date = models.DateField('Плотность при 150 - дата измерения', blank=True, null=True)
    cvt150exp = models.IntegerField('Плотность при 150 - срок годности', blank=True, null=True)
    cvt150dead = models.DateField('150 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead150 = models.DateField('кинематика 150 годен до', blank=True, null=True)
    cvtminus20 = models.CharField('Плотность при -20 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamicminus20 = models.CharField('Динамика при -20 - АЗ', max_length=30, blank=True, null=True)
    cvtminus20date = models.DateField('Плотность при -20 - дата измерения', blank=True, null=True)
    cvtminus20exp = models.IntegerField('Плотность при -20 - срок годности', blank=True, null=True)
    cvtminus20dead = models.DateField('-20 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdeadminus20 = models.DateField('кинематика -20 годен до', blank=True, null=True)

    def __str__(self):
        return f'плотность и динамика результаты для {self.name} партия {self.lot} шифр {self.cipher} '

    class Meta:
        verbose_name = 'Вязкость нефтепродуктов, плотность и динамика'
        verbose_name_plural = 'Вязкость нефтепродуктов, плотность и динамика'
