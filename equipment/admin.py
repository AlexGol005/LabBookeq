from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
import tablib


# реестр  классы для отображения в админке

# класс для загрузки/выгрузки  типа/модификации
class MeasurEquipmentCharaktersResource(resources.ModelResource):
    class Meta:
        model = MeasurEquipmentCharakters
        
# класс подробностей реестр 
class MeasurEquipmentCharaktersAdmin(ImportExportActionModelAdmin):
    resource_class = MeasurEquipmentCharaktersResource
    list_display = ('reestr' , 'name', 'modificname', 'typename')
    search_fields = ['reestr',]
        
# фиксация формы в админке реестр 
admin.site.register(MeasurEquipmentCharakters, MeasurEquipmentCharaktersAdmin)

admin.site.register(Manufacturer)
admin.site.register(Rooms)
admin.site.register(Personchange)
admin.site.register(MeasurEquipment)
admin.site.register(Equipment)
admin.site.register(CommentsEquipment)
# admin.site.register(Verificationequipment)
admin.site.register(Roomschange)
admin.site.register(VerificatorPerson)
admin.site.register(Verificators)
admin.site.register(DocsCons)
admin.site.register(CompanyCard)
admin.site.register(MeteorologicalParameters)
admin.site.register(TestingEquipmentCharakters)
admin.site.register(TestingEquipment)
admin.site.register(Attestationequipment)
admin.site.register(HelpingEquipmentCharakters)
admin.site.register(HelpingEquipment) 
autocomplete_fields = ['question']
class ChoiceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['question']



# class ChoiceAdmin(admin.ModelAdmin):
    
@admin.register(Verificationequipment)
class NoteAdmin(admin.ModelAdmin):
    autocomplete_fields = ['companyName']

# это для поиска по выпадающему списку
# class VerificationequipmentCycleAdmin(admin.ModelAdmin):
#     autocomplete_fields = ['companyName']

# admin.site.register(Verificationequipment, VerificationequipmentCycleAdmin)

