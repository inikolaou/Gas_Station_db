import sqlite3
import csv

def createPumpTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE PUMP
                        (Id                         INTEGER     NOT NULL,
                        Tank_Id                     INTEGER     NOT NULL,
                        T_GS_Longitude              REAL        NOT NULL,
                        T_GS_Latitude               REAL        NOT NULL,
                        Current_State               INTEGER     NOT NULL DEFAULT 0,
                        Last_Check_Up               TEXT        NOT NULL,
                        Nozzle_Last_Check_Up        TEXT        NOT NULL,
                        Product_Quantity            REAL        NOT NULL,
                        PRIMARY KEY (Id, Tank_Id, T_GS_Longitude, T_GS_Latitude),
                        FOREIGN KEY (Tank_Id, T_GS_Longitude, T_GS_Latitude) REFERENCES TANK(Id, GS_Longitude, GS_Latitude) ON UPDATE CASCADE ON DELETE CASCADE
                        );''')
            insertFromCsv("Datasets/pump.csv")
        except Exception as e:
            pass # Database created
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['ID'], tuple['Tank_ID'], tuple['T_GS_Longitude'],
                       tuple['T_GS_Latitude'], tuple['Current_State'],
                       tuple['Last_Check_Up'], tuple['Nozzle_Last_Check_Up'],
                       tuple['Product_Quantity'], conn)
    conn.close()

def insertInto(id, tank_id, tank_gs_longitude, tank_gs_latitude, current_state, last_check_up, nozzle_check_up, quantity, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO PUMP
                            VALUES (?,?,?,?,?,?,?,?);''',
                            (id, tank_id, tank_gs_longitude, tank_gs_latitude,
                             current_state, last_check_up, nozzle_check_up,
                             quantity))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
               c.execute('''INSERT INTO PUMP
                            VALUES (?,?,?,?,?,?,?,?);''',
                            (id, tank_id, tank_gs_longitude, tank_gs_latitude,
                             current_state, last_check_up, nozzle_check_up,
                             quantity))
            except Exception:
                pass

def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from PUMP")
    data = c.fetchall()
    conn.close()
    return data