from django.test import TestCase
from videos.models import Video


class VideoModelTests(TestCase):
    '''Test video model'''

    def setUp(self):
        '''Run before each test'''
        
        Video.objects.create(title='This is a test title')

    def test_valid_title(self):
        '''Testing valid title'''
        
        title = 'This is a test title'
        queryset = Video.objects.filter(title=title)

        self.assertTrue(queryset.exists())

    def test_created_count(self):
        '''Test there is only one video in database which created in setUp'''

        queryset = Video.objects.all()

        self.assertEqual(queryset.count(), 1)