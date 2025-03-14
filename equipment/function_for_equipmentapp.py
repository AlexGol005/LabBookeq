"""
Модуль проекта LabJournal, приложение equipment.
Данный модуль .function_for_equipmentapp содержит функции для приложения equipment.
"""
from users.models import Company
from equipment.models import Equipment


def get_exnumber(request, have_exnumber):
    for_exnamber_tail = Company.objects.get(userid=request.user.profile.userid).pk
    try:
        a = Equipment.objects.filter(exnumber__startswith=have_exnumber).filter(pointer=request.user.profile.userid).last().exnumber
        b = int(str(a)[1:5]) + 1
        c = str(b).rjust(4, '0')
        d = str(have_exnumber) + c + '_' + str(for_exnamber_tail)
        exnumber = d
    except:
        exnumber =  str(have_exnumber) + '0001' + '_' + str(for_exnamber_tail)
    return exnumber
