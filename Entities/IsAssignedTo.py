import sqlite3
import csv


def createIsAssignedToTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE IS_ASSIGNED_TO
                        (
                        Essn        TEXT               NOT NULL,
                        Serv_Id     INTEGER            NOT NULL,
                        FOREIGN KEY (Serv_Id)       REFERENCES SERVICE(Id)   ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (Essn)          REFERENCES EMPLOYEE(Ssn) ON UPDATE CASCADE ON DELETE CASCADE
                        );''')
            insertFromCsv()
        except Exception as e:
            print(e)
    conn.close()


def insertFromCsv():
    fileName = "Datasets/is_assigned_to.csv"
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Essn'], tuple['Serv_ID'],  conn)
    conn.close()


def insertInto(essn, serv_id, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO IS_ASSIGNED_TO
                            VALUES (?,?);''', (essn, serv_id))
            except Exception:
                pass  # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO IS_ASSIGNED_TO
                            VALUES (?,?);''', (essn, serv_id))
            except Exception as e:
                print("IS ASSIGNED TO")
                print(e)  # tuple already added
                print(essn, serv_id)


def searchBy(essn, service_id):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (essn):
            if (service_id):
                c.execute('''
                        SELECT * 
                        FROM IS_ASSIGNED_TO
                        WHERE Essn = ? AND Serv_Id = ?''',
                          (essn, service_id))
            else:
                c.execute('''
                        SELECT * 
                        FROM IS_ASSIGNED_TO
                        WHERE Essn = ?''',
                          (essn, ))
        else:
            c.execute('''
                    SELECT * 
                    FROM IS_ASSIGNED_TO
                    WHERE Serv_Id = ?''',
                      (service_id, ))
    data = c.fetchall()
    conn.close()
    return data


def update(essn, service_id, previous_service_id):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE IS_ASSIGNED_TO
                        SET Serv_Id = ?
                        WHERE Essn = ? AND Serv_Id = ?''',
                      (service_id, essn, previous_service_id))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()


def delete(essn_servid):
    essn_servid = essn_servid.split('_')
    essn = essn_servid[0]
    service_id = essn_servid[1]
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''DELETE FROM IS_ASSIGNED_TO
                        WHERE Essn = ? AND Serv_Id = ?''',
                      (essn, service_id))
        except Exception as e:
            print(e)
    conn.close()


def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from IS_ASSIGNED_TO")
    data = c.fetchall()
    conn.close()
    return data
