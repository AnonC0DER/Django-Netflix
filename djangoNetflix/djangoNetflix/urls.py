from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('playlists.urls')),
    path('category/', include('categories.urls')),
    path('categories/', include('categories.urls')),
]
