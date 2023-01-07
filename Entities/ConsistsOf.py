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
            insertFromCsv()
        except Exception as e:
            print(e)
    conn.close()


def insertFromCsv():
    fileName = "Datasets/consists_of.csv"
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Supply_ID'], tuple['Prod_ID'],
                       tuple['Cost'], tuple['Quantity'], conn)
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
                pass  # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO CONSISTS_OF
                            VALUES (?,?,?,?);''', (supply_id, prod_id, cost, quantity))
            except Exception as e:
                print("CONSISTS OF")
                print(e)  # tuple already added
                print(supply_id, prod_id, cost, quantity)


def searchBy(supply_id, prod_id, cost, quantity):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (supply_id):
            if (prod_id):
                c.execute('''
                    SELECT * 
                    FROM CONSISTS_OF
                    WHERE Supply_Id = ? AND Prod_Id = ?''',
                          (supply_id, prod_id))
            else:
                c.execute('''
                    SELECT * 
                    FROM CONSISTS_OF
                    WHERE Supply_Id = ?''',
                          (supply_id, ))
        elif (prod_id):
            if (cost):
                if (quantity):
                    c.execute('''
                        SELECT * 
                        FROM CONSISTS_OF
                        WHERE Prod_Id = ? AND Cost = ? AND Quantity = ?''',
                              (prod_id, cost, quantity))
                else:
                    c.execute('''
                        SELECT * 
                        FROM CONSISTS_OF
                        WHERE Prod_Id = ? AND Cost = ?''',
                              (prod_id, cost))
            else:
                c.execute('''
                    SELECT * 
                    FROM CONSISTS_OF
                    WHERE Prod_Id = ?''',
                          (prod_id, ))
        elif (cost):
            if (quantity):
                c.execute('''
                    SELECT * 
                    FROM CONSISTS_OF
                    WHERE Cost = ? AND Quantity = ?''',
                          (cost, quantity))
            else:
                c.execute('''
                    SELECT * 
                    FROM CONSISTS_OF
                    WHERE Cost = ?''',
                          (cost, ))
        elif (quantity):
            c.execute('''
                SELECT * 
                FROM CONSISTS_OF
                WHERE Quantity = ?''',
                      (quantity, ))

    data = c.fetchall()
    conn.close()
    return data


def update(supply_id, prod_id, cost, quantity, previous_prod_id):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE CONSISTS_OF
                        SET Prod_Id = ?, Cost = ?, Quantity = ?
                        WHERE Supply_Id = ? AND Prod_Id = ?''',
                      (prod_id, cost, quantity, supply_id, previous_prod_id))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()


def delete(supply_prod):
    supply_prod = supply_prod.split('_')
    supply_id = supply_prod[0]
    prod_id = supply_prod[1]
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''DELETE FROM CONSISTS_OF
                        WHERE Supply_Id = ? AND Prod_Id = ?''',
                      (supply_id, prod_id))
        except Exception as e:
            print(e)
    conn.close()


def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from CONSISTS_OF")
    data = c.fetchall()
    conn.close()
    return data
