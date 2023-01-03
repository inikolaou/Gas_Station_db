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
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
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

def searchBy(id, expected_arrival_date, real_arrival_date, sup_email, gs_longitude, gs_latitude):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (id):
            c.execute('''
                SELECT * 
                FROM SUPPLY
                WHERE Id = ?''',
                (id, ))
        elif (expected_arrival_date):
            if (gs_longitude and gs_latitude):
                c.execute('''
                    SELECT * 
                    FROM SUPPLY
                    WHERE Expected_Arrival_Date = ? AND GS_Longitude = ? AND GS_Latitude = ?''',
                    (expected_arrival_date, gs_longitude, gs_latitude))
            else:
                c.execute('''
                    SELECT * 
                    FROM SUPPLY
                    WHERE Expected_Arrival_Date = ?''',
                    (expected_arrival_date, ))
        elif (real_arrival_date):
            if (gs_longitude and gs_latitude):
                c.execute('''
                    SELECT * 
                    FROM SUPPLY
                    WHERE Real_Arrival_Date = ? AND GS_Longitude = ? AND GS_Latitude = ?''',
                    (real_arrival_date, gs_longitude, gs_latitude))
            else:
                c.execute('''
                    SELECT * 
                    FROM SUPPLY
                    WHERE Real_Arrival_Date = ?''',
                    (real_arrival_date, ))
        elif (sup_email):
            c.execute('''
                SELECT * 
                FROM SUPPLY
                WHERE Sup_Email = ?''',
                (sup_email, ))
        elif (gs_longitude and gs_latitude):
            c.execute('''
                SELECT * 
                FROM SUPPLY
                WHERE GS_Longitude = ? AND GS_Latitude = ?''',
                (gs_longitude, gs_latitude))
    data = c.fetchall()
    conn.close()
    return data

def update(id, expected_arrival_date, real_arrival_date, sup_email, gs_longitude, gs_latitude):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE SUPPLY
                        SET Expected_Arrival_Date = ?, Real_Arrival_Date = ?, Sup_Email = ?,
                        GS_Longitude = ?, GS_Latitude = ? WHERE Id = ?''', 
                        (expected_arrival_date, real_arrival_date,
                        sup_email, gs_longitude, gs_latitude, id))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()

def delete(id):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''DELETE FROM SUPPLY
                        WHERE Id = ?''', (id, ))
        except Exception as e:
            print(e)
    conn.close()

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from SUPPLY")
    data = c.fetchall()
    conn.close()
    return data