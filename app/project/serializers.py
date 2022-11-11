"""
Views for the projects APIs
"""
from rest_framework import serializers
from core.models import (
    Company,
    Project,
    Image,
    Detail,
    Extra,
    Referral,
)


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
            'extras', 'company_related' , 'company'
        ]
        read_only_fields = ['id']

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


class CompanySerializer(serializers.ModelSerializer):
    """Company Serializer"""

    models = ProjectSerializer(many=True, required=False)

    class Meta:
        model = Company
        fields = ['id', 'name', 'icon', 'models']


class ReferralSerializer(serializers.ModelSerializer):
    """Referral serializer"""

    project = ProjectSerializer(required=False)

    class Meta:
        model = Referral
        fields = ['id', 'status', 'project', 'user_referral']
        read_only_fields = ['id']
