import sqlite3
import csv
import pandas as pd

df = pd.read_csv("gas_station.csv")
li = []
for date in df['Start_Date']:
    numbers = date.split('/')
    if (len(numbers[0]) == 1):
        if (len(numbers[1]) == 1):
            day = '0' + numbers[0]
            month = '0' + numbers[1]
        else:
            day = '0' + numbers[0]
            month = numbers[1]
    else:
        if (len(numbers[1]) == 1):
            day = numbers[0]
            month = '0' + numbers[1]
        else:
            day = numbers[0]
            month = numbers[1]
    correct_date = '/'.join([day, month, numbers[2]])
    li.append(correct_date)
df['Start_Date'] = li
df.to_csv("gas_station.csv", index=False)

def createGasStationTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE GAS_STATION
                        (Longitude                  REAL        NOT NULL,
                        Latitude                    REAL        NOT NULL,
                        Type_of_Service             TEXT        NOT NULL,
                        Start_Date                  TEXT        NOT NULL,
                        Minimarket                  INTEGER     NOT NULL DEFAULT 0,
                        Mgr_Ssn                     TEXT,
                        PRIMARY KEY (Longitude, Latitude),
                        FOREIGN KEY (Mgr_Ssn) REFERENCES EMPLOYEE(Ssn) ON UPDATE CASCADE ON DELETE SET NULL
                        );''')
            insertFromCsv("Datasets/gas_station.csv")
        except Exception as e:
            pass # Database created
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
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

def searchBy(longitude, latitude, type_of_service, minimarket, mgr_ssn):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (longitude and latitude):
            c.execute('''
                    SELECT * 
                    FROM GAS_STATION
                    WHERE Longitude = ? AND Latitude = ?''',
                    (longitude, latitude))
        elif (type_of_service):
            if (minimarket):
                if (mgr_ssn):
                    c.execute('''
                    SELECT * 
                    FROM GAS_STATION
                    WHERE Type_of_Service = ? AND Minimarket = ? AND Mgr_Ssn = ?''',
                    (type_of_service, minimarket, mgr_ssn))
                else:
                    c.execute('''
                    SELECT * 
                    FROM GAS_STATION
                    WHERE Type_of_Service = ? AND Minimarket = ?''',
                    (type_of_service, minimarket))
            elif (mgr_ssn):
                c.execute('''
                    SELECT * 
                    FROM GAS_STATION
                    WHERE Type_of_Service = ? AND Mgr_Ssn = ?''',
                    (type_of_service, mgr_ssn))
            else:
                c.execute('''
                    SELECT * 
                    FROM GAS_STATION
                    WHERE Type_of_Service = ?''',
                    (type_of_service, ))
        elif (minimarket):
            if (mgr_ssn):
                c.execute('''
                    SELECT * 
                    FROM GAS_STATION
                    WHERE Minimarket = ? AND Mgr_Ssn = ?''',
                    (minimarket, mgr_ssn))
            else:
                c.execute('''
                    SELECT * 
                    FROM GAS_STATION
                    WHERE Minimarket = ?''',
                    (minimarket, ))
        else:
            c.execute('''
                    SELECT * 
                    FROM GAS_STATION
                    WHERE Mgr_Ssn = ?''',
                    (mgr_ssn, ))
    data = c.fetchall()
    conn.close()
    return data

def update(longitude, latitude, type_of_service, start_date, minimarket, mgr_ssn):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE GAS_STATION
                        SET Type_of_Service = ?, Start_Date = ?, 
                            Minimarket = ?, Mgr_Ssn = ?
                        WHERE Longitude = ? AND Latitude = ?''', 
                        (type_of_service, start_date, minimarket, mgr_ssn, longitude, latitude))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()

def delete(longitude_latitude):
    longitude_latitude = longitude_latitude.split('_')
    longitude = longitude_latitude[0]
    latitude = longitude_latitude[1]
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''DELETE FROM
                        GAS_STATION WHERE
                        Longitude = ? AND Latitude = ?''', (longitude, latitude))
        except Exception as e:
            print(e)
    conn.close()

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from GAS_STATION")
    data = c.fetchall()
    conn.close()
    return data