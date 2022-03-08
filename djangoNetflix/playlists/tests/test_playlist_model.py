from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
from playlists.models import Playlist
from videos.models import Video
from djangoNetflix.db.models import PublishStateOptions

class PlaylistModelTests(TestCase):
    '''Test video model'''
    def create_videos(self):
        '''Create sample video objects'''
        video_a = Video.objects.create(title='My title', video_id='abc123')
        video_b = Video.objects.create(title='My title', video_id='abc1234')
        video_c = Video.objects.create(title='My title', video_id='abc1235')
        
        self.video_a = video_a
        self.video_b = video_b
        self.video_c = video_c
        self.v_qs = Video.objects.all()

    def setUp(self):
        '''Run before each test and create two Playlist objects'''
        self.create_videos()
        
        self.obj_a = Playlist.objects.create(
            title='This is a test title',
            video=self.video_a
        )
        obj_b = Playlist.objects.create(
            title='This is a test title2',
            state=PublishStateOptions.PUBLISH,
            video=self.video_a,
        )
        obj_b.videos.set(self.v_qs)
        obj_b.save()
        self.obj_b = obj_b

    def test_playlist_video_items(self):
        '''Test there's a foreign key connection'''
        self.assertEqual(self.obj_a.video, self.video_a)
    
    def test_playlist_video_through_model(self):
        '''Test playlist video through model'''
        v_qs = sorted(list(self.v_qs.values_list('id')))
        video_qs = sorted(list(self.obj_b.videos.all().values_list('id')))
        playlist_item_qs = sorted(list(self.obj_b.playlistitem_set.all().values_list('video')))

        self.assertEqual(v_qs, video_qs, playlist_item_qs)

    def test_playlist_video(self):
        '''Test playlist video items'''
        count = self.obj_b.videos.all().count()
        
        self.assertEqual(count, 3)

    def test_video_playlist_ids_propery(self):
        '''Test video playlist ids'''
        ids = self.obj_a.video.get_playlist_ids()
        actual_ids = list(Playlist.objects.filter(video=self.video_a).values_list('id', flat=True))

        self.assertEqual(ids, actual_ids)

    def test_video_playlist(self):
        '''Test there's a foreign key connection'''
        queryset = self.video_a.playlist_featured.all()
        
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