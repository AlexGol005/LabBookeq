from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from setups.models import Order

class Command(BaseCommand):
    def handle(self, *args, **options):
			PeriodicTask.objects.create(
					name='Repeat',
					task='repeat_minus',
					interval=IntervalSchedule.objects.get(every=60, period='seconds'),
          start_time=timezone.now(),
				)
