import numpy as np
from scipy import signal

def create_fingerprint(audio_data, Fs):
    if audio_data.ndim > 1:
        audio = audio_data[:, 0]
    else:
        audio = audio_data.copy()

    audio = audio.astype(np.float64)
    if np.max(np.abs(audio)) > 0:
        audio /= np.max(np.abs(audio))

    window_length_s = 0.5
    window_length_samples = int(window_length_s * Fs)
    window_length_samples += window_length_samples % 2
    nr_peaks = 15
    pad_amount = window_length_samples - audio.size % window_length_samples
    song_input = np.pad(audio, (0, pad_amount), mode='constant')

    freq, times, stft_result = signal.stft(
        song_input, Fs,
        nperseg=window_length_samples, nfft=window_length_samples,
        return_onesided=True)

    stft_magnitude = np.abs(stft_result)

    fingerprint_map = []

    for time_idx, window in enumerate(stft_magnitude.T):
        spectrum = window

        peaks, props = signal.find_peaks(spectrum, prominence=0, distance=20)

        n_peaks = min(nr_peaks, len(peaks))

        if n_peaks > 0:
            largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]

            for peak_index in peaks[largest_peaks]:
                frequency = freq[peak_index]
                fingerprint_map.append([time_idx, frequency])

    return fingerprint_map