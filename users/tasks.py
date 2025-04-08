# from celery import shared_task
from datetime import timedelta, date, datetime
from django.http import HttpResponse

import sys
sys.path.append('/home/LabJournal/LabBookeq/users')

from users.models import monthly_payment, Company, CompanyBalanceChange
# request
now = date.today()

nowtime = datetime.today().isoformat()

# @shared_task
def take_rent():
  note_list = Company.objects.filter(payement_date=now)
  for i in note_list:
    if i.balance >=monthly_payment:
      CompanyBalanceChange.objects.create(company=i, reason='Автоматическое списание ежемесячного платежа', amount=-monthly_payment)
      i.payement_date = i.payement_date + timedelta(days=30)
      i.pay = True
      i.save()
    else:
      i.payement_date = i.payement_date + timedelta(days=1)
      i.pay = False
      i.save()

take_rent()
