from django.urls import path
from playlists.views import FeaturedPlaylistListView, TVShowListView, MovieListView

urlpatterns = [
    path('movies/', MovieListView.as_view()),
    path('shows/', TVShowListView.as_view()),
    path('', FeaturedPlaylistListView.as_view())
]