"""
Корневой модуль проекта LabJournaly.
Данный модуль exelbase.py содержит стили и функци для формирования документов exel с данными из базы данных сайта.
"""

from PIL import Image
from django.db.models import Value

# стили
import xlwt
from django.db.models.functions import Concat
from django.http import HttpResponse
from xlwt import Alignment, Borders

from equipment.models import CompanyCard, MeteorologicalParameters
from functstandart import get_dateformat
from main.models import AttestationJ

al10 = Alignment()
al10.horz = Alignment.HORZ_CENTER
al10.vert = Alignment.VERT_CENTER
al10.wrap = 1

al1 = Alignment()
al1.horz = Alignment.HORZ_CENTER
al1.vert = Alignment.VERT_CENTER

al2 = Alignment()
al2.horz = Alignment.HORZ_RIGHT
al2.vert = Alignment.VERT_CENTER

al20 = Alignment()
al20.horz = Alignment.HORZ_RIGHT
al20.vert = Alignment.VERT_CENTER
al20.wrap = 1

al3 = Alignment()
al3.horz = Alignment.HORZ_LEFT
al3.vert = Alignment.VERT_CENTER

b1 = Borders()
b1.left = 1
b1.right = 1
b1.top = 1
b1.bottom = 1

b2 = Borders()
b2.left = 6
b2.right = 6
b2.bottom = 6
b2.top = 6

# заголовки жирным шрифтом, с границами ячеек == style1
style_headers = xlwt.XFStyle()
style_headers.font.bold = True
style_headers.font.name = 'Times New Roman'
style_headers.font.height = 20 * 8
style_headers.borders = b1
style_headers.alignment = al10

# обычные ячейки, с границами ячеек == style2
style_plain = xlwt.XFStyle()
style_plain.font.name = 'Times New Roman'
style_plain.font.height = 20 * 8
style_plain.borders = b1
style_plain.alignment = al10

# обычные ячейки, с толстыми границами ячеек
style_plain_bb = style_plain
style_plain_bb.font.name = 'Times New Roman'
style_plain_bb.font.height = 20 * 8
style_plain_bb.borders = b2
style_plain_bb.alignment = al10

# обычные ячейки с датами, с границами ячеек == style3
style_date = xlwt.XFStyle()
style_date.font.name = 'Times New Roman'
style_date.font.height = 20 * 8
style_date.borders = b1
style_date.alignment = al10
style_date.num_format_str = 'DD.MM.YYYY г'

# обычные ячейки, с границами ячеек, c форматом чисел '0.00'  == style4
style_2dp = xlwt.XFStyle()
style_2dp.font.name = 'Times New Roman'
style_2dp.font.height = 20 * 8
style_2dp.borders = b1
style_2dp.alignment = al1
style_2dp.num_format_str = '0.00'

# обычные ячейки, с границами ячеек, c форматом чисел '0.00000'  == style5
style_5dp = xlwt.XFStyle()
style_5dp.font.name = 'Times New Roman'
style_5dp.font.height = 20 * 8
style_5dp.borders = b1
style_5dp.alignment = al1
style_5dp.num_format_str = '0.00000'

# обычные ячейки, с границами ячеек, c форматом чисел '0.0000'
style_4dp = xlwt.XFStyle()
style_4dp.font.name = 'Times New Roman'
style_4dp.font.height = 20 * 8
style_4dp.borders = b1
style_4dp.alignment = al1
style_4dp.num_format_str = '0.0000'

# обычные ячейки, без границ  == style6
style_plain_nobor = xlwt.XFStyle()
style_plain_nobor.font.name = 'Times New Roman'
style_plain_nobor.font.height = 20 * 8
style_plain_nobor.alignment = al10

# обычные ячейки, без границ, сдвинуто вправо  == style7
style_plain_nobor_r = xlwt.XFStyle()
style_plain_nobor_r.font.name = 'Times New Roman'
style_plain_nobor_r.font.height = 20 * 8
style_plain_nobor_r.alignment = al2

# обычные ячейки, без границ, сдвинуто влево
style_plain_nobor_l = xlwt.XFStyle()
style_plain_nobor_l.font.name = 'Times New Roman'
style_plain_nobor_l.font.height = 20 * 8
style_plain_nobor_l.alignment = al3

