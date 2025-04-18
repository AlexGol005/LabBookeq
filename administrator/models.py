from django.db import models
from django.urls import reverse


class Regstr(models.Model):
    date = models.DateField('Дата', auto_now_add=True)
    text = models.TextField('Текст записи')


    def __str__(self):
        return f' {self.date}'

    class Meta:
        verbose_name = 'О регистрации'
        verbose_name_plural = 'О регистрации'


class About(models.Model):
    date = models.DateField('Дата', auto_now_add=True)
    text = models.TextField('Текст записи')


    def __str__(self):
        return f' {self.date}'

    class Meta:
        verbose_name = 'О сайте'
        verbose_name_plural = 'О сайте'


class Manual(models.Model):
    date = models.DateField('Дата', auto_now_add=True)
    text = models.TextField('Текст записи')


    def __str__(self):
        return f' {self.date}'

    class Meta:
        verbose_name = 'Мануал по работе на сайте'
        verbose_name_plural = 'Мануал по работе на сайте'


class PolitycaConfident(models.Model):
    date = models.DateField('Дата', auto_now_add=True)
    text = models.TextField('Текст записи')


    def __str__(self):
        return f' {self.date}'


class Oferta(models.Model):
    date = models.DateField('Дата', auto_now_add=True)
    text = models.TextField('Текст записи')


    def __str__(self):
        return f' {self.date}'

    class Meta:
        verbose_name = 'Договор-оферта'
        verbose_name_plural = 'Договор-оферта'
      
