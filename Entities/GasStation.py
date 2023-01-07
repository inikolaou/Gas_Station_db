import sqlite3
import csv


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
            insertFromCsv()
        except Exception as e:
            print(e)
    conn.close()


def insertFromCsv():
    fileName = "Datasets/gas_station.csv"
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
                pass  # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO GAS_STATION
                            VALUES (?,?,?,?,?,?);''', (longitude, latitude, type_of_service,
                                                       start_date, minimarket, mgr_ssn))
            except Exception as e:
                print("GAS STATION")
                print(longitude, latitude)
                print(e)  # tuple already added


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


def allGSLongitudesLatitudes():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select Longitude, Latitude from GAS_STATION")
    data = c.fetchall()
    conn.close()
    return data


def allTypesOfService():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select DISTINCT Type_of_Service from GAS_STATION")
    data = c.fetchall()
    conn.close()
    return data


def getGSLongitudeLatitudeNoMinimarketSelf():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute('''
                SELECT Longitude, Latitude
                FROM GAS_STATION
                WHERE Type_of_Service='Self Service' AND Minimarket=0
                ''')
    data = c.fetchall()
    conn.close()
    return data
