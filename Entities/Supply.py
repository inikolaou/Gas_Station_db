import sqlite3
import csv

def createSupplyTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE SUPPLY 
                        (Id                     INTEGER     NOT NULL,
                        Expected_Arrival_Date   TEXT        NOT NULL,
                        Real_Arrival_Date       TEXT        NOT NULL,
                        Sup_Email               TEXT        NOT NULL,
                        GS_Longitude            REAL        NOT NULL,
                        GS_Latitude             REAL        NOT NULL,
                        PRIMARY KEY (Id),
                        FOREIGN KEY (Sup_Email) REFERENCES SUPPLIER(Email) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (GS_Longitude, GS_Latitude) REFERENCES GAS_STATION(Longitude, Latitude) ON UPDATE CASCADE ON DELETE CASCADE
                        );''')
            insertFromCsv("Datasets/supply.csv")
        except Exception as e:
            pass
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['ID'], tuple['Expected_Arrival_Date'], tuple['Real_Arrival_Date'], tuple['Sup_Email'],
                       tuple['GS_Longitude'], tuple['GS_Latitude'], conn)
    conn.close()

def insertInto(id, expected_arrival_date, real_arrival_date, sup_email, gs_longitude, gs_latitude, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO SUPPLY
                            VALUES (?,?,?,?,?,?);''',
                            (id, expected_arrival_date, real_arrival_date,
                             sup_email, gs_longitude, gs_latitude))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO SUPPLY
                            VALUES (?,?,?,?,?,?);''',
                            (id, expected_arrival_date, real_arrival_date,
                             sup_email, gs_longitude, gs_latitude))
            except Exception as e:
                pass

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from SUPPLY")
    data = c.fetchall()
    conn.close()
    return data