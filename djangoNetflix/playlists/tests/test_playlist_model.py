from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
from playlists.models import Playlist
from videos.models import Video
from djangoNetflix.db.models import PublishStateOptions

class PlaylistModelTests(TestCase):
    '''Test video model'''

    def setUp(self):
        '''Run before each test and create two Playlist objects'''
        video_a = Video.objects.create(title='My title', video_id='abc123')
        self.video_a = video_a

        self.obj_a = Playlist.objects.create(
            title='This is a test title',
            video=video_a
        )
        self.obj_b = Playlist.objects.create(
            title='This is a test title2',
            state=PublishStateOptions.PUBLISH,
            video=video_a
        )

    def test_playlist_video(self):
        '''Test there's a foreign key connection'''
        self.assertEqual(self.obj_a.video, self.video_a)

    def test_video_playlist(self):
        '''Test there's a foreign key connection'''
        queryset = self.video_a.playlist_set.all()
        
        self.assertEqual(queryset.count(), 2)

    def test_slug_field(self):
        '''Test slug of objects are correct'''
        title = self.obj_a.title
        test_slug = slugify(title)

        self.assertEqual(test_slug, self.obj_a.slug)

    def test_valid_title(self):
        '''Testing valid title'''
        
        title = 'This is a test title'
        queryset = Playlist.objects.filter(title=title)

        self.assertTrue(queryset.exists())

    def test_created_count(self):
        '''Test there is only one video in database which created in setUp'''

        queryset = Playlist.objects.all()

        self.assertEqual(queryset.count(), 2)

    def test_draft_case(self):
        '''Test draft case works in videos'''
        queryset = Playlist.objects.filter(state=PublishStateOptions.DRAFT)

        self.assertEqual(queryset.count(), 1)

    def test_publish_case(self):
        '''Test publish case works in videos'''
        queryset = Playlist.objects.filter(state=PublishStateOptions.PUBLISH)
        now = timezone.now()
        published_queryset = Playlist.objects.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )

        self.assertTrue(published_queryset.exists())
    
    def test_publish_manager(self):
        published_queryset = Playlist.objects.all().published()
        published_queryset2 = Playlist.objects.published()

        self.assertTrue(published_queryset.exists())
        self.assertTrue(published_queryset.count(), published_queryset2.count())