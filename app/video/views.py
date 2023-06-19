from django.shortcuts import render

from rest_framework import viewsets

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from video.serializers import YoutubeItemSerializer

from core.models import (
    YoutubeItem
)

class YouTubeVideoViewSet(viewsets.ModelViewSet):
    """YoutubeVideo View Set"""
    serializer_class = YoutubeItemSerializer
    queryset = YoutubeItem.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        api_data = request.data

        kind = api_data['kind']
        etag = api_data['etag']
        id_kind = api_data['id']['kind']
        id_video_id = api_data['id']['videoId']
        snippet_published_at = api_data['snippet']['publishedAt']
        snippet_channel_id = api_data['snippet']['channelId']
        snippet_title = api_data['snippet']['title']
        snippet_description = api_data['snippet']['description']

        snippet_thumbnails_default_url = api_data['snippet']['thumbnails']['default']['url']
        snippet_thumbnails_default_width = api_data['snippet']['thumbnails']['default']['width']
        snippet_thumbnails_default_height = api_data['snippet']['thumbnails']['default']['height']

        snippet_thumbnails_medium_url = api_data['snippet']['thumbnails']['medium']['url']
        snippet_thumbnails_medium_width = api_data['snippet']['thumbnails']['medium']['width']
        snippet_thumbnails_medium_height = api_data['snippet']['thumbnails']['medium']['height']

        snippet_thumbnails_high_url = api_data['snippet']['thumbnails']['high']['url']
        snippet_thumbnails_high_width = api_data['snippet']['thumbnails']['high']['width']
        snippet_thumbnails_high_height = api_data['snippet']['thumbnails']['high']['height']

        snippet_channel_title = api_data['snippet']['channelTitle']
        snippet_live_broadcast_content = api_data['snippet']['liveBroadcastContent']
        snippet_publish_time = api_data['snippet']['publishTime']

        try:
            if YoutubeItem.objects.filter(id_video_id=api_data['id']['videoId']):
                return Response({'video': [ 'This video already exist' ]}, status=400)
            item = YoutubeItem.objects.create(
                kind=kind,
                etag=etag,
                id_kind=id_kind,
                id_video_id=id_video_id,
                snippet_published_at=snippet_published_at,
                snippet_channel_id = snippet_channel_id,
                snippet_title = snippet_title,
                snippet_description = snippet_description,

                snippet_thumbnails_default_url = snippet_thumbnails_default_url,
                snippet_thumbnails_default_width = snippet_thumbnails_default_width,
                snippet_thumbnails_default_height = snippet_thumbnails_default_height,

                snippet_thumbnails_medium_url = snippet_thumbnails_medium_url,
                snippet_thumbnails_medium_width = snippet_thumbnails_medium_width,
                snippet_thumbnails_medium_height = snippet_thumbnails_medium_height,

                snippet_thumbnails_high_url = snippet_thumbnails_high_url,
                snippet_thumbnails_high_width = snippet_thumbnails_high_width,
                snippet_thumbnails_high_height = snippet_thumbnails_high_height,

                snippet_channel_title = snippet_channel_title,
                snippet_live_broadcast_content = snippet_live_broadcast_content,
                snippet_publish_time = snippet_publish_time
            )
            serializer = self.get_serializer(item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'message': [ 'Error saving the video' ]}, status=500)
