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
from functstandart import get_dateformat
from users.models import Profile, Company

URL = 'equipment'
now = date.today()
from equipment.exel import get_affirmation, get_author




# Стили

size = 11

# обкновенные границы ячеек
b1 = Borders()
b1.left = 1
b1.right = 1
b1.top = 1
b1.bottom = 1

# a1 выравнивание по центру по горизонтали и по вертикали, обтекание wrap тип 1
a1 = Alignment()
a1.horz = Alignment.HORZ_CENTER
a1.vert = Alignment.VERT_CENTER
a1.wrap = 1


# style_plain_border обычные ячейки, с границами ячеек
style_plain_border = xlwt.XFStyle()
style_plain_border.font.name = 'Times New Roman'
style_plain_border.borders = b1
style_plain_border.alignment = a1
style_plain_border.font.height = 20 * size


def export_orderverification_xls(request, object_ids):
    '''представление для выгрузки списка на поверку'''
    company = Company.objects.get(userid=request.user.profile.userid)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="base.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('1', cell_overwrite_ok=True)
    q = object_ids[17:-3].split("', '")
    try:
        note = Equipment.objects.filter(id__in=q)
    except:
        note = Equipment.objects.filter(id=1)
    rows = note.values_list(
        'pk', )
    row_num = 1
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], style_plain_border)
    wb.save(response)
    return response
