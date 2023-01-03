import sqlite3
import csv

def createSupplierTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE SUPPLIER
                        (Email          TEXT    NOT NULL,
                        Fname           TEXT    NOT NULL,
                        Lname           TEXT    NOT NULL,
                        Phone_Number    INTEGER         ,
                        Longitude       REAL    NOT NULL,
                        Latitude        REAL    NOT NULL,
                        PRIMARY KEY (Email))
                        ;''')
            insertFromCsv("Datasets/supplier.csv")
        except Exception as e:
            pass # Database created
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Email'], tuple['Fname'], tuple['Lname'],
                       tuple['Phone_Number'], tuple['Longitude'],
                       tuple['Latitude'], conn)
    conn.close()

def insertInto(email, fname, lname, phone_number, longitude, latitude, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO SUPPLIER
                            VALUES (?,?,?,?,?,?);''',
                            (email, fname, lname, phone_number,
                             longitude, latitude))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO SUPPLIER
                            VALUES (?,?,?,?,?,?);''',
                            (email, fname, lname, phone_number,
                             longitude, latitude))
            except Exception:
                pass
            
def searchBy(email, phone_number, longitude, latitude):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (email):
            c.execute('''
                        SELECT * 
                        FROM SUPPLIER
                        WHERE Email = ?''',
                        (email, ))
        elif (phone_number):
            c.execute('''
                    SELECT * 
                    FROM SUPPLIER
                    WHERE Phone_Number = ?''',
                    (phone_number, ))
        elif (longitude and latitude):
            c.execute('''
                    SELECT * 
                    FROM SUPPLIER
                    WHERE Longitude = ? AND Latitude = ?''',
                    (longitude, latitude))
    data = c.fetchall()
    conn.close()
    return data

def update(email, fname, lname, phone_number, longitude, latitude):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE SUPPLIER
                        SET Fname = ?, Lname = ?, Phone_Number = ?,
                        Longitude = ?, Latitude = ? WHERE Email = ?''', 
                        (fname, lname, phone_number, longitude,
                         latitude, email))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()

def delete(email):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''
            DELETE FROM SUPPLIER
            WHERE Email = ?
            ''', (email, ))
        except Exception as e:
            print(e)
    conn.close()

def searchByName():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select Fname from SUPPLIER")
    data = c.fetchall()
    conn.close()
    return data

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from SUPPLIER")
    data = c.fetchall()
    conn.close()
    return data