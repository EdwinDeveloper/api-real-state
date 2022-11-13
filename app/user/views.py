"""
Views for the user API
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import (
    generics, authentication, permissions, mixins, viewsets, status
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from rest_framework.response import Response

from user.serializers import (
    UserSerializer,
    UserSetInvestmentSerializer,
    AuthTokenSerializer,
)
from core.models import (
    User,
    Project,
)


class CreateUserView(
    generics.CreateAPIView,
    mixins.UpdateModelMixin,
):
    """Create a new user in the system"""
    serializer_class = UserSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'investmentsw',
                OpenApiTypes.STR,
                description='Adding a new investment to an user'
            )
        ]
    )
)
class UserViewSets(viewsets.ModelViewSet):
    """Logic User"""
    serializer_class = UserSetInvestmentSerializer
    queryset = User.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    @action(methods=['POST'], detail=True, url_path='set-investment')
    def set_investment(self, request, pk=None):
        """set project to a User"""
        try:

            objectSerializer = UserSetInvestmentSerializer(data=request.data)

            if objectSerializer.is_valid():
                project = Project.objects.get(id=objectSerializer.data['investment_id'])
                user = User.objects.get(id=objectSerializer.data['user_id'])
                user.investments.add(project)
                user.save()
                u = UserSerializer(user)

                return Response(u.data, status.HTTP_200_OK)
            
            return Response(objectSerializer.errors, status. HTTP_400_BAD_REQUEST)
        except:
            return Response(objectSerializer.errors, status. HTTP_400_BAD_REQUEST)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_class = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user"""
        return self.request.user
