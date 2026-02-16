from django.conf import settings
from rest_framework import serializers

from short import utils as short_utils
from short import models as short_models


MAX_URL_LENGTH = short_models.ShortLink.original_url.field.max_length


class ShortenInputSerializer(serializers.Serializer):
    original_url = serializers.URLField(max_length=MAX_URL_LENGTH)

    def create(self, validated_data):
        return short_utils.create_short_url(validated_data["original_url"])


class ShortenOutputSerializer(serializers.Serializer):
    short_url = serializers.SerializerMethodField()

    def get_short_url(self, obj):
        base_url = getattr(settings, "SHORT_BASE_URL", "http://localhost:8000/api/short/to_read")
        return f"{base_url}/{obj.code}"


class ReadOutputSerializer(serializers.Serializer):
    original_url = serializers.URLField(max_length=MAX_URL_LENGTH)
