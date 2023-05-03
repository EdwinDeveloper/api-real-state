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


from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from core.models import User
import uuid

from user.serializers import (
    UserSerializer,
    UserStaffSerializer,
    UserEndSerializer,
    AuthTokenSerializer,
)
from core.models import (
    User,
    Project,
)

# from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class CreateUserView(
    generics.CreateAPIView,
    mixins.UpdateModelMixin,
):
    """Create a new user in the system"""
    serializer_class = UserSerializer


# @extend_schema_view(
#     list=extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 'investmentsw',
#                 OpenApiTypes.STR,
#                 description='Adding a new investment to an user'
#             )
#         ]
#     )
# )
class UserViewSets(viewsets.ModelViewSet):
    """Logic User"""
    serializer_class = UserStaffSerializer
    queryset = User.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    @action(methods=['PATCH'], detail=False, url_path='active-user')
    def patch_user(self, request, pk=None):
        """Path user"""
        try:
            user = User.objects.get(id=request.data['id'])
            user.is_active = request.data['is_active']
            user.save()
            return Response({ 'is_active': user.is_active }, status.HTTP_200_OK)
        except:
            return Response( { "error": "error" } , status. HTTP_400_BAD_REQUEST)

class UserEndSerializer(viewsets.ModelViewSet):

    serializer_class = UserEndSerializer
    queryset = User.objects.all()

    """End user reset password"""
    @action(methods=['POST'], detail=False, url_path='reset')
    def reset(self, request, *args, **kwargs):
        try:
            uidb64 = request.data.get('uidb64')
            token = request.data.get('token')
            uid = urlsafe_base64_decode(uidb64).decode('utf-8')
            user = User.objects.get(pk=uid)
            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(request.data.get('password'))
                user.save()
                return Response( { "message": "Contraseña modificada" } , status.HTTP_201_OK)
            else:
                return Response( { "message": "Usuario invalido" } , status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response( { "error": e.args[0] } , status.HTTP_400_BAD_REQUEST)

    """End user management"""
    @action(methods=['POST'], detail=False, url_path='reset-password')
    def password_reset(self, request, pk=None):
        try:
            email = request.data['email']
            user = User.objects.filter(email=email).first()
            # reset_token = user.generate_reset_token()
            if user:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                user.token = token
                user.save()
                reset_password_link = f'http://localhost:8000/api/user/reset-password-template?token={token}&uidb64={uidb64}'
                subject = 'Password Reset Request'
                html_message = render_to_string('email.html', {'reset_password_link': reset_password_link})
                plain_message = strip_tags(html_message)
                from_email = 'lafamiliaesgrande@gmail.com'
                to = email
                send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                messages.success(request, 'Email sent')
                return Response({ "message": "Email sended" } , status.HTTP_200_OK)
            else:
                messages.error(request, 'User not found')
                return Response({ "message": "User not available" } , status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response( { "error": e.args[0] } , status.HTTP_400_BAD_REQUEST)


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
