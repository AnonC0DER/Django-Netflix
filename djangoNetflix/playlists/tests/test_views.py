from urllib import response
from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from playlists.models import Playlist, TVShowProxy, MovieProxy
from videos.models import Video
from djangoNetflix.db.models import PublishStateOptions


class PlaylistViewTestCase(TestCase):
    '''Test Playlist viwes'''
    fixtures = ['projects']

    def test_queryset(self):
        '''Test queryset exists'''
        self.assertTrue(Playlist.objects.exists())

    def test_movies_count(self):
        '''Test movies count'''     
        qs = MovieProxy.objects.all()

        self.assertEqual(qs.count(), 1)
    
    def test_tv_shows_count(self):
        '''Test TV shows count'''     
        qs = TVShowProxy.objects.all()

        self.assertEqual(qs.count(), 1)
    
    def test_show_detail_view(self):
        '''Test show detail view'''
        show = TVShowProxy.objects.all().published().first()
        url = show.get_absolute_url()
        res = self.client.get(url)
        context = res.context
        obj = context['object']

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, f'{show.title}')
        self.assertIsNotNone(url)
        self.assertEqual(obj.id, show.id)
        
    def test_show_detail_redirect_view(self):
        '''Test TV show redirect url view'''
        show = TVShowProxy.objects.all().published().first()
        url = f'/shows/{show.slug}'
        response = self.client.get(url, follow=True)
        
        self.assertEqual(response.status_code, 200)

    def test_shows_list_view(self):
        '''Test show detail view'''
        shows_qs = TVShowProxy.objects.all().published()
        response = self.client.get('/shows/')
        context = response.context
        res_qs = context['object_list']

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(shows_qs.order_by('-timestamp'), res_qs.order_by('-timestamp'))

    def test_movie_detail_view(self):
        '''Test movie detail view'''
        movie = MovieProxy.objects.all().published().first()
        url = movie.get_absolute_url()
        response = self.client.get(url)
        context = response.context
        obj = context['object']

        self.assertIsNotNone(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'{movie.title}') 
        self.assertEqual(obj.id, movie.id)

    def test_movie_detail_redirect_view(self):
        '''Test movie redirect url view'''
        movie = MovieProxy.objects.all().published().first()
        url = f'/movies/{movie.slug}'
        response = self.client.get(url, follow=True)
        
        self.assertEqual(response.status_code, 200)

    def test_movies_list_view(self):
        '''Test movie detail view'''
        movies_qs = MovieProxy.objects.all().published()
        response = self.client.get('/movies/')
        context = response.context
        res_qs = context['object_list']

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(movies_qs.order_by('-timestamp'), res_qs.order_by('-timestamp'))

    def test_search_none_view(self):
        '''Test search nothing and get none'''
        res = self.client.get('/search/')
        ply_qs = Playlist.objects.none()
        context = res.context
        r_qs = context['object_list']

        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(ply_qs.order_by('-timestamp'), r_qs.order_by('-timestamp'))
        self.assertContains(res, 'Perform a search')
    
    def test_search_results_view(self):
        '''Test search a query and get result'''
        query = 'Action'
        res = self.client.get(f'/search/?q={query}')
        ply_qs = Playlist.objects.all().search(query=query)
        context = res.context
        r_qs = context['object_list']

        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(ply_qs.order_by('-timestamp'), r_qs.order_by('-timestamp'))
        self.assertContains(res, f'Searched for {query}')