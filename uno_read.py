import serial
import time
from datetime import datetime


# Arduino Variables
# ha_ard = serial.Serial(port = '/dev/cu.usbmodem1301', baudrate = 9600,
# timeout = 0.1) # Arduino 1
# hu_ard = serial.Serial(port = '', baudrate = 9600, timeout = 0.1) # Arduino 2
# so_ard = serial.Serial(port = '', baudrate = 9600, timeout = 0.1) # Arduino 3
# si_ard = serial.Serial(port = '', baudrate = 9600, timeout = 0.1) # Arduino 4
# arduino_list = [ha_ard, hu_ard, so_ard, si_ard]

# Flag Variables
fOveride = True;

################################################################################

def main():
    # Commented code should work if proper serial ports are entered for Arduinos
    # setup_db()
    # while True:
    #     convert_TXT_SQL(arduino_list)
    print("<main> : Ran code")

################################################################################

def setup_db():
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
                      res          integer(4), /* Resistance in Ohms */
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

def convert_TXT_SQL(ard_list):
    try:

        ''' SQLite3 CONNECTION '''
        conn = sqlite3.connect("veles_data.db")
        curs = conn.cursor()
        print("Attempting connection to SQLite3...\n")

        ''' CREATE TIMESTAMP '''
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        ''' COLLECTING DATA FROM SERIAL '''
        data_list = []
        for ard in ard_list:
            data = ard.readline()
            ard_data = data.split("\t") # data from plant

            if len(ard_data) != 6: # Checks if all 6 expected values are present
                print("ERROR: %s had invalid read from sensors at %s..."
                    % (ard_data[0], current_time))
                continue

            ard_data.append(currTime)
            data_list.append(tuple(ard_data))


        ''' INSERT DATA INTO DATABASE '''
        db_insert = """INSERT INTO sensor_data
                    (pname, pnumber, cap, res, tempC, tempF, currTime)
                    VALUES (?, ?, ?, ?, ?, ?, ?);"""
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
