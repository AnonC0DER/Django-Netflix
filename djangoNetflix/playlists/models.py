from django.db import models
from django.db.models import Avg, Max, Min, Q
from django.contrib.contenttypes.fields import GenericRelation
from djangoNetflix.db.models import PublishStateOptions
from videos.models import Video
from categories.models import Category
from tags.models import TaggedItem
from ratings.models import Rating


class PlaylistQuerySet(models.QuerySet):
    '''Filter publish Playlist queryset'''
    def published(self):
        return self.filter(
            state=PublishStateOptions.PUBLISH
        )
    
    def search(self, query=None):
        if query is None:
            return self.none()
        return self.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__title__icontains=query) |
            Q(category__slug__icontains=query) |
            Q(tags__tag__icontains=query) 
        ).distinct()
    
    def movie_or_show(self):
        return self.filter(
            Q(type=Playlist.PlaylistTypeChoices.MOVIE) |
            Q(type=Playlist.PlaylistTypeChoices.SHOW)
        )


class PlaylistManager(models.Manager):
    '''Custom model manager'''
    def get_queryset(self):
        # using=self._db -> use current database
        return PlaylistQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()
    
    def featured_playlists(self):
        return self.get_queryset().filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)
        

# class Featured(models.Model):
#     '''Featured model'''
#     playlists = models.ManyToManyField('Playlist', blank=True)



class Playlist(models.Model):
    '''Playlist model'''
    class PlaylistTypeChoices(models.TextChoices):
        '''Playlist type choices'''
        MOVIE = 'MOV', 'Movie'
        SHOW = 'TVS', 'TV Show'
        SEASON = 'SEA', 'Season'
        PLAYLIST = 'PLY', 'Playlist'

    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    related = models.ManyToManyField('self', blank=True, related_name='related', through='PlaylistRelated')
    category = models.ForeignKey(Category, related_name='playlists', blank=True, null=True, on_delete=models.SET_NULL)
    order = models.IntegerField(default=1)
    title = models.CharField(max_length=220)
    type = models.CharField(max_length=3, choices=PlaylistTypeChoices.choices, default=PlaylistTypeChoices.PLAYLIST)
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
    tags = GenericRelation(TaggedItem, related_query_name='playlist')
    ratings = GenericRelation(Rating, related_query_name='playlist')

    objects = PlaylistManager()

    def __str__(self):
        return self.title
    
    def get_related_items(self):
        return self.playlistrelated_set.all()
    
    def get_absolute_url(self):
        if self.is_movie:
            return f'/movies/{self.slug}/'
        
        if self.is_show:
            return f'/shows/{self.slug}/'
        
        if self.is_season and self.parent is not None:
            return f'/shows/{self.parent.slug}/seasons/{self.slug}/'
        
        return f'/playlists/{self.slug}/'
    
    @property
    def is_season(self):
        return self.type == self.PlaylistTypeChoices.SEASON
        
    @property
    def is_movie(self):
        return self.type == self.PlaylistTypeChoices.MOVIE
    
    @property
    def is_show(self):
        return self.type == self.PlaylistTypeChoices.SHOW

    def get_rating_avg(self):
        return Playlist.objects.filter(id=self.id).aggregate(average=Avg('ratings__value'))
    
    def get_rating_spread(self):
        return Playlist.objects.filter(id=self.id).aggregate(max=Max('ratings__value'), min=Min('ratings__value'))

    def get_short_display(self):
        return ''

    @property
    def is_published(self):
        return self.active
    
    def get_video_id(self):
        '''Get main video ID render video for users'''
        if self.video is None:
            return None
        return self.video.get_video_id()

    def get_clips(self):
        '''Get clips to render clips for users'''
        return self.playlistitem_set.all().published()


class MovieProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(type=Playlist.PlaylistTypeChoices.MOVIE)


class MovieProxy(Playlist):
    '''TV show proxy model'''
    objects = MovieProxyManager()
    
    def get_movie_id(self):
        '''Get movie ID render movie for users'''
        return self.get_video_id()

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.MOVIE
        super().save(*args, **kwargs)


class TVShowProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=True,
        type=Playlist.PlaylistTypeChoices.SHOW)


class TVShowProxy(Playlist):
    '''TV show proxy model'''
    objects = TVShowProxyManager()
    
    class Meta:
        verbose_name = 'TV Show'
        verbose_name_plural = 'TV Shows'
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.SHOW
        super().save(*args, **kwargs)
    
    @property
    def seasons(self):
        return self.playlist_set.published()

    def get_short_display(self):
        return f'{self.playlist_set.published().count()} Seasons'

    
class TVShowSeasonProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=False,
        type=Playlist.PlaylistTypeChoices.SEASON)


class TVShowSeasonProxy(Playlist):
    '''Season proxy model'''

    objects = TVShowSeasonProxyManager()
    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.SEASON
        super().save(*args, **kwargs)
    
    def get_season_trailer(self):
        '''Get episodes to render episodes for users'''
        return self.get_video_id()

    def get_episodes(self):
        '''Get episodes to render episodes for users'''
        return self.playlistitem_set.all().published()


class PlaylistItemQuerySet(models.QuerySet):
    '''Filter publish Playlist queryset'''
    def published(self):
        return self.filter(
            playlist__state=PublishStateOptions.PUBLISH,
            video__state=PublishStateOptions.PUBLISH
        )


class PlaylistItemManager(models.Manager):
    '''Custom model manager'''
    def get_queryset(self):
        # using=self._db -> use current database
        return PlaylistItemQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PlaylistItemManager()

    class Meta:
        ordering = ['order', '-timestamp']


def pr_limit_choices_to():
    return Q(type=Playlist.PlaylistTypeChoices.MOVIE) | Q(type=Playlist.PlaylistTypeChoices.SHOW)

class PlaylistRelated(models.Model):
    '''Playlist related model'''
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    related = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='related_item', limit_choices_to=pr_limit_choices_to)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)