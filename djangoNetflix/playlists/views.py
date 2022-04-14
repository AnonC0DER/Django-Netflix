from django.http import Http404
from django.utils import timezone
from django.views.generic import ListView, DetailView
from playlists.models import Playlist, MovieProxy, TVShowProxy, TVShowSeasonProxy
from djangoNetflix.db.models import PublishStateOptions 
from playlists.mixins import PlaylistMixin


class SearchView(PlaylistMixin, ListView):
    def get_context_data(self):
        query = self.request.GET.get('q')
        context = super().get_context_data()
        if query is not None:
            context['title'] = f'Searched for {query}'
        
        else:
            context['title'] = 'Perform a search'

        return context


    def get_queryset(self):
        query = self.request.GET.get('q')
        return Playlist.objects.all().movie_or_show().published().search(query=query)


class PlaylistDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/playlist_detail.html'
    queryset = Playlist.objects.all()

    # def get_object(self):
    #     request = self.request
    #     kwargs = self.kwargs
    #     print(request, kwargs)
    #     return self.get_queryset().filter(**kwargs).first()


class MovieListView(PlaylistMixin, ListView):
    queryset = MovieProxy.objects.all()
    title = 'Movies'


class MovieDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/movie_detail.html'
    queryset = MovieProxy.objects.all()


class TVShowListView(PlaylistMixin, ListView):
    queryset = TVShowProxy.objects.all()
    title = 'TVShows'


class TVShowDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/tvshow_detail.html'
    queryset = TVShowProxy.objects.all()

    
class TVShowSeasonDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/season_detail.html'
    queryset = TVShowSeasonProxy.objects.all()

    def get_object(self):
        kwargs = self.kwargs
        show_slug = kwargs.get('showSlug')
        season_slug = kwargs.get('seasonSlug')
        now = timezone.now()
        try:
            obj = TVShowSeasonProxy.objects.get(
                state=PublishStateOptions.PUBLISH,
                publish_timestamp__lte=now,
                parent__slug__iexact=show_slug,
                slug__iexact=season_slug
            )
        except TVShowSeasonProxy.MultipleObjectsReturned:
            qs = TVShowSeasonProxy.objects.filter(
                parent__slug__iexact=show_slug,
                slug__iexact=season_slug
            ).published()
            obj = qs.first()
        except:
            raise Http404

        return obj


class FeaturedPlaylistListView(PlaylistMixin, ListView):
    template_name = 'playlists/featured_list.html'
    queryset = Playlist.objects.featured_playlists()
    title = 'Featured'

    