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
    CommentsEquipment.objects.create(forNote = instance, note = 'поменяли статус', date = now)

