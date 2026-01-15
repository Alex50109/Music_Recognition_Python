import numpy as np

upper_frequency = 23000
bits = 10

def create_hashes(fingerprint, song_id = None):
    hashes = {}

    for idx, (time, frequency) in enumerate(fingerprint):
        for time2, frequency2 in fingerprint[idx: idx + 100]:
            difference = time2 - time

            if difference <= 1 or difference > 10:
                continue

            freq_bin = frequency / upper_frequency * (2 ** bits)
            freq_bin2 = frequency2 / upper_frequency * (2 ** bits)

            hash_val = int(freq_bin) | (int(freq_bin2) << 10) | (int(difference) << 20)
            hashes[hash_val] = (time, song_id)

    return hashes