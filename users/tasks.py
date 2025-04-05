from celery import shared_task
from datetime import timedelta, date
from django.http import HttpResponse
from .models import monthly_payment, Company, CompanyBalanceChange
# request
now = date.today()

@shared_task
def take_rent():
  note_list = Company.objects.filter(payement_date=now)
  b = note_list.values_list('name')
  for i in note_list:
    if i.balance >=monthly_payment:
      CompanyBalanceChange.objects.create(company=i, reason='Автоматическое списание ежемесячного платежа', amount=-monthly_payment)
    else:
      i.pay = False
      i.save()
  # a = '???'
  # b = list(b)
  # return HttpResponse(f'123-{a}-{b}')
