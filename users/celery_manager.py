# from django.http import HttpResponse
# from datetime import timedelta, date, datetime
# from django_celery_beat.models import PeriodicTask, IntervalSchedule
# from .tasks import take_rent
# nowtime = datetime.today().isoformat()

# def schedule_take_rent(request):
#   # http://www.journallabeq.ru/celerytest2/
#   a=0
#   interval, _ = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)
#   PeriodicTask.objects.get_or_create(interval=interval, name="Ежемесячная автооплата 10", task="users.tasks.take_rent")
#   a+=1
#   b = nowtime
#   return HttpResponse(f'123-{a}--{b}')
  
