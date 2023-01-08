import sqlite3
import csv


def createPurchaseTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE PURCHASE
                        (Id                 INTEGER     NOT NULL,
                        Purchase_Date       TEXT        NOT NULL,
                        Type_of_Payment     TEXT        NOT NULL,
                        Cus_Email           TEXT                ,
                        GS_Longitude        REAL                ,
                        GS_Latitude         REAL                ,
                        Pump_Id             INTEGER             ,
                        Tank_Id             INTEGER             ,
                        PRIMARY KEY (Id),
                        FOREIGN KEY (Cus_Email) REFERENCES CUSTOMER(Email) ON UPDATE CASCADE ON DELETE SET NULL,
                        FOREIGN KEY (Pump_Id, Tank_Id, GS_Longitude, GS_Latitude) REFERENCES PUMP(Id, Tank_Id, T_GS_Longitude, T_GS_Latitude)
                                    ON UPDATE CASCADE ON DELETE SET NULL
                        );''')
            insertFromCsv()
        except Exception as e:
            # print(e)
            pass  # Table already created and data from csv has been passed to the database
    conn.close()


def insertFromCsv():
    fileName = "Datasets/purchase.csv"
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['ID'], tuple['Purchase_Date'],
                       tuple['Type_of_Payment'], tuple['Cus_Email'],
                       tuple['GS_Longitude'], tuple['GS_Latitude'],
                       tuple['Pump_ID'], tuple['Tank_ID'], conn)
    conn.close()


def insertInto(id, purchase_date, type_of_payment, cus_email, gs_longitude, gs_latitude, pump_id, tank_id, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO PURCHASE
                            VALUES (?,?,?,?,?,?,?,?);''',
                          (id, purchase_date, type_of_payment, cus_email,
                           gs_longitude, gs_latitude, pump_id, tank_id))
            except Exception:
                pass  # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO PURCHASE
                            VALUES (?,?,?,?,?,?,?,?);''',
                          (id, purchase_date, type_of_payment, cus_email,
                           gs_longitude, gs_latitude, pump_id, tank_id))
            except Exception as e:
                pass


def searchBy(id, purchase_date, type_of_payment, cus_email, gs_longitude, gs_latitude, pump_id, tank_id):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (id):
            c.execute('''
                      SELECT * 
                      FROM PURCHASE
                      WHERE Id = ?''',
                      (id, ))
        elif (purchase_date):
            if (type_of_payment):
                if (cus_email or cus_email == None):
                    if (gs_longitude and gs_latitude):
                        if (pump_id):
                            if (tank_id):
                                c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                        AND Cus_Email = ? AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Pump_Id = ? AND Tank_Id = ?
                                        ''',
                                          (purchase_date, type_of_payment, cus_email,
                                           gs_longitude, gs_latitude, pump_id, tank_id))
                            else:
                                c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                        AND Cus_Email = ? AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Pump_Id = ?
                                        ''',
                                          (purchase_date, type_of_payment, cus_email,
                                           gs_longitude, gs_latitude, pump_id))
                        elif (tank_id):
                            c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                        AND Cus_Email = ? AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Tank_Id = ?
                                        ''',
                                      (purchase_date, type_of_payment, cus_email,
                                       gs_longitude, gs_latitude, tank_id))
                        else:
                            c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                        AND Cus_Email = ? AND GS_Longitude = ? 
                                        AND GS_Latitude = ?
                                        ''',
                                      (purchase_date, type_of_payment, cus_email,
                                       gs_longitude, gs_latitude))
                    elif (pump_id):
                        if (tank_id):
                            c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                        AND Cus_Email = ? AND Pump_Id = ? AND Tank_Id = ?
                                        ''',
                                      (purchase_date, type_of_payment, cus_email, pump_id, tank_id))
                        else:
                            c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                        AND Cus_Email = ? AND Pump_Id = ?
                                        ''',
                                      (purchase_date, type_of_payment, cus_email, pump_id))
                    elif (tank_id):
                        c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                    AND Cus_Email = ? AND Tank_Id = ?
                                    ''',
                                  (purchase_date, type_of_payment, cus_email, tank_id))
                    else:
                        c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                    AND Cus_Email = ?
                                    ''',
                                  (purchase_date, type_of_payment, cus_email))
                elif (gs_longitude and gs_latitude):
                    if (pump_id):
                        if (tank_id):
                            c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                        AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Pump_Id = ? AND Tank_Id = ?
                                        ''',
                                      (purchase_date, type_of_payment,
                                       gs_longitude, gs_latitude, pump_id, tank_id))
                        else:
                            c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                        AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Pump_Id = ?
                                        ''',
                                      (purchase_date, type_of_payment,
                                       gs_longitude, gs_latitude, pump_id))
                    elif (tank_id):
                        c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                        AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Tank_Id = ?
                                        ''',
                                  (purchase_date, type_of_payment,
                                   gs_longitude, gs_latitude, tank_id))
                    else:
                        c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                        AND GS_Longitude = ? 
                                        AND GS_Latitude = ?
                                        ''',
                                  (purchase_date, type_of_payment,
                                   gs_longitude, gs_latitude))
                elif (pump_id):
                    if (tank_id):
                        c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                    AND Pump_Id = ? AND Tank_Id = ?
                                    ''',
                                  (purchase_date, type_of_payment, pump_id, tank_id))
                    else:
                        c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                    AND Pump_Id = ?
                                    ''',
                                  (purchase_date, type_of_payment, pump_id))
                elif (tank_id):
                    c.execute('''
                                SELECT * 
                                FROM PURCHASE
                                WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                AND Tank_Id = ?
                                ''',
                              (purchase_date, type_of_payment, tank_id))
                else:
                    c.execute('''
                                SELECT * 
                                FROM PURCHASE
                                WHERE Purchase_Date = ? AND Type_of_Payment = ?
                                ''',
                              (purchase_date, type_of_payment))
            elif (cus_email or cus_email == None):
                if (gs_longitude and gs_latitude):
                    if (pump_id):
                        if (tank_id):
                            c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ?
                                        AND Cus_Email = ? AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Pump_Id = ? AND Tank_Id = ?
                                        ''',
                                      (purchase_date, cus_email,
                                       gs_longitude, gs_latitude, pump_id, tank_id))
                        else:
                            c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ?
                                        AND Cus_Email = ? AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Pump_Id = ?
                                        ''',
                                      (purchase_date, cus_email,
                                       gs_longitude, gs_latitude, pump_id))
                    elif (tank_id):
                        c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ?
                                        AND Cus_Email = ? AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Tank_Id = ?
                                        ''',
                                  (purchase_date, cus_email,
                                   gs_longitude, gs_latitude, tank_id))
                    else:
                        c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ?
                                        AND Cus_Email = ? AND GS_Longitude = ? 
                                        AND GS_Latitude = ?
                                        ''',
                                  (purchase_date, cus_email,
                                   gs_longitude, gs_latitude))
                elif (pump_id):
                    if (tank_id):
                        c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ?
                                        AND Cus_Email = ? AND Pump_Id = ? AND Tank_Id = ?
                                        ''',
                                  (purchase_date, cus_email, pump_id, tank_id))
                    else:
                        c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Purchase_Date = ?
                                        AND Cus_Email = ? AND Pump_Id = ?
                                        ''',
                                  (purchase_date, cus_email, pump_id))
                elif (tank_id):
                    c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Purchase_Date = ?
                                    AND Cus_Email = ? AND Tank_Id = ?
                                    ''',
                              (purchase_date, cus_email, tank_id))
                else:
                    c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Purchase_Date = ?
                                    AND Cus_Email = ?
                                    ''',
                              (purchase_date, cus_email))
            elif (gs_longitude and gs_latitude):
                if (pump_id):
                    if (tank_id):
                        c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Purchase_Date = ?
                                    AND GS_Longitude = ? 
                                    AND GS_Latitude = ? AND Pump_Id = ? AND Tank_Id = ?
                                    ''',
                                  (purchase_date,
                                   gs_longitude, gs_latitude, pump_id, tank_id))
                    else:
                        c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Purchase_Date = ?
                                    AND GS_Longitude = ? 
                                    AND GS_Latitude = ? AND Pump_Id = ?
                                    ''',
                                  (purchase_date,
                                   gs_longitude, gs_latitude, pump_id))
                elif (tank_id):
                    c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Purchase_Date = ?
                                    AND GS_Longitude = ? 
                                    AND GS_Latitude = ? AND Tank_Id = ?
                                    ''',
                              (purchase_date,
                               gs_longitude, gs_latitude, tank_id))
                else:
                    c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Purchase_Date = ?
                                    AND GS_Longitude = ? 
                                    AND GS_Latitude = ?
                                    ''',
                              (purchase_date,
                               gs_longitude, gs_latitude))
            elif (pump_id):
                if (tank_id):
                    c.execute('''
                                SELECT * 
                                FROM PURCHASE
                                WHERE Purchase_Date = ?
                                AND Pump_Id = ? AND Tank_Id = ?
                                ''',
                              (purchase_date, pump_id, tank_id))
                else:
                    c.execute('''
                                SELECT * 
                                FROM PURCHASE
                                WHERE Purchase_Date = ?
                                AND Pump_Id = ?
                                ''',
                              (purchase_date, pump_id))
            elif (tank_id):
                c.execute('''
                            SELECT * 
                            FROM PURCHASE
                            WHERE Purchase_Date = ? AND Tank_Id = ?
                            ''',
                          (purchase_date, tank_id))
            else:
                c.execute('''
                            SELECT * 
                            FROM PURCHASE
                            WHERE Purchase_Date = ?
                            ''',
                          (purchase_date, ))
        elif (type_of_payment):
            if (cus_email or cus_email == None):
                if (gs_longitude and gs_latitude):
                    if (pump_id):
                        if (tank_id):
                            c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Type_of_Payment = ?
                                        AND Cus_Email = ? AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Pump_Id = ? AND Tank_Id = ?
                                        ''',
                                      (type_of_payment, cus_email,
                                       gs_longitude, gs_latitude, pump_id, tank_id))
                        else:
                            c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Type_of_Payment = ?
                                        AND Cus_Email = ? AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Pump_Id = ?
                                        ''',
                                      (type_of_payment, cus_email,
                                       gs_longitude, gs_latitude, pump_id))
                    elif (tank_id):
                        c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Type_of_Payment = ?
                                        AND Cus_Email = ? AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Tank_Id = ?
                                        ''',
                                  (type_of_payment, cus_email,
                                   gs_longitude, gs_latitude, tank_id))
                    else:
                        c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Type_of_Payment = ?
                                        AND Cus_Email = ? AND GS_Longitude = ? 
                                        AND GS_Latitude = ?
                                        ''',
                                  (type_of_payment, cus_email,
                                   gs_longitude, gs_latitude))
                elif (pump_id):
                    if (tank_id):
                        c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Type_of_Payment = ?
                                        AND Cus_Email = ? AND Pump_Id = ? AND Tank_Id = ?
                                        ''',
                                  (type_of_payment, cus_email, pump_id, tank_id))
                    else:
                        c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Type_of_Payment = ?
                                        AND Cus_Email = ? AND Pump_Id = ?
                                        ''',
                                  (type_of_payment, cus_email, pump_id))
                elif (tank_id):
                    c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Type_of_Payment = ?
                                    AND Cus_Email = ? AND Tank_Id = ?
                                    ''',
                              (type_of_payment, cus_email, tank_id))
                else:
                    c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Type_of_Payment = ?
                                    AND Cus_Email = ?
                                    ''',
                              (type_of_payment, cus_email))
            elif (gs_longitude and gs_latitude):
                if (pump_id):
                    if (tank_id):
                        c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Type_of_Payment = ?
                                        AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Pump_Id = ? AND Tank_Id = ?
                                        ''',
                                  (type_of_payment,
                                   gs_longitude, gs_latitude, pump_id, tank_id))
                    else:
                        c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Type_of_Payment = ?
                                        AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Pump_Id = ?
                                        ''',
                                  (type_of_payment,
                                   gs_longitude, gs_latitude, pump_id))
                elif (tank_id):
                    c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Type_of_Payment = ?
                                        AND GS_Longitude = ? 
                                        AND GS_Latitude = ? AND Tank_Id = ?
                                        ''',
                              (type_of_payment,
                               gs_longitude, gs_latitude, tank_id))
                else:
                    c.execute('''
                                        SELECT * 
                                        FROM PURCHASE
                                        WHERE Type_of_Payment = ?
                                        AND GS_Longitude = ? 
                                        AND GS_Latitude = ?
                                        ''',
                              (type_of_payment,
                               gs_longitude, gs_latitude))
            elif (pump_id):
                if (tank_id):
                    c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Type_of_Payment = ?
                                    AND Pump_Id = ? AND Tank_Id = ?
                                    ''',
                              (type_of_payment, pump_id, tank_id))
                else:
                    c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Type_of_Payment = ?
                                    AND Pump_Id = ?
                                    ''',
                              (type_of_payment, pump_id))
            elif (tank_id):
                c.execute('''
                                SELECT * 
                                FROM PURCHASE
                                WHERE Type_of_Payment = ?
                                AND Tank_Id = ?
                                ''',
                          (type_of_payment, tank_id))
            else:
                c.execute('''
                                SELECT * 
                                FROM PURCHASE
                                WHERE Type_of_Payment = ?
                                ''',
                          (type_of_payment, ))
        elif (cus_email or cus_email == None):
            if (gs_longitude and gs_latitude):
                if (pump_id):
                    if (tank_id):
                        c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Cus_Email = ? AND GS_Longitude = ? 
                                    AND GS_Latitude = ? AND Pump_Id = ? AND Tank_Id = ?
                                    ''',
                                  (cus_email,
                                   gs_longitude, gs_latitude, pump_id, tank_id))
                    else:
                        c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Cus_Email = ? AND GS_Longitude = ? 
                                    AND GS_Latitude = ? AND Pump_Id = ?
                                    ''',
                                  (cus_email,
                                   gs_longitude, gs_latitude, pump_id))
                elif (tank_id):
                    c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Cus_Email = ? AND GS_Longitude = ? 
                                    AND GS_Latitude = ? AND Tank_Id = ?
                                    ''',
                              (cus_email,
                               gs_longitude, gs_latitude, tank_id))
                else:
                    c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Cus_Email = ? AND GS_Longitude = ? 
                                    AND GS_Latitude = ?
                                    ''',
                              (cus_email,
                               gs_longitude, gs_latitude))
            elif (pump_id):
                if (tank_id):
                    c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Cus_Email = ? AND Pump_Id = ? AND Tank_Id = ?
                                    ''',
                              (cus_email, pump_id, tank_id))
                else:
                    c.execute('''
                                    SELECT * 
                                    FROM PURCHASE
                                    WHERE Cus_Email = ? AND Pump_Id = ?
                                    ''',
                              (cus_email, pump_id))
            elif (tank_id):
                c.execute('''
                                SELECT * 
                                FROM PURCHASE
                                WHERE Cus_Email = ? AND Tank_Id = ?
                                ''',
                          (cus_email, tank_id))
            else:
                c.execute('''
                                SELECT * 
                                FROM PURCHASE
                                WHERE Cus_Email = ?
                                ''',
                          (cus_email, ))
        elif (gs_longitude and gs_latitude):
            if (pump_id):
                if (tank_id):
                    c.execute('''
                                SELECT * 
                                FROM PURCHASE
                                WHERE GS_Longitude = ? 
                                AND GS_Latitude = ? AND Pump_Id = ? AND Tank_Id = ?
                                ''',
                              (gs_longitude, gs_latitude, pump_id, tank_id))
                else:
                    c.execute('''
                                SELECT * 
                                FROM PURCHASE
                                WHERE GS_Longitude = ? 
                                AND GS_Latitude = ? AND Pump_Id = ?
                                ''',
                              (gs_longitude, gs_latitude, pump_id))
            elif (tank_id):
                c.execute('''
                                SELECT * 
                                FROM PURCHASE
                                WHERE GS_Longitude = ? 
                                AND GS_Latitude = ? AND Tank_Id = ?
                                ''',
                          (gs_longitude, gs_latitude, tank_id))
            else:
                c.execute('''
                                SELECT * 
                                FROM PURCHASE
                                WHERE GS_Longitude = ? 
                                AND GS_Latitude = ?
                                ''',
                          (gs_longitude, gs_latitude))
        elif (pump_id):
            if (tank_id):
                c.execute('''
                            SELECT * 
                            FROM PURCHASE
                            WHERE Pump_Id = ? AND Tank_Id = ?
                            ''',
                          (pump_id, tank_id))
            else:
                c.execute('''
                            SELECT * 
                            FROM PURCHASE
                            WHERE Pump_Id = ?
                            ''',
                          (pump_id, ))
        else:
            c.execute('''
                        SELECT * 
                        FROM PURCHASE
                        WHERE Tank_Id = ?
                        ''',
                      (tank_id, ))
    data = c.fetchall()
    conn.close()
    return data


def update(id, purchase_date, type_of_payment, cus_email, gs_longitude, gs_latitude, pump_id, tank_id):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE PURCHASE
                        SET Purchase_Date= ?, Type_of_Payment= ?, Cus_Email= ?,
                        GS_Longitude= ?, GS_Latitude= ?, Pump_Id= ?, Tank_Id= ?
                        WHERE Id= ?''',
                      (purchase_date, type_of_payment, cus_email, gs_longitude, gs_latitude, pump_id, tank_id, id))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()


