from django.db import models

from django.db import models
from django.urls import reverse


class Hike(models.Model):
    reality = models.BooleanField(verbose_name='Пройдено',
                                           blank=True, null=True, default=False)
    date = models.DateField('Дата добавления записи', auto_now_add=True, db_index=True)
    date_fact = models.DateField('Дата похода', blank=True, null=True)
    title = models.CharField('Заголовок', max_length=10000, blank=True, null=True)
    metatitle = models.CharField('Метазаголовок страницы', max_length=10000, blank=True, null=True)
    description = models.TextField('Метаописание страницы', blank=True, null=True)
    keywords = models.TextField('Ключевые слова', blank=True, null=True)
    text = models.TextField('Текст записи.')
    start_station = models.CharField('Вокзал отправления туда', max_length=10000, blank=True, null=True)
    aim_station = models.CharField('Вокзал прибытия туда', max_length=10000, blank=True, null=True)
    aim_station = models.CharField('Вокзал прибытия туда', max_length=10000, blank=True, null=True)
    back_station = models.CharField('Вокзал отправления оттуда', max_length=10000, blank=True, null=True)
    travel_details = models.TextField('Подробности добирания',  blank=True, null=True)
    attractions = models.TextField('Достопримечательности',  blank=True, null=True)
    w_r = models.TextField('Погода и дорога', blank=True, null=True)
    kilometers = models.CharField('Примерный километраж', max_length=10000, blank=True, null=True)
    pictures = models.CharField('Ссылка на альбом с фото', max_length=10000, blank=True, null=True)
    country = models.CharField('Страна', max_length=10000, blank=True, null=True, default='Россия')
    region = models.CharField('Регион', max_length=10000, blank=True, null=True, default='СПб и ЛО')
    type = models.CharField('Тип записи', max_length=10000, blank=True, null=True, default='Идея для прогулки/поездки')
    
    
    def __str__(self):
        return f' {self.date} , {self.title}'

    class Meta:
        verbose_name = 'Хайкинг'
        verbose_name_plural = 'Хайкинг'


class Comments(models.Model):
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    text = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(Hike, verbose_name='К записи', on_delete=models.PROTECT,
                                related_name='comments')
    author = models.CharField('Автор', max_length=50)

    def __str__(self):
        return f' {self.author} , к {self.forNote.title},  от {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('blogstr', kwargs={'pk': self.forNote.pk})

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pk']
