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
import requests
from django.http import HttpResponse

from project.serializers import (
    ProjectSerializer,
    ReferralSerializer,
    BonusSerializer,
    CompanySerializer,
    ReferralManagementSerializer,
    InvestmentSerializer,
    InvestmentManagementSerializer
)
from collections import OrderedDict

from core.models import (
    Project,
    Referral,
    User,
    Bonus,
    Company,
    Investment,
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    projects = serializers.SerializerMethodField('get_All_Projects')
    referrals = ReferralSerializer(many=True, required=False)
    # investments = ProjectSerializer(many=True, required=False)
    investments = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField('get_videos')
    bonuses = serializers.SerializerMethodField('get_all_bonuses')
    companies = serializers.SerializerMethodField('get_all_companies')
    users = serializers.SerializerMethodField('get_all_users_not_staff')
    staff = serializers.SerializerMethodField('get_all_users_staff')

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'country_code', 'phone_number',
            'gender', 'birthday', 'email',
            'password', 'name', 'last_name',
            'is_active', 'is_staff', 'investments',
            'referrals', 'projects', 'videos', 'bonuses',
            'companies', 'users', 'staff'
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        read_only_fiels = ['id']

    def get_investments(self, validate_data):
        """get all user invertions"""
        user = User.objects.get(email=validate_data)
        investments = Investment.objects.filter(user_id=user.id)
        serializer = InvestmentSerializer(investments, many=True)
        return serializer.data

    def get_videos(self, validated_data):
        """get all videos"""
        try:
            response = requests.get("https://www.googleapis.com/youtube/v3/search?key=AIzaSyBL848RUWQcfJkLmTL2cn4VkWcmSCxiOU8&channelId=UCCf4BrsWz7BaegKR6q29tyQ&part=snippet,id&order=date&maxResults=6")
        except Exception as e:
            return {
                "kind": "youtube#searchListResponse",
                "etag": "",
                "nextPageToken": "",
                "regionCode": "MX",
                "pageInfo": {
                    "totalResults": 0,
                    "resultsPerPage": 0
                },
                "items": []
            }

        return response.json()

    def to_representation(self, instance):
        data = super(serializers.ModelSerializer, self).to_representation(instance)
        if self.context['request'].method == 'POST':
            result = OrderedDict()
            result['data'] = data
            result['message'] = ['User Created']
            result['status'] = 'success'
            return result
        
        return data

    def get_all_users_not_staff(self, validated_data):
        """get all users not staff"""
        userIsStaff = User.objects.filter(email=validated_data, is_staff=True).exists()
        if userIsStaff:
            users =  User.objects.filter(is_staff=False)
            serialized = UserManagementSerializer(users, many=True)
            return serialized.data
    
    def get_all_users_staff(self, validate_data):
        """get all users staff"""
        userIsStaff = User.objects.filter(is_staff=True)
        serialized = UserManagementSerializer(userIsStaff, many=True)
        return serialized.data

    def get_All_Projects(self, validated_data):
        """get all projects"""
        projects = Project.objects.all()
        serialized = ProjectSerializer(projects, many=True)
        return serialized.data

    def get_all_bonuses(self, validated_data):
        """get all bonuses"""
        userIsStaff = User.objects.filter(email=validated_data, is_staff=True).exists()
        if userIsStaff:    
            bonuses = Bonus.objects.all()
            serialized = BonusSerializer(bonuses, many=True)
            return serialized.data

    def get_all_companies(self, validate_data):
        """get all companies"""
        userIsStaff = User.objects.filter(email=validate_data, is_staff=True).exists()
        if userIsStaff:
            companies = Company.objects.all()
            serialized = CompanySerializer(companies, many=True)
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


class UserStaffSerializer(serializers.ModelSerializer):
    """Serializer to set a new investment"""

    # user_id = serializers.CharField(max_length=255)
    # investment_id = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['id', 'is_active', 'is_staff']
        read_only_fiels = ['id']
    

class UserEndSerializer(serializers.ModelSerializer):
    """Serializer to manage the end user"""

    class Meta:
        model = User
        fields = ['email']
        read_only_fiels = ['id']


class UserManagementSerializer(serializers.ModelSerializer):
    """Serializer to manage users from the platform"""

    investments = serializers.SerializerMethodField()
    referrals = ReferralManagementSerializer(many=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'last_name', 'country_code', 'phone_number', 'email', 'investments', 'referrals', 'is_active', 'is_staff']

    def get_investments(self, validate_data):
        """get all user invertions"""
        user = User.objects.get(email=validate_data)
        investments = Investment.objects.filter(user_id=user.id)
        serializer = InvestmentSerializer(investments, many=True)
        return serializer.data

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
