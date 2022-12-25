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
            insertFromCsv("Datasets/service.csv")
        except Exception as e:
            pass # Database created
    conn.close()

def insertFromCsv(fileName):
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
                pass # tuple already added
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

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from SERVICE")
    data = c.fetchall()
    conn.close()
    return data