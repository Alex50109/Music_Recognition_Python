from rest_framework import serializers
from .models import MusicFile

class AudioStringSerializer(serializers.Serializer):

    audio_string = serializers.CharField(
        max_length=1000000,
        required=True,
        help_text="Base64 encoded audio snippet or pre-fingerprinted hash string."
    )

class MusicFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicFile
        fields = ['id', 'title', 'artist']