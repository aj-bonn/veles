import sqlite3
import serial
import time
import schedule
from datetime import datetime
from threading import Thread


# Arduino Variables – input port
ha_ard = serial.Serial(port = '/dev/cu.usbmodem1201', baudrate = 9600, timeout = 0.1)
# ha_ard = serial.Serial(port = '/dev/ttyACM0', baudrate = 9600, timeout = 0.1)
# hu_ard = serial.Serial(port = '/dev/ttyACM1', baudrate = 9600, timeout = 0.1)
# so_ard = serial.Serial(port = '/dev/ttyACM2', baudrate = 9600, timeout = 0.1)
# si_ard = serial.Serial(port = '/dev/ttyACM3', baudrate = 9600, timeout = 0.1)
arduino_list = [ha_ard] #, hu_ard, so_ard, si_ard

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

    schedule.every().hour.at(":16").do(convert_TXT_SQL)
    schedule.every().hour.at(":15").do(convert_TXT_SQL)
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
            reset = input("Table already created... Overide? (Y/n): ")
            print(reset)
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

        ''' CREATE TIMESTAMP '''
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        ''' COLLECTING DATA FROM SERIAL '''
        data_list = []
        for ard in arduino_list:
            # Thread(target=receiving, args=(ard,)).start()
            # sdata = last_received
            sdata = readLastLine(ard)
            ard_data = sdata.split('\t')
            # ard_data = str(data, 'ascii').split("\t") # data from plant

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
                ard_data[8] = float(ard_data[8][0:6])

            ard_data.append(current_time)
            print(ard_data)

            data_list.append(tuple(ard_data))


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

def receiving(ser):
    global last_received

    buffer_string = ''
    while True:
        rdata = ser.readline(ser.inWaiting())
        buffer_string = buffer_string + rdata.decode('utf-8')
        if '\n' in buffer_string:
            lines = buffer_string.split('\n')
            last_received = lines[-2]
            buffer_string = lines[-1]

################################################################################

def readLastLine(ser):
    last_data = ''
    while True:
        data = ser.readline()
        data = data.decode('utf-8')
        if data != '':
            last_data = data
        else:
            return last_data

################################################################################

if __name__ == "__main__":
    main()
