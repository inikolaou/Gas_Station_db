import sqlite3
import csv

def createEmployeeTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE EMPLOYEE
                        (Ssn            TEXT        NOT NULL        ,
                        Fname           TEXT        NOT NULL        ,
                        Lname           TEXT        NOT NULL        ,
                        Birth_Date      TEXT        NOT NULL        ,
                        Phone_Number    INTEGER     NOT NULL        ,
                        Email           TEXT        NOT NULL        ,
                        Longitude       REAL        NOT NULL        ,
                        Latitude        REAL        NOT NULL        ,
                        Role            TEXT        NOT NULL        ,
                        Hours           INTEGER     NOT NULL        ,
                        Super_Ssn       INTEGER     DEFAULT     NULL,
                        GS_Longitude    REAL        NOT NULL        ,
                        GS_Latitude     REAL        NOT NULL        ,
                        PRIMARY KEY (Ssn)                           ,
                        FOREIGN KEY (Super_Ssn)    REFERENCES EMPLOYEE(Ssn) ON UPDATE CASCADE ON DELETE SET NULL,
                        FOREIGN KEY (GS_Longitude) REFERENCES GAS_STATION(Longitude) ON UPDATE CASCADE ON DELETE SET NULL,
                        FOREIGN KEY (GS_Latitude)  REFERENCES GAS_STATION(Latitude) ON UPDATE CASCADE ON DELETE SET NULL
                        );''')
            insertFromCsv("Datasets/employee.csv")
        except Exception as e:
            pass # Database created
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Ssn'], tuple['Fname'],
                        tuple['Lname'], tuple['Email'], tuple['Birth_Date'],tuple['Phone_Number'], tuple['Longitude'],
                        tuple['Latitude'], tuple['Role'], tuple['Hours'],
                        tuple['Super_Ssn'], tuple['GS_Longitude'], tuple['GS_Latitude'], conn)
    conn.close()

def insertInto(ssn, fname, lname, email, birth_date, phone_number, longitude, latitude, 
        role, hours, super_ssn, gs_longitude, gs_latitude, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO EMPLOYEE
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);''', 
                            (ssn, fname, lname, email, birth_date, phone_number,
                            longitude, latitude, role, hours, super_ssn,
                            gs_longitude, gs_latitude))
            except Exception as e:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO EMPLOYEE
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);''', 
                            (ssn, fname, lname, email, birth_date, phone_number,
                            longitude, latitude, role, hours, super_ssn,
                            gs_longitude, gs_latitude))
            except Exception as e:
                pass

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