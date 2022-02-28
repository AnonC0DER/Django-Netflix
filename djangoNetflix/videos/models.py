from django.db import models

class Video(models.Model):
    '''Video model'''
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True) # this-is-my-video
    video_id = models.CharField(max_length=220)
    active = models.BooleanField(default=True)
    # timestamp
    # update
    # state
    # publish_timestamp

    def __str__(self):
        return self.title
    
    @property
    def is_published(self):
        return self.active


class VideoAllProxy(Video):
    '''Video proxy model, inherit from Video class'''

    class Meta:
        proxy = True
        verbose_name = 'All Video'
        verbose_name_plural = 'All Videos'


class VideoPublishedProxy(Video):
    '''Video proxy model, inherit from Video class'''

    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'