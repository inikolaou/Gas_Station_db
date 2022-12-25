import sqlite3
import csv

def createOffersTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE OFFERS 
                        (Prod_Id        INTEGER     NOT NULL,
                        GS_Longitude    REAL        NOT NULL,
                        GS_Latitude     REAL        NOT NULL,
                        Quantity        REAL        NOT NULL,
                        PRIMARY KEY (Prod_Id, GS_Longitude, GS_Latitude, Quantity),
                        FOREIGN KEY (Prod_Id) REFERENCES PRODUCT(Id) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (GS_Longitude, GS_Latitude) REFERENCES GAS_STATION(Longitude, Latitude) ON UPDATE CASCADE ON DELETE CASCADE
                        );''')
            insertFromCsv("Datasets/offers.csv")
        except Exception as e:
            pass
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Prod_ID'], tuple['GS_Longitude'], tuple['GS_Latitude'], tuple['Quantity'], conn)
    conn.close()

def insertInto(prod_id, gs_longitude, gs_latitude, quantity, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO OFFERS
                            VALUES (?,?,?,?);''', (prod_id, gs_longitude, gs_latitude, quantity))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO OFFERS
                            VALUES (?,?,?,?);''', (prod_id, gs_longitude, gs_latitude, quantity))
            except Exception as e:
                pass

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from OFFERS")
    data = c.fetchall()
    conn.close()
    return data