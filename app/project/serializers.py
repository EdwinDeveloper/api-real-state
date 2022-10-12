"""
Views for the projects APIs
"""
from rest_framework import serializers
from core.models import (
    Project,
    Price,
    Detail,
    Extra,
)


class PriceSerializer(serializers.ModelSerializer):
    """Price Serializer"""

    class Meta:
        model = Price
        fields = ['id', 'key', 'info']
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

    prices = PriceSerializer(many=True, required=False)
    details = DetailSerializer(many=True, required=False)
    extras = ExtraSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = [
            'id', 'company', 'name',
            'description', 'prices', 'details',
            'extras'
        ]
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

    def _get_or_create_extras(self, extras, project):
        """Handle getting or creating prices as needed"""
        for extra in extras:
            extra_obj, created = Extra.objects.get_or_create(
                **extra,
            )
            project.extras.add(extra_obj)

    def create(self, validated_data):
        """Create a project"""
        prices = validated_data.pop('prices', [])
        details = validated_data.pop('details', [])
        extras = validated_data.pop('extras', [])
        project = Project.objects.create(**validated_data)
        self._get_or_create_prices(prices, project)
        self._get_or_create_details(details, project)
        self._get_or_create_extras(extras, project)

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

        extras = validated_data.pop('extras', None)
        if extras is not None:
            instance.Extras.clear()
            self._get_or_create_extras(extras, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
