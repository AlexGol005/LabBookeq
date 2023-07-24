from django.contrib import admin

from bdanswers.models import Bdanswers


@admin.register(Bdanswers)
class NoteAdmin(admin.ModelAdmin):
    search_fields = ['number']
