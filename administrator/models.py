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
      
