from django.db.models.signals import pre_save
from django.utils import timezone
from django.dispatch import receiver
from django.utils.text import slugify
from playlists import models


@receiver(pre_save, sender=models.Playlist)
def publish_state_pre_save(sender, instance, *args, **kwargs):
    '''Set publish_timestamp using pre_save signal'''
    is_publish = instance.state == models.PublishStateOptions.PUBLISH
    is_draft = instance.state == models.PublishStateOptions.DRAFT

    if is_publish and instance.publish_timestamp is None:
        instance.publish_timestamp = timezone.now()

    elif is_draft:
        instance.publish_timestamp = None


@receiver(pre_save, sender=models.Playlist)
def slugify_pre_save(sender, instance, *args, **kwargs):
    '''Set slug using pre_save signal'''
    title = instance.title
    slug = instance.slug

    if slug is None:
        instance.slug = slugify(title)