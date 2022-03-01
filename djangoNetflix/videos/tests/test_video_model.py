from django.test import TestCase
from django.utils import timezone
from videos.models import Video

class VideoModelTests(TestCase):
    '''Test video model'''

    def setUp(self):
        '''Run before each test'''
        Video.objects.create(title='This is a test title')
        Video.objects.create(
            title='This is a test title',
            state=Video.VideoStateOptions.PUBLISH
        )

    def test_valid_title(self):
        '''Testing valid title'''
        
        title = 'This is a test title'
        queryset = Video.objects.filter(title=title)

        self.assertTrue(queryset.exists())

    def test_created_count(self):
        '''Test there is only one video in database which created in setUp'''

        queryset = Video.objects.all()

        self.assertEqual(queryset.count(), 2)

    def test_draft_case(self):
        '''Test draft case works in videos'''
        queryset = Video.objects.filter(state=Video.VideoStateOptions.DRAFT)

        self.assertEqual(queryset.count(), 1)

    def test_publish_case(self):
        '''Test publish case works in videos'''
        queryset = Video.objects.filter(state=Video.VideoStateOptions.PUBLISH)
        now = timezone.now()
        published_queryset = Video.objects.filter(
            state=Video.VideoStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )

        self.assertTrue(published_queryset.exists())