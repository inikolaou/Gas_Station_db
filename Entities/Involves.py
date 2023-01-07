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
            insertFromCsv()
        except Exception as e:
            pass
    conn.close()


def insertFromCsv():
    fileName = "Datasets/involves.csv"
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Prod_ID'], tuple['Pur_ID'],
                       tuple['Quantity'], conn)
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
                pass  # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO INVOLVES
                            VALUES (?,?,?);''', (prod_id, pur_id, quantity))
            except Exception as e:
                print("INVOLVES")
                print(e)  # tuple already added
                print(prod_id, pur_id, quantity)


def searchBy(prod_id, pur_id, quantity):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (pur_id):
            c.execute('''
                SELECT * 
                FROM INVOLVES
                WHERE Pur_Id = ?''',
                      (pur_id, ))
        elif (prod_id):
            if (quantity):
                c.execute('''
                    SELECT * 
                    FROM INVOLVES
                    WHERE Prod_Id = ?, Quantity = ?''',
                          (prod_id, quantity))
            else:
                c.execute('''
                    SELECT * 
                    FROM INVOLVES
                    WHERE Prod_Id = ?''',
                          (prod_id, ))
        elif (quantity):
            c.execute('''
                SELECT * 
                FROM INVOLVES
                WHERE Quantity = ?''',
                      (quantity, ))
    data = c.fetchall()
    conn.close()
    return data


def update(prod_id, pur_id, quantity, previous_prod_id):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE INVOLVES
                        SET Prod_Id = ?, Quantity = ?
                        WHERE Prod_Id = ? AND Pur_Id = ?''',
                      (prod_id, quantity, previous_prod_id, pur_id))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()


def delete(prod_pur):
    prod_pur = prod_pur.split('_')
    prod_id = prod_pur[0]
    pur_id = prod_pur[1]
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''DELETE FROM INVOLVES
                        WHERE Prod_Id = ? AND Pur_Id = ?''',
                      (prod_id, pur_id))
        except Exception as e:
            print(e)
    conn.close()


def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from INVOLVES")
    data = c.fetchall()
    conn.close()
    return data
