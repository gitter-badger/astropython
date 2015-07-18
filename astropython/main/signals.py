from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User,Group

@receiver(post_save,sender=User)
def add_to_preview(sender,instance,**kwargs):
    instance.groups.add(Group.objects.get(name="Preview Users"))

