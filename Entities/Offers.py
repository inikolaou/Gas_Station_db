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
            insertFromCsv()
        except Exception as e:
            print(e)
    conn.close()


def insertFromCsv():
    fileName = "Datasets/offers.csv"
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Prod_ID'], tuple['GS_Longitude'],
                       tuple['GS_Latitude'], tuple['Quantity'], conn)
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
                pass  # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO OFFERS
                            VALUES (?,?,?,?);''', (prod_id, gs_longitude, gs_latitude, quantity))
            except Exception as e:
                pass


def searchBy(prod_id, gs_longitude, gs_latitude, quantity):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (prod_id):
            if (gs_longitude and gs_latitude):
                c.execute('''
                        SELECT * 
                        FROM OFFERS
                        WHERE Prod_Id = ? AND GS_Longitude = ? AND GS_Latitude = ?''',
                          (prod_id, gs_longitude, gs_latitude))
            else:
                c.execute('''
                        SELECT * 
                        FROM OFFERS
                        WHERE Prod_Id = ?''',
                          (prod_id, ))
        elif (gs_longitude and gs_latitude):
            c.execute('''
                    SELECT * 
                    FROM OFFERS
                    WHERE GS_Longitude = ? AND GS_Latitude = ?''',
                      (gs_longitude, gs_latitude))
        else:
            c.execute('''
                        SELECT * 
                        FROM OFFERS
                        WHERE Quantity = ?''',
                      (quantity, ))

    data = c.fetchall()
    conn.close()
    return data


def update(prod_id, previous_prod_id, gs_longitude, gs_latitude, quantity):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE OFFERS
                        SET Prod_Id = ?, Quantity = ?
                        WHERE Prod_Id = ? AND GS_Longitude = ? AND GS_Latitude = ?''',
                      (prod_id, quantity, previous_prod_id, gs_longitude, gs_latitude))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()


def delete(prodid_longitude_latitude):
    prodid_longitude_latitude = prodid_longitude_latitude.split('_')
    prod_id = prodid_longitude_latitude[0]
    gs_longitude = prodid_longitude_latitude[1]
    gs_latitude = prodid_longitude_latitude[2]
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''DELETE FROM
                        OFFERS WHERE
                        Prod_Id = ? AND GS_Longitude = ? AND GS_Latitude = ?''',
                      (prod_id, gs_longitude, gs_latitude))
        except Exception as e:
            print(e)
    conn.close()


def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from OFFERS")
    data = c.fetchall()
    conn.close()
    return data
