import sqlite3

class SqliteWrapper:
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(database=db_file)
            return conn
        except Exception as e:
            print(e)
        return conn

    def execute(conn, sql):
        try:
            c = conn.cursor()
            return c.execute(sql)
        except Exception as e:
            print(e)

    def select_execute(conn, sql):
        try:
            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()
        except Exception as e:
            print(e)