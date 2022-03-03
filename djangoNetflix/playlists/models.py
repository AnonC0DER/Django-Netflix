from django.db import models
from django.utils import timezone
from djangoNetflix.db.models import PublishStateOptions
from videos.models import Video

class PlaylistQuerySet(models.QuerySet):
    '''Filter publish Playlist queryset'''
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )


class PlaylistManager(models.Manager):
    '''Custom model manager'''
    def get_queryset(self):
        # using=self._db -> use current database
        return PlaylistQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()
        

class Playlist(models.Model):
    '''Playlist model'''
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True) # this-is-my-video
    video = models.ForeignKey(Video, null=True, on_delete=models.SET_NULL) # one video per playlist
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices,
    default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    objects = PlaylistManager()

    def __str__(self):
        return self.title
    
    @property
    def is_published(self):
        return self.active