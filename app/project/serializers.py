"""
Views for the projects APIs
"""
from rest_framework import serializers
from core.models import (
    Project,
    Price,
    Detail,
    AditionalInfo,
)


class PriceSerializer(serializers.ModelSerializer):
    """Price Serializer"""

    class Meta:
        model = Price
        fields = ['id', 'name', 'amount']
        read_only_fields = ['id']


class DetailSerializer(serializers.ModelSerializer):
    """Detail Serializer"""

    class Meta:
        model = Detail
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class AditionalInfoSerializer(serializers.ModelSerializer):
    """Aditional Info Serializer"""

    class Meta:
        model = AditionalInfo
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']



class ProjectSerializer(serializers.ModelSerializer):
    """Project Serializer"""

    prices = PriceSerializer(many=True, required=False)
    details = DetailSerializer(many=True, required=False)
    aditionalInfos = AditionalInfoSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'company', 'name', 'description', 'prices', 'details', 'aditionalInfos']
        read_only_fields = ['id']
    
    def _get_or_create_prices(self, prices, project):
        """Handle getting or creating prices as needed"""
        for price in prices:
            price_obj, created = Price.objects.get_or_create(
                **price,
            )
            project.prices.add(price_obj)
    
    def _get_or_create_details(self, details, project):
        """Handle getting or creating prices as needed"""
        for detail in details:
            detail_obj, created = Detail.objects.get_or_create(
                **detail,
            )
            project.details.add(detail_obj)

    def _get_or_create_aditionalInfos(self, aditionalInfos, project):
        """Handle getting or creating prices as needed"""
        for info in aditionalInfos:
            info_obj, created = AditionalInfo.objects.get_or_create(
                **info,
            )
            project.aditionalInfos.add(info_obj)
    
    def create(self, validated_data):
        """Create a project"""
        prices = validated_data.pop('prices', [])
        details = validated_data.pop('details', [])
        aditionalInfos = validated_data.pop('aditionalInfos', [])
        project = Project.objects.create(**validated_data)
        self._get_or_create_prices(prices, project)
        self._get_or_create_details(details, project)
        self._get_or_create_aditionalInfos(aditionalInfos, project)

        return project
    
    def update(self, instance, validated_data):
        """Update project"""
        prices = validated_data.pop('prices', None)
        if prices is not None:
            instance.prices.clear()
            self._get_or_create_prices(prices, instance)

        details = validated_data.pop('details', None)
        if details is not None:
            instance.details.clear()
            self._get_or_create_details(details, instance)

        aditionalInfos = validated_data.pop('aditionalInfos', None)
        if aditionalInfos is not None:
            instance.AditionalInfos.clear()
            self._get_or_create_aditionalInfos(aditionalInfos, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
