import sqlite3
import csv

def createPumpTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE PUMP
                        (Id                         INTEGER     NOT NULL,
                        Current_State               INTEGER     NOT NULL,
                        Last_Check_Up               TEXT        NOT NULL,
                        Nozzle_Last_Check_Up        TEXT        NOT NULL,
                        Product_Quantity            REAL        NOT NULL,
                        Tank_Id                     INTEGER     NOT NULL,
                        GS_Longitude                REAL        NOT NULL,
                        GS_Latitude                 REAL        NOT NULL,
                        PRIMARY KEY (Id, Tank_Id, GS_Longitude, GS_Latitude),
                        FOREIGN KEY (Tank_Id)      REFERENCES TANK(Id) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (GS_Longitude, GS_Latitude) REFERENCES TANK(GS_Longitude, GS_Latitude) ON UPDATE CASCADE ON DELETE CASCADE
                        );''')
            insertFromCsv("Datasets/pump.csv")
        except Exception as e:
            pass # Database created
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['ID'], tuple['Current_State'], tuple['Last_Check_Up'], 
            tuple['Nozzle_Last_Check_Up'], tuple['Product_Quantity'], tuple['Tank_ID'], 
            tuple['T_GS_Longitude'], tuple['T_GS_Latitude'], conn)
    conn.close()

def insertInto(id, current_state, last_check_up, nozzle_check_up, quantity, tank_id, tank_longitude, tank_latitude, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO PUMP
                            VALUES (?,?,?,?,?,?,?,?);''', (id, current_state, last_check_up,
                            nozzle_check_up, quantity, tank_id, tank_longitude, tank_latitude))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
               c.execute('''INSERT INTO PUMP
                            VALUES (?,?,?,?,?,?,?,?);''', (id, current_state, last_check_up,
                            nozzle_check_up, quantity, tank_id, tank_longitude, tank_latitude))
            except Exception:
                pass

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from PUMP")
    data = c.fetchall()
    conn.close()
    return data