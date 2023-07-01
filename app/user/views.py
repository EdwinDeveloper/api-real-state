"""
Views for the user API
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
import os
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
    def active_or_inactive_user_or_staff(self, request, pk=None):
        """Path user"""
        try:
            user = User.objects.get(id=request.data['id'])
            user.is_active = request.data['is_active']
            user.save()
            return Response({ 'is_active': user.is_active }, status.HTTP_200_OK)
        except:
            return Response( { "error": "error" } , status. HTTP_400_BAD_REQUEST)
        
    @action(methods=['PATCH'], detail=False, url_path='eliminate-superuser-status')
    def eliminate_superuser_status(self, request, pk=None):
        """Eliminate superuser status"""
        try:
            user = User.objects.get(id=request.data['id'])
            user.is_superuser = False
            user.save()
            return Response( { 'is_superuser': user.is_superuser }, status.HTTP_200_OK )
        except Exception as e:
            return Response( { "error": str(e) } )
        
    @action(methods=['PATCH'], detail=False, url_path='activate-superuser-status')
    def eliminate_superuser_status(self, request, pk=None):
        """Eliminate superuser status"""
        try:
            user = User.objects.get(id=request.data['id'])
            user.is_superuser = True
            user.save()
            return Response( { 'is_superuser': user.is_superuser }, status.HTTP_200_OK )
        except Exception as e:
            return Response( { "error": str(e) } )
    
    @action(methods=['PATCH'], detail=False, url_path='make-staff')
    def make_staff(self, request, pk=None):
        """Path user"""
        try:
            user = User.objects.get(id=request.data['id'])
            user.is_staff = request.data['is_staff']
            user.save()
            return Response({ 'is_staff': user.is_staff }, status.HTTP_200_OK)
        except:
            return Response( { "error": "error" } , status. HTTP_400_BAD_REQUEST)

class UserEndSerializer(viewsets.ModelViewSet):

    serializer_class = UserEndSerializer
    queryset = User.objects.all()

    """Update user data"""
    @action(methods=['PATCH'], detail=False, url_path="user-update")
    def user_update(self, request, *args, **kwargs):
        try:
            check = User.objects.get(phone_number=request.data['phone_number'])
            if check.id == request.data['id']:
                user = User.objects.get(id=request.data['id'])
                user.name = request.data['name']
                user.last_name = request.data['last_name']
                user.phone_number = request.data['phone_number']
                user.save()
                return Response( { "message": "Usuario actualizado" } , status.HTTP_200_OK)
            return Response( { "message": "Telefono ya utilizado" } , status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response( { "error": e.args[0] } , status.HTTP_400_BAD_REQUEST)

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
                return Response( { "message": "Contraseña modificada" } , status.HTTP_200_OK)
            else:
                return Response( { "message": "Usuario invalido" } , status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response( { "error": e.args[0] } , status.HTTP_400_BAD_REQUEST)

    """End user management"""
    @action(methods=['POST'], detail=False, url_path='reset-password')
    def password_reset(self, request, pk=None):
        try:
            server_host = os.environ.get('SERVER_HOST')
            email = request.data['email']
            user = User.objects.filter(email=email).first()
            if user:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                user.token = token
                user.save()
                reset_password_link = f'{server_host}/api/user/reset-password-template?token={token}&uidb64={uidb64}'
                subject = 'Password Reset Request'
                html_message = render_to_string('email.html', {'reset_password_link': reset_password_link})
                plain_message = strip_tags(html_message)
                from_email =  os.environ.get('EMAIL_USER')
                to = email
                send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                messages.success(request, 'Email sent')
                return Response({ 
                    "message": "Email Sended, check your email"                    
                 } , status.HTTP_200_OK)
            else:
                messages.error(request, 'User not found')
                return Response( {
                    "email": [
                        "Email does not exist"
                    ]
                } , status.HTTP_400_BAD_REQUEST)
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
