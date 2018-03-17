import sqlite3


class Database(object):
    def __init__(self):
        self.connection = self.create_connection()
        self.create_table(self.connection)

    def create_connection(self):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect("/home/szczocik/Workspaces/argumentationSemantics/ArgTest/database")
            return conn
        except sqlite3.Error as e:
            print(e)
        return None

    def create_table(self, conn):
        sql = """ CREATE TABLE IF NOT EXISTS conflict_free (
                    id integer PRIMARY KEY,
                    arguments text NOT NULL
                    ); """

        try:
            c = conn.cursor()
            c.execute(sql)
        except sqlite3.Error as e:
            print(e)

    def add_conflict_free_set(self, args):
        sql = """ INSERT INTO conflict_free(arguments)
                  VALUES (?) """
        try:
            cur = self.connection.cursor()
            cur.execute(sql, str(args))
        except sqlite3.Error as e:
            print(e)

    def get_conflict_free_sets(self):
        sql = """ SELECT * FROM conflict_free """

        try:
            cur = self.connection.cursor()
            all = cur.fetchall()
            print("Printing all conflict free sets")
            for row in all:
                print('{0}: {1}'.format(row[0], format[1]))
        except sqlite3.Error as e:
            print(e)
