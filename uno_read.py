import sqlite3
import serial
import time
import schedule
from datetime import datetime


# Arduino Variables – input port
ha_ard = serial.Serial(port = '/dev/ttyACM0', baudrate = 9600, timeout = 0.1)
hu_ard = serial.Serial(port = '/dev/ttyACM1', baudrate = 9600, timeout = 0.1)
#so_ard = serial.Serial(port = '/dev/ttyACM2', baudrate = 9600, timeout = 0.1)
#si_ard = serial.Serial(port = '/dev/ttyACM3', baudrate = 9600, timeout = 0.1)
# arduino_list = [ha_ard, hu_ard, so_ard, si_ard]
arduino_list = [ha_ard, hu_ard]

# Flag Variables
fOveride = False;

################################################################################

# code must be ran using nohup python3 uno_read.py &

def main():
    print("<main> : Beginning code...")

    while True:
        print("<main> : Would you like to setup the data table? <Y/n>")
        table_set = input()
        table_set = table_set.lower()

        if table_set == 'y':
            setup_db()
            break
        elif table_set == 'n':
            break
        else:
            print("<main> ERROR: Improper input, please try again...")

    schedule.every().hour.at(":43").do(convert_TXT_SQL)
    schedule.every().hour.at(":30").do(convert_TXT_SQL)

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
            reset = input("Table already created... Overide? (Y/n)")
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
                      pname        varchar(25) not null, /* Plant Name */
                      pnumber      integer(2), /* Species - Sensor/Control */
                      cap          integer(3), /* Capacitance in Farads */
                      percH20      integer(2), /* Percent of Water */
                      moisStat     varchar(7), /* Plant Moisture Status */
                      res          integer(4), /* Resistance in Ohms */
                      lum          integer(4), /* Lumens */
                      tempC        integer(3), /* Temperature in Celsius */
                      tempF        integer(3), /* Temperature in Fahrenheit */
                      currTime     time, /* Time that data was taken */
                      primary key (pnumber)
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
    
    try:
        ''' SQLite3 CONNECTION '''
        conn = sqlite3.connect("veles_data.db")
        curs = conn.cursor()
        print("<convert_TXT_SQL> : Attempting connection to SQLite3...")

        ''' CREATE TIMESTAMP '''
        now = datetime.now()
        curr_time = now.strftime("%H:%M:%S")

        ''' COLLECTING DATA FROM SERIAL '''
        data_list = []
        for ard in arduino_list:
            data = ard.readline()
            ard_data = str(data, 'ascii').split("\t") # data from plant

            if len(ard_data) != 6: # Checks if all 6 expected values are present
                print("<convert_TXT_SQL> ERROR: %s had invalid read from sensors at %s..."
                    % (ard_data[0], current_time))
                continue

            ard_data.append(currTime)
            data_list.append(tuple(ard_data))


        ''' INSERT DATA INTO DATABASE '''
        db_insert = """INSERT INTO sensor_data
                    (pname, pnumber, cap, percH20, moisStat, res, lum
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
            % currTime)

    finally:
        if conn:
            conn.close()
            print("<convert_TXT_SQL> : SQLite3 connection closed...")

################################################################################

if __name__ == "__main__":
    main()
