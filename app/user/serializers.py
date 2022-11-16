"""
Serializers for the user API View
"""
from xml.dom import ValidationErr
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.response import Response

from project.serializers import (
    ProjectSerializer,
    ReferralSerializer,
)

from core.models import (
    Project,
    Referral,
    User,
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    projects = serializers.SerializerMethodField('get_All_Projects')
    referrals = ReferralSerializer(many=True, required=False)
    investments = ProjectSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'country_code', 'phone_number',
            'gender', 'birthday', 'email',
            'password', 'name', 'last_name',
            'is_active', 'is_staff', 'investments',
            'referrals', 'projects'
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        read_only_fiels = ['id']

    # def get_All_Referrals(self, *validated_data):
    #     """get all referrals"""
    #     print(validated_data)
    #     referrals = Referral.objects.filter(user='d3c416e0-71af-4119-94c5-7756840bdf4e')
    #     serialized = ReferralSerializer(referrals, many=True)
    #     return serialized.data

    def get_All_Projects(self, validated_data):
        """get all projects"""
        projects = Project.objects.all()
        serialized = ProjectSerializer(projects, many=True)
        return serialized.data

    def _get_or_add_projects(self, projects, user):
        """Handle getting or add projects as needed"""

        for project in projects:
            try:
                project_obj, finded = Project.objects.get(
                    model=project['model']
                )
                user.investments.set(project_obj)
            except Project.DoesNotExist:
                raise ValidationErr("NOT FOUND IN THE SYSTEM")

    def _get_or_add_referrals(self, referrals, user):
        """Handle getting or add referrals as needed"""
        for referral in referrals:
            referral_obj, finded = Referral.objects.get(
                **referral
            )
            user.referrals.add(referral_obj)

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user"""
        password = validated_data.pop('password', None)

        investments = validated_data.pop('investments', None)
        referrals = validated_data.pop('referrals', None)

        user = super(UserSerializer, self).update(instance, validated_data)

        if password:
            user.set_password(password)

        if investments is not None:
            instance.investments.clear()
            self._get_or_add_projects(investments, instance)
        
        if referrals is not None:
            instance.referrals.clear()
            self._get_or_add_referrals(referrals, instance)

        user.save()

        return user
    
    def set_investment(self, validate_data):
        """set an investment to a user"""
        print(validate_data)
        return "Hola"


class UserSetInvestmentSerializer(serializers.ModelSerializer):
    """Serializer to set a new investment"""

    user_id = serializers.CharField(max_length=255)
    investment_id = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['id', 'user_id', 'investment_id']
        read_only_fiels = ['id']

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
