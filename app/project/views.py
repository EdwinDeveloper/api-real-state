"""
Views for the projects APIs
"""
from rest_framework import (
    viewsets,
    authentication,
    permissions,
    # mixins,
)
from rest_framework import (
    status
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import (
    Project,
    Company,
    Referral,
    Bonus,
    Investment
)

from project import serializers
from collections import OrderedDict


class ReferralViewSets(viewsets.ModelViewSet):
    """Referral serializer"""
    serializer_class = serializers.ReferralSerializer
    queryset = Referral.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retrieves projects for authentication user"""
        return self.queryset.all().order_by('-id')

    def perform_create(self, serializer):
        """Create a new Recipe"""
        serializer.save()

    # @action(methods=['POST'], detail=True, url_path='new-referral')
    # def new_referral(self, request, pk=None):
    #     """create a new referral"""
    #     try:
    #         objectSerializer = serializers.ReferralSerializer(data=request.data)
    #         if objectSerializer.is_valid():
    #             user = 
    #             return Response(status.HTTP_200_OK)
    #         return Response(objectSerializer.errors, status. HTTP_400_BAD_REQUEST)
    #     except:
    #         return Response(objectSerializer.errors, status. HTTP_400_BAD_REQUEST)


class BonusViewSets(viewsets.ModelViewSet):
    """View for manage bonuses APIs"""
    serializer_class = serializers.BonusSerializerAdmin
    queryset = Bonus.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


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

    # def list(self, request, *args, **kwargs):
    #     if request.method == 'GET':
    #         res = super(ProjectViewSets, self).list(request, *args, **kwargs)
    #         res.data = {"status": "success", "message": "all projects", "data": res.data}
    #         return res


class ProjectAdminViewSets(viewsets.ModelViewSet):
    """View for manage admin projects APIs"""
    serializer_class = serializers.ProjectAdminSerializer
    queryset = Project.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.method == 'GET':
            res = super(ProjectAdminViewSets, self).list(request, *args, **kwargs)
            res.data = {"status": "success", "message": "all projects", "data": res.data}
            return res


class CompanyViewSets(viewsets.ModelViewSet):
    """View for manage companies APIs"""

    serializer_class = serializers.CompanySerializerAdmin
    queryset = Company.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class InvestmentAdminViewSets(viewsets.ModelViewSet):
    """View for manage Investment APIs"""

    serializer_class = serializers.InvestmentManagementSerializer
    queryset = Investment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
