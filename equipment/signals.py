from django.db.models.signals import post_save, post_init, pre_save
from django.dispatch import receiver

from .models import *



# @receiver(post_save, sender=CommentsEquipment)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Test.objects.create()




# @receiver(pre_save, sender=Equipment)
# def change_status_equipment_get_instance(sender, instance, **kwargs):
#   instance._previous_status = instance.status


# @receiver(post_save, sender=Equipment)
# def change_status_equipment(sender, instance, created,**kwargs):
#   if instance._previous_status != instance.status:
#     a = CommentsEquipment.objects.create(forNote = instance, note = 'поменяли статус')
#     a.save()
#     instance.save()



@receiver(post_init, sender=Equipment)
def lead_post_init(sender, instance, **kwargs):
  instance._previous_status = instance.status
 

@receiver(post_save, sender=Equipment, dispatch_uid="update_stock_count")
  def criar_slug(sender, instance, created,**kwargs):
    if instance._previous_status != instance.status:
      CommentsEquipment.objects.create(forNote = instance, note = 'поменяли статус')

      instance.save()




# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from .models import Profile


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()
        

