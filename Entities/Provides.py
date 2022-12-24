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
            insertFromCsv("Datasets/provides.csv")
        except Exception as e:
            pass
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Serv_ID'], tuple['GS_Longitude'], tuple['GS_Latitude'], conn)
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
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO PROVIDES
                            VALUES (?,?,?);''', (serv_id, gs_longitude, gs_latitude))
            except Exception as e:
                pass

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from PROVIDES")
    data = c.fetchall()
    conn.close()
    return data