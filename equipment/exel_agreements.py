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

# style_plain_noborder_bold обычные ячейки, без границ, жирный шрифт
style_plain_noborder_bold = xlwt.XFStyle()
style_plain_noborder_bold.font.name = 'Times New Roman'
style_plain_noborder_bold.alignment = acc
style_plain_noborder_bold.font.height = 20 * size
style_plain_noborder_bold.font.bold = True

# style_plain_noborder_italic обычные ячейки, без границ, курсив
style_plain_noborder_italic = xlwt.XFStyle()
style_plain_noborder_italic.font.name = 'Times New Roman'
style_plain_noborder_italic.alignment = acc
style_plain_noborder_italic.font.height = 20 * size
style_plain_noborder_italic.font.italic = True

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
    one = f'Заявка'
    two = f'на выполнение работ (оказание услуг) по поверке (калибровке) СИ, аттестации ИО и иных работ (услуг) в области обеспечения единства'
    three = f'измерений'
    verificator_head_position = a.aqq.verificator.head_position
    verificator_companyName  = a.aqq.verificator.companyName 
    verificator_head_name = a.aqq.verificator.head_name 
    outgoing_number = f'Исх. № {nnow} от {gnow}'
    customer_card_number = f'№ учетной карточки {a.aqq.ver_agreement_card}'
    contract_request = f'Просим провести периодическую, первичную, после ремонта (нужное подчеркнуть) поверку / калибровку СИ, аттестацию ИО и иных работ (услуг) '\
    f'в области обеспечения единства измерений в соответствии с договором (гос. контрактом) № {a.aqq.ver_agreement_number} от {a.aqq.ver_agreement_date}.'
    payment_number = f'Если оплата была по предварительному счету обязательно указать номер счета и дату или номер платежного поручения________________________________'
    agree = f'Согласие на передачу ФБУ «Тест-С.-Петербург» сведений о владельце СИ в ФИФ ОЕИ'
    yesno = f'ДА   ▭     	НЕТ ▭'
    dop_agree = f'Если заказчик не является владельцем СИ, Заказчик заявляет о получении согласия от владельца СИ на передачу  ФБУ «Тест-С.-Петербург» сведений о владельце СИ в ФИФ ОЕИ'


    
    row_num = 1
    columns = [f'{one}'
    ]
    ws.write(row_num, 1, columns[0], style_plain_noborder_bold)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 1
    columns = [f'{two}'
    ]
    ws.write(row_num, 1, columns[0], style_plain_noborder_bold)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 1
    columns = [f'{three}'
    ]
    ws.write(row_num, 1, columns[0], style_plain_noborder_bold)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 1
    columns = [f'{verificator_head_position}',
    ]
    ws.write(row_num, len_sheet-4, columns[0], style_right_noborder)
    ws.merge(row_num, row_num, len_sheet-4, len_sheet-1)

    row_num += 1
    columns = [f'{verificator_companyName}'
    ]
    ws.write(row_num, len_sheet-4, columns[0], style_right_noborder)
    ws.merge(row_num, row_num, len_sheet-4, len_sheet-1)

    row_num += 1
    columns = [f'{verificator_head_name}'
    ]
    ws.write(row_num, len_sheet-4, columns[0], style_right_noborder)
    ws.merge(row_num, row_num, len_sheet-4, len_sheet-1)

    row_num += 2
    columns = [f'{outgoing_number}',
               f'{customer_card_number}',               
    ]
    ws.write(row_num, 1, columns[0], style_left_noborder)
    ws.merge(row_num, row_num, 1, 4)
    ws.write(row_num, len_sheet-4, columns[1], style_right_noborder)
    ws.merge(row_num, row_num, len_sheet-4, len_sheet-1)

    row_num += 1
    columns = [f'{contract_request}'
    ]
    ws.write(row_num, 1, columns[0], style_plain_noborder)
    ws.merge(row_num, row_num, 1, len_sheet-1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 800

    row_num += 1
    columns = [f'{payment_number}'
    ]
    ws.write(row_num, 1, columns[0], style_plain_noborder_italic)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 2
    columns = [f'{agree}'
    ]
    ws.write(row_num, 1, columns[0], style_plain_noborder_bold)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 1
    columns = [f'{yesno}'
    ]
    ws.write(row_num, 1, columns[0], style_plain_noborder)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 1
    columns = [f'{dop_agree}'
    ]
    ws.write(row_num, 1, columns[0], style_plain_noborder)
    ws.merge(row_num, row_num, 1, len_sheet-1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 800

        


    
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
