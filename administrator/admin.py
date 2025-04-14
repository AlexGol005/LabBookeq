from django import forms
from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
import tablib

from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Инфо о регистрации классы для отображения в админке

# класс для загрузки/выгрузки Инфо о регистрации
class RegstrResource(resources.ModelResource):
    class Meta:
        model = Regstr

# класс добавления стилей к окну Инфо о регистрации
class RegstrAdminForm(forms.ModelForm):
    text = forms.CharField(label="Текст", widget=CKEditorUploadingWidget())
    class Meta:
        model = Regstr
        fields = '__all__'
        
# класс подробностей Инфо о регистрации   
class RegstrAdmin(ImportExportActionModelAdmin):
    resource_class = RegstrResource
    list_display = ('date', 'text',)
    search_fields = ['text']
    form = RegstrAdminForm
        
# фиксация формы в админке Инфо о регистрации
admin.site.register(Regstr, RegstrAdmin)



# Страница о сайте классы для отображения в админке

# класс для загрузки/выгрузки Страница о сайте
class AboutResource(resources.ModelResource):
    class Meta:
        model = About

# класс добавления стилей к окну Страница о сайте
class AboutAdminForm(forms.ModelForm):
    text = forms.CharField(label="Текст", widget=CKEditorUploadingWidget())
    class Meta:
        model = About
        fields = '__all__'
        
# класс подробностей Страница о сайте
class AboutAdmin(ImportExportActionModelAdmin):
    resource_class = AboutResource
    list_display = ('date', 'text',)
    search_fields = ['text']
    form = AboutAdminForm
        
# фиксация формы в админке Страница о сайте
admin.site.register(About, AboutAdmin)



# Страница Мануал классы для отображения в админке

# класс для загрузки/выгрузки Мануал
class ManualResource(resources.ModelResource):
    class Meta:
        model = Manual

# класс добавления стилей к окну Мануал
class ManualAdminForm(forms.ModelForm):
    text = forms.CharField(label="Текст", widget=CKEditorUploadingWidget())
    class Meta:
        model = Manual
        fields = '__all__'
        
# класс подробностей Мануал
class ManualAdmin(ImportExportActionModelAdmin):
    resource_class = ManualResource
    list_display = ('date', 'text',)
    search_fields = ['text']
    form = ManualAdminForm
        
# фиксация формы в админке Мануал
admin.site.register(Manual, ManualAdmin)


# Страница Политика конфиденциальности классы для отображения в админке

# класс для загрузки/выгрузки Политика конфиденциальности
class PolitycaConfidentResource(resources.ModelResource):
    class Meta:
        model = PolitycaConfident

# класс добавления стилей к окну Политика конфиденциальности
class PolitycaConfidentAdminForm(forms.ModelForm):
    text = forms.CharField(label="Текст", widget=CKEditorUploadingWidget())
    class Meta:
        model = PolitycaConfident
        fields = '__all__'
        
# класс подробностей Политика конфиденциальности
class PolitycaConfidentAdmin(ImportExportActionModelAdmin):
    resource_class = PolitycaConfidentResource
    list_display = ('date', 'text',)
    search_fields = ['text']
    form = PolitycaConfidentAdminForm
        
# фиксация формы в админке Политика конфиденциальности
admin.site.register(PolitycaConfident, PolitycaConfidentAdmin)


# Страница Договор-оферта классы для отображения в админке

# класс для загрузки/выгрузки Договор-оферта
class OfertaResource(resources.ModelResource):
    class Meta:
        model = Oferta

# класс добавления стилей к окну Договор-оферта
class OfertaAdminForm(forms.ModelForm):
    text = forms.CharField(label="Текст", widget=CKEditorUploadingWidget())
    class Meta:
        model = Oferta
        fields = '__all__'
        
# класс подробностей Договор-оферта
class OfertaAdmin(ImportExportActionModelAdmin):
    resource_class = OfertaResource
    list_display = ('date', 'text',)
    search_fields = ['text']
    form = OfertaAdminForm
        
# фиксация формы в админке Договор-оферта
admin.site.register(Oferta,OfertaAdmin)
