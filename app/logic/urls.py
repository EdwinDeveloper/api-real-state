"""
URL mapping for the logic app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()  # We create a default router

app_name = 'logic'

urlpatterns = [
    path('', include(router.urls)),
]