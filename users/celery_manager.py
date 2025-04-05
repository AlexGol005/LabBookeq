from django.http import HttpResponse
from django_celery_beat.models import PeriodicTask, IntervalScedule
from .tasks import take_rent

def schedule_take_rent(request):
  interval, _ = IntervalScedule.objects.get_or_create(every=600, period=IntervalScedule.SECONDS)
  PeriodicTask.objects.create(interval=interval, name="Ежемесячная автооплата", task="users.tasks.take_rent")
  return HttpResponse(f'123-{a}-{b}-{c}')
  
