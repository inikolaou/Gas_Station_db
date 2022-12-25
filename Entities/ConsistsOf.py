import sqlite3
import csv

def createConsistsOfTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE CONSISTS_OF 
                        (Supply_Id  INTEGER     NOT NULL,
                        Prod_Id     INTEGER     NOT NULL,
                        Cost        REAL        NOT NULL,
                        Quantity    REAL        NOT NULL,
                        PRIMARY KEY (Supply_Id, Prod_Id),
                        FOREIGN KEY (Supply_Id) REFERENCES SUPPLY(Id) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (Prod_Id) REFERENCES PRODUCT(Id) ON UPDATE CASCADE ON DELETE CASCADE
                        );''')
            insertFromCsv("Datasets/consists_of.csv")
        except Exception as e:
            pass
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Supply_ID'], tuple['Prod_ID'], tuple['Cost'], tuple['Quantity'], conn)
    conn.close()

def insertInto(supply_id, prod_id, cost, quantity, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO CONSISTS_OF
                            VALUES (?,?,?,?);''', (supply_id, prod_id, cost, quantity))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO CONSISTS_OF
                            VALUES (?,?,?,?);''', (supply_id, prod_id, cost, quantity))
            except Exception as e:
                pass

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from CONSISTS_OF")
    data = c.fetchall()
    conn.close()
    return data