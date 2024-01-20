import sqlite3
class SqlLite:
    def __init__(self, dbPath):
        self.db = sqlite3.connect(dbPath, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.db.isolation_level = None
    def __del__(self):
        self.cursor.close()
        self.db.close()

    def getCursor(self):
        return self.db.cursor()

    def executeSQL(self, sql):
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        return res