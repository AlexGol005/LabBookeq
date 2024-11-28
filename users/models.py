from django.db import models  
from django.contrib.auth.models import User
from PIL import  Image

from equipment.models import Agreementverification

ORDERFORMCHOISE = (
        ('ФБУ «Тест-С.-Петербург»', 'ФБУ «Тест-С.-Петербург»'),
        ('ФГУП "ВНИИМ ИМ. Д.И.МЕНДЕЛЕЕВА"', 'ФГУП "ВНИИМ ИМ. Д.И.МЕНДЕЛЕЕВА"'),
    )




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    name = models.CharField('ФИО/роль', max_length=40, default=None, null=True)
    userposition = models.CharField('Должность', max_length=50, null=True, blank=True)
    userid = models.CharField('Идентификатор организации (10 случайных цифр)', max_length=50, default=None, null=True)
    img = models.ImageField('Фото сотрудника', default='user_images/default.png', upload_to='user_images')
    pay = models.BooleanField ('Оплачено', default=True)


    def __str__(self):
        return f'Организация: {self.userid}; пользователь: {self.name}; логин: {self.user.username}'

    def save(self, *args, **kwargs):
        super().save()
        image = Image.open(self.img.path)
        if image.height > 256 or image.width > 256:
            resize = (256, 256)
            image.thumbnail(resize)
            image.save(self.img.path)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'



class Company(models.Model):
    userid = models.CharField('Идентификатор организации (10 случайных цифр)', max_length=50, default=None, null=True, blank=True, unique=True)
    name = models.CharField('Название организации краткое', max_length=100, default=None, null=True, blank=True)
    name_big = models.CharField('Название организации полное', max_length=100, default=None, null=True, blank=True)
    attestat = models.CharField('Аттестат аккредитации', max_length=200, default=None, null=True, blank=True)
    requisits =  models.TextField('Реквизиты организации', default=None, null=True, blank=True)
    adress =  models.TextField('Адрес организации юридический', max_length=100, default=None, null=True, blank=True)
    adress_lab =  models.TextField('Адрес лаборатории физический', max_length=100, default=None, null=True, blank=True)
    phone =  models.CharField('Телефон организации юридический', max_length=15, default=None, null=True, blank=True)
    phone_lab =  models.CharField('Телефон лаборатории', max_length=15, default=None, null=True, blank=True)
    direktor_position = models.CharField('Должность главного лица компании', max_length=40, default=None, null=True, blank=True)
    direktor_name = models.CharField('ФИО главного лица компании', max_length=100, default=None, null=True, blank=True)
    headlab_position = models.CharField('Должность главного лица лаборатории', max_length=100, default=None, null=True, blank=True)
    headlab_name = models.CharField('ФИО главного лица лаборатории', max_length=100, default=None, null=True, blank=True)
    manager_position = models.CharField('Должность лица ответственного за оборудование', max_length=100, default=None, null=True, blank=True)
    manager_name = models.CharField('ФИО лица ответственного за оборудование', max_length=100, default=None, null=True, blank=True)
    manager_email = models.CharField('email лица ответственного за оборудование', max_length=100, default=None, null=True, blank=True)
    manager_phone = models.CharField('телефон лица ответственного за оборудование', max_length=100, default=None, null=True, blank=True)
    caretaker_position = models.CharField('Должность завхоза', max_length=100, default=None, null=True, blank=True)
    caretaker_name = models.CharField('ФИО завхоза', max_length=100, default=None, null=True, blank=True)
    email = models.CharField('email организации', max_length=40, default=None, null=True, blank=True)
    pay = models.BooleanField ('Оплачено', default=True)
    activ_verificator = models.ForeignKey(Agreementverification, on_delete=models.PROTECT, verbose_name='Активный в данный момент оформления договор с компанией-поверителем') 

    def __str__(self):
        return f'Организация: {self.userid}; {self.name}'

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Employees(models.Model):
    userid = models.ForeignKey(Company, verbose_name = 'Идентификатор организации', on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField('ФИО', max_length=40, default=None, null=True, blank=True)
    position = models.CharField('Должность', max_length=40, default=None, null=True, blank=True)


    def __str__(self):
        return f'{self.name};{self.position};({self.userid.userid}) '

    class Meta:
        verbose_name = 'Сотрудники'
        verbose_name_plural = 'Сотрудники'
    
