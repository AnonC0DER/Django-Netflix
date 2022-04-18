from django.urls import path
from ratings.views import rate_obj_view

urlpatterns = [
    path('object-rate/', rate_obj_view, name='obj-rate')
]