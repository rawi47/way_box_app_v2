#!/usr/bin/python

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None




def select_all_by(conn,table,values):
    """
    Query table by condition
    :param conn: the Connection object
    :param param:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT " + values + " FROM " + table)

    return cur.fetchall()




if __name__ == '__main__':
    pass