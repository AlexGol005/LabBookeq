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
admin.site.register(CommentsEquipment)
admin.site.register(Roomschange)
admin.site.register(DocsCons)
admin.site.register(MeteorologicalParameters)
admin.site.register(TestingEquipmentCharakters)
admin.site.register(TestingEquipment)
admin.site.register(Attestationequipment)
admin.site.register(HelpingEquipmentCharakters)
admin.site.register(HelpingEquipment) 
admin.site.register(ServiceEquipmentU) 
admin.site.register(ServiceEquipmentUFact)


@admin.register(Verificators)
class VerificatorsAdmin(admin.ModelAdmin):
    fields = ['companyName', ]


@admin.register(Verificationequipment)
class VerificationequipmentAdmin(admin.ModelAdmin):

    form = make_ajax_form(Verificationequipment, {
        'verificator': 'verificator_tag'
    })

@admin.register(Calibrationequipment)
class CalibrationequipmentAdmin(admin.ModelAdmin):

    form = make_ajax_form(Calibrationequipment, {
        'verificator': 'verificator_tag'
    })

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):

    form = make_ajax_form(Equipment, {
        'manufacturer': 'manufacturer_tag'
    })

@admin.register(MeasurEquipment)
class MeasurEquipmentAdmin(admin.ModelAdmin):

    form = make_ajax_form(MeasurEquipment, {
        'charakters': 'mecharakters_tag'
    })


@admin.register(ServiceEquipmentME)
class ServiceEquipmentMEAdmin(admin.ModelAdmin):

    form = make_ajax_form(ServiceEquipmentME, {
        'charakters': 'mecharakters_tag'
    })


@admin.register(Agreementverification)
class AgreementverificationAdmin(admin.ModelAdmin):

    form = make_ajax_form(Agreementverification, {
        'verificator': 'verificator_tag'
    })
