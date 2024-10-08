from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
import tablib


class KareliahistoryResource(resources.ModelResource):
    class Meta:
        model = Kareliahistory
        
#class NoteAdmin(ImportExportActionModelAdmin):
    #resource_class = ProductResource
    #list_display = ('pk', 'text',)



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
