# Music Recognition API

This is a Django-based API that records audio from the microphone, fingerprints it, and matches it against a database of songs using hashing algorithms.

# How it works
1. **Record**: Captures 7 seconds of audio.
2. **Fingerprint**: Performs STFT (Fourier Transform) to find frequency peaks.
3. **Hash**: Creates unique hashes based on peak time differences.
4. **Match**: Compares hashes against a pre-built `database.pickle`.

# Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
