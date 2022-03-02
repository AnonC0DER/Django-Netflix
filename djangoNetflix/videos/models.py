from django.db import models
from django.utils import timezone
from djangoNetflix.db.models import PublishStateOptions


class VideoQuerySet(models.QuerySet):
    '''Filter publish video queryset'''
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )


class VideoManager(models.Manager):
    '''Custom model manager'''
    def get_queryset(self):
        # using=self._db -> use current database
        return VideoQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()
        

class Video(models.Model):
    '''Video model'''
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True) # this-is-my-video
    video_id = models.CharField(max_length=220, unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices,
    default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    objects = VideoManager()

    def __str__(self):
        return self.title
    
    @property
    def is_published(self):
        return self.active


class VideoAllProxy(Video):
    '''Video proxy model, inherit from Video class'''

    class Meta:
        proxy = True
        verbose_name = 'All Video'
        verbose_name_plural = 'All Videos'


class VideoPublishedProxy(Video):
    '''Video proxy model, inherit from Video class'''

    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'