from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

try:
    from .record_from_mic import record_from_mic
    from .create_fingerprint import create_fingerprint
    from .create_hash import create_hashes
    from .matching import score
except ImportError as e:
    print(f"Import Error: {e}")

@api_view(['POST'])
def recognize_music(request):

    try:
        print("Starting recording...")
        Fs, audio = record_from_mic(seconds=7.0)
        print("Recording finished")

        fingerprints = create_fingerprint(audio, Fs)
        hashes = create_hashes(fingerprints)

        song_name, max_score = score(hashes)

        print(f"💯 Score: {max_score}")

        if song_name:
            print(f"Match found ✅: {song_name} (Score: {score})")
            return Response({
                "title": song_name,
                "artist": f"Confidence Score: {int(max_score)}",
                "score": max_score
            }, status=status.HTTP_200_OK)
        else:
            print("No match found.")
            return Response({"message": "No match found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("\n!!! SERVER CRASHED !!!")
        return Response({
            "message": f"Server Error: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def index(request):
    return render(request, 'api/index.html')