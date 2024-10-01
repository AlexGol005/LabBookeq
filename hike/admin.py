from django.contrib import admin
from .models import *






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
