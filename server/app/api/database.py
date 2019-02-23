import sqlite3 as lite

def get_database():
    connection = lite.connect('app.db')
    