import sqlite3
import logging

class SqlLite:
    def __init__(self, dbPath):
        self.db = sqlite3.connect(dbPath, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.db.isolation_level = None
    def __del__(self):
        self.cursor.close()
        self.db.close()

    def getCursor(self):
        return self.db.cursor()

    def executeSQL(self, sql):
        try:
            logging.debug(sql)
            res = self.cursor.execute(sql).fetchall()
            self.db.commit()
            return res
        except Exception as e:
            print(e)
            self.db.rollback()