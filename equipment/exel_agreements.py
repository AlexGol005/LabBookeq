"""
Модуль проекта LabJournal, приложения equipment.
Приложение equipment это обширное приложение, включает все про лабораторное оборудование и лабораторные помещения
Данный модуль exel_agreements.py выводит представления для выгрузки заявок на поверку по формам разных компаний-поверителей в формате exel.
"""

from itertools import chain
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

# acc90 выравнивание по центру по горизонтали и по вертикали, обтекание wrap тип 1, повернуто на 90 градусов
acc90 = Alignment()
acc90.horz = Alignment.HORZ_CENTER
acc90.vert = Alignment.VERT_CENTER
acc90.wrap = 1
acc90.rota = Alignment.ROTATION_STACKED

# acl ыравнивание по центру по вертикали и слева по горизонтали, обтекание wrap тип 1
acl = Alignment()
acl.horz = Alignment.HORZ_LEFT
acl.vert = Alignment.VERT_CENTER
acl.wrap = 1


# st90 обычные ячейки, с границами, повернут текст на 90 градусов
st90 = xlwt.easyxf('align: rotation 90;' 'font: name Times New Roman, height 220;' 'borders: left thin, right thin, top thin, bottom thin;' 'alignment: wrap on, horizontal center, vertical center;')


# style_plain_border обычные ячейки, с границами 
style_plain_border = xlwt.XFStyle()
style_plain_border.font.name = 'Times New Roman'
style_plain_border.borders = b1
style_plain_border.alignment = acc
style_plain_border.font.height = 20 * size

# style_left_border обычные ячейки, с границами, выравнивание по левому краю 
style_left_border = xlwt.XFStyle()
style_left_border.font.name = 'Times New Roman'
style_left_border.borders = b1
style_left_border.alignment = acl
style_left_border.font.height = 20 * size

# style_plain_border_90 обычные ячейки, с границами, повернут текст на 90 градусов
style_plain_border_90 = xlwt.XFStyle()
style_plain_border_90.font.name = 'Times New Roman'
style_plain_border_90.borders = b1
# style_plain_border_90.alignment = acc90
style_plain_border_90.font.height = 20 * size


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

# style_left_noborder_italic обычные ячейки, без границ, курсив, выравнивание по левому краю
style_left_noborder_italic = xlwt.XFStyle()
style_left_noborder_italic.font.name = 'Times New Roman'
style_left_noborder_italic.alignment = acl
style_left_noborder_italic.font.height = 20 * size
style_left_noborder_italic.font.italic = True

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

