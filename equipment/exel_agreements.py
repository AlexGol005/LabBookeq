"""
Модуль проекта LabJournal, приложения equipment.
Приложение equipment это обширное приложение, включает все про лабораторное оборудование и лабораторные помещения
Данный модуль exel_agreements.py выводит представления для выгрузки заявок на поверку по формам разных компаний-поверителей в формате exel.
"""


import xlwt
import pytils.translit
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, request
from django.db.models import Max, Q, Value, CharField, Count, Sum
from django.db.models.functions import Concat, Substr 
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from xlwt import Alignment, Borders

from equipment.constants import servicedesc0
from equipment.forms import*
from equipment.models import*
from formstandart import YearForm
from functstandart import get_dateformat, get_dateformat_to_number
from users.models import Profile, Company

URL = 'equipment'
now = date.today()
gnow = get_dateformat(now)
nnow = get_dateformat_to_number(now)
from equipment.exel import get_affirmation, get_author




# Стили

size = 11

# обкновенные границы ячеек
b1 = Borders()
b1.left = 1
b1.right = 1
b1.top = 1
b1.bottom = 1

# acc выравнивание по центру по горизонтали и по вертикали, обтекание wrap тип 1
acc = Alignment()
acc.horz = Alignment.HORZ_CENTER
acc.vert = Alignment.VERT_CENTER
acc.wrap = 1

# acr выравнивание по центру по вертикали и справа по горизонтали, обтекание wrap тип 1
acr = Alignment()
acr.horz = Alignment.HORZ_RIGHT
acr.vert = Alignment.VERT_CENTER
acr.wrap = 1

# acl выравнивание по центру по вертикали и справа по горизонтали, обтекание wrap тип 1
acl = Alignment()
acl.horz = Alignment.HORZ_LEFT
acl.vert = Alignment.VERT_CENTER
acl.wrap = 1


# style_plain_border обычные ячейки, с границами 
style_plain_border = xlwt.XFStyle()
style_plain_border.font.name = 'Times New Roman'
style_plain_border.borders = b1
style_plain_border.alignment = acc
style_plain_border.font.height = 20 * size

# style_plain_noborder обычные ячейки, без границ
style_plain_noborder = xlwt.XFStyle()
style_plain_noborder.font.name = 'Times New Roman'
style_plain_noborder.alignment = acc
style_plain_noborder.font.height = 20 * size

# style_right_noborder обычные ячейки, без границ, выравнивание по правому краю
style_right_noborder = xlwt.XFStyle()
style_right_noborder.font.name = 'Times New Roman'
style_right_noborder.alignment = acr
style_right_noborder.font.height = 20 * size

# style_left_noborder обычные ячейки, без границ, выравнивание по левому краю
style_left_noborder = xlwt.XFStyle()
style_left_noborder.font.name = 'Times New Roman'
style_left_noborder.alignment = acl
style_left_noborder.font.height = 20 * size


def export_orderverification_template_xls(object_ids):
    pass







def export_orderverification_xls(request, object_ids):
    '''Поверитель: base если нет специальной формы для данного поверителя и прочие исключения'''
    ruser = request.user.profile.userid
    company = Company.objects.get(userid=ruser)
    try:
        a = Activeveraqq.objects.get(pointer=ruser)
        exelnumber = a.aqq.verificator.pk
    except:
        exelnumber = 'list_equipment'
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{exelnumber}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(f'{exelnumber}', cell_overwrite_ok=True)
    ws.header_str = b' '
    ws.footer_str = b' '
    
    q = object_ids[17:-3].split("', '")
    try:
        note = Equipment.objects.filter(id__in=q)
    except:
        note = Equipment.objects.filter(id=1)
    rows = note.values_list(
        'pk', )
    # конец стандартной шапки
    
    # ширина колонок и их количество
    len_sheet = 11
    ws.col(0).width = 500
    ws.col(1).width = 500
    ws.col(2).width = 500
    ws.col(3).width = 3000
    ws.col(4).width = 2000
    ws.col(5).width = 500
    ws.col(6).width = 500
    ws.col(7).width = 500
    ws.col(8).width = 2000
    ws.col(9).width = 1500
    ws.col(10).width = 1500
    ws.col(11).width = 500
    
    row_num = 1
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], style_plain_border)
    wb.save(response)
    return response



def export_orderverification_14_xls(request, object_ids):
    '''Поверитель: не указан'''
    ruser = request.user.profile.userid
    company = Company.objects.get(userid=ruser)
    try:
        a = Activeveraqq.objects.get(pointer=ruser)
        exelnumber = a.aqq.verificator.pk
    except:
        exelnumber = 'list_equipment'
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{exelnumber}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(f'{exelnumber}', cell_overwrite_ok=True)
    ws.header_str = b' '
    ws.footer_str = b' '
    
    q = object_ids[17:-3].split("', '")
    try:
        note = Equipment.objects.filter(id__in=q)
    except:
        note = Equipment.objects.filter(id=1)
    rows = note.values_list(
        'pk', )
    # конец стандартной шапки
    
    # ширина колонок и их количество
    len_sheet = 11
    ws.col(0).width = 500
    ws.col(1).width = 500
    ws.col(2).width = 500
    ws.col(3).width = 3000
    ws.col(4).width = 2000
    ws.col(5).width = 500
    ws.col(6).width = 500
    ws.col(7).width = 500
    ws.col(8).width = 2000
    ws.col(9).width = 1500
    ws.col(10).width = 1500
    ws.col(11).width = 500
    
    row_num = 1
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], style_plain_border)
    wb.save(response)
    return response



