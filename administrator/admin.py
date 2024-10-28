from django import forms
from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
import tablib

from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Блог классы для отображения в админке

# класс для загрузки/выгрузки Блог
class RegstrResource(resources.ModelResource):
    class Meta:
        model = Regstr


# класс добавления стилей к окну Блог
class RegstrAdminForm(forms.ModelForm):
    text = forms.CharField(label="Текст", widget=CKEditorUploadingWidget())
    class Meta:
        model = Regstr
        fields = '__all__'
        
# класс подробностей Блог   
class RegstrAdmin(ImportExportActionModelAdmin):
    resource_class = RegstrResource
    list_display = ('date', 'text',)
    search_fields = ['text']
    form = RegstrAdminForm
        
# фиксация формы в админке Блог
admin.site.register(Regstr, RegstrAdmin)
