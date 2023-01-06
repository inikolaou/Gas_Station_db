import sqlite3
import csv

def createCustomerTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE CUSTOMER
                        (Email              TEXT        NOT NULL,
                        Fname               TEXT        NOT NULL,
                        Lname               TEXT        NOT NULL,
                        Birth_Date          TEXT        NOT NULL,
                        Phone_Number        INTEGER     NOT NULL,
                        Longitude           REAL        NOT NULL,
                        Latitude            REAL        NOT NULL,
                        Remaining_Points    INTEGER     DEFAULT 0,
                        PRIMARY KEY (Email)
                        );''')
            insertFromCsv("Datasets/customer.csv")
        except Exception as e:
            pass # Database created
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Email'], tuple['Fname'], tuple['Lname'],
                       tuple['Birth_Date'],tuple['Phone_Number'],
                       tuple['Longitude'],tuple['Latitude'],
                       tuple['Remaining_Points'], conn)
    conn.close()

def insertInto(email, fname, lname, birth_date, phone_number, longitude, latitude, 
        rem_points, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO CUSTOMER
                            VALUES (?,?,?,?,?,?,?,?);''', 
                            (email, fname, lname, birth_date, phone_number,
                            longitude, latitude, rem_points))
            except Exception as e:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO CUSTOMER
                            VALUES (?,?,?,?,?,?,?,?);''', 
                            (email, fname, lname, birth_date, phone_number,
                            longitude, latitude, rem_points))
            except Exception as e:
                pass

def searchBy(email, phone_number, rem_points):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (email):
            c.execute('''
                        SELECT * 
                        FROM CUSTOMER
                        WHERE Email = ?''',
                        (email, ))
        elif (phone_number):
            if (rem_points):
                c.execute('''
                    SELECT * 
                    FROM CUSTOMER
                    WHERE Phone_Number = ? AND Remaining_Points = ?''',
                    (phone_number, rem_points))
            else:
                c.execute('''
                        SELECT * 
                        FROM CUSTOMER
                        WHERE Phone_Number = ?''',
                        (phone_number, ))
        else:
            c.execute('''
                SELECT * 
                FROM CUSTOMER
                WHERE Remaining_Points = ?''',
                (rem_points, ))

    data = c.fetchall()
    conn.close()
    return data

def update(email, fname, lname, birth_date, phone_number, longitude, latitude, 
        rem_points):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE CUSTOMER
                        SET Fname = ?, Lname = ?, Birth_Date = ?,
                        Phone_Number = ?, Longitude = ?, Latitude = ?,
                        Remaining_Points = ? WHERE Email = ?''', 
                        (fname, lname, birth_date, phone_number, longitude,
                        latitude, rem_points, email))
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
            DELETE FROM CUSTOMER
            WHERE Email = ?
            ''', (email, ))
        except Exception as e:
            print(e)
    conn.close()

def searchByName():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select Fname from CUSTOMER")
    data = c.fetchall()
    conn.close()
    return data

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from CUSTOMER")
    data = c.fetchall()
    conn.close()
    return data

def allCustomerEmails():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select Email from CUSTOMER")
    data = c.fetchall()
    conn.close()
    return data

def allCustomerNames():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select Name from CUSTOMER")
    data = c.fetchall()
    conn.close()
    return data

def allCustomerPhoneNumbers():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select Phone_Number from CUSTOMER")
    data = c.fetchall()
    conn.close()
    return data