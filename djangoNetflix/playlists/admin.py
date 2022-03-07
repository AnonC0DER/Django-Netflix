from django.contrib import admin
from playlists.models import Playlist, PlaylistItem

class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0

class PlaylistAdmin(admin.ModelAdmin):
    '''Playlist admin page'''
    inlines = [PlaylistItemInline]
    class Meta:
        model = Playlist

admin.site.register(Playlist, PlaylistAdmin)