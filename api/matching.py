from collections import defaultdict
from typing import Dict, List, Tuple

from .record_from_mic import record_from_mic
from .create_fingerprint import create_fingerprint
from .database import load_database, Database, SongIndex

print("Loading database...")
database, song_index = load_database()

# nu mai am song_id aici deci ramane dictionar hash->ferestre pentru microfon
MicHashes = Dict[int, List[int]]

def create_hashes_mic(fingerprint: List[List[float]]) -> MicHashes:
    upper_frequency = 23000
    bits = 10

    hashes: Dict[int, List[int]] = defaultdict(list)

    for idx, (time1, freq1) in enumerate(fingerprint):
        for time2, freq2 in fingerprint[idx: idx + 100]:
            diff = time2 - time1

            if diff <= 1 or diff > 10:
                continue

            freq_bin1 = freq1 / upper_frequency * (2 ** bits)
            freq_bin2 = freq2 / upper_frequency * (2 ** bits)

            h = int(freq_bin1) | (int(freq_bin2) << 10) | (int(diff) << 20)

            hashes[h].append(int(time1))

    return dict(hashes)

def score_hashes_against_database_mic(
        H_mic: MicHashes,
        database: Database
) -> List[Tuple[int, Tuple[int, int]]]:
    matches_per_song: Dict[int, List[Tuple[int, int, int]]] = {}

    # pentru toate hashurile si timpii lor din microfon verific baza de date
    for h, mic_times in H_mic.items():
        if h not in database:
            continue

        matching_occurrences = database[
            h]  # lista de (t_db, song_id)- se suprascrie la fiecare hash cu timpii si melodiile din baza de date coresp aceluiasi hash

        for t_db, song_id in matching_occurrences:
            if song_id not in matches_per_song:
                matches_per_song[song_id] = []

            # fiecarei melodii ii pun hashul, fereastra din inreg microfon, fereastra din baza de date la care se gaseste
            for t_mic in mic_times:
                matches_per_song[song_id].append((h, t_mic,
                                                  t_db))  # pana aici o sa am un dictionar de song_id -> hashuri de la microfon si ferestrele ancora in care s au gasit(popt sa fie fi zgmotote totusi)

    # offset, scorare
    scores: Dict[int, Tuple[int, int]] = {}

    for song_id, matches in matches_per_song.items():
        song_scores_by_offset: Dict[int, int] = {}  # va avea offseturile si nr lor de aparitii

        for h, t_mic, t_db in matches:
            delta = t_db - t_mic  # offset
            if delta not in song_scores_by_offset:
                song_scores_by_offset[delta] = 0
            song_scores_by_offset[
                delta] += 1  # daca melodia e corecta multe matchuri vor avea acelasi delta si multe nr de aparitii

        best = (0, 0)  # (offset, scor)
        for offset, score in song_scores_by_offset.items():
            if score > best[1]:  # caut cel mai mare nr de aparitii
                best = (offset, score)

        scores[
            song_id] = best  # salvez cel mai mare nr pt song_id la care sunt ca dupa sa le compar pe toate melodiile intre ele

    # 3) sortez dupa best_score descrescator, deci primul element e cel cu cele mai multe aparitii de offset, deci melodia cautata
    sorted_scores = list(sorted(scores.items(), key=lambda x: x[1][1], reverse=True))
    return sorted_scores


def score(hashes):
    # ia output din create_hash.py si il converteste

    if not database:
        return None, 0

    # Converteste {h: (t, id)} -> {h: [t]}, ex: 123:(50, None) -> 123:[50]
    H_mic_adapter = defaultdict(list)
    for h, val in hashes.items():
        # if val is tuple (time, id) or just time
        if isinstance(val, (tuple, list)):
            t = val[0]
        else:
            t = val
        H_mic_adapter[h].append(t)

    rezultate = score_hashes_against_database_mic(H_mic_adapter, database)

    if not rezultate:
        return None, 0

    top_id, (offset, scor) = rezultate[0]
    song_name = song_index.get(top_id, f"Unknown ID {top_id}")

    return song_name, scor

def start_app(seconds: float = 10.0, Fs: int = 44100, min_score: int = 25) -> None:
    print("[PAS 1] Se incarca baza de date...")
    # database, song_index = load_database() # l am pus la inceput

    print(f"[PAS 2] Se inregistreaza... ({seconds} sec)")
    Fs_rec, audio = record_from_mic(seconds=seconds, Fs=Fs)  # (Fs, audio)

    print("[PAS 3] Fingerprint...")
    fp = create_fingerprint(audio, Fs_rec)

    print("[PAS 4] Hash-uri microfon ...")
    H_mic = create_hashes_mic(fp)

    print("[PAS 5] Matching...")
    rezultate = score_hashes_against_database_mic(H_mic, database)

    if not rezultate:
        print("Nicio potrivire.")
        return

    top_id, (offset, scor) = rezultate[0]
    if scor < min_score:
        print("Potrivire nesigură (scor mic).")
        print(f"Top: {song_index.get(top_id, '?')} | scor={scor} | offset={offset}")
        return

    print(f"MELODIE: {song_index.get(top_id, '?')}")
    print(f"Scor: {scor} | Offset: {offset}")

    print("\nTop 5:")
    for sid, (off, sc) in rezultate[:5]:
        print(f"  - {song_index.get(sid, '?')} | scor={sc} | offset={off}")

if __name__ == "__main__":
    start_app(seconds=12.0, Fs=44100, min_score=25)