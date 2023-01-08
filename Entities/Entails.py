import sqlite3
import csv


def createEntailsTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE ENTAILS 
                        (Serv_Id    INTEGER     NOT NULL,
                        Pur_Id      INTEGER     NOT NULL,
                        PRIMARY KEY (Serv_Id, Pur_Id),
                        FOREIGN KEY (Serv_Id) REFERENCES SERVICE(Id) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (Pur_Id) REFERENCES PURCHASE(Id) ON UPDATE CASCADE ON DELETE CASCADE
                        );''')
            insertFromCsv()
        except Exception as e:
            #print(e)
            pass # Table already created and data from csv has been passed to the database
    conn.close()


def insertFromCsv():
    fileName = "Datasets/entails.csv"
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
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
                pass  # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO ENTAILS
                            VALUES (?,?);''', (serv_id, pur_id))
            except Exception as e:
                print("ENTAILS")
                print(e)  # tuple already added


def searchBy(serv_id, pur_id):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (pur_id):
            c.execute('''
                SELECT * 
                FROM ENTAILS
                WHERE Pur_Id = ?''',
                      (pur_id, ))
        elif (serv_id):
            c.execute('''
                SELECT * 
                FROM ENTAILS
                WHERE Serv_Id = ?''',
                      (serv_id, ))
    data = c.fetchall()
    conn.close()
    return data


def update(serv_id, pur_id, previous_serv_id):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE ENTAILS
                        SET Serv_Id = ?
                        WHERE Pur_Id = ? AND Serv_Id = ?''',
                      (serv_id, pur_id, previous_serv_id))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()


def delete(serv_pur):
    serv_pur = serv_pur.split('_')
    serv_id = serv_pur[0]
    pur_id = serv_pur[1]
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''DELETE FROM ENTAILS
                        WHERE Serv_Id = ? AND Pur_Id = ?''',
                      (serv_id, pur_id))
        except Exception as e:
            print(e)
    conn.close()


def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from ENTAILS")
    data = c.fetchall()
    conn.close()
    return data
