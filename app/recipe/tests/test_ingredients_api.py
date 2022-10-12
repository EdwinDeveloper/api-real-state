"""
Tests for the ingredients API
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def create_user(email='edwindeveloper@outlook.com', password='test123'):
    """Create and return user"""
    return get_user_model().objects.create_user(email=email, password=password)



