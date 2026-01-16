# Music Recognition API

This is a Django-based API that records audio from the microphone, fingerprints it, and matches it against a database of songs using hashing algorithms.

# How it works
1. **Record**: Captures 12 seconds of audio.
2. **Fingerprint**: Performs STFT (Fourier Transform) to find frequency peaks.
3. **Hash**: Creates unique hashes based on peak time differences.
4. **Match**: Compares hashes against a pre-built `database.pickle`.

# DO NOT
1. Open the .pickle files (they will get corrupted)

# Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

# How to run
1. Open the terminal in Pycharm
2. Run the server using this command: python manage.py runserver
3. Go to the link http://127.0.0.1:8000/api/
4. Press the button and wait for the result!
