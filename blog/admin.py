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
class BlogResource(resources.ModelResource):
    class Meta:
        model = Blog


# класс добавления стилей к окну Блог
class BlogAdminForm(forms.ModelForm):
    text = forms.CharField(label="Текст", widget=CKEditorUploadingWidget())
    class Meta:
        model = Blog
        fields = '__all__'
        
# класс подробностей Блог   
class BlogAdmin(ImportExportActionModelAdmin):
    resource_class = BlogResource
    list_display = ('pk', 'date', 'title',)
    search_fields = ['pk', 'title', 'text']
    form = BlogAdminForm
        
# фиксация формы в админке Блог
admin.site.register(Blog, BlogAdmin)
