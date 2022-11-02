"""
URL mapping for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()  # We create a default router
router.register('recipes', views.RecipeViewSets)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
# Above we create a new endpoint call recipes

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
