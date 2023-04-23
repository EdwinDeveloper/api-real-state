"""
URL mappings for the user API
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from user import views

router = DefaultRouter()  # We create a default router
router.register('set', views.UserViewSets)

app_name = 'user'


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    # path('user/', views.UserViewSets.as_view({'get': 'list'}), name='user')
    path('', include(router.urls)),
]
