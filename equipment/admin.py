from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
import tablib



admin.site.register(Manufacturer)
admin.site.register(Rooms)
admin.site.register(Personchange)
admin.site.register(MeasurEquipment)
admin.site.register(Equipment)
admin.site.register(CommentsEquipment)
admin.site.register(Verificationequipment)
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

# реестр без типа/модификации классы для отображения в админке

# класс для загрузки/выгрузки реестр без типа/модификации
class MeasurEquipmentCharaktersResource(resources.ModelResource):
    class Meta:
        model = MeasurEquipmentCharakters
        
# класс подробностей реестр без типа/модификации   
class MeasurEquipmentCharaktersAdmin(ImportExportActionModelAdmin):
    resource_class = MeasurEquipmentCharaktersResource
    list_display = ('reestr', 'modificname', 'typename')
    search_fields = ['reestr',]
        
# фиксация формы в админке реестр без типа/модификации
admin.site.register(MeasurEquipmentCharakters, MeasurEquipmentCharaktersAdmin)