def export_orderverification_1_xls(request, object_ids):
    '''Поверитель: ФБУ "ТЕСТ-С.-ПЕТЕРБУРГ"'''
    ruser = request.user.profile.userid
    company = Company.objects.get(userid=ruser)
    try:
        a = Activeveraqq.objects.get(pointer=ruser)
        exelnumber = a.aqq.verificator.pk
    except:
        exelnumber = 'list_equipment'
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{exelnumber}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(f'{exelnumber}', cell_overwrite_ok=True)
    ws.header_str = b' '
    ws.footer_str = b' '
    
    q = object_ids[17:-3].split("', '")
    try:
        note = Equipment.objects.filter(id__in=q)
    except:
        note = Equipment.objects.filter(id=1)
    rows = note.values_list(
        'pk', )
    # конец стандартной шапки
    
    # ширина колонок и их количество
    len_sheet = 11
    ws.col(0).width = 500
    ws.col(1).width = 3000
    ws.col(2).width = 3000
    ws.col(3).width = 4500
    ws.col(4).width = 4500
    ws.col(5).width = 3000
    ws.col(6).width = 3000
    ws.col(7).width = 3000
    ws.col(8).width = 3000
    ws.col(9).width = 3000
    ws.col(10).width = 3000
    ws.col(11).width = 500

    # переменные
    verificator_head_position = a.aqq.verificator.head_position
    verificator_companyName  = a.aqq.verificator.companyName 
    verificator_head_name = a.aqq.verificator.head_name 
    outgoing_number = f'Исх. № {nnow} от {gnow}'
    customer_card_number = f'№ учетной карточки {a.aqq.ver_agreement_card}'
    
    row_num = 1
    columns = [f'Заявка'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain_noborder)
        ws.merge(row_num, row_num, 1, len_sheet)

    row_num += 1
    columns = [f'на выполнение работ (оказание услуг) по поверке (калибровке) СИ, аттестации ИО и иных работ (услуг) в области обеспечения единства'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain_noborder)
        ws.merge(row_num, row_num, 1, len_sheet)

    row_num += 1
    columns = [f'измерений'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain_noborder)
        ws.merge(row_num, row_num, 0, len_sheet)

    row_num += 1
    columns = [f'{verificator_head_position}',
               f'{verificator_head_position}',
               f'{verificator_head_position}',
               f'{verificator_head_position}',
               f'{verificator_head_position}',
               f'{verificator_head_position}',
               f'{verificator_head_position}',
               f'{verificator_head_position}',
               f'{verificator_head_position}',
               f'{verificator_head_position}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num+len_sheet, columns[col_num], style_right_noborder)
        ws.merge(row_num, row_num, len_sheet-3, len_sheet)

    row_num += 1
    columns = [f'{verificator_companyName}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_right_noborder)
        ws.merge(row_num, row_num, len_sheet-3, len_sheet)

    row_num += 1
    columns = [f'{verificator_head_name}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_right_noborder)
        ws.merge(row_num, row_num, len_sheet-3, len_sheet)

    row_num += 2
    columns = [f'{outgoing_number}',
               f'{customer_card_number}',
               
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style_left_noborder)
        ws.merge(row_num, row_num, 1, 5)
    for col_num in range(1,2):
        ws.write(row_num, col_num, columns[col_num], style_right_noborder)
        ws.merge(row_num, row_num, len_sheet-4, len_sheet)
        


    
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], style_plain_border)
    wb.save(response)
    return response


def export_orderverification_9_xls(request, object_ids):
    '''Поверитель: ФГУП "ВНИИМ ИМ. Д.И.МЕНДЕЛЕЕВА"'''
    ruser = request.user.profile.userid
    company = Company.objects.get(userid=ruser)
    try:
        a = Activeveraqq.objects.get(pointer=ruser)
        exelnumber = a.aqq.verificator.pk
    except:
        exelnumber = 'list_equipment'
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{exelnumber}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(f'{exelnumber}', cell_overwrite_ok=True)
    ws.header_str = b' '
    ws.footer_str = b' '
    
    q = object_ids[17:-3].split("', '")
    try:
        note = Equipment.objects.filter(id__in=q)
    except:
        note = Equipment.objects.filter(id=1)
    rows = note.values_list(
        'pk', )
    # конец стандартной шапки
    
    # ширина колонок и их количество
    len_sheet = 11
    ws.col(0).width = 500
    ws.col(1).width = 500
    ws.col(2).width = 500
    ws.col(3).width = 3000
    ws.col(4).width = 2000
    ws.col(5).width = 500
    ws.col(6).width = 500
    ws.col(7).width = 500
    ws.col(8).width = 2000
    ws.col(9).width = 1500
    ws.col(10).width = 1500
    ws.col(11).width = 500

    row_num = 1
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], style_plain_border)
    wb.save(response)
    return response
