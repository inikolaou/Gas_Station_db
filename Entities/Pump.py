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
        except Exception as e:
            print(e)
    conn.close()


def insertFromCsv():
    fileName = "Datasets/pump.csv"
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
                pass  # tuple already added
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


def searchBy(id, tank_id, tank_gs_longitude, tank_gs_latitude, current_state, last_check_up, nozzle_check_up, quantity):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (id):
            if (tank_id):
                if (tank_gs_longitude and tank_gs_latitude):
                    c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Id = ? AND Tank_Id = ? AND T_GS_Longitude = ? AND T_GS_Latitude = ?''',
                              (id, tank_id, tank_gs_longitude, tank_gs_latitude))
                else:
                    c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Id = ? AND Tank_Id = ?''',
                              (id, tank_id))
            elif (tank_gs_longitude and tank_gs_latitude):
                c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Id = ? AND T_GS_Longitude = ? AND T_GS_Latitude = ?''',
                          (id, tank_gs_longitude, tank_gs_latitude))
            else:
                c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Id = ?''',
                          (id, ))
        elif (tank_id):
            if (tank_gs_longitude and tank_gs_latitude):
                c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Tank_Id = ? AND T_GS_Longitude = ? AND T_GS_Latitude = ?''',
                          (tank_id, tank_gs_longitude, tank_gs_latitude))
            else:
                c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Tank_Id = ?''',
                          (tank_id, ))
        elif (tank_gs_longitude and tank_gs_latitude):
            c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE T_GS_Longitude = ? AND T_GS_Latitude = ?''',
                      (tank_gs_longitude, tank_gs_latitude))
        elif (current_state):
            if (last_check_up):
                if (nozzle_check_up):
                    if (quantity):
                        c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Current_State = ? AND Last_Check_Up = ? 
                            AND Nozzle_Last_Check_Up = ? AND Product_Quantity = ?''',
                                  (current_state, last_check_up, nozzle_check_up, quantity))
                    else:
                        c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Current_State = ? AND Last_Check_Up = ? 
                            AND Nozzle_Last_Check_Up = ?''',
                                  (current_state, last_check_up, nozzle_check_up))
                elif (quantity):
                    c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Current_State = ? AND Last_Check_Up = ? 
                            AND Product_Quantity = ?''',
                              (current_state, last_check_up, quantity))
                else:
                    c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Current_State = ? AND Last_Check_Up = ?''',
                              (current_state, last_check_up))
            elif (nozzle_check_up):
                if (quantity):
                    c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Current_State = ?
                            AND Nozzle_Last_Check_Up = ? AND Product_Quantity = ?''',
                              (current_state, nozzle_check_up, quantity))
                else:
                    c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Current_State = ?
                            AND Nozzle_Last_Check_Up = ?''',
                              (current_state, nozzle_check_up))
            elif (quantity):
                c.execute('''
                        SELECT * 
                        FROM PUMP
                        WHERE Current_State = ?
                        AND Product_Quantity = ?''',
                          (current_state, quantity))
            else:
                c.execute('''
                        SELECT * 
                        FROM PUMP
                        WHERE Current_State = ?''',
                          (current_state, ))
        elif (last_check_up):
            if (nozzle_check_up):
                if (quantity):
                    c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Last_Check_Up = ? 
                            AND Nozzle_Last_Check_Up = ? AND Product_Quantity = ?''',
                              (last_check_up, nozzle_check_up, quantity))
                else:
                    c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Last_Check_Up = ? 
                            AND Nozzle_Last_Check_Up = ?''',
                              (last_check_up, nozzle_check_up))
            elif (quantity):
                c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Last_Check_Up = ? 
                            AND Product_Quantity = ?''',
                          (last_check_up, quantity))
            else:
                c.execute('''
                            SELECT * 
                            FROM PUMP
                            WHERE Last_Check_Up = ?''',
                          (last_check_up, ))
        elif (nozzle_check_up):
            if (quantity):
                c.execute('''
                        SELECT * 
                        FROM PUMP
                        WHERE Nozzle_Last_Check_Up = ? AND Product_Quantity = ?''',
                          (nozzle_check_up, quantity))
            else:
                c.execute('''
                        SELECT * 
                        FROM PUMP
                        WHERE Nozzle_Last_Check_Up = ?''',
                          (nozzle_check_up, ))
        else:
            c.execute('''
                    SELECT * 
                    FROM PUMP
                    WHERE Product_Quantity = ?''',
                      (quantity, ))
    data = c.fetchall()
    conn.close()
    return data


def update(id, tank_id, tank_gs_longitude, tank_gs_latitude, current_state, last_check_up, nozzle_check_up, quantity):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE PUMP
                        SET Current_State = ?, Last_Check_Up = ?, Nozzle_Last_Check_Up = ?,
                        Product_Quantity = ? 
                        WHERE Id = ? AND Tank_Id = ? AND T_GS_Longitude = ? AND T_GS_Latitude = ?''',
                      (current_state, last_check_up, nozzle_check_up, quantity,
                       id, tank_id, tank_gs_longitude, tank_gs_latitude))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()


def delete(id_tankId_tankLongitude_tankLatitude):
    id_tankId_tankLongitude_tankLatitude = id_tankId_tankLongitude_tankLatitude.split(
        '_')
    pump_id = id_tankId_tankLongitude_tankLatitude[0]
    tank_id = id_tankId_tankLongitude_tankLatitude[1]
    tank_longitude = id_tankId_tankLongitude_tankLatitude[2]
    tank_latitude = id_tankId_tankLongitude_tankLatitude[3]
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''DELETE FROM
                        PUMP WHERE
                        Id = ? AND Tank_Id = ? AND T_GS_Longitude = ? AND T_GS_Latitude = ?''',
                      (pump_id, tank_id, tank_longitude, tank_latitude))
        except Exception as e:
            print(e)
    conn.close()


def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from PUMP")
    data = c.fetchall()
    conn.close()
    return data
