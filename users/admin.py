from django.contrib import  admin

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget

from . models import *

admin.site.register(Profile)


@admin.register(Company)  
class NoteAdmin(admin.ModelAdmin):
    list_display = ('userid', 'name', 'pay')
    search_fields = ['userid', 'name',]

# сотрудники  классы для отображения в админке

# класс для загрузки/выгрузки  сотрудники
class EmployeesResource(resources.ModelResource):
    class Meta:
        model = Employees
        
# класс подробностей сотрудники 
class EmployeesAdmin(ImportExportActionModelAdmin):
    resource_class = EmployeesResource
    list_display = ('get_userid' , 'name', 'position', )
    def get_userid(self, obj):
        return obj.userid.userid
    # get_name.admin_order_field  = 'author'  #Allows column order sorting
    get_userid.short_description = 'ID компании'  #Renames column head
    search_fields = ['name',]

# фиксация формы в админке сотрудники 
admin.site.register(Employees, EmployeesAdmin)
