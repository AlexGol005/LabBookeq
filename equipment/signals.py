from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_init, sender=Equipment)
def change_status_equipment_get_instance(sender, instance, **kwargs):
  instance._previous_equipment = instance.equipment


@receiver(post_save, sender=Equipment)
def change_status_equipment(sender, instance, updated,**kwargs):
  if instance._previous_equipment.status != instance.equipment.status:
    a = CommentsEquipment.objects.get(forNote = instance)
    a.note = 'поменяли статус'
    a.save()
    instance.save()
        

