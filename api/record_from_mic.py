import sounddevice as sd


def record_from_mic(seconds: float = 7.0, Fs: int = 44100):

    print(f" Recording {seconds} seconds at {Fs} Hz...")

    audio = sd.rec(
        int(seconds * Fs),   #cate esantioane o sa am pe durata inregistrarii
        samplerate=Fs,
        channels=1,
        dtype="float32"
    )  #returneaza , in cazul asta ceva de forma audio.shape = (7*44100 , 1) dar mie imi tb un array 1D de 7*44100 elemente (amplitudini luate din 1/Fs in 1/FS)
    sd.wait()

    audio = audio.squeeze()  # (N,1) -> (N,)
    print(" Done")

    return Fs, audio