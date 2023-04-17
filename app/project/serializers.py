"""
Views for the projects APIs
"""
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from core.models import (
    Company,
    Project,
    Image,
    Detail,
    Extra,
    Referral,
    Bonus,
    User,
    Investment,
)
from collections import OrderedDict


class ImageSerializer(serializers.ModelSerializer):
    """Price Serializer"""

    class Meta:
        model = Image
        fields = ['id', 'url']
        read_only_fields = ['id']


class DetailSerializer(serializers.ModelSerializer):
    """Detail Serializer"""

    class Meta:
        model = Detail
        fields = ['id', 'key', 'info']
        read_only_fields = ['id']


class ExtraSerializer(serializers.ModelSerializer):
    """Extra Info Serializer"""

    class Meta:
        model = Extra
        fields = ['id', 'key', 'info']
        read_only_fields = ['id']

    
class ProjectReferralSerializer(serializers.ModelSerializer):
    """Project Referral Serializer"""

    class Meta:
        model = Project
        fields = ['name', 'model']
        read_only_fields = ['id']

class StaffReferralSerializer(serializers.ModelSerializer):
    """Staff Referral Serializer"""
    class Meta:
        model = User
        fields = ['name', 'last_name']
        read_only_fields = ['id']


class ProjectManagementSerializer(serializers.ModelSerializer):
    """Get all the user investment"""

    class Meta:
        model = Project
        fields = ['id']


