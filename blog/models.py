from django.db import models

class Blog(models.Model):
    date = models.DateField('Дата', auto_now_add=True)
    title = models.CharField('Заголовок', max_length=10000)
    text = models.TextField('Текст записи')

    def __str__(self):
        return f' {self.date} , {self.title}'

    class Meta:
        verbose_name = 'О лабораторном оборудовании'
        verbose_name_plural = 'О лабораторном оборудовании'
