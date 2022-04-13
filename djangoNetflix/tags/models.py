from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class TaggedItemManager(models.Manager):
    def unique_list(self):
        tags_set = set(self.get_queryset().values_list('tag', flat=True))
        tags_list = sorted(list(tags_set))
        return tags_list
        

class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = TaggedItemManager()

    @property
    def slug(self):
        return self.tag

    # def get_related_object(self):
    #     Klass = self.content_type.model_class()
    #     return Klass.object.get(id=self.object_id)