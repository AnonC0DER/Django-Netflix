from django.test import TestCase
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from django.db.utils import IntegrityError
from playlists.models import Playlist

class TaggedItemTestCase(TestCase):
    '''Tests to test TaggedItem model'''
    def setUp(self):
        ply_title = 'New title'
        self.ply_obj = Playlist.objects.create(title=ply_title)
        self.ply_obj2 = Playlist.objects.create(title=ply_title)
        self.ply_title = ply_title
        self.ply_obj.tags.add(TaggedItem(tag='new-tag'), bulk=False)
        self.ply_obj2.tags.add(TaggedItem(tag='new-tag'), bulk=False)
        
    def test_content_type_is_not_null(self):
        '''Test content type isn't null'''
        with self.assertRaises(IntegrityError):
            TaggedItem.objects.create()

    def test_create_via_content_type(self):
        '''Test creating a TaggedItem object via content type'''
        c_type = ContentType.objects.get(app_label='playlists', model='playlist')
        tag_a = TaggedItem.objects.create(
            content_type=c_type, 
            object_id=1,
            tag='new-tag'
        )
        tag_b = TaggedItem.objects.create(
            content_type=c_type, 
            object_id=100,
            tag='new-tag2'
        )

        self.assertIsNotNone(tag_a.pk)
        self.assertIsNotNone(tag_b.pk)

    def test_create_via_model_content_type(self):
        '''Test creating a TaggedItem object via model content type'''
        c_type = ContentType.objects.get_for_model(Playlist)
        tag_a = TaggedItem.objects.create(
            content_type=c_type, 
            object_id=1,
            tag='new-tag'
        )
    
        self.assertIsNotNone(tag_a.pk)

    def test_create_via_app_loader_content_type(self):
        '''Test creating a TaggedItem object via app loader content type'''
        PlaylistKlass = apps.get_model(app_label='playlists', model_name='Playlist')
        c_type = ContentType.objects.get_for_model(PlaylistKlass)
        tag_a = TaggedItem.objects.create(
            content_type=c_type, 
            object_id=1,
            tag='new-tag'
        )

        self.assertIsNotNone(tag_a.pk)

    def test_related_field(self):
        '''Test related field'''
        self.assertEqual(self.ply_obj.tags.count(), 1)
    
    def test_related_field_create(self):
        '''Test related field create'''
        self.ply_obj.tags.create(tag='another-new-tag')
        
        self.assertEqual(self.ply_obj.tags.count(), 2)
    
    def test_related_field_via_content_type(self):
        '''Test related field via content type'''
        c_type = ContentType.objects.get_for_model(Playlist)
        tag_qs = TaggedItem.objects.filter(
            content_type=c_type, 
            object_id=self.ply_obj.id,
        )

        self.assertEqual(tag_qs.count(), 1)
    
    def test_direct_obj_creation(self):
        '''Test direct pbject creation'''
        obj = self.ply_obj
        tag = TaggedItem.objects.create(
            content_object=obj,
            tag='another1'
        )

        self.assertIsNotNone(tag.pk)