# style_left_noborder_bold обычные ячейки, без границ, выравнивание по левому краю, жирный шрифт
style_left_noborder_bold = xlwt.XFStyle()
style_left_noborder_bold.font.name = 'Times New Roman'
style_left_noborder_bold.alignment = acl
style_left_noborder_bold.font.height = 20 * size
style_left_noborder_bold.font.bold = True


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
    ws.col(3).width = 4000
    ws.col(4).width = 4000
    ws.col(5).width = 500
    ws.col(6).width = 500
    ws.col(7).width = 500
    ws.col(8).width = 8000
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
    if not q:
        q = ['1']
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
    if not q:
        q = ['1']
    try:
        note = Equipment.objects.filter(id__in=q)
    except:
        note = Equipment.objects.filter(id=1)      
    # конец стандартной шапки

    # ширина колонок и их количество
    len_sheet = 12
    ws.col(0).width = 300
    ws.col(1).width = 2000
    ws.col(2).width = 3500
    ws.col(3).width = 5000
    ws.col(4).width = 4500
    ws.col(5).width = 3500
    ws.col(6).width = 2500
    ws.col(7).width = 2500
    ws.col(8).width = 3500
    ws.col(9).width = 3500
    ws.col(10).width = 3500
    ws.col(11).width = 300

        # данные
    rows1 = MeasurEquipment.objects.filter(equipment__pk__in=q).\
    annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),\
             num=Value('1'),\
             note=Value('поверка'),\
             cod1=Value(''),).\
    values_list(
        'charakters__reestr',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipment__yearmanuf',
        'num',
        'note',
        'cod1',
        'cod1',
    )
                         
    rows2 = TestingEquipment.objects.filter(equipment__pk__in=q).\
    annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),\
             num=Value('1'),\
             note=Value('аттестация'),\
             cod1=Value(''),).\
    values_list(
        'cod1',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipment__yearmanuf',
        'num',
        'note',
        'cod1',
        'cod1',
    )

    

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
    if a.aqq.public_agree:
        yesno = f'ДА   ☑     	НЕТ  ☐'
    else:
        yesno = f'ДА    ☐    	НЕТ ☑'
    dop_agree = f'Если заказчик не является владельцем СИ, Заказчик заявляет о получении согласия от владельца СИ на передачу  ФБУ «Тест-С.-Петербург» сведений о владельце СИ в ФИФ ОЕИ'
    table_headers = ['№ П/П',
                     '№ гос.реестра', 
                     'Наименование СИ (ИО), иных работ (услуг) в области обеспечения единства измерений', 
                     'Тип СИ (ИО) Модификация (класс точности, диапазон измерений, количество каналов или количество штук в наборе)',
                     'Заводской (инвентарный) номер',
                     'Год выпуска',
                     'Кол-во СИ (ИО)',
                     'Примечание (поверка/калибровка)',
                     'Эталон/Разряд/Рег. № ФИФ (указывается для эталонов)',
                     'Владелец (если отличается от заявителя)'
                    ]
    urgency = 'Срочность:	нет	☑	1 день	☐	3 дня	☐	5 дней	☐'
    req = 'Реквизиты организации '
    cname =f'- полное и сокращенное наименование предприятия Заказчика: {company.name_big} ({company.name}) '
    inn_kpp = f'- {company.requisits}'
    contact_person = f'- Контактное лицо: {company.manager_name}'
    contact_phone = f'Контактный телефон: {company.manager_phone}'
    contact_email = f'Эл. почта: {company.manager_email}'
    signature = f'{company.direktor_position}__________________________________________{company.direktor_name}'
            
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
    
    row_num += 1
    for col_num in range(len(table_headers)):
         ws.write(row_num, col_num+1, table_headers[col_num], style_plain_border)


    for row in rows1:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num + 2, row[col_num], style_plain_border)
    for row in rows2:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num + 2, row[col_num], style_plain_border)
            
    a = row_num
    for col_num in range(1):
        for row_num in range(16, a + 1):
            ws.write(row_num, col_num+1, f'{row_num - 15}', style_plain_border)

    row_num += 2
    columns = [f'{urgency}'
    ]
    ws.write(row_num, 1, columns[0], style_left_noborder)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 2
    columns = [f'{req}'
    ]
    ws.write(row_num, 1, columns[0], style_left_noborder)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 1
    columns = [f'{cname}'
    ]
    ws.write(row_num, 1, columns[0], style_left_noborder)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 1
    columns = [f'{inn_kpp}'
    ]
    ws.write(row_num, 1, columns[0], style_left_noborder)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 1
    columns = [f'{contact_person}'
    ]
    ws.write(row_num, 1, columns[0], style_left_noborder)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 1
    columns = [f'{contact_phone}'
    ]
    ws.write(row_num, 1, columns[0], style_left_noborder)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 1
    columns = [f'{contact_email}'
    ]
    ws.write(row_num, 1, columns[0], style_left_noborder)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 2
    columns = [f'{signature}'
    ]
    ws.write(row_num, 1, columns[0], style_plain_noborder)
    ws.merge(row_num, row_num, 1, len_sheet-1)                                
        
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
    try:
        q = object_ids[17:-3].split("', '")
    except:
        q = [1]
    try:
        note = Equipment.objects.filter(id__in=q)
    except:
        note = Equipment.objects.filter(id=1)      
    # конец стандартной шапки

    # ширина колонок и их количество
    len_sheet = 17
    ws.col(0).width = 300
    ws.col(1).width = 2000
    ws.col(2).width = 4500
    ws.col(3).width = 2000
    ws.col(4).width = 4500
    ws.col(5).width = 2500
    ws.col(6).width = 2500
    ws.col(7).width = 2500
    ws.col(8).width = 2500
    ws.col(9).width = 2500
    ws.col(10).width = 2500
    ws.col(11).width = 2500
    ws.col(12).width = 2500
    ws.col(13).width = 2500
    ws.col(14).width = 2500
    ws.col(15).width = 2500
    ws.col(16).width = 2500
    ws.col(17).width = 2500
    ws.col(18).width = 300

    # данные
    rows1 = MeasurEquipment.objects.filter(equipment__pk__in=q).\
    annotate(name_mod_type=Concat('charakters__name', 'charakters__typename', Value('/ '), 'charakters__modificname'),\
             exnumber_short=Substr('equipment__exnumber',1,5),\
             num=Value('1'),\
             note=Value('поверка'),\
             cod1=Value(''),\
             pr1=Value('ПР'),\
             sv1=Value('да'),\
             period1=Value('месяц')).\
    values_list(
        'name_mod_type',
        'equipment__yearmanuf',
        'charakters__reestr',
        'equipment__lot',
        'exnumber_short',
        'cod1',
        'cod1',
        'cod1',
        'pr1',
        'cod1',
        'sv1',
        'sv1',
        'period1',
        'cod1',
        'cod1',
    )
                         
    rows2 = TestingEquipment.objects.filter(equipment__pk__in=q).\
    annotate(name_mod_type=Concat('charakters__name', 'charakters__typename', Value('/ '), 'charakters__modificname'),\
             exnumber_short=Substr('equipment__exnumber',1,5),\
             num=Value('1'),\
             note=Value('поверка'),\
             cod1=Value(''),\
             pr1=Value('ПР'),\
             sv1=Value('да'),\
             period1=Value('месяц')).\
    values_list(
        'name_mod_type',
        'equipment__yearmanuf',
        'cod1',
        'equipment__lot',
        'exnumber_short',
        'cod1',
        'cod1',
        'cod1',
        'pr1',
        'cod1',
        'sv1',
        'sv1',
        'period1',
        'cod1',
        'cod1',
    )

    

    # переменные ФГУП "ВНИИМ ИМ. Д.И.МЕНДЕЛЕЕВА
    one = f'Заявка на проведение работ (оказание услуг) по поверке СИ'
    verificator_head_position = a.aqq.verificator.head_position
    verificator_companyName  = a.aqq.verificator.companyName 
    verificator_head_name = a.aqq.verificator.head_name 
    outgoing_number = f'Исх. № {nnow} от {gnow}'
    customer_card_number = f'№ учетной карточки {a.aqq.ver_agreement_card}'
    contract_request = f'Просим провести периодическую, первичную, после ремонта (нужное подчеркнуть) поверку / калибровку СИ, аттестацию ИО и иных работ (услуг) '\
    f'в области обеспечения единства измерений в соответствии с договором (гос. контрактом) № {a.aqq.ver_agreement_number} от {a.aqq.ver_agreement_date}.'
    payment_number = f'Если оплата была по предварительному счету обязательно указать номер счета и дату или номер платежного поручения________________________________'
    if a.aqq.public_agree:
        yesno = f'ДА   ☑     	НЕТ  ☐'
    else:
        yesno = f'ДА    ☐     	НЕТ ☑'
    if {a.aqq.ver_agreement_number}:
        nu = a.aqq.ver_agreement_number
    else:
        nu = '(указать номер договора)'
    dop_agree = f'Прошу ☐ оформить коммерческое предложение / ☐ заключить договор / ☐ выставить счет по договору {nu} /'\
    f'☐ выставить счет гарантийному письму за проведение поверки следующих средств измерений:'

    table_headers = ['№',
                     'Наименование, тип, модификация СИ /отдельные автономные блоки и др.',
                     'Год выпуска СИ',
                     'Рег. номер типа СИ /\n регистрационный номер эталона\n в ФИФ по ОЕИ',
                     'Идентификационный номер СИ 1)',
                     'Идентификационный номер СИ 1)',
                     'Метрологические характеристики\n (разряд, КТ, ПГ), предел\n (диапазон) измерений, каналы,\n компоненты и т.д',
                     'Объем поверки2)',
                     'СИ применяемое в качестве эталона',
                     'Вид поверки 3)',
                     'Поверка по результатам калибровки 4)',
                     'Оформить свидетельство о поверке',
                     'Выдать протокол поверки \n(кроме поверки по результатам калибровки)',
                     'Срок предоставления СИ (месяц, год)',
                     'Срочность выполнения 5)',
                     'Примечание',
                    ]

    footnote = '1) при отсутствии необходимости в публикации заводского номера в ФИФ по ОЕИ необходимо дополнительно указать инвентарный номер или другое буквенно-цифровое обозначение, который(ое) будет передан(о) в ФИФ по ОЕИ.\n'\
    '2) графа заполняется в случае поверки в сокращенном объеме.\n'\
    '3) периодическая – ПР; первичная – П.\n'\
    '4) в соответствии с Постановлением Правительства РФ от 2 апреля 2015 г. № 311 «Об утверждении Положения о признании результатов калибровки при поверке средств измерений'\
    'в сфере государственного регулирования обеспечения единства измерений».\n'\
    '5) по предварительному согласованию с подразделением-исполнителем (за доп. плату).'

    foot2 ='Заявитель подтверждает, что указанные в заявке средства измерений не входят в перечень средств измерений, периодическая поверка которых осуществляется только аккредитованными в установленном порядке'\
    'в области обеспечения единства измерений государственными региональными центрами метрологии, утвержденный постановлением Правительства Российской Федерации от 20 апреля 2010 г. № 250.'


    req = 'Реквизиты организации '
    cname =f'- полное и сокращенное наименование предприятия Заказчика: {company.name_big} ({company.name}) '
    inn_kpp = f'- {company.requisits}'
    contact_person = f'- Контактное лицо: {company.manager_name}'
    contact_phone = f'Контактный телефон: {company.manager_phone}'
    contact_email = f'Эл. почта: {company.manager_email}'
    blanc = "                          "
    signature = f'{company.direktor_position       }{blanc}__________________________________________{blanc}{       company.direktor_name}'
    signature2 = f'ФИО контактного лица: {company.manager_name          }{blanc}Телефон: {company.manager_phone          }	{blanc}	E-mail: {company.manager_email }	'
            
    row_num = 1
    columns = [f'{one}'
    ]
    ws.write(row_num, 1, columns[0], style_plain_noborder_bold)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 1
    columns = [f'В {verificator_companyName}'
    ]
    ws.write(row_num, len_sheet-4, columns[0], style_right_noborder)
    ws.merge(row_num, row_num, len_sheet-4, len_sheet-1)

    row_num += 2
    columns = [f'{outgoing_number}',
               f'От кого: {company.name}',               
    ]
    ws.write(row_num, 1, columns[0], style_left_noborder)
    ws.merge(row_num, row_num, 1, 4)
    ws.write(row_num, len_sheet-4, columns[1], style_right_noborder)
    ws.merge(row_num, row_num, len_sheet-4, len_sheet-1)

    row_num += 1
    columns = [f'Адрес места проведения работ по поверке (в случае выездной поверки): {company.adress_lab}'
    ]
    ws.write(row_num, 1, columns[0], style_left_noborder_bold)
    ws.merge(row_num, row_num, 1, len_sheet-1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 800


    row_num += 1
    columns = [f'Соглашение на передачу сведений о владельце СИ в ФИФ по ОЕИ {yesno}'
    ]
    ws.write(row_num, 1, columns[0], style_left_noborder_bold)
    ws.merge(row_num, row_num, 1, len_sheet-1)


    row_num += 1
    columns = [f'{dop_agree}'
    ]
    ws.write(row_num, 1, columns[0], style_plain_noborder)
    ws.merge(row_num, row_num, 1, len_sheet-1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 800
    
    row_num += 1
    for col_num in range(0, 2):
         ws.write(row_num, col_num + 1, table_headers[col_num], style_plain_border)
         ws.merge(row_num, row_num+1, col_num+1, col_num+1, style_plain_border)
    for col_num in range(2, 4):
         ws.write(row_num, col_num+1, table_headers[col_num], st90)
         ws.merge(row_num, row_num+1, col_num+1, col_num+1, st90)
    for col_num in range(4, 6):
         ws.write(row_num, 5, table_headers[4], style_plain_border)
         ws.merge(row_num, row_num, 5, 6, style_plain_border)
         ws.row(row_num).height_mismatch = True
         ws.row(row_num).height = 600
    for col_num in range(7, len(table_headers)+1):
        ws.write(row_num, col_num, table_headers[col_num-1], st90)
        ws.merge(row_num, row_num+1, col_num, col_num, st90)

    row_num += 1
    columns = [f'Заводской номер',
               f'Инвентарный\n или буквенно-\nцифровое\n обозначение',
    ]
    i=0
    for col_num in range(5, 7):
         ws.write(row_num, col_num, columns[i], st90)
         i +=1
       


    row_num += 1
    columns=[i for i in range(1,17)]
    for col_num in range(len(table_headers)):
         ws.write(row_num, col_num+1, columns[col_num], style_plain_border)

    for row in rows1:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num + 2, row[col_num], style_plain_border)
    for row in rows2:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num + 2, row[col_num], style_plain_border)
            
    a = row_num
    for col_num in range(1):
        for row_num in range(11, a + 1):
            ws.write(row_num, col_num+1, f'{row_num - 10}', style_plain_border)

    row_num += 1
    columns = [f'{footnote}'
    ]
    ws.write(row_num, 1, columns[0], style_left_border)
    ws.merge(row_num, row_num, 1, len_sheet-1, style_left_border)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 2000
    
    row_num += 1
    columns = [f'{foot2}'
    ]
    ws.write(row_num, 1, columns[0], style_left_noborder_italic)
    ws.merge(row_num, row_num, 1, len_sheet-1, style_left_noborder_italic)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 800

    row_num += 2
    columns = [f'Реквизиты организации согласно учётной карточке предприятия прилагаю.'
    ]
    ws.write(row_num, 1, columns[0], style_left_noborder_bold)
    ws.merge(row_num, row_num, 1, len_sheet-1)

    row_num += 2
    columns = [f'{signature}'
    ]
    ws.write(row_num, 1, columns[0], style_plain_noborder)
    ws.merge(row_num, row_num, 1, len_sheet-1) 

    row_num += 2
    columns = [f'{signature2}'
    ]
    ws.write(row_num, 1, columns[0], style_plain_noborder)
    ws.merge(row_num, row_num, 1, len_sheet-1) 

        
    wb.save(response)
    return response