def delete(id):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''DELETE FROM PURCHASE
                        WHERE Id= ? ''',
                      (id, ))
        except Exception as e:
            print(e)
    conn.close()


def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from PURCHASE")
    data = c.fetchall()
    conn.close()
    return data


def allPurchaseIds():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select Id from PURCHASE")
    data = c.fetchall()
    conn.close()
    return data


def allPurchaseinfo():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute('''
                SELECT PUR.ID, PUR.GS_Longitude, PUR.GS_Latitude, P.Name, P.Price * I.Quantity
                FROM PURCHASE as PUR, INVOLVES as I, PRODUCT as P
                WHERE PUR.ID = I.Pur_Id AND I.Prod_Id = P.ID
                GROUP BY PUR.GS_Longitude, PUR.GS_Longitude, I.Prod_Id
                UNION
                SELECT PUR.ID, PUR.GS_Longitude, PUR.GS_Latitude, S.Name, S.Price
                FROM PURCHASE AS PUR, ENTAILS as E, SERVICE as S
                WHERE PUR.ID = E.Pur_Id AND E.Serv_Id = S.ID
                GROUP BY PUR.GS_Longitude, PUR.GS_Longitude, E.Serv_Id
                ORDER BY PUR.GS_Longitude, PUR.GS_Longitude
            ''')
    data = c.fetchall()
    conn.close()
    return data


def allSuppliesinfo():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute('''
                SELECT S.GS_Longitude, S.GS_Latitude, sum(C.Cost)
                FROM SUPPLY AS S, CONSISTS_OF AS C, PRODUCT AS P
                WHERE S.ID = C.Supply_Id AND C.Prod_Id = P.ID
                GROUP BY S.GS_Longitude, S.GS_Latitude
                ORDER BY S.GS_Longitude, S.GS_Latitude
            ''')
    data = c.fetchall()
    conn.close()
    return data


def groupByGSCoords():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute('''
                SELECT PUR.GS_Longitude, PUR.GS_Latitude, sum(P.Price * I.Quantity)
                FROM PURCHASE as PUR, INVOLVES as I, PRODUCT as P
                WHERE PUR.ID = I.Pur_Id AND I.Prod_Id = P.ID
                GROUP BY PUR.GS_Longitude, PUR.GS_Longitude, I.Prod_Id
                UNION
                SELECT PUR.GS_Longitude, PUR.GS_Latitude, sum(S.Price)
                FROM PURCHASE AS PUR, ENTAILS as E, SERVICE as S
                WHERE PUR.ID = E.Pur_Id AND E.Serv_Id = S.ID
                GROUP BY PUR.GS_Longitude, PUR.GS_Longitude, E.Serv_Id
                ORDER BY PUR.GS_Longitude, PUR.GS_Longitude
            ''')
    data = c.fetchall()
    conn.close()
    return data


def groupByGSCoordsAllProducts():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute('''
                SELECT PUR.GS_Longitude, PUR.GS_Latitude, sum(P.Price * I.Quantity)
                FROM PURCHASE as PUR, INVOLVES as I, PRODUCT as P
                WHERE PUR.ID = I.Pur_Id AND I.Prod_Id = P.ID
                GROUP BY PUR.GS_Longitude, PUR.GS_Longitude
                ORDER BY PUR.GS_Longitude, PUR.GS_Longitude
            ''')
    data = c.fetchall()
    conn.close()
    return data


def groupByGSCoordsAllServices():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute('''
                SELECT PUR.GS_Longitude, PUR.GS_Latitude, sum(S.Price)
                FROM PURCHASE AS PUR, ENTAILS as E, SERVICE as S
                WHERE PUR.ID = E.Pur_Id AND E.Serv_Id = S.ID
                GROUP BY PUR.GS_Longitude, PUR.GS_Longitude
                ORDER BY PUR.GS_Longitude, PUR.GS_Longitude
            ''')
    data = c.fetchall()
    conn.close()
    return data


def productAnalysis():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute('''
                SELECT P.Name, sum(P.Price * I.Quantity), count(PUR.ID)
                FROM PURCHASE as PUR, INVOLVES as I, PRODUCT as P
                WHERE PUR.ID = I.Pur_Id AND I.Prod_Id = P.ID
                GROUP BY I.Prod_Id
            ''')
    data = c.fetchall()
    conn.close()
    return data


def serviceAnalysis():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute('''
                SELECT S.Name, sum(S.Price), count(PUR.ID)
                FROM PURCHASE as PUR, ENTAILS as E, SERVICE as S
                WHERE PUR.ID = E.Pur_Id AND E.Serv_Id = S.ID
                GROUP BY E.Serv_Id
            ''')
    data = c.fetchall()
    conn.close()
    return data
