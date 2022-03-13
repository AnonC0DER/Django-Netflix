from django.contrib import admin
from playlists.models import TVShowSeasonProxy, Playlist, PlaylistItem, TVShowProxy, MovieProxy

class MovieProxyAdmin(admin.ModelAdmin):
    list_display = ['title']
    fields = ['title', 'description', 'state', 'video', 'slug']
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
    inlines = [TVShowSeasonProxyInline]
    list_display = ['title']
    fields = ['title', 'description', 'state', 'video', 'slug']
    class Meta:
        model = TVShowProxy
    
    def get_queryset(self, request):
        return TVShowProxy.objects.all()


class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0


class PlaylistAdmin(admin.ModelAdmin):
    '''Playlist admin page'''
    inlines = [PlaylistItemInline]
    class Meta:
        model = Playlist

    def get_queryset(self, request):
        return Playlist.objects.filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)

admin.site.register(TVShowProxy, TVShowProxyAdmin)
admin.site.register(TVShowSeasonProxy, TVShowSeasonProxyAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(MovieProxy, MovieProxyAdmin)