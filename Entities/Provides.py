import sqlite3
import csv


def createProvidesTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE PROVIDES
                        (Serv_Id        INTEGER     NOT NULL,
                        GS_Longitude    REAL        NOT NULL,
                        GS_Latitude     REAL        NOT NULL,
                        PRIMARY KEY (Serv_Id, GS_Longitude, GS_Latitude),
                        FOREIGN KEY (Serv_Id) REFERENCES SERVICE(Id) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (GS_Longitude, GS_Latitude) REFERENCES GAS_STATION(Longitude, Latitude) ON UPDATE CASCADE ON DELETE CASCADE
                        );''')
            insertFromCsv()
        except Exception as e:
            print(e)
    conn.close()


def insertFromCsv():
    fileName = "Datasets/provides.csv"
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Serv_ID'], tuple['GS_Longitude'],
                       tuple['GS_Latitude'], conn)
    conn.close()


def insertInto(serv_id, gs_longitude, gs_latitude, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO PROVIDES
                            VALUES (?,?,?);''', (serv_id, gs_longitude, gs_latitude))
            except Exception:
                pass  # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO PROVIDES
                            VALUES (?,?,?);''', (serv_id, gs_longitude, gs_latitude))
            except Exception as e:
                pass


def searchBy(serv_id, gs_longitude, gs_latitude):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (serv_id):
            if (gs_longitude and gs_latitude):
                c.execute('''
                        SELECT * 
                        FROM PROVIDES
                        WHERE Serv_Id = ? AND
                        GS_Longitude = ? AND GS_Latitude = ?''',
                          (serv_id, gs_longitude, gs_latitude))
            else:
                c.execute('''
                        SELECT * 
                        FROM PROVIDES
                        WHERE Serv_Id = ?''',
                          (serv_id, ))
        elif (gs_longitude and gs_latitude):
            c.execute('''
                    SELECT * 
                    FROM PROVIDES
                    WHERE GS_Longitude = ? AND GS_Latitude = ?''',
                      (gs_longitude, gs_latitude))
    data = c.fetchall()
    conn.close()
    return data


def update(serv_id, gs_longitude, gs_latitude, previous_serv_id):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE PROVIDES
                        SET Serv_Id = ?
                        WHERE Serv_Id = ? AND GS_Longitude = ?
                        AND GS_Latitude = ?''',
                      (serv_id, previous_serv_id, gs_longitude, gs_latitude))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()


def delete(serv_gslong_lat):
    serv_gslong_lat = serv_gslong_lat.split('_')
    serv_id = serv_gslong_lat[0]
    gs_longitude = serv_gslong_lat[1]
    gs_latitude = serv_gslong_lat[2]
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''DELETE FROM PROVIDES
                        WHERE Serv_Id = ? AND GS_Longitude = ?
                        AND GS_Latitude = ?''',
                      (serv_id, gs_longitude, gs_latitude))
        except Exception as e:
            print(e)
    conn.close()


def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from PROVIDES")
    data = c.fetchall()
    conn.close()
    return data
