import sqlite3 as lite

def get_database():
    connection = lite.connect('app.db', check_same_thread=False)

    cursor = connection.cursor()

    """
    cursor.execute("DROP TABLE PLAN")
    cursor.execute("DROP TABLE USERS")
    cursor.execute("DROP TABLE QUERIES")
    #"""

    cursor.execute("CREATE TABLE IF NOT EXISTS QUERIES (query_id INT NOT NULL, uuid INT, time DATETIME, response_code INT, query_hash BINARY(32), PRIMARY KEY (query_id), FOREIGN KEY (uuid) REFERENCES USERS(uuid))")
    cursor.execute("CREATE TABLE IF NOT EXISTS USERS (uuid INT NOT NULL, last_query INT, PRIMARY KEY (uuid), FOREIGN KEY (last_query) REFERENCES QUERIES(query_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS CITIES (iata_name CHAR(3) NOT NULL, city_name VARCHAR(255), image VARCHAR(1024), PRIMARY KEY (iata_name))")
    cursor.execute("CREATE TABLE IF NOT EXISTS PLAN (start_date DATE, end_date DATE, origin CHAR(3), destination CHAR(3), price INT, url VARCHAR(1024), like BIT, query_id INT, FOREIGN KEY (query_id) REFERENCES QUERIES(query_id), FOREIGN KEY (destination) REFERENCES CITIES(iata_name))")
    cursor.execute("CREATE TABLE IF NOT EXISTS WISHLIST (plan_id INT, like BIT, url VARCHAR(1024), FOREIGN KEY (plan_id) REFERENCES PLAN(id))")

    cursor.execute('SELECT iata_name, city_name FROM CITIES')

    print(cursor.fetchone())

    return connection, cursor