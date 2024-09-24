from django.contrib import admin
from .models import *



admin.site.register(Hike)
admin.site.register(Comments)
admin.site.register(Bookmarks)

@admin.register(Itbookmarks)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'type',)
    search_fields = ['pk']
    

