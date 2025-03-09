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
    list_display = ('reestr' , 'name', 'modificname', 'typename', 'created_at', 'updated_at', 'created_by', 'updated_by', )
    search_fields = ['reestr',]


# характеристики ИО  классы для отображения в админке
# класс для загрузки/выгрузки  характеристики ИО
class TestingEquipmentCharaktersResource(resources.ModelResource):
    class Meta:
        model = TestingEquipmentCharakters
        
# класс подробностей характеристики ИО 
class TestingEquipmentCharaktersAdmin(ImportExportActionModelAdmin):
    resource_class =TestingEquipmentCharaktersResource
    list_display = ('name', 'modificname', 'typename', 'created_at', 'updated_at', 'created_by', 'updated_by', )
    search_fields = ['name',]

# характеристики ВО  классы для отображения в админке
# класс для загрузки/выгрузки  характеристики ВО
class HelpingEquipmentCharaktersResource(resources.ModelResource):
    class Meta:
        model = HelpingEquipmentCharakters
        
# класс подробностей характеристики ИО 
class HelpingEquipmentCharaktersAdmin(ImportExportActionModelAdmin):
    resource_class = HelpingEquipmentCharaktersResource
    list_display = ('name', 'modificname', 'typename', 'created_at', 'updated_at', 'created_by', 'updated_by', )
    search_fields = ['name',]
        
# фиксация формы в админке характеристики СИ/ИО/ВО 
admin.site.register(MeasurEquipmentCharakters, MeasurEquipmentCharaktersAdmin)
admin.site.register(TestingEquipmentCharakters, TestingEquipmentCharaktersAdmin)
admin.site.register(HelpingEquipmentCharakters, HelpingEquipmentCharaktersAdmin)

# Единица ЛО -  классы для отображения в админке
# класс для загрузки/выгрузки  Единица ЛО
class EquipmentResource(resources.ModelResource):
    class Meta:
        model = Equipment
        
# класс подробностей Единица ЛО
class EquipmentAdmin(admin.ModelAdmin):
    form = make_ajax_form(Equipment, {
        'manufacturer': 'manufacturer_tag'
    })
    resource_class = EquipmentResource
    list_display = ('exnumber', 'lot', 'created_at', 'updated_at', 'created_by', 'updated_by', )
    search_fields = ['exnumber', 'lot']

admin.site.register(Equipment, EquipmentResource)



admin.site.register(Test)
admin.site.register(Manufacturer)
admin.site.register(Rooms)
admin.site.register(Personchange)
admin.site.register(CommentsEquipment)
admin.site.register(Roomschange)
admin.site.register(DocsCons)
admin.site.register(MeteorologicalParameters)

admin.site.register(TestingEquipment)
admin.site.register(Attestationequipment)

admin.site.register(HelpingEquipment) 
admin.site.register(ServiceEquipmentU) 
admin.site.register(ServiceEquipmentUFact)
admin.site.register(Activeveraqq)
admin.site.register(Verificators)



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

@admin.register(ServiceEquipmentTE)
class ServiceEquipmentTEAdmin(admin.ModelAdmin):

    form = make_ajax_form(ServiceEquipmentTE, {
        'charakters': 'techarakters_tag'
    })

@admin.register(ServiceEquipmentHE)
class ServiceEquipmentHEAdmin(admin.ModelAdmin):

    form = make_ajax_form(ServiceEquipmentHE, {
        'charakters': 'hecharakters_tag'
    })


@admin.register(Agreementverification)
class AgreementverificationAdmin(admin.ModelAdmin):

    form = make_ajax_form(Agreementverification, {
        'verificator': 'verificator_tag'
    })
