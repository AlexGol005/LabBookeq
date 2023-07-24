from django.db import models

class Bdanswers(models.Model):
    """Вопросы и ответы по теме профпереподготовка Базы данных"""
    number = models.CharField('Номер вопроса', max_length=4, unique=True)
    question = models.TextField('Вопрос')
    answer = models.TextField('Ответ')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Вопросы и ответы бд'
        verbose_name_plural = 'Вопросы и ответы бд'
