from oracledb import *
from traceback import *


class Model:
    def __init__(self):
        self.song_dict = {}
        self.db_status = True
        self.conn = None
        self.cur = None
        try:
            init_oracle_client()
            self.conn = connect("mouzikka/music@DESKTOP-EFPHEOE:1522/XE")
            print("Connected Successfully to the database")
            self.cur = self.conn.cursor()
        except DatabaseError:
            print("getting error while connecting to the database")
            self.db_status = False
            print(f"Database Error:{format_exc()}")

    def get_db_status(self):
        return self.db_status

    def get_song_count(self):
        return len(self.song_dict)

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
            print("Cursor Closed")
        if self.conn is not None:
            self.conn.close()
            print("Connection Closed")

    def add_song(self, song_name, song_path):
        self.song_dict[song_name] = song_path
        print(f"Song added:{self.song_dict[song_name]}")

    def get_song_path(self, song_name):
        return self.song_dict[song_name]

    def remove_song(self, song_name):
        self.song_dict.pop(song_name)
        print(f"After deletion {self.song_dict}")

    def search_song_in_favorites(self, song_name):
        print("song name", song_name)
        self.cur.execute("select * from myfavorites where song_name=:1", (song_name,))
        song_tuple = self.cur.fetchone()
        print("song_tuple is", song_tuple)
        if song_tuple is None:
            return False
        return True

    def add_song_to_favorites(self, song_name, song_path):
        print("inside the model add song to fav")
        is_song_present = self.search_song_in_favorites(song_name)
        if is_song_present == True:
            return "song already present in favorites"
        self.cur.execute("Select max(song_id) from myfavorites")
        last_song_id = self.cur.fetchone()[0]
        next_song_id = 1
        if last_song_id is not None:
            next_song_id = last_song_id + 1
        self.cur.execute("insert into myfavorites values(:1,:2,:3)", (next_song_id, song_name, song_path))
        self.conn.commit()
        return "song_successfully added to your favourites "

    def load_song_from_favorites(self):
        self.cur.execute("select song_name,song_path from myfavorites")
        song_present = False
        for song_name, song_path in self.cur:
            self.song_dict[song_name] = song_path
            song_present = True
        if song_present == True:
            return "List populate from favorites"
        else:
            return "No song present in  your favorites"

    def remove_song_from_favorites(self, song_name):
        self.cur.execute(f"Delete from myfavorites where song_name{song_name,}")
        count = self.cur.rowcount
        if count == 0:
            return "Song not present in your favorites"
        else:
            self.song_dict.pop(song_name)
            self.conn.commit()
            return "Song deleted from your favorites"
