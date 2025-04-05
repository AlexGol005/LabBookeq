from celery import shared_task
from datetime import timedelta, date
from django.http import HttpResponse
from .models import monthly_payment, Company, CompanyBalanceChange

now = date.today()

@shared_task
def take_rent(request):
  note_list = Company.objects.filter(payement_date=now)
  note_all_list = Company.objects.values_list('payement_date')
  for i in note_list:
    CompanyBalanceChange.objects.create(company=i, reason='Автоматическое списание ежемесячного платежа', amount=monthly_payment)
  return HttpResponse(f'123-{note_all_list}')