# обычные ячейки, без границ, сдвинуто влево, c датовым форматом
style_plain_nobor_l_date = xlwt.XFStyle()
style_plain_nobor_l_date.font.name = 'Times New Roman'
style_plain_nobor_l_date.font.height = 20 * 8
style_plain_nobor_l_date.alignment = al3
style_plain_nobor_l_date.num_format_str = 'DD.MM.YYYY г.'

# обычные ячейки, с границами, сдвинуто вправо  == style7
style_plain_r = xlwt.XFStyle()
style_plain_r.font.name = 'Times New Roman'
style_plain_r.font.height = 20 * 8
style_plain_r.alignment = al20

# выгружаем протоколы испытаний - 1 базовая функция


def export_protocolbase_xls(request, pk, MODEL, parameter, extrainfo, get_for_columns1, get_for_columns2,
                            conclusion, columns1, columns2):
    """представление для выгрузки протокола испытаний в ексель"""

    # формируем источники данных
    company = CompanyCard.objects.get(pk=1)
    note = MODEL.objects. \
        annotate(name_rm=Concat('name', Value(' п. '), 'lot')). \
        annotate(performer_rm=Concat('performer__profile__userposition', Value(' '), 'performer__username')). \
        annotate(equipment_set=Concat('equipment1__charakters__name',
                                      Value(' тип '), 'equipment1__charakters__typename',
                                      Value(', свидетельство о поверке № '), 'equipment1__newcertnumber',
                                      Value(' от '), 'equipment1__newdate',
                                      Value(' действительно до '), 'equipment1__newdatedead',
                                      Value('; \n'),
                                      'equipment2__charakters__name',
                                      Value(' тип '), 'equipment2__charakters__typename',
                                      Value(', свидетельство о поверке № '), 'equipment2__newcertnumber',
                                      Value(' от '), 'equipment2__newdate',
                                      Value(' действительно до '), 'equipment2__newdatedead',
                                      )). \
        annotate(equipment_set2=Concat('equipment3__charakters__name',
                                       Value(' тип '), 'equipment3__charakters__typename',
                                       Value(', свидетельство о поверке № '), 'equipment3__newcertnumber',
                                       Value(' от '), 'equipment3__newdate',
                                       Value(' действительно до '), 'equipment3__newdatedead',
                                       Value('; \n'),
                                       'equipment4__charakters__name',
                                       Value(' тип '), 'equipment4__charakters__typename',
                                       Value(', свидетельство о поверке № '), 'equipment4__newcertnumber',
                                       Value(' от '), 'equipment4__newdate',
                                       Value(' действительно до '), 'equipment4__newdatedead',
                                       )). \
        get(pk=pk)

    meteo = MeteorologicalParameters.objects. \
        annotate(equipment_meteo=Concat('equipment1__charakters__name',
                                        Value(' тип '), 'equipment1__charakters__typename',
                                        Value(', свидетельство о поверке № '), 'equipment1__newcertnumber',
                                        Value(' от '), 'equipment1__newdate',
                                        # Value(', '),
                                        Value(' действительно до '), 'equipment1__newdatedead',
                                        Value('; \n'),
                                        'equipment2__charakters__name',
                                        Value(' тип '), 'equipment2__charakters__typename',
                                        Value(', свидетельство о поверке № '), 'equipment2__newcertnumber',
                                        Value(' от '), 'equipment2__newdate',
                                        Value(' действительно до '), 'equipment2__newdatedead',
                                        )). \
        get(date__exact=note.date, roomnumber__roomnumber__exact=note.room)

    # создаем выгрузку
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{note.pk}_protocol.xls"'

    # добавляем книгу и страницу с названием
    wb = xlwt.Workbook()
    ws = wb.add_sheet('protocol', cell_overwrite_ok=True)

    # ширина столбцов
    ws.col(0).width = 400
    ws.col(1).width = 6000
    ws.col(2).width = 3500
    ws.col(3).width = 3500
    ws.col(4).width = 2700
    ws.col(5).width = 2700
    ws.col(6).width = 2700
    ws.col(7).width = 3900
    ws.col(8).width = 3900

    # логотип и колонтитулы
    Image.open(company.imglogoadress.path).convert("RGB").save('logo.bmp')
    ws.insert_bitmap('logo.bmp', 0, 2)
    sheet = wb.get_sheet(0)
    sheet.header_str = b'1/1'
    sheet.footer_str = b' '

    row_num = 3
    columns = [
        company.sertificat,
        company.sertificat,
        company.sertificat,
        company.sertificat,
        '',
        company.affirmationproduction,
        company.affirmationproduction,
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], style_plain_nobor)
        ws.merge(row_num, row_num, 0, 3, style_plain_nobor)
    for col_num in range(6, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain_nobor)
        ws.merge(row_num, row_num, 6, 7, style_plain_nobor)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 900

    row_num += 1
    columns = [
        '"___" _______ "20___"    ',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain_r)
        ws.merge(row_num, row_num, 0, 7, style_plain_r)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 400

    note.date = get_dateformat(note.date)

    row_num += 1
    columns = [
        f'ПРОТОКОЛ ИСПЫТАНИЙ № {note.pk} от {note.date} по {note.ndocument}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain_nobor)
        ws.merge(row_num, row_num, 0, 7, style_plain_nobor)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 400

    row_num += 1
    columns = [
        '1 Наименование объекта/образца испытаний:',
        '1 Наименование объекта/образца испытаний:',
        note.name_rm,
        note.name_rm,
        note.name_rm,
        note.name_rm,
        note.name_rm,
        note.name_rm,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.sowner == None:
        note.sowner = '-'

    row_num += 1
    columns = [
        '2 Изготовитель материала СО: ',
        '2 Изготовитель материала СО: ',
        note.sowner,
        note.sowner,
        note.sowner,
        note.sowner,
        note.sowner,
        note.sowner,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)

    row_num += 1
    columns = [
        '3 Испытатель: ',
        '3 Испытатель: ',
        note.performer_rm,
        note.performer_rm,
        note.performer_rm,
        note.performer_rm,
        note.performer_rm,
        note.performer_rm,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)

    row_num += 1
    columns = [
        '4 Идентификационные данные объектов/образцов:',
        '4 Идентификационные данные объектов/образцов: ',
        note.get_constit_display(),
        note.get_constit_display(),
        note.get_constit_display(),
        note.get_constit_display(),
        note.get_constit_display(),
        note.get_constit_display(),
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 1
    columns = [
        '5 Дата отбора проб:',
        '5 Дата отбора проб: ',
        note.date,
        note.date,
        note.date,
        note.date,
        note.date,
        note.date,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)

    row_num += 1
    columns = [
        '6 Дата и место проведения испытаний:',
        '6 Дата и место проведения испытаний: ',
        f'{note.date}, {company.adress}, ком. {note.room}',
        f'{note.date}, {company.adress}, ком. {note.room}',
        f'{note.date}, {company.adress}, ком. {note.room}',
        f'{note.date}, {company.adress}, ком. {note.room}',
        f'{note.date}, {company.adress}, ком. {note.room}',
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 1
    columns = [
        '7 Условия проведения измерений:',
        '7 Условия проведения измерений:',
        '',
        '',
        '',
        '',
        '',
        '',
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 1
    columns = [
        '7.1 Условия проведения \n измерений соответствуют требованиям рабочей \n эксплуатации средств измерений:',
        '7.1 Условия проведения \n измерений соответствуют требованиям рабочей \n эксплуатации средств измерений:',
        meteo.equipment_meteo,
        meteo.equipment_meteo,
        meteo.equipment_meteo,
        meteo.equipment_meteo,
        meteo.equipment_meteo,
        meteo.equipment_meteo,
    ]
    for col_num in range(0, 2):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 0, 1, style_plain)
    for col_num in range(0, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1000

    row_num += 1
    columns = [
        '7.2 Условия окружающей среды:',
        '7.2 Условия окружающей среды:',
        '',
        '',
        '',
        '',
        '',
        '',
    ]
    for col_num in range(0, 2):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 0, 1, style_plain)
    for col_num in range(0, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)

    row_num += 1
    columns = [
        'давление, кПа',
        'давление, кПа',
        meteo.pressure,
        meteo.pressure,
        meteo.pressure,
        meteo.pressure,
        meteo.pressure,
        meteo.pressure,
    ]
    for col_num in range(0, 2):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 0, 1, style_plain)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)

    row_num += 1
    columns = [
        'температура, °С',
        'температура, °С',
        meteo.temperature,
        meteo.temperature,
        meteo.temperature,
        meteo.temperature,
        meteo.temperature,
        meteo.temperature,
    ]
    for col_num in range(0, 2):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 0, 1, style_plain)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)

    row_num += 1
    columns = [
        'влажность, %',
        'влажность, %',
        meteo.humidity,
        meteo.humidity,
        meteo.humidity,
        meteo.humidity,
        meteo.humidity,
        meteo.humidity,
    ]
    for col_num in range(0, 2):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 0, 1, style_plain)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)

    row_num += 1
    columns = [
        '8 Измеряемый параметр: ',
        '8 Измеряемый параметр: ',
        parameter,
        parameter,
        parameter,
        parameter,
        parameter,
        parameter,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)

    row_num += 1
    columns = [
        '9 Метод измерений/методика \n измерений:  ',
        '9 Метод измерений/методика \n измерений:  ',
        note.get_ndocument_display(),
        note.get_ndocument_display(),
        note.get_ndocument_display(),
        note.get_ndocument_display(),
        note.get_ndocument_display(),
        note.get_ndocument_display(),
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 1
    columns = [
        '10 Средства измерений:  ',
        '10 Средства измерений:  ',
        note.equipment_set,
        note.equipment_set,
        note.equipment_set,
        note.equipment_set,
        note.equipment_set,
        note.equipment_set,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1000

    row_num += 1
    columns = [
        '  ',
        '  ',
        note.equipment_set2,
        note.equipment_set2,
        note.equipment_set2,
        note.equipment_set2,
        note.equipment_set2,
        note.equipment_set2,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1000

    row_num += 1
    columns = [
        '11 Обработка результатов испытаний:  ',
        '11 Обработка результатов испытаний:  ',
        f'В соответствии с {note.ndocument}',
        f'В соответствии с {note.ndocument}',
        f'В соответствии с {note.ndocument}',
        f'В соответствии с {note.ndocument}',
        f'В соответствии с {note.ndocument}',
        f'В соответствии с {note.ndocument}',
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 1
    columns = [
        '12 Результаты испытаний:  ',
        '12 Результаты испытаний:  ',
        'приведены в таблице 1  ',
        'приведены в таблице 1  ',
        'приведены в таблице 1  ',
        'приведены в таблице 1  ',
        'приведены в таблице 1  ',
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)

    row_num += 1
    columns = [
        'Таблица 1. Результаты испытаний  ',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain_nobor)
        ws.merge(row_num, row_num, 0, 7, style_plain_nobor)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 400

    row_num += 1
    columns11 = [] + columns1
    get_for_columns1(ws, row_num)

    row_num += 1
    columns22 = [] + columns2
    get_for_columns2(ws, row_num)

    row_num += 1
    columns = [
        'Дополнительные сведения: ',
        'Дополнительные сведения: ',
        extrainfo,
        extrainfo,
        extrainfo,
        extrainfo,
        extrainfo,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)

    row_num += 1
    columns = [
        'Выводы: ',
        'Выводы: ',
        conclusion,
        conclusion,
        conclusion,
        conclusion,
        conclusion,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 0, 1, style_plain)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 7, style_plain)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 800

    row_num += 1
    columns = [
        company.prohibitet
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain_bb)
        ws.merge(row_num, row_num, 0, 7, style_plain_bb)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1000

    row_num += 1
    columns = [
        f'Исполнитель {note.performer.profile.userposition} {note.performer.username}  ____________________',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain_nobor)
        ws.merge(row_num, row_num, 0, 7, style_plain_nobor)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 800

    # все записываем
    wb.save(response)
    return response

# блок функций: выгружаем страницы журналов измерений


def export_base_kinematicviscosity_xls(request, pk, MODEL):
    """кинематическая вязкость - выгрузка страницы журнала"""
    # источник данных
    note = MODEL.objects.get(pk=pk)

    # создаем выгрузку
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="viscosity_kin_str_{note.pk}.xls"'

    # добавляем книгу и страницу с названием
    wb = xlwt.Workbook(encoding='utf-8')
    nn = str(note.name)[:18]
    nl = str(note.lot)[:6]
    ws = wb.add_sheet(f'{nn}, п. {nl}, t {note.temperature}', cell_overwrite_ok=True)
    ws.header_str = b''
    ws.footer_str = b''

    # высота строк
    for i in range(0, 21):
        ws.row(i).height_mismatch = True
        ws.row(i).height = 600
    ws.row(21).height_mismatch = True
    ws.row(21).height = 800
    for i in range(22, 25):
        ws.row(i).height_mismatch = True
        ws.row(i).height = 600

    # ширина столбцов
    ws.col(0).width = 4100
    ws.col(1).width = 4100
    ws.col(2).width = 4100
    ws.col(5).width = 4100

    # строчка 1 и далее все строки последовательно
    row_num = 0
    columns = [
                 f'{AttestationJ.objects.get(id=1).name}_{note.date.year}'
               ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain_nobor_r)
        ws.merge(row_num, row_num, 0, 5, style_plain_nobor_r)

    row_num += 2
    columns = [
        'Дата измерения',
        'Название',
        'Номер партии',
        'Шифр',
        'Шифр',
        'Т, °C',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 800
        ws.merge(row_num, row_num, 3, 4, style_headers)

    row_num += 1
    columns = [
        note.date,
        note.name,
        note.lot,
        note.cipher,
        note.cipher,
        note.temperature,
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style_date)
    for col_num in range(1, 4):
        ws.write(row_num, col_num, columns[col_num], style_plain)
    for col_num in range(4, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_2dp)
        ws.merge(row_num, row_num, 3, 4, style_plain)

    row_num += 1
    columns = [
        f'Проведение испытаний по {note.ndocument}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 5, style_headers)

    row_num += 1
    columns = [
        '№ виск-ра',
        str(note.ViscosimeterNumber1),
        str(note.ViscosimeterNumber1),
        str(note.ViscosimeterNumber2),
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style_headers)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 1, 2, style_plain)
        ws.merge(row_num, row_num, 3, 5, style_plain)

    row_num += 1
    columns = [
        'Константа вискозиметра, мм2/с2',
        'К1',
        'К1',
        'К2',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(6, 7, 0, 0, style_headers)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 1, 2, style_plain)
        ws.merge(row_num, row_num, 3, 5, style_plain)

    row_num += 1
    columns = [
        'Константа вискозиметра, мм2/с2',
        note.Konstant1,
        note.Konstant1,
        note.Konstant2,
    ]
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 1, 2, style_plain)
        ws.merge(row_num, row_num, 3, 5, style_plain)

    row_num += 1
    columns = [
        'Время истечения 1',
        'τ11, мин',
        'τ11, с',
        'τ21, мин',
        'τ21, мин',
        'τ21, с',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, 9, 0, 0, style_headers)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 3, 4, style_headers)

    row_num += 1
    columns = [
        'Время истечения 1',
        f'{note.plustimeminK1T1}:{ note.plustimesekK1T1}',
        note.timeK1T1_sec,
        f'{note.plustimeminK2T1}:{ note.plustimesekK2T1}',
        f'{note.plustimeminK2T1}:{ note.plustimesekK2T1}',
        note.timeK2T1_sec,
    ]
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_2dp)
        ws.merge(row_num, row_num, 3, 4, style_2dp)

    row_num += 1
    columns = [
        'Время истечения 2',
        'τ12, мин',
        'τ12, с',
        'τ22, мин',
        'τ22, мин',
        'τ22, с',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, 11, 0, 0, style_headers)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 3, 4, style_headers)

    am21 = f'{note.plustimeminK1T2}:{note.plustimesekK1T2}'
    as21 = note.timeK1T2_sec
    am22 = f'{note.plustimeminK2T2}:{note.plustimesekK2T2}'
    as22 = note.timeK1T2_sec

    if not note.plustimeminK1T2 and not note.plustimesekK1T2:
        am21 = '-'
        as21 = '-'
    if not note.plustimeminK2T2 and not note.plustimesekK2T2:
        am22 = '-'
        as22 = '-'

    row_num += 1
    columns = [
        'Время истечения 2',
        am21,
        as21,
        am22,
        am22,
        as22,
    ]
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_2dp)
        ws.merge(row_num, row_num, 3, 4, style_2dp)

    row_num += 1
    columns = [
        'Время истечения среднее',
        'τ1(сред.), c',
        'τ2(сред.), c',
        'τ2(сред.), c',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(12, 13, 0, 0, style_headers)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 1, 2, style_plain)
        ws.merge(row_num, row_num, 3, 5, style_plain)

    row_num += 1
    columns = [
               'Время истечения среднее',
               note.timeK1_avg,
               note.timeK2_avg,
               note.timeK2_avg
               ]

    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_2dp)
        ws.merge(row_num, row_num, 1, 2, style_2dp)
        ws.merge(row_num, row_num, 3, 5, style_2dp)

    row_num += 1
    columns = [
        'Вязкость кинематическая  νi= Кi * τi',
        'ν1, мм2/с',
        'ν2, мм2/с',
        'ν2, мм2/с',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, 15, 0, 0, style_headers)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 1, 2, style_plain)
        ws.merge(row_num, row_num, 3, 5, style_plain)

    row_num += 1
    columns = [
        'Вязкость кинематическая  νi= Кi * τi',
        note.viscosity1,
        note.viscosity2,
        note.viscosity2,
    ]
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_5dp)
        ws.merge(row_num, row_num, 1, 2, style_5dp)
        ws.merge(row_num, row_num, 3, 5, style_5dp)

    row_num += 1
    columns = [
        'Обработка результатов'
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 5, style_headers)

    row_num += 1
    columns = [
        'νсред = (ν1 + ν2)/2',
        'νсред = (ν1 + ν2)/2',
        '(|ν1 - ν2|)/νсред) * 100%',
        '(|ν1 - ν2|)/νсред) * 100%',
        'Критерий приемлемости, r, %',
        'Критерий приемлемости, r, %',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 1, style_headers)
        ws.merge(row_num, row_num, 2, 3, style_headers)
        ws.merge(row_num, row_num, 4, 5, style_headers)

    row_num += 1
    columns = [
        note.viscosityAVG,
        note.viscosityAVG,
        note.accMeasurement,
        note.accMeasurement,
        note.kriteriy,
        note.kriteriy,
    ]
    for col_num in range(0, 2):
        ws.write(row_num, col_num, columns[col_num], style_5dp)
        ws.merge(row_num, row_num, 0, 1, style_5dp)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 2, 3, style_plain)
        ws.merge(row_num, row_num, 4, 5, style_plain)

    row_num += 1
    columns = [
        f'Результат измерений: {note.resultMeas}'
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 5, style_headers)

    row_num += 1
    columns = [
       'Фиксация результатов'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 5, style_headers)

    row_num += 1
    columns = [
        'ν мм2/с',
        'Предыдущее νпред, мм2/с',
        'Разница с νпред, %',
        'Состав пробы'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 3, 5, style_headers)

    note.result = str(note.result).replace('.', ',')
    note.oldresult = str(note.oldresult).replace('.', ',')

    if note.deltaoldresult == None:
        note.deltaoldresult = '-'
        note.oldresult = '-'

    row_num += 1
    columns = [
        note.result,
        note.oldresult,
        note.deltaoldresult,
        note.get_constit_display(),
        note.get_constit_display(),
        note.get_constit_display(),
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 3, 5, style_plain)

    row_num += 1
    columns = [
        'Исполнитель',
        'Исполнитель.',
        'Исполнитель',
        'ОТК',
        'ОТК',
        'ОТК',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 2, style_headers)
        ws.merge(row_num, row_num, 3, 5, style_headers)

    row_num += 1
    columns = [
        str(note.performer),
        str(note.performer),
        str(note.performer),
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 0, 2, style_plain)
        ws.merge(row_num, row_num, 3, 5, style_plain)

    row_num += 1
    columns = [
        f'Страница № {note.pk} ',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain_nobor_r)
        ws.merge(row_num, row_num, 0, 5, style_plain_nobor_r)

    wb.save(response)
    return response
