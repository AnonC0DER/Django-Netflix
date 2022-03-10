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
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    order = models.IntegerField(default=1)
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True) # this-is-my-video
    video = models.ForeignKey(Video, null=True, blank=True, on_delete=models.SET_NULL, related_name='playlist_featured') # one video per playlist
    videos = models.ManyToManyField(Video, blank=True, related_name='playlist_item', through='PlaylistItem')
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


class TVShowProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=True)


class TVShowProxy(Playlist):
    '''TV show proxy model'''
    objects = TVShowProxyManager()
    
    class Meta:
        verbose_name = 'TV Show'
        verbose_name_plural = 'TV Shows'
        proxy = True


class TVShowSeasonProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=False)


class TVShowSeasonProxy(Playlist):
    '''Season proxy model'''

    objects = TVShowSeasonProxyManager()
    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'
        proxy = True


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-timestamp']