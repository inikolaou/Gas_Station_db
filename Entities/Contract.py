import sqlite3
import csv

def createContractTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        c.execute('''CREATE TABLE IF NOT EXISTS CONTRACT
                    (Id             INTEGER     NOT NULL,
                    Start_Date      TEXT        NOT NULL,
                    End_Date        TEXT        NOT NULL,
                    Salary          REAL        NOT NULL,
                    PRIMARY KEY (Id));''')
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['id'], tuple['Start_Date'],
                        tuple['End_Date'], tuple['Salary'], conn)
    conn.close()

def insertInto(id, start_date, end_date, salary, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO CONTRACT
                            VALUES (?,?,?,?);''', (id, start_date,
                            end_date, salary))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO CONTRACT
                            VALUES (?,?,?,?);''', (id, start_date,
                            end_date, salary))
            except Exception:
                pass

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from CONTRACT")
    data = c.fetchall()
    conn.close()
    return data