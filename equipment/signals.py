from django.db.models.signals import post_save, post_init
from django.dispatch import receiver

from .models import *


@receiver(post_init, sender=Equipment)
def change_status_equipment_get_instance(sender, instance, **kwargs):
  instance._previous_equipment = instance.equipment


@receiver(post_save, sender=Equipment)
def change_status_equipment(sender, instance, updated,**kwargs):
  if instance._previous_equipment.status != instance.equipment.status:
    a = CommentsEquipment.objects.create(forNote = instance, note = 'поменяли статус')
    a.save()
    instance.save()


# @receiver(pre_save, sender=Equipment)
# def create_comm(sender, instance, updated, **kwargs):
#     if updated:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_comm(sender, instance, **kwargs):
#     instance.profile.save()
        

