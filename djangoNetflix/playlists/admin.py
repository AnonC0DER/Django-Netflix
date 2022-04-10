from django.contrib import admin
from tags.admin import TaggedItemInline
from playlists.models import PlaylistRelated, TVShowSeasonProxy, Playlist, PlaylistItem, TVShowProxy, MovieProxy

class MovieProxyAdmin(admin.ModelAdmin):
    list_display = ['title']
    fields = ['title', 'description', 'state', 'category', 'video', 'slug']
    class Meta:
        model = MovieProxy

    def get_queryset(self, request):
        return MovieProxy.objects.all()


class SeasonEpisodeInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0


class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    '''Playlist admin page'''
    inlines = [SeasonEpisodeInline]
    list_display = ['title', 'parent']
    class Meta:
        model = TVShowSeasonProxy
    
    def get_queryset(self, request):
        return TVShowSeasonProxy.objects.all()


class TVShowSeasonProxyInline(admin.TabularInline):
    model = TVShowSeasonProxy
    extra = 0
    fields = ['order', 'title', 'state']


class TVShowProxyAdmin(admin.ModelAdmin):
    '''Playlist admin page'''
    inlines = [TaggedItemInline, TVShowSeasonProxyInline]
    list_display = ['title']
    fields = ['title', 'description', 'state', 'category', 'video', 'slug']
    class Meta:
        model = TVShowProxy
    
    def get_queryset(self, request):
        return TVShowProxy.objects.all()


class PlaylistRelatedInline(admin.TabularInline):
    model = PlaylistRelated
    fk_name = 'playlist'
    extra = 0


class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0


class PlaylistAdmin(admin.ModelAdmin):
    '''Playlist admin page'''
    inlines = [PlaylistItemInline, PlaylistRelatedInline]
    fields = [
        'title',
        'description',
        'slug',
        'state',
        'active'
    ]

    class Meta:
        model = Playlist

    def get_queryset(self, request):
        return Playlist.objects.filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)

admin.site.register(TVShowProxy, TVShowProxyAdmin)
admin.site.register(TVShowSeasonProxy, TVShowSeasonProxyAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(MovieProxy, MovieProxyAdmin)