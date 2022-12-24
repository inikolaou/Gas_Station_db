import sqlite3
import csv

def createInvolvesTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE INVOLVES 
                        (Prod_Id    INTEGER     NOT NULL,
                        Pur_Id      INTEGER     NOT NULL,
                        Quantity    REAL        NOT NULL,
                        PRIMARY KEY (Prod_Id, Pur_Id),
                        FOREIGN KEY (Prod_Id) REFERENCES PRODUCT(Id) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (Pur_Id) REFERENCES PURCHASE(Id) ON UPDATE CASCADE ON DELETE CASCADE
                        );''')
            insertFromCsv("Datasets/involves.csv")
        except Exception as e:
            pass
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Prod_ID'], tuple['Pur_ID'], tuple['Quantity'], conn)
    conn.close()

def insertInto(prod_id, pur_id, quantity, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO INVOLVES
                            VALUES (?,?,?);''', (prod_id, pur_id, quantity))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO INVOLVES
                            VALUES (?,?,?);''', (prod_id, pur_id, quantity))
            except Exception as e:
                pass

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from INVOLVES")
    data = c.fetchall()
    conn.close()
    return data