from datetime import timedelta, date, datetime
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from users.models import *

now = date.today()
nowtime = datetime.today().isoformat()


class Command(BaseCommand):
    def take_rent(self):
        note_list = Company.objects.filter(payement_date=now)
        not_pay_i = []
        pay_i = []
        for i in note_list:
            if i.balance >=monthly_payment:
                CompanyBalanceChange.objects.create(company=i, reason='Автоматическое списание ежемесячного платежа', amount=-monthly_payment)
                i.payement_date = i.payement_date + timedelta(days=30)
                i.pay = True
                pay_i.append(i)
                i.save()
            else:
                i.payement_date = i.payement_date + timedelta(days=1)
                i.pay = False
                not_pay_i.append(i)
                i.save() 
        not_pay_companies = CompanyActiveEmployesLists.objects.filter(company__in=not_pay_i)
        pay_companies = CompanyActiveEmployesLists.objects.filter(company__in=pay_i)
        for j in not_pay_companies:
            j.list_employees
            j_list = str(j.list_employees[-1:])
            j_list = j_list.split(", ")
            u = User.objects.filter(pk__in=j_list)
            for f in u:
                f.is_active = False
                f.save()
        for j in pay_companies:
            j.list_employees
            j_list = str(j.list_employees[-1:])
            j_list = j_list.split(", ")
            u = User.objects.filter(pk__in=j_list)
            for f in u:
                f.is_active = True
                f.save()
        print(f'Автоматическое списание. Не оплачено: {not_pay_i}. Оплачено: {pay_i}')


    def handle(self, *args, **options):
        self.take_rent()



    # def access_restriction(self):
    #   note_list = Company.objects.filter(pay=False)
    #   for i in note_list:
    #     instance=User.objects.get(pk=str)
    #     instance.is_active = False
    #     pass


