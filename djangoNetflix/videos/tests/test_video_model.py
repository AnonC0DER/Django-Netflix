from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
from videos.models import Video
from djangoNetflix.db.models import PublishStateOptions

class VideoModelTests(TestCase):
    '''Test video model'''

    def setUp(self):
        '''Run before each test and create two Video objects'''
        self.obj_a = Video.objects.create(
            title='This is a test title',
            video_id='abc'
        )
        self.obj_b = Video.objects.create(
            title='This is a test title2',
            state=PublishStateOptions.PUBLISH,
            video_id='abcd'
        )

    def test_slug_field(self):
        '''Test slug of objects are correct'''
        title = self.obj_a.title
        test_slug = slugify(title)

        self.assertEqual(test_slug, self.obj_a.slug)

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
        queryset = Video.objects.filter(state=PublishStateOptions.DRAFT)

        self.assertEqual(queryset.count(), 1)
    
    def test_draft_case_2(self):
        '''Test draft case works in videos'''
        obj = Video.objects.filter(state=PublishStateOptions.DRAFT).first()

        self.assertFalse(obj.is_published)

    def test_publish_case(self):
        '''Test publish case works in videos'''
        now = timezone.now()
        published_queryset = Video.objects.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )

        self.assertTrue(published_queryset.exists())
    
    def test_publish_case_2(self):
        '''Test publish case works in videos'''
        obj = Video.objects.filter(state=PublishStateOptions.PUBLISH).first()

        self.assertTrue(obj.is_published)

    def test_publish_manager(self):
        published_queryset = Video.objects.all().published()
        published_queryset2 = Video.objects.published()

        self.assertTrue(published_queryset.exists())
        self.assertTrue(published_queryset.count(), published_queryset2.count())