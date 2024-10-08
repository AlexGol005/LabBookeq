from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
import tablib

from ckeditor_uploader.widgets import CKEditorUploadingWidget

class KareliahistoryAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Kareliahistory
        fields = '__all__'
        
class KareliahistoryResource(resources.ModelResource):
    class Meta:
        model = Kareliahistory

class KareliahistoryAdmin(ImportExportActionModelAdmin):
    resource_class = KareliahistoryResource
    list_display = ('pk', 'text',)
    search_fields = ['pk', 'title', 'text']
    form = MovieAdminForm

admin.site.register(Kareliahistory, KareliahistoryAdmin)


@admin.register(Itbookmarks)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'type',)
    search_fields = ['pk']

@admin.register(Bookmarks)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text')
    search_fields = ['pk', 'text']
    
@admin.register(Hike)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', )

    search_fields = ['pk', 'title', 'attractions']

#@admin.register(Kareliahistory)
#class NoteAdmin(admin.ModelAdmin):
    #list_display = ('pk', 'title', )

    #search_fields = ['pk', 'title', 'text']



