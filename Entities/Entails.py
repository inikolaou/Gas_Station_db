import sqlite3
import csv

def createEntailsTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE ENTAILS 
                        (Serv_ID    INTEGER     NOT NULL,
                        Pur_ID      INTEGER     NOT NULL,
                        PRIMARY KEY (Serv_ID, Pur_ID),
                        FOREIGN KEY (Serv_Id) REFERENCES SERVICE(Id) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (Pur_Id) REFERENCES PURCHASE(Id) ON UPDATE CASCADE ON DELETE CASCADE
                        );''')
            insertFromCsv("Datasets/entails.csv")
        except Exception as e:
            pass
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Serv_ID'], tuple['Pur_ID'], conn)
    conn.close()

def insertInto(serv_id, pur_id, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO ENTAILS
                            VALUES (?,?);''', (serv_id, pur_id))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO ENTAILS
                            VALUES (?,?);''', (serv_id, pur_id))
            except Exception as e:
                pass

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from ENTAILS")
    data = c.fetchall()
    conn.close()
    return data