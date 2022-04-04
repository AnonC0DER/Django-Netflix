from django.urls import path
from playlists.views import (
    PlaylistDetailView, MovieDetailView, 
    FeaturedPlaylistListView, TVShowListView, 
    MovieListView, TVShowDetailView,
    TVShowSeasonDetailView
)

'''
It's better to use IDs in big projects like Netflix.
Databases do really well with indexing integers.
'''

urlpatterns = [
    path('', FeaturedPlaylistListView.as_view()),
    path('media/<int:pk>/', PlaylistDetailView.as_view()),
    
    path('movies/', MovieListView.as_view()),
    path('movies/<slug:slug>/', MovieDetailView.as_view()),
    
    path('shows/', TVShowListView.as_view()),
    path('shows/<slug:slug>/', TVShowDetailView.as_view()),
    path('shows/<slug:slug>/seasons/', TVShowDetailView.as_view()),
    path('shows/<slug:showSlug>/seasons/<slug:seasonsSlug>/', TVShowSeasonDetailView.as_view()),
]