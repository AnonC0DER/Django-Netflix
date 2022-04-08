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
    
    def get_video_id(self):
        if not self.is_published:
            return None
        return self.video_id

    @property
    def is_published(self):
        if self.active is False:
            return False
            
        state = self.state
        if state == PublishStateOptions.PUBLISH:
            return True
        
        else:
            return False
    
    def get_playlist_ids(self):
        return list(self.playlist_featured.all().values_list('id', flat=True))


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