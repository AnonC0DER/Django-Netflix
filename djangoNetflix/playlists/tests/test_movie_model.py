from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
from playlists.models import MovieProxy
from videos.models import Video
from djangoNetflix.db.models import PublishStateOptions

class MovieProxyTests(TestCase):
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
        '''Run before each test and create two movie objects'''
        self.create_videos()
        self.movie_title = 'This is a test title'
        self.movie_a = MovieProxy.objects.create(
            title=self.movie_title,
            video=self.video_a
        )
        self.movie_a_dup = MovieProxy.objects.create(
            title=self.movie_title,
            video=self.video_a
        )
        movie_b = MovieProxy.objects.create(
            title='This is a test title2',
            state=PublishStateOptions.PUBLISH,
            video=self.video_a,
        )
        self.published_items_count = 1
        movie_b.videos.set(self.v_qs)
        movie_b.save()
        self.movie_b = movie_b

    def test_movie_video_items(self):
        '''Test there's a foreign key connection'''
        self.assertEqual(self.movie_a.video, self.video_a)
    
    def test_movie_clip_items(self):
        '''Test movie clip items'''
        count = self.movie_b.videos.all().count()
        self.assertEqual(count, 3)
    
    def test_movies_slug_unique(self):
        '''Test movie_a obj slug and movie_a_dup slug are not the same (unique)'''
        self.assertNotEqual(self.movie_a.slug, self.movie_a_dup.slug)

    def test_slug_field(self):
        '''Test slug of objects are correct'''
        title = self.movie_title
        test_slug = slugify(title)

        self.assertEqual(test_slug, self.movie_a.slug)

    def test_valid_title(self):
        '''Testing valid title'''    
        title = self.movie_title
        queryset = MovieProxy.objects.filter(title=title)

        self.assertTrue(queryset.exists())

    def test_draft_case(self):
        '''Test draft case works in videos'''
        queryset = MovieProxy.objects.filter(state=PublishStateOptions.DRAFT)

        self.assertEqual(queryset.count(), 2)

    def test_publish_manager(self):
        '''Test publish manager'''
        published_queryset = MovieProxy.objects.all().published()
        published_queryset2 = MovieProxy.objects.published()

        self.assertTrue(published_queryset.exists())
        self.assertTrue(published_queryset.count(), published_queryset2.count())
        self.assertEqual(published_queryset.count(), self.published_items_count)