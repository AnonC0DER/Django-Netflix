from django.db.models.signals import pre_save
from django.utils import timezone
from django.dispatch import receiver
from djangoNetflix.db.utils import get_unique_slug
from playlists import models
from categories.models import Category


@receiver(pre_save, sender=models.Playlist)
@receiver(pre_save, sender=models.MovieProxy)
@receiver(pre_save, sender=models.TVShowSeasonProxy)
@receiver(pre_save, sender=models.TVShowProxy)
def publish_state_pre_save(sender, instance, *args, **kwargs):
    '''Set publish_timestamp using pre_save signal'''
    is_publish = instance.state == models.PublishStateOptions.PUBLISH
    is_draft = instance.state == models.PublishStateOptions.DRAFT

    if is_publish and instance.publish_timestamp is None:
        instance.publish_timestamp = timezone.now()

    elif is_draft:
        instance.publish_timestamp = None


@receiver(pre_save, sender=models.Playlist)
@receiver(pre_save, sender=models.MovieProxy)
@receiver(pre_save, sender=models.TVShowSeasonProxy)
@receiver(pre_save, sender=models.TVShowProxy)
@receiver(pre_save, sender=Category)
def unique_slugify_pre_save(sender, instance, *args, **kwargs):
    '''Set slug using pre_save signal'''
    slug = instance.slug

    if slug is None:
        instance.slug = get_unique_slug(instance, size=5)