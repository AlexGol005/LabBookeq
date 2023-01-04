from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image


class AttestationJ(models.Model):
    date = models.DateField('Дата создания журнала', default=timezone.now)
    name = models.CharField('Наименование журнала', max_length=1000, default='')
    ndocument = models.CharField('Методы испытаний', max_length=100, default='')
    performer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ответственный за ведение журнала')
    for_url = models.CharField('Адрес журнала', max_length=100, default='')
    extra_info = models.TextField('Доп', blank=True, null=True)
    str_html = models.TextField('HTML код для страницы журнала', blank=True, null=True)
    formuls = models.TextField('Формулы для расчётов', blank=True, null=True)
    img = models.ImageField('Картинка для журнала', default='user_images/default.png', upload_to='user_images')

    def __str__(self):
        return f' {self.name}'

    def save(self, *args, **kwargs):
        super().save()
        image = Image.open(self.img.path)
        if image.height > 1000 or image.width > 1000:
            resize = (1000, 1000)
            image.thumbnail(resize)
            image.save(self.img.path)

    def get_absolute_url(self):
        return reverse(self.for_url)

    class Meta:
        verbose_name = 'Журнал измерений'
        verbose_name_plural = 'Журналы измерений'


class ResultValueJ(models.Model):
    date = models.DateField('Дата создания журнала', default=timezone.now)
    name = models.CharField('Наименование журнала', max_length=100, default='')
    for_url = models.CharField('Адрес журнала', max_length=100, default='')
    CM = models.TextField('для проб', blank=True, null=True)
    extra_info = models.TextField('Доп', blank=True, null=True)

    def __str__(self):
        return f' {self.name}'

    def get_absolute_url(self):
        return reverse(self.for_url)

    class Meta:
        verbose_name = 'Журнал результатов измерений'
        verbose_name_plural = 'Журналы результатов измерений'
