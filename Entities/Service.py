import sqlite3
import csv


def createServiceTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE SERVICE
                        (Id                         INTEGER     NOT NULL,
                        Name                        TEXT        NOT NULL,
                        Price                       REAL        NOT NULL,
                        Corresponding_Points        INTEGER     NOT NULL,
                        PRIMARY KEY (Id))
                        ;''')
            insertFromCsv()
        except Exception as e:
            #print(e)
            pass # Table already created and data from csv has been passed to the database
    conn.close()


def insertFromCsv():
    fileName = "Datasets/service.csv"
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['ID'], tuple['Name'],
                       tuple['Price'], tuple['Corresponding_Points'], conn)
    conn.close()


def insertInto(id, name, price, points, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO SERVICE
                            VALUES (?,?,?,?);''', (id, name,
                                                   price, points))
            except Exception:
                pass  # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO SERVICE
                            VALUES (?,?,?,?);''', (id, name,
                                                   price, points))
            except Exception:
                pass


def searchBy(id, price, points):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (id):
            c.execute('''
                SELECT * 
                FROM SERVICE
                WHERE Id = ?''',
                      (id, ))
        elif (price):
            if (points):
                c.execute('''
                    SELECT * 
                    FROM SERVICE
                    WHERE Price = ? AND Corresponding_Points = ?''',
                          (price, points))
            else:
                c.execute('''
                    SELECT * 
                    FROM SERVICE
                    WHERE Price = ?''',
                          (price, ))
        elif (points):
            c.execute('''
                SELECT * 
                FROM SERVICE
                WHERE Corresponding_Points = ?''',
                      (points, ))
    data = c.fetchall()
    conn.close()
    return data


def update(id, name, price, points):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE SERVICE
                        SET Name = ?, Price = ?, Corresponding_Points = ?
                        WHERE Id = ?''',
                      (name, price, points, id))
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
            DELETE FROM SERVICE
            WHERE Id = ?''', (id, ))
        except Exception as e:
            print(e)
    conn.close()


def searchByName():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select Name from SERVICE")
    data = c.fetchall()
    conn.close()
    return data


def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from SERVICE")
    data = c.fetchall()
    conn.close()
    return data


def allServiceIds():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select Id from SERVICE")
    data = c.fetchall()
    conn.close()
    return data
