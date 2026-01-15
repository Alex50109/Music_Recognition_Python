import pickle
import os
from typing import Dict, List, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

Database = Dict[int, List[Tuple[int, int]]] #type hint
#database[hash] o sa fie o lista de (time, song-id). time era fereastra(index) in care erau frecventele(modif in freq_bin) din fingerprint
#hash -- diferenta frecv2 frecv1 ma rog modificate cat sa intre pe 20+ biti
#dict in care cheia e un hash si val e o lista de aparitii ale hashului in orice melodie
SongIndex = Dict[int, str]
#cheia e song_id si val e numele/calea audio

def save_database(
    database: Database,
    song_index: SongIndex,
    db_path: str = "database.pickle",
    index_path: str = "song_index.pickle"
) -> None: #nu returneaza nmc
    #databse si song index vor fi dict(obiecte Python) care respecta descrierea aia - type hint
    #db_path si index path sunt stringuri(nume) pentru bazele de date(fisiere) care se salveaza pe disc

    full_db_path = os.path.join(BASE_DIR, db_path)
    full_index_path = os.path.join(BASE_DIR, index_path)
    with open(full_db_path, "wb") as f:  #creeaza/deschide un fisier pe disc cu numele dat in db_path, il preg pt scriere binara,OBIECTUL fisier returnat e stocat intr o variabila f; f = open(db_path, "wb")
        pickle.dump(database, f, pickle.HIGHEST_PROTOCOL) #pickle.dump ia un ob Python(database) il serializeaza(tr bytes) si il scrie intr un ob fisier(f) --pe disc se actualizeaza si  database.pickle

    with open(full_index_path, "wb") as f:
        pickle.dump(song_index, f, pickle.HIGHEST_PROTOCOL)


def load_database(
    db_path: str = "database.pickle",
    index_path: str = "song_index.pickle"
) -> tuple[Database, SongIndex]:
    full_db_path = os.path.join(BASE_DIR, db_path)
    full_index_path = os.path.join(BASE_DIR, index_path)
    with open(full_db_path, "rb") as f:
        database: Database = pickle.load(f)

    with open(full_index_path, "rb") as f:
        song_index: SongIndex = pickle.load(f)

    return database, song_index