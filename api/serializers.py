from rest_framework import serializers
from .models import MusicFile

# A. Serializer for handling the incoming string data (microphone input)
class AudioStringSerializer(serializers.Serializer):
    # The client MUST send a JSON body with a key named 'audio_string'
    audio_string = serializers.CharField(
        max_length=1000000,
        required=True,
        help_text="Base64 encoded audio snippet or pre-fingerprinted hash string."
    )

# B. Serializer for handling the outgoing song data (database output)
class MusicFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicFile
        # Only return the relevant song metadata to the client
        fields = ['id', 'title', 'artist']