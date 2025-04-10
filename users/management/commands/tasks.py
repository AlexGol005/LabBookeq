from datetime import timedelta, date, datetime

from django.core.management.base import BaseCommand

from users.models import *

now = date.today()
nowtime = datetime.today().isoformat()


class Command(BaseCommand):
    def take_rent(self):
      note_list = Company.objects.filter(payement_date=now)
      not_pay_i = []
      for i in note_list:
        if i.balance >=monthly_payment:
          CompanyBalanceChange.objects.create(company=i, reason='Автоматическое списание ежемесячного платежа', amount=-monthly_payment)
          i.payement_date = i.payement_date + timedelta(days=30)
          i.pay = True
          i.save()
        else:
          i.payement_date = i.payement_date + timedelta(days=1)
          i.pay = False
          not_pay_i.append(i)
          i.save()
        not_pay_companies = CompanyActiveEmployesLists.objects.filter(company__in=not_pay_i)     
        print('Автоматическое списание. Не оплачено {not_pay_companies}')


    def handle(self, *args, **options):
        self.take_rent()



    # def access_restriction(self):
    #   note_list = Company.objects.filter(pay=False)
    #   for i in note_list:
    #     instance=User.objects.get(pk=str)
    #     instance.is_active = False
    #     pass


