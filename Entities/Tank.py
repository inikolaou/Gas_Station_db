import sqlite3
import csv

def createTankTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE TANK
                        (Id                         INTEGER     NOT NULL,
                        Last_Check_Up               TEXT        NOT NULL,
                        Capacity                    REAL        NOT NULL,
                        Quantity                    REAL        NOT NULL,
                        Prod_Id                     INTEGER     NOT NULL,
                        GS_Longitude                REAL        NOT NULL,
                        GS_Latitude                 REAL        NOT NULL,
                        PRIMARY KEY (Id, GS_Longitude, GS_Latitude),
                        FOREIGN KEY (Prod_Id)     REFERENCES PRODUCT(Id) ON UPDATE CASCADE ON DELETE SET NULL,
                        FOREIGN KEY (GS_Longitude, GS_Latitude) REFERENCES GAS_STATION(Longitude, Latitude) ON UPDATE CASCADE ON DELETE CASCADE
                        );''')
            insertFromCsv("Datasets/tank.csv")
        except Exception as e:
            pass # Database created
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['ID'], tuple['Last_Check_Up'], tuple['Capacity'],
                        tuple['Quantity'], tuple['Prod_ID'], tuple['GS_Longitude'], 
                        tuple['GS_Latitude'], conn)
    conn.close()

def insertInto(id, last_check, capacity, quantity, product_id, longitude, latitude, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO TANK
                            VALUES (?,?,?,?,?,?,?);''', (id, last_check, capacity,
                            quantity, product_id, longitude, latitude))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO TANK
                            VALUES (?,?,?,?,?,?,?);''', (id, last_check, capacity,
                            quantity, product_id, longitude, latitude))
            except Exception:
                pass

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from TANK")
    data = c.fetchall()
    conn.close()
    return data