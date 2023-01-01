import sqlite3
import csv

def createSignsTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE SIGNS
                        (Essn           TEXT        NOT NULL,
                        Contract_Id     INTEGER     NOT NULL DEFAULT 3,
                        FOREIGN KEY (Essn)  REFERENCES EMPLOYEE(Ssn) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (Contract_Id) REFERENCES CONTRACT(Id) ON UPDATE CASCADE ON DELETE SET DEFAULT
                        );''')
            insertFromCsv("Datasets/signs.csv")
        except Exception as e:
            pass # Database created
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Essn'], tuple['Contract_ID'], conn)
    conn.close()

def insertInto(essn, contract_id, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO SIGNS
                            VALUES (?,?);''', (essn, contract_id))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO SIGNS
                            VALUES (?,?);''', (essn, contract_id))
            except Exception:
                pass

def searchBy(essn, contract_id):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (essn):
            if (contract_id):
                c.execute('''
                        SELECT * 
                        FROM SIGNS
                        WHERE Essn = ? AND Contract_Id = ?''',
                        (essn, contract_id))
            else:
                c.execute('''
                        SELECT * 
                        FROM SIGNS
                        WHERE Essn = ?''',
                        (essn, ))
        else:
            c.execute('''
                    SELECT * 
                    FROM SIGNS
                    WHERE Contract_Id = ?''',
                    (contract_id, ))
    data = c.fetchall()
    conn.close()
    return data

def update(essn, contract_id, previous_contract_id):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE SIGNS
                        SET Contract_Id = ?
                        WHERE Essn = ? AND Contract_Id = ?''', 
                        (contract_id, essn, previous_contract_id))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()

def delete(essn_contract):
    essn_contract = essn_contract.split('_')
    essn = essn_contract[0]
    contract_id = essn_contract[1]
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''DELETE FROM
                        SIGNS WHERE
                        Essn = ? AND Contract_Id = ?''', (essn, contract_id))
        except Exception as e:
            print(e)
    conn.close()

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from SIGNS")
    data = c.fetchall()
    conn.close()
    return data