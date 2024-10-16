from django.db import models
from django.contrib.auth.models import User
from PIL import  Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    name = models.CharField('ФИО/роль', max_length=40, default=None, null=True)
    userposition = models.CharField('Должность', max_length=50, null=True, blank=True)
    userid = models.CharField('Идентификатор организации=ИНН_ГГММДД регистрации)', max_length=50, default=None, null=True)
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
