from celery import shared_task
from django_celery_beat.models import PeriodicTask
from datetime import timedelta, date
from .models import Company
now = date.today()

@shared_task(name="repeat_minus")
def repeat_order_make():
	order = Company.objects.filter(payement_date=now.date)
	task = PeriodicTask.objects.get(name='Repeat order {}'.format(order_id))
	task.enabled = False
	task.save()
