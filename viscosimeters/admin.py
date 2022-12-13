from django.contrib import admin
from .models import Viscosimeters, ViscosimeterType


@admin.register(ViscosimeterType)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('diameter', 'pairNumber', 'viscosity1000', 'range')
    fields = (('range', 'diameter'), 'pairNumber', 'viscosity1000',)


@admin.register(Viscosimeters)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'konstant' )
