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
            insertFromCsv("Datasets/purchase.csv")
        except Exception as e:
            pass
    conn.close()


def insertFromCsv(fileName):
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


def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from PURCHASE")
    data = c.fetchall()
    conn.close()
    return data
