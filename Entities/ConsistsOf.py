import sqlite3
import csv

def createIsAssignedToTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE IS_ASSIGNED_TO
                        (Serv_Id    INTEGER         NOT NULL,
                        Essn        TEXT            NOT NULL,
                        FOREIGN KEY (Serv_Id)       REFERENCES SERVICE(Id)   ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (Essn)          REFERENCES EMPLOYEE(Ssn) ON UPDATE CASCADE ON DELETE CASCADE
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
            insertInto(tuple['Serv_ID'], tuple['Essn'], conn)
    conn.close()

def insertInto(serv_id, essn, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO IS_ASSIGNED_TO
                            VALUES (?,?);''', (serv_id, essn))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO IS_ASSIGNED_TO
                            VALUES (?,?);''', (serv_id, essn))
            except Exception as e:
                pass

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from IS_ASSIGNED_TO")
    data = c.fetchall()
    conn.close()
    return data