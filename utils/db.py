import os
import sqlite3
from .files import *


class DataBaseController:
    def __init__(self):
        super(DataBaseController, self).__init__()
        self.connection = sqlite3.connect("photocloud.db")
        self.id = 1
        self.username = ''

    def create_db(self, name, properties):
        cursor = self.connection.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name} ({properties});""")

    def get_user_with_filter(self, filter):
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT rowid, * FROM users WHERE {filter};""")
        fetched = cursor.fetchone()
        self.id = fetched[0]
        self.username = fetched[1]
        return fetched

    def add_data_to_db(self, name, properties):
        cursor = self.connection.cursor()
        cursor.execute(f"""INSERT INTO {name} VALUES ({properties});""")
        self.connection.commit()

    def add_blob_to_db(self, id, photo, date):
        cursor = self.connection.cursor()
        sqlite_insert_blob_query = """INSERT INTO photos
                                  (id, blob, date) VALUES (?, ?, ?);"""
        emp_photo = convert_to_binary_data(photo)
        data_tuple = (id, emp_photo, date)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        self.connection.commit()

    def read_blob_data(self):
        cursor = self.connection.cursor()
        print('reading', self.id)
        sql_fetch_blob_query = """SELECT * from photos where id = ?;"""
        cursor.execute(sql_fetch_blob_query, (self.id,))
        record = cursor.fetchall()
        for index, row in enumerate(record):
            id = row[0]
            photo = row[1]
            print(id, len(record))
            try:
                os.mkdir('photos')
            except FileExistsError:
                pass
            photo_path = os.path.join("photos", str(id) + "_" + str(index) + ".jpg")
            write_to_file(photo, photo_path)

    def check_existing_db(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
