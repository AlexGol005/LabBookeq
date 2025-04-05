from django.http import HttpResponse
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .tasks import take_rent

def schedule_take_rent(request):
  interval, _ = IntervalSchedule.objects.get_or_create(every=600, period=IntervalSchedule.SECONDS)
  PeriodicTask.objects.get(interval=interval, name="Ежемесячная автооплата", task="users.tasks.take_rent")
  return HttpResponse(f'123-{a}-{b}-{c}')
  
