from django.db.models.signals import post_save 
from django.dispatch import receiver 
from ratings.models import Rating


@receiver(post_save, sender=Rating)
def rating_post_save(sender, instance, created, *args, **kwargs):
    '''if the rating obj is already exists delete will be deleted'''
    if created:
        # triggger new content_object calculation
        content_type = instance.content_type
        user = instance.user
        qs = Rating.objects.filter(user=user, content_type=content_type, object_id=instance.object_id).exclude(pk=instance.pk)

        if qs.exists():
            qs.delete()