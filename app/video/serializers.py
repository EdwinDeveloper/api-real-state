"""
Serializers for Video API
"""
from rest_framework import serializers

from core.models import (
    YoutubeItem,
)

class YoutubeItemSerializer(serializers.ModelSerializer):
    """Youtube Item Serializer"""

    class Meta:
        model = YoutubeItem
        fields = [
            'id', 'kind', 'etag', 'id_kind', 'id_video_id',
            'snippet_published_at', 'snippet_channel_id', 'snippet_title', 'snippet_description',
            'snippet_thumbnails_default_url', 'snippet_thumbnails_default_width', 'snippet_thumbnails_default_height',
            'snippet_thumbnails_medium_url', 'snippet_thumbnails_medium_width', 'snippet_thumbnails_medium_height',
            'snippet_thumbnails_high_url', 'snippet_thumbnails_high_width', 'snippet_thumbnails_high_height',
            'snippet_channel_title', 'snippet_live_broadcast_content', 'snippet_publish_time',
        ]
        read_only_fields = ['id']
    

    def to_representation(self, instance):
        # Customize the response format
        return {
            'kind': instance.kind,
            'etag': instance.etag,
            'id': {
                'kind': instance.id_kind,
                'videoId': instance.id_video_id,
            },
            'snippet': {
                'publishedAt': instance.snippet_published_at,
                'channelId': instance.snippet_channel_id,
                'title': instance.snippet_title,
                'description': instance.snippet_description,
            },
            'thumbnails': {
                'default': {
                    'url': instance.snippet_thumbnails_default_url,
                    'width': instance.snippet_thumbnails_default_width,
                    'height': instance.snippet_thumbnails_default_height,
                },
                'medium': {
                    'url': instance.snippet_thumbnails_medium_url,
                    'width': instance.snippet_thumbnails_medium_width,
                    'height': instance.snippet_thumbnails_medium_height,
                },
                'high': {
                    'url': instance.snippet_thumbnails_high_url,
                    'width': instance.snippet_thumbnails_high_width,
                    'height': instance.snippet_thumbnails_high_height,
                }
            },
            'channelTitle': instance.snippet_channel_title,
            'liveBroadcastContent': instance.snippet_live_broadcast_content,
            'publishTime': instance.snippet_publish_time,
        }