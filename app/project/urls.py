"""
URL mapping for the project app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from project import views


router = DefaultRouter()  # We create a default router
router.register('projects', views.ProjectViewSets)
router.register('projectsAdmin', views.ProjectAdminViewSets)
router.register('companies', views.CompanyViewSets)
router.register('referral', views.ReferralViewSets)
router.register('commission', views.CommissionViewSets)

app_name = 'project'

urlpatterns = [
    path('', include(router.urls)),
]
