# -*- coding: utf-8 -*-
import sqlite3
import serial
import time
import schedule
from datetime import datetime
from threading import Thread

# Arduino Variables
arduino_list = []

# Other Variables
fOveride = False;
last_received = ''


################################################################################

def main():
    print("<main> : Beginning code...")

    while True:
        print()
        table_set = input("<main> : Would you like to setup the data table? (Y/n): ")
        table_set = table_set.lower()

        if table_set == 'y':
            setup_db()
            break
        elif table_set == 'n':
            break
        else:
            print("<main> ERROR: Improper input, please try again...")

    schedule.every().hour.at(":59").do(convert_TXT_SQL)
    schedule.every().hour.at(":14").do(convert_TXT_SQL)
    schedule.every().hour.at(":29").do(convert_TXT_SQL)
    schedule.every().hour.at(":44").do(convert_TXT_SQL)
    print("<main> : Schedule set...")

    print("<main> : Beginning data collection...")
    time.sleep(3)
    while True:
        schedule.run_pending()
        time.sleep(1)

################################################################################

def setup_db():
    global fOveride

    try:
        ''' SQLite3 CONNECTION '''
        conn = sqlite3.connect("veles_data.db")
        curs = conn.cursor()
        print("<setup_db> : Attempting connection to SQLite3...")

        ''' CREATING TABLE '''
        # Get rid of possible duplicate
        while fOveride == False:
            reset = input("<setup_db> : Table already created... Overide? (Y/n): ")
            reset.lower()
            if reset == 'y':
                fOveride = True
                curs.execute("DROP TABLE IF EXISTS SENSOR_DATA")
            elif reset != 'n':
                print("<setup_db> ERROR: Improper input...")
            else:
                return

        table = """ CREATE TABLE sensor_data (
                      pname        varchar(10) not null, /* Plant Name */
                      pnumber      integer(2), /* Species - Sensor/Control */
                      cap          integer(3), /* Capacitance in Farads */
                      percMois     integer(3) not null, /* Percent of Water */
                      moisStat     varchar(7), /* Plant Moisture Status */
                      res          integer(4), /* Resistance in Ohms */
                      lux          float(10) not null, /* Lumens */
                      tempC        float(4), /* Temperature in Celsius */
                      tempF        float(4), /* Temperature in Fahrenheit */
                      currTime     time /* Time that data was taken */
                    ); """ # Establishing table formating

        curs.execute(table)
        curs.close()

    except sqlite3.Error as error:
        print("<setup_db> ERROR: Something went wrong working with SQLite3..."
            , error)

    else:
        print("<setup_db> : Created table...")
        fOveride = 1

    finally:
        if conn:
            conn.close()
            print("<setup_db> : SQLite3 connection closed...")

################################################################################

def convert_TXT_SQL():
    global arduino_list
    global last_received

    try:
        ''' SQLite3 CONNECTION '''
        conn = sqlite3.connect("veles_data.db")
        curs = conn.cursor()
        print("<convert_TXT_SQL> : Attempting connection to SQLite3...")

        ''' CONNECT TO ARDUINO(S) '''
        print("<convert_TXT_SQL> : Connecting to arduino(s)...")
        connect_ards()
        time.sleep(60) #take a minute of data
        print("<convert_TXT_SQL> : Taking data from arduino(s)...")

        ''' CREATE TIMESTAMP '''
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        ''' COLLECTING DATA FROM SERIAL '''
        data_list = []
        for ard in range(4):
            sdata = readLastLine(arduino_list[ard])

            ard_data = sdata.split('\t')

            if len(ard_data) != 9: # Checks if all 6 expected values are present
                print("<convert_TXT_SQL> ERROR: %s had invalid read from sensors at %s..."
                    % (ard_data[0], current_time))
            else:
                ard_data[1] = int(ard_data[1])
                ard_data[2] = int(ard_data[2])
                ard_data[3] = int(ard_data[3])
                ard_data[5] = int(ard_data[5])
                ard_data[6] = float(ard_data[6])
                ard_data[7] = float(ard_data[7])
                ard_data[8] = float(ard_data[8][:-2])
            ard_data.append(current_time)

            print("<convert_TXT_SQL> : Listing data taken from %s at %s... "
                % (ard_data[0], current_time))
            print(ard_data)

            data_list.append(tuple(ard_data))
        disconnect_ards()

        ''' INSERT DATA INTO DATABASE '''
        db_insert = """INSERT INTO sensor_data
                    (pname, pnumber, cap, percMois, moisStat, res, lux
                        , tempC, tempF, currTime)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        curs.executemany(db_insert, data_list)
        conn.commit()
        curs.close()

    except sqlite3.Error as error:
        print("<convert_TXT_SQL> ERROR: Something went wrong working with"
        , "SQLite3...", error)

    else:
        print("<convert_TXT_SQL> : Successfully added data to table at %s"
            % current_time)

    finally:
        if conn:
            conn.close()
            print("<convert_TXT_SQL> : SQLite3 connection closed...")

################################################################################

def connect_ards():
    global arduino_list
    ard1 = serial.Serial(port = '/dev/ttyACM0', baudrate = 9600, timeout = 1.5)
    ard2 = serial.Serial(port = '/dev/ttyACM1', baudrate = 9600, timeout = 1.5)
    ard3 = serial.Serial(port = '/dev/ttyACM2', baudrate = 9600, timeout = 1.5)
    ard4 = serial.Serial(port = '/dev/ttyACM3', baudrate = 9600, timeout = 1.5)
    arduino_list = [ard1, ard2, ard3, ard4] #ard1, ard2, ard3, ard4

    ''' For testing the arduinos '''
    # ard1 = serial.Serial(port = '/dev/cu.usbmodem1201', baudrate = 9600, timeout = 0.1)
    # ard2 = serial.Serial(port = '/dev/cu.usbmodem1301', baudrate = 9600, timeout = 0.1)
    # arduino_list = [ard1, ard2]

################################################################################

def disconnect_ards():
    global arduino_list
    for ard in arduino_list:
        ard.close()

################################################################################

def readLastLine(ser):
    last_data = ''
    seclast_data = ''
    while True:
        data = ser.readline()
        data = data.decode('ISO-8859-1')
        if data != '':
            last_data = data
            seclast_data = last_data
        elif (len(last_data.split('\t')) != 9):
            return seclast_data
        else:
            return last_data

################################################################################

if __name__ == "__main__":
    main()
