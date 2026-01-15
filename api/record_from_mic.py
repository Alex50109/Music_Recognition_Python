import sounddevice as sd


def record_from_mic(seconds: float = 7.0, Fs: int = 44100):

    print(f" Recording {seconds} seconds at {Fs} Hz...")

    audio = sd.rec(
        int(seconds * Fs),
        samplerate=Fs,
        channels=1,
        dtype="float32"
    )
    sd.wait()

    audio = audio.squeeze()
    print(" Done")

    return Fs, audio