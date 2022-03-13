from django.test import TestCase
from categories.models import Category
from playlists.models import Playlist

class CategoryTestCase(TestCase):
    '''Tests to test Category model'''

    def setUp(self):
        cat_a = Category.objects.create(title='Action')
        cat_b = Category.objects.create(title='Comedy', active=False)
        self.play_a = Playlist.objects.create(title='This is a test', category=cat_a)

        self.cat_a = cat_a
        self.cat_b = cat_b

    def test_is_active(self):
        '''Test cat_a object is active'''
        self.assertTrue(self.cat_a.active)

    def test_is_not_active(self):
        '''Test cat_a object is not active'''
        self.assertFalse(self.cat_b.active)

    def test_related_playlist(self):
        '''Test related playlist'''
        queryset = self.cat_a.playlists.all()

        self.assertEqual(queryset.count(), 1)