import sqlite3
import csv

def createProductTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE PRODUCT
                        (Id                         INTEGER     NOT NULL,
                        Name                        TEXT        NOT NULL,
                        Type                        TEXT        NOT NULL,
                        Price                       REAL        NOT NULL,
                        Corresponding_Points        INTEGER     NOT NULL,
                        PRIMARY KEY (Id))
                        ;''')
            insertFromCsv("Datasets/product.csv")
        except Exception as e:
            pass # Database created
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['ID'], tuple['Name'], tuple['Type'],
                        tuple['Price'], tuple['Corresponding_Points'], conn)
    conn.close()

def insertInto(id, name, type, price, points, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO PRODUCT
                            VALUES (?,?,?,?,?);''',
                            (id, name, type, price, points))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO PRODUCT
                            VALUES (?,?,?,?,?);''',
                            (id, name, type, price, points))
            except Exception:
                pass
            
def searchBy(id, type, price, points):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (id):
            c.execute('''
                SELECT * 
                FROM PRODUCT
                WHERE Id = ?''',
                (id, ))
        elif (type):
            if (price):
                if (points):
                    c.execute('''
                        SELECT * 
                        FROM PRODUCT
                        WHERE Type = ? AND Price = ? AND Corresponding_Points = ?''',
                        (type, price, points))
                else:
                    c.execute('''
                        SELECT * 
                        FROM PRODUCT
                        WHERE Type = ? AND Price = ?''',
                        (type, price))
            elif (type):
                c.execute('''
                    SELECT * 
                    FROM PRODUCT
                    WHERE Type = ?''',
                    (type, ))
        elif (points):
            c.execute('''
                SELECT * 
                FROM PRODUCT
                WHERE Corresponding_Points = ?''',
                (points, ))
        elif (price):
            c.execute('''
                SELECT * 
                FROM PRODUCT
                WHERE Price = ?''',
                (price, ))
    data = c.fetchall()
    conn.close()
    return data

def update(id, name, type, price, points):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE PRODUCT
                        SET Name = ?, Type = ?,
                        Price = ?, Corresponding_Points = ?
                        WHERE Id = ?''',
                        (name, type, price, points, id))
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
            c.execute('''
            DELETE FROM PRODUCT
            WHERE Id = ?''', (id, ))
        except Exception as e:
            print(e)
    conn.close()

def searchByName():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select Name from PRODUCT")
    data = c.fetchall()
    conn.close()
    return data

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from PRODUCT")
    data = c.fetchall()
    conn.close()
    return data