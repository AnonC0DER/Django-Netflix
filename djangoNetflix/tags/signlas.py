from django.db.models.signals import pre_save
from django.dispatch import receiver
from tags.models import TaggedItem

@receiver(pre_save, sender=TaggedItem)
def lowercase_tag(sender, instance, *args, **kwargs):
    instance.tag = f'{instance.tag}'.lower()