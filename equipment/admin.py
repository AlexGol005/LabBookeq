from django.contrib import admin
from .models import *
from .lookups import *

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
import tablib
from ajax_select.admin import AjaxSelectAdmin
from ajax_select import make_ajax_form

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
admin.site.register(Roomschange)
admin.site.register(VerificatorPerson)
# admin.site.register(Verificators)
admin.site.register(DocsCons)
admin.site.register(CompanyCard)
admin.site.register(MeteorologicalParameters)
admin.site.register(TestingEquipmentCharakters)
admin.site.register(TestingEquipment)
admin.site.register(Attestationequipment)
admin.site.register(HelpingEquipmentCharakters)
admin.site.register(HelpingEquipment) 

@admin.register(Verificators)
class VerificatorsAdmin(admin.ModelAdmin):
    fields = ['companyName', ]


@admin.register(Verificationequipment)
class VerificationequipmentAdmin(admin.ModelAdmin):

    form = make_ajax_form(Verificationequipment, {
        'verificator': 'verificator_tag'
    })


# admin.site.register(Verificationequipment)

# @admin.register(Verificationequipment)
# class VerificationequipmentAdmin(AjaxSelectAdmin):

#     form = make_ajax_form(Verificationequipment, {
#         # fieldname: channel_name
#         'verificator': 'verificator_tag'
#     })
#-------------------------------------------------------
# class ChoiceAdmin(admin.ModelAdmin):
    
# @admin.register(Verificationequipment)
# class NoteAdmin(admin.ModelAdmin):
#     autocomplete_fields = ['companyName']

# это для поиска по выпадающему списку
# class VerificationequipmentCycleAdmin(admin.ModelAdmin):
#     autocomplete_fields = ['companyName']

# admin.site.register(Verificationequipment, VerificationequipmentCycleAdmin)

