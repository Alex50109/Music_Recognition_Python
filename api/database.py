import pickle
import os
from typing import Dict, List, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

Database = Dict[int, List[Tuple[int, int]]]
SongIndex = Dict[int, str]

def save_database(
    database: Database,
    song_index: SongIndex,
    db_path: str = "database.pickle",
    index_path: str = "song_index.pickle"
) -> None:
    full_db_path = os.path.join(BASE_DIR, db_path)
    full_index_path = os.path.join(BASE_DIR, index_path)

    with open(full_db_path, "wb") as f:
        pickle.dump(database, f, pickle.HIGHEST_PROTOCOL)

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