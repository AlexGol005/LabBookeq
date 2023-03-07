from django.db import models
from django.urls import reverse


class Blog(models.Model):
    date = models.DateField('Дата', auto_now_add=True)
    title = models.CharField('Заголовок', max_length=10000)
    metatitle = models.CharField('Метазаголовок страницы', max_length=10000, blank=True, null=True)
    description = models.TextField('Метаописание страницы', blank=True, null=True)
    keywords = models.TextField('Ключевые слова', blank=True, null=True)
    text = models.TextField('Текст записи')




    def __str__(self):
        return f' {self.date} , {self.title}'

    class Meta:
        verbose_name = 'О лабораторном оборудовании'
        verbose_name_plural = 'О лабораторном оборудовании'


class Comments(models.Model):
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    text = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(Blog, verbose_name='К записи блога', on_delete=models.PROTECT,
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
