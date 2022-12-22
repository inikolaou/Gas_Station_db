import sqlite3
import csv

def createGasStationTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE GAS_STATION
                        (
                        Longitude                   REAL        NOT NULL,
                        Latitude                    REAL        NOT NULL,
                        Type_of_Service             TEXT        NOT NULL,
                        Start_Date                  TEXT        NOT NULL,
                        Minimarket                  INTEGER     NOT NULL,
                        Mgr_Ssn                     TEXT        ,
                        PRIMARY KEY (Longitude, Latitude),
                        FOREIGN KEY (Mgr_Ssn) REFERENCES EMPLOYEE(Ssn) ON UPDATE CASCADE ON DELETE SET NULL
                        );''')
            insertFromCsv("Datasets/gas_station.csv")
        except Exception as e:
            pass # Database created
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Longitude'], tuple['Latitude'], tuple['Type_of_Service'],
                        tuple['Start_Date'], tuple['Minimarket'], tuple['Mgr_Ssn'], conn)
    conn.close()

def insertInto(longitude, latitude, type_of_service, start_date, minimarket, mgr_ssn, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO GAS_STATION
                            VALUES (?,?,?,?,?,?);''', (longitude, latitude, type_of_service,
                            start_date, minimarket, mgr_ssn))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO GAS_STATION
                            VALUES (?,?,?,?,?,?);''', (longitude, latitude, type_of_service,
                            start_date, minimarket, mgr_ssn))
            except Exception:
                pass

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from GAS_STATION")
    data = c.fetchall()
    conn.close()
    return data