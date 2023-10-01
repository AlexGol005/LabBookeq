from django.contrib import admin
from django import forms

from bdanswers.models import Bdanswers

# from ckeditor_uploader.widgets import CKEditorUploadingWidget


# class PostAdminForm(forms.ModelForm):
#     answer = forms.CharField(label='Ответ', widget=CKEditorUploadingWidget())
#     class Meta:
#         model = Bdanswers
#         fields = '__all__'


@admin.register(Bdanswers)
class NoteAdmin(admin.ModelAdmin):
    search_fields = ['number']
    # form = PostAdminForm
