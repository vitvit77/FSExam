import sqlite3

# DB_NAME = "sensors.db"

def get_database_connection():
    con = sqlite3.connect("sensors.db")

    return con

def create_table():
    create_table_sens = """ CREATE TABLE Sensors(
        id          INTEGER PRIMARY KEY     AUTOINCREMENT,
        qty      TEXT                NOT NULL,
        description       TEXT                NOT NULL
    )   
    """

    create_table_sens_param = """ CREATE TABLE sensorinfo(
        id          INTEGER PRIMARY KEY     AUTOINCREMENT,
        sensor_id      INTEGER                NOT NULL,
        param       REAL                NOT NULL
    )   
    """
    con = get_database_connection()
    con.execute(create_table_sens)
    con.execute(create_table_sens_param)
    con.close()

con = get_database_connection()

create_table()