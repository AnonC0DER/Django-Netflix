from django.urls import path
from playlists.views import FeaturedPlaylistListView, TVShowListView, MovieListView

'''
It's better to use IDs in big projects like Netflix.
Databases do really well with indexing integers.
'''

urlpatterns = [
    path('', FeaturedPlaylistListView.as_view()),
    path('media/<int:id>/', FeaturedPlaylistListView.as_view()),
    
    path('movies/', MovieListView.as_view()),
    path('movies/<slug:slug>/', MovieListView.as_view()),
    
    path('shows/', TVShowListView.as_view()),
    path('shows/<slug:slug>/', TVShowListView.as_view()),
    path('shows/<slug:slug>/seasons/', TVShowListView.as_view()),
    path('shows/<slug:showSlug>/seasons/<slug:seasonsSlug>/', TVShowListView.as_view()),
]