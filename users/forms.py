from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import *


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Введите логин',
                               required=True,
                               help_text='инициалы и фамилия без пробелов',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                               'placeholder': 'И.И.Иванов'}))
    name = forms.CharField(label='ФИО',
                               required=True,
                               help_text='ФИО полностью',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                               'placeholder': 'Иваонов Иван Иванович'}))
    # userlastname = forms.CharField(label='Фамилия',
    #                                required=True,
    #                                widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                              'placeholder': 'Фамилия'}))
    # userfirstname = forms.CharField(label='Имя', required=True,
    #                                 widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                               'placeholder': 'Имя'}))
    # userpatronymic = forms.CharField(label='Отчество',
    #                                  required=False,
    #                                  widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                                'placeholder': 'Отчество'}))
    userposition = forms.CharField(label='Должность',
                                   required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Должность'}))
    # usertelnumber = forms.CharField(label='Телефон',
    #                                required=True,
    #                                widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                              'placeholder': 'Телефон'}))
    password1 = forms.CharField(label='Введите пароль',
                                required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                           'placeholder': 'введите пароль' }))
    password2 = forms.CharField(label='Подтвердите пароль',
                                required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                           'placeholder': 'повторно введите пароль' }))
    user_email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'ваш email'})
                             )


    class Meta:
        model = User
        # fields = ['username', 'userlastname', 'userfirstname', 'userpatronymic', 'userposition', 'email', 'usertelnumber', 'password1', 'password1' ]
        fields = ['username', 'password1', 'password1', 'user_email', ]

class UserUdateForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'ваш email'})
                             )
    username = forms.CharField(label='Введите логин',
                               required=True,
                               help_text='Фамилия и инициалы без пробелов',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                               'placeholder': 'И.О.Фамилия'}))


    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUdateForm(forms.ModelForm):
    img = forms.ImageField(label='загрузить фото', widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['img']



class CompanyCreateForm(forms.ModelForm):
    """форма для обновления профиля компании"""
    name = forms.CharField(label='Название краткое', widget=forms.TextInput(attrs={'class': 'form-control',}))
    name_big = forms.CharField(label='Название полное', widget=forms.TextInput(attrs={'class': 'form-control',}))
    requisits = forms.CharField(label='Реквизиты', widget=forms.Textarea(attrs={'class': 'form-control',}))
    adress = forms.CharField(label='Адрес юридический', widget=forms.Textarea(attrs={'class': 'form-control',}))
    adress_lab = forms.CharField(label='Адрес физический', widget=forms.Textarea(attrs={'class': 'form-control',}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control',}))
    phone_lab = forms.CharField(label='Телефон лаборатории', widget=forms.TextInput(attrs={'class': 'form-control',}))
    direktor_position = forms.CharField(label='Должность главного лица компании', widget=forms.TextInput(attrs={'class': 'form-control',}))
    direktor_name = forms.CharField(label='ФИО главного лица компании', widget=forms.TextInput(attrs={'class': 'form-control',}))
    headlab_position = forms.CharField(label='Должность главного лица лаборатории', widget=forms.TextInput(attrs={'class': 'form-control',}))
    headlab_name = forms.CharField(label='ФИО главного лица лаборатории', widget=forms.TextInput(attrs={'class': 'form-control',}))
    email = forms.CharField(label='email', widget=forms.TextInput(attrs={'class': 'form-control',}))
    attestat = forms.CharField(label='Данные аттестата аккредитации', required=False, widget=forms.Textarea(attrs={'class': 'form-control',}))
    manager_position = forms.CharField(label='Должность лица ответственного за оборудование', widget=forms.TextInput(attrs={'class': 'form-control',}))
    manager_name = forms.CharField(label='ФИО лица ответственного за оборудование', widget=forms.TextInput(attrs={'class': 'form-control',}))
    manager_phone = forms.CharField(label='Телефон лица ответственного за оборудование', widget=forms.TextInput(attrs={'class': 'form-control',}))
    manager_email = forms.CharField(label='email лица ответственного за оборудование', widget=forms.TextInput(attrs={'class': 'form-control',}))
    caretaker_position = forms.CharField(label='Должность завхоза', widget=forms.TextInput(attrs={'class': 'form-control',}))
    caretaker_name = forms.CharField(label='ФИО завхоза', widget=forms.TextInput(attrs={'class': 'form-control',}))

                        
    class Meta:
        model = Company
        fields = [
                 'name', 
                 'name_big', 
                'requisits', 
                'adress', 
                'adress_lab',  
                'phone',
                'phone_lab',
                'direktor_position', 
                'direktor_name', 
                'headlab_position', 
                'headlab_name', 
                'email', 
                'attestat', 
                'manager_position',
                'manager_name',
                'caretaker_position',
                'caretaker_name' ,
                'manager_phone',
                'manager_email',            
                  ]


class EmployeesUpdateForm(forms.ModelForm):
    """форма для создания обновления сотрудника компании"""
    name = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class': 'form-control',}))
    position = forms.CharField(label='Должность', widget=forms.TextInput(attrs={'class': 'form-control',}))
                             
    class Meta:
        model = Employees
        fields = [
                 'name', 
                'position', 
                  ]

