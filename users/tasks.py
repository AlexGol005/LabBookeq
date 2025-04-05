from celery import shared_task
from datetime import timedelta, date
from django.http import HttpResponse
from .models import monthly_payment, Company, CompanyBalanceChange

now = date.today()

@shared_task
def take_rent(request):
  note_list = Company.objects.filter(payement_date=now)
  note_all = Company.objects.all()
  note_all_list = []
  for j in note_all:
    note_all_list = note_all_list.append(1)
  for i in note_list:
    CompanyBalanceChange.objects.create(company=i, reason='Автоматическое списание ежемесячного платежа', amount=monthly_payment)
    i_list = i_list.append(i)
  return HttpResponse(f'123-{note_all_list}')
