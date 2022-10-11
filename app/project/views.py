"""
Views for the projects APIs
"""
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Project,
)

from project import serializers


class ProjectViewSets(viewsets.ModelViewSet):
    """View for manage project APIs"""
    serializer_class = serializers.ProjectSerializer
    queryset = Project.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieves projects for authentication user"""
        return self.queryset.all().order_by('-id')
    
    def perform_create(self, serializer):
        """Create a new Recipe"""
        serializer.save()