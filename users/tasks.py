from celery import shared_task
from datetime import timedelta, date

from .models import monthly_payment, Company, CompanyBalanceChange

now = date.today()

@shared_task
def take_rent():
  note_list = Company.objects.filter(payement_date=now)
  for i in note_list:
    CompanyBalanceChange.objects.create(company=i, reason='Автоматическое списание ежемесячного платежа', amount=monthly_payment)
  return HttpResponse(note_list)
