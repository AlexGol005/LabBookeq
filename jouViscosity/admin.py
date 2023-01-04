from django.contrib import admin
from .models import*


@admin.register(ViscosityKinematicResult)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(ViscosityDinamicResult)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id',)