class ProjectSerializer(serializers.ModelSerializer):
    """Project Serializer"""

    company  = serializers.SerializerMethodField('get_company_name')

    images = ImageSerializer(many=True, required=False)
    details = DetailSerializer(many=True, required=False)
    extras = ExtraSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'model',
            'description', 'pre_sale_price', 'pre_sale_date',
            'premises_delivery_date', 'rent_price_approximate',
            'resale_price_approximate', 'images', 'details',
            'extras', 'company_related' , 'company', 'bonus',
        ]
        read_only_fields = ['id']

    # @extend_schema_field(str)
    def get_company_name(self, obj):
        """get name company"""
        company = Company.objects.filter(id=obj.company_related_id)
        serialized = CompanySerializer(company, many=True)
        serialized.data[0].pop('models', None)
        return serialized.data[0]

    def _get_or_create_images(self, images, project):
        """Handle getting or creating prices as needed"""
        for image in images:
            image_obj, created = Image.objects.get_or_create(
                **image,
            )
            project.images.add(image_obj)

    def _get_or_create_details(self, details, project):
        """Handle getting or creating prices as needed"""
        for detail in details:
            detail_obj, created = Detail.objects.get_or_create(
                **detail,
            )
            project.details.add(detail_obj)

    def _get_or_create_extras(self, extras, project):
        """Handle getting or creating prices as needed"""
        for extra in extras:
            extra_obj, created = Extra.objects.get_or_create(
                **extra,
            )
            project.extras.add(extra_obj)

    def create(self, validated_data):
        """Create a project"""
        images = validated_data.pop('images', [])
        details = validated_data.pop('details', [])
        extras = validated_data.pop('extras', [])
        project = Project.objects.create(**validated_data)
        self._get_or_create_images(images, project)
        self._get_or_create_details(details, project)
        self._get_or_create_extras(extras, project)

        return project

    def update(self, instance, validated_data):
        """Update project"""
        images = validated_data.pop('images', None)
        if images is not None:
            instance.images.clear()
            self._get_or_create_images(images, instance)

        details = validated_data.pop('details', None)
        if details is not None:
            instance.details.clear()
            self._get_or_create_details(details, instance)

        extras = validated_data.pop('extras', None)
        if extras is not None:
            instance.extras.clear()
            self._get_or_create_extras(extras, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    

class ProjectAdminSerializer(serializers.ModelSerializer):
    """Get all projects list"""

    class Meta:
        model = Project
        fields = ['id']


class CompanySerializer(serializers.ModelSerializer):
    """Company Serializer"""

    models = ProjectSerializer(many=True, required=False)

    class Meta:
        model = Company
        fields = ['id', 'name', 'icon', 'models']


class CompanySerializerAdmin(serializers.ModelSerializer):
    """Company Serializer"""

    models = ProjectSerializer(many=True, required=False)

    class Meta:
        model = Company
        fields = ['id', 'name', 'icon', 'models']
    
    
    def to_representation(self, instance):
        data = super(serializers.ModelSerializer, self).to_representation(instance)
        if self.context['request'].method == 'POST':
            result = OrderedDict()
            result['data'] = data
            result['message'] = ['Company Created']
            result['status'] = 'success'
            return result
        if self.context['request'].method == 'PATCH':
            result = OrderedDict()
            result['data'] = data
            result['message'] = ['Company Updated']
            result['status'] = 'success'
            return result
        
        return data


class ReferralManagementSerializer(serializers.ModelSerializer):
    """Get all referrals from one single user"""

    referrals = serializers.SerializerMethodField('get_referrals')

    class Meta:
        model = Referral
        fields = ('id', 'phone_number', 'country_code', 'gender', 'name', 'last_name',
            'project', 'bonus', 'status', 'referrals')
        read_only_fields = ['id']

    def get_referrals(self, obj):
        """Get referrals info from one users"""
        userReferrals = Referral.objects.filter(user_id=obj)
        serialized = ReferralSerializer(userReferrals, many=True)
        return serialized.data



class ReferralSerializer(serializers.ModelSerializer):
    """Referral serializer"""

    info_project = serializers.SerializerMethodField('get_project_info')
    info_staff = serializers.SerializerMethodField('get_staff_info')

    class Meta:
        model = Referral
        fields = ('id', 'country_code', 'phone_number', 'gender', 'name', 'user_id',
         'last_name', 'project', 'bonus', 'status', 'info_project', 'staff', 'info_staff')
        read_only_fields = ['id']

    def to_representation(self, instance):
        data = super(serializers.ModelSerializer, self).to_representation(instance)
        if self.context['request'].method == 'POST':
            result = OrderedDict()
            result['data'] = data
            result['message'] = ['Referral Created']
            result['status'] = 'success'
            return result
        if self.context['request'].method == 'PATCH':
            result = OrderedDict()
            result['data'] = data
            result['message'] = ['Referral Updated']
            result['status'] = 'success'
            return result
        
        return data

    def get_project_info(self, obj):
        """get project info"""
        project_id = str(obj).split('/')[0]
        project = Project.objects.filter(id=project_id)
        serialized = ProjectReferralSerializer(project, many=True)
        return  serialized.data

    def get_staff_info(self, obj):
        """get staff info"""
        staff_id = str(obj).split('/')[1]
        staff = User.objects.filter(id=staff_id)
        serialized = StaffReferralSerializer(staff, many=True)
        return  serialized.data

    def create(self, validated_data, **kwargs):
        """create a referral"""
        project_bonus = validated_data['project'].pre_sale_price * Bonus.objects.get(id=validated_data['bonus']).percentage
        validated_data['bonus'] = project_bonus
        referral = Referral.objects.create(**validated_data)
        user = User.objects.get(id=validated_data['user_id'])
        user.referrals.add(referral)
        user.save()
        return referral


class BonusSerializer(serializers.ModelSerializer):
    """Bonus serializer"""

    class Meta:
        model = Bonus
        fields = '__all__'
        read_only_fields = ['id']


class BonusSerializerAdmin(serializers.ModelSerializer):
    """Bonus serializer"""

    class Meta:
        model = Bonus
        fields = '__all__'
        read_only_fields = ['id']

    def to_representation(self, instance):
        data = super(serializers.ModelSerializer, self).to_representation(instance)
        if self.context['request'].method == 'POST':
            result = OrderedDict()
            result['data'] = data
            result['message'] = ['Bonus Created']
            result['status'] = 'success'
            return result
        if self.context['request'].method == 'PATCH':
            result = OrderedDict()
            result['data'] = data
            result['message'] = ['Bonus Updated']
            result['status'] = 'success'
            return result
        
        return data


class InvestmentSerializer(serializers.ModelSerializer):
    """Investments"""

    project = serializers.SerializerMethodField()

    class Meta:
        model = Investment
        fields = ('id', 'bonus', 'status', 'user_id', 'project', 'ordinary')
        read_only_fields = ['id']
    
    def get_project(self, validate_data):
        """get investment"""
        project = Project.objects.get(id=validate_data.project.id)
        serializers = ProjectSerializer(project)
        return serializers.data
    

class InvestmentManagementSerializer(serializers.ModelSerializer):
    """Investments"""

    class Meta:
        model = Investment
        fields = '__all__'
        read_only_fields = ['id']
    
    def create(self, validated_data, **kwargs):  
        """create an investment"""
        previous = Investment.objects.filter(user_id=validated_data['user_id'])
        validated_data['ordinary'] = len(previous)+1
        investment = Investment.objects.create(**validated_data)
        return investment
