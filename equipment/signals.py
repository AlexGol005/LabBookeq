from django.db.models.signals import post_save, post_init, pre_save
from django.dispatch import receiver
from datetime import date

from .models import *

now = date.today()

@receiver(post_init, sender=Equipment)
def lead_post_init(sender, instance, **kwargs):
  instance._previous_status = instance.status
 

@receiver(post_save, sender=Equipment, dispatch_uid="update_stock_count")
def criar_slug(sender, instance, created,**kwargs):
  if instance._previous_status != instance.status:
    if instance.status == 'Э':
      CommentsEquipment.objects.create(forNote = instance, note = 'Оборудование введено в эксплуатацию', date = now, type = 'добавлена автоматически при изменении статуса')
    if instance.status == 'РЕ':
      CommentsEquipment.objects.create(forNote = instance, note = 'Отправлено в ремонт', date = now, type = 'добавлена автоматически при изменении статуса')
    if instance.status == 'С':
      CommentsEquipment.objects.create(forNote = instance, note = 'Списано', date = now, type = 'добавлена автоматически при изменении статуса')
    if instance.status == 'Р':
      CommentsEquipment.objects.create(forNote = instance, note = 'Отправлено на резервное хранение', date = now, type = 'добавлена автоматически при изменении статуса')

