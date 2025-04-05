from celery import shared_task
from datetime import timedelta, date
from django.http import HttpResponse
from .models import monthly_payment, Company, CompanyBalanceChange

now = date.today()

@shared_task
def take_rent(request):
  note_list = Company.objects.filter(payement_date=now)
  # note_list = Company.objects.all()
  i_list = []
  for i in note_list:
    CompanyBalanceChange.objects.create(company=i, reason='Автоматическое списание ежемесячного платежа', amount=monthly_payment)
    i_list = i_list.append(i)
  return HttpResponse(f'123-{i_list}')
