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
            pass  # Database created
    conn.close()


def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
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
                pass  # tuple already added
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


def searchBy(id, last_check, capacity, quantity, product_id, longitude, latitude):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (id):
            if (longitude and latitude):
                c.execute('''
                        SELECT * 
                        FROM TANK
                        WHERE Id = ? AND GS_Longitude = ? AND GS_Latitude = ?''',
                          (id, longitude, latitude))
            else:
                c.execute('''
                        SELECT * 
                        FROM TANK
                        WHERE Id = ?''',
                          (id, ))
        elif (longitude and latitude):
            c.execute('''
                    SELECT * 
                    FROM TANK
                    WHERE GS_Longitude = ? AND GS_Latitude = ?''',
                      (longitude, latitude))
        elif (last_check):
            if (capacity):
                if (quantity):
                    if (product_id):
                        c.execute('''
                                SELECT * 
                                FROM TANK
                                WHERE Last_Check_Up = ? AND Capacity = ? AND Quantity = ?
                                AND Prod_Id = ?''',
                                  (last_check, capacity, quantity, product_id))
                    else:
                        c.execute('''
                                SELECT * 
                                FROM TANK
                                WHERE Last_Check_Up = ? AND Capacity = ? AND Quantity = ?''',
                                  (last_check, capacity, quantity))
                else:
                    c.execute('''
                                SELECT * 
                                FROM TANK
                                WHERE Last_Check_Up = ? AND Capacity = ? AND Prod_Id = ?''',
                              (last_check, capacity, product_id))
            elif (quantity):
                if (product_id):
                    c.execute('''
                                SELECT * 
                                FROM TANK
                                WHERE Last_Check_Up = ? AND Quantity = ?
                                AND Prod_Id = ?''',
                              (last_check, quantity, product_id))
                else:
                    c.execute('''
                                SELECT * 
                                FROM TANK
                                WHERE Last_Check_Up = ? AND Quantity = ?''',
                              (last_check, quantity))
            elif (product_id):
                c.execute('''
                            SELECT * 
                            FROM TANK
                            WHERE Last_Check_Up = ? AND Prod_Id = ?''',
                          (last_check, product_id))
            else:
                c.execute('''
                            SELECT * 
                            FROM TANK
                            WHERE Last_Check_Up = ? ''',
                          (last_check, ))
        elif (capacity):
            if (quantity):
                if (product_id):
                    c.execute('''
                            SELECT * 
                            FROM TANK
                            WHERE Capacity = ? AND Quantity = ?
                            AND Prod_Id = ?''',
                              (capacity, quantity, product_id))
                else:
                    c.execute('''
                            SELECT * 
                            FROM TANK
                            WHERE Capacity = ? AND Quantity = ?''',
                              (capacity, quantity))
            elif (product_id):
                c.execute('''
                        SELECT * 
                        FROM TANK
                        WHERE Capacity = ? AND Prod_Id = ?''',
                          (capacity, product_id))
            else:
                c.execute('''
                        SELECT * 
                        FROM TANK
                        WHERE Capacity = ?''',
                          (capacity, ))
        elif (quantity):
            if (product_id):
                c.execute('''
                        SELECT * 
                        FROM TANK
                        WHERE Quantity = ? AND Prod_Id = ?''',
                          (quantity, product_id))
            else:
                c.execute('''
                        SELECT * 
                        FROM TANK
                        WHERE Quantity = ?''',
                          (quantity, ))
        else:
            c.execute('''
                    SELECT * 
                    FROM TANK
                    WHERE Prod_Id = ?''',
                      (product_id, ))

    data = c.fetchall()
    conn.close()
    return data


def update(id, last_check, capacity, quantity, product_id, longitude, latitude):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE TANK
                        SET Last_Check_Up = ?, Capacity = ?, Quantity = ?,
                        Prod_Id = ? 
                        WHERE Id = ? AND GS_Longitude = ? AND GS_Latitude = ?''',
                      (last_check, capacity, quantity, product_id, id, longitude, latitude))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()


def delete(id_longitude_latitude):
    id_longitude_latitude = id_longitude_latitude.split('_')
    id = id_longitude_latitude[0]
    longitude = id_longitude_latitude[1]
    latitude = id_longitude_latitude[2]
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''DELETE FROM
                        TANK WHERE
                        Id = ? AND GS_Longitude = ? AND GS_Latitude = ?''',
                      (id, longitude, latitude))
        except Exception as e:
            print(e)
    conn.close()


def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from TANK")
    data = c.fetchall()
    conn.close()
    return data

def allTankIds():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select Id from TANK")
    data = c.fetchall()
    conn.close()
    return data