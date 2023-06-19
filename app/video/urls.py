"""
URL mappings for the user API
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from video import views

router = DefaultRouter()  # We create a default router
router.register('video', views.YouTubeVideoViewSet)

app_name = 'video'

urlpatterns = [
    path('', include(router.urls)),
]
