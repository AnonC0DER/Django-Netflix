from django.contrib import admin
from videos import models


class VideoAllAdmin(admin.ModelAdmin):
    '''Customize what inside of the VideoAdmin'''

    list_display =  ['title', 'video_id']
    search_fields = ['title']
    # list_filter =  ['video_id']
    
    class Meta:
        model = models.VideoAllProxy


class VideoPublishedProxyAdmin(admin.ModelAdmin):
    '''Customize what inside of the VideoProxyAdmin'''

    list_display =  ['title', 'video_id']
    search_fields = ['title']
    # list_filter =  ['video_id']
    
    class Meta:
        model = models.VideoPublishedProxy
    
    def get_queryset(self, request):
        return models.VideoPublishedProxy.objects.filter(active=True)


admin.site.register(models.VideoAllProxy, VideoAllAdmin)
admin.site.register(models.VideoPublishedProxy, VideoPublishedProxyAdmin)