import sqlite3
import csv

def createEmployeeTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE EMPLOYEE
                        (Ssn            TEXT        NOT NULL    ,
                        Fname           TEXT        NOT NULL    ,
                        Lname           TEXT        NOT NULL    ,
                        Birth_Date      TEXT        NOT NULL    ,
                        Phone_Number    INTEGER     NOT NULL    ,
                        Email           TEXT        NOT NULL    ,
                        Longitude       REAL        NOT NULL    ,
                        Latitude        REAL        NOT NULL    ,
                        Role            TEXT        NOT NULL    ,
                        Hours           INTEGER     NOT NULL    ,
                        Super_Ssn       TEXT        DEFAULT NULL,
                        GS_Longitude    REAL                    ,
                        GS_Latitude     REAL                    ,
                        PRIMARY KEY (Ssn),
                        FOREIGN KEY (Super_Ssn)    REFERENCES EMPLOYEE(Ssn) ON UPDATE CASCADE ON DELETE SET NULL,
                        FOREIGN KEY (GS_Longitude, GS_Latitude) REFERENCES GAS_STATION(Longitude, Latitude) ON UPDATE CASCADE ON DELETE SET NULL
                        );''')
            insertFromCsv("Datasets/employee.csv")
        except Exception as e:
            pass # Database created
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Ssn'], tuple['Fname'], tuple['Lname'],
                       tuple['Birth_Date'],tuple['Phone_Number'], tuple['Email'],
                       tuple['Longitude'], tuple['Latitude'], tuple['Role'],
                       tuple['Hours'], tuple['Super_Ssn'], tuple['GS_Longitude'],
                       tuple['GS_Latitude'], conn)
    conn.close()

def insertInto(ssn, fname, lname, birth_date, phone_number, email, longitude, latitude, 
        role, hours, super_ssn, gs_longitude, gs_latitude, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO EMPLOYEE
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);''', 
                            (ssn, fname, lname, birth_date, phone_number, email,
                            longitude, latitude, role, hours, super_ssn,
                            gs_longitude, gs_latitude))
            except Exception as e:
                print(e) # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO EMPLOYEE
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);''', 
                            (ssn, fname, lname, birth_date, phone_number, email,
                            longitude, latitude, role, hours, super_ssn,
                            gs_longitude, gs_latitude))
            except Exception as e:
                pass

def update(ssn, fname, lname, email, birth_date, phone_number, longitude, latitude, 
        role, hours, super_ssn, gs_longitude, gs_latitude):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE EMPLOYEE
                        SET Fname = ?, Lname = ?, Birth_Date = ?,
                        Phone_Number = ?, Email = ?, Longitude = ?,
                        Latitude = ?, Role = ?, Hours = ?, Super_Ssn = ?,
                        GS_Longitude = ?, GS_Latitude = ? WHERE Ssn = ?''', 
                        (fname, lname, birth_date, phone_number, email,
                        longitude, latitude, role, hours, super_ssn,
                        gs_longitude, gs_latitude, ssn))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()

def delete(ssn):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''DELETE FROM
                        EMPLOYEE WHERE
                        Ssn = ?''', (ssn,))
        except Exception as e:
            print(e)
    conn.close()

def searchByName():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select Fname from EMPLOYEE")
    data = c.fetchall()
    conn.close()
    return data

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from EMPLOYEE")
    data = c.fetchall()
    conn.close()
    return data

def orderEmployeesBySalaryByGasStation(salary):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute('''
    SELECT E.GS_Longitude, Essn, Salary
    FROM EMPLOYEE as E, SIGNS JOIN CONTRACT ON Contract_Id=Id
    WHERE Essn=E.Ssn
    GROUP BY E.GS_Longitude, Essn
    HAVING Salary = ?
    ORDER BY E.GS_Longitude;
    ''', (float(salary),))
    data = c.fetchall()
    conn.close()
    return data