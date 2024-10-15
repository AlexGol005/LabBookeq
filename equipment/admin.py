from django.contrib import admin
from .models import *



admin.site.register(Manufacturer)
admin.site.register(Rooms)
admin.site.register(MeasurEquipmentCharakters)
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
admin.site.register(MeasurEquipmentReestr) 

# реестр без типа/модификации классы для отображения в админке

# класс для загрузки/выгрузки реестр без типа/модификации
class MeasurEquipmentReestrResource(resources.ModelResource):
    class Meta:
        model = MeasurEquipmentReestr
        
# класс подробностей реестр без типа/модификации   
class MeasurEquipmentReestrAdmin(ImportExportActionModelAdmin):
    resource_class = MeasurEquipmentReestrResource
    list_display = ('pk', 'text',)
    search_fields = ['reestr',]
        
# фиксация формы в админке реестр без типа/модификации
admin.site.register(MeasurEquipmentReestr, MeasurEquipmentReestrAdmin)


