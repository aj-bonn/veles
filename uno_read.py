import serial
import time
from datetime import datetime


# Arduino Variables
ha_ard = serial.Serial(port = '/dev/cu.usbmodem1301', baudrate = 9600,
timeout = 0.1) # Arduino 1
# hu_ard = serial.Serial(port = '', baudrate = 9600, timeout = 0.1) # Arduino 2
# so_ard = serial.Serial(port = '', baudrate = 9600, timeout = 0.1) # Arduino 3
# si_ard = serial.Serial(port = '', baudrate = 9600, timeout = 0.1) # Arduino 4

# Flag Variables
fOveride = 0;

################################################################################

def main():
    print("Ran code")

################################################################################

def setup_db():
    ''' ESTABLISHING CONNECTION '''
    conn = sqlite3.connect("veles_data.db")
    curs = conn.cursor()

    ''' CREATING TABLE '''
    # Get rid of possible duplicate
    while fOveride is 1:
        reset = input("Table already created... Overide? (Y/n)")
        print(reset)
        reset.lower()
        if reset is "y":
            fOveride = 0
            curs.execute("DROP TABLE IF EXISTS VELES_DATA")
        elif reset not "n":
            print("ERROR: Improper input...")
        else:
            return

    table = CREATE TABLE veles_data (
      pname        varchar(25) not null, /* Plant Name */
      pnumber      integer(2), /* Species - Sensor/Control */
      cap          integer(3), /* Capacitance in Farads */
      res          integer(4), /* Resistance in Ohms */
      tempC        integer(3), /* Temperature in Celsius */
      tempF        integer(3), /* Temperature in Fahrenheit */
      currTime     time, /* Time that data was taken */
      primary key (pnumber)
    ); # Establishing table formating

    curs.execute(table)
    print("Created table...")
    conn.close()

    fOveride = 1

################################################################################

def convert_TXT_SQL(ard_list):
    for ard in ard_list:
        data = ard.readline()
        plist = data.split("\t") # data from plant
        i = 0 # counter variable
        if len(plist) not 6:
            print("ERROR: Invalid read from sensors...")
            return



    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")

################################################################################

#  might not need this
def write_data(ard):
    pdata = []
    pdata.append(ard.readline())

    f = open("plant_data.txt", "a")
    f.write(plant)
    f.close()

def convert_TXT_JSON(ard_list):
    data_pts = ['pname', 'pnumber', 'cap', 'res', 'C', 'F', 'time']
    pdict = {}

    for ard in ard_list:
        data = ard.readline()
        plist = data.split("\t") # data from plant
        i = 0 # counter variable
        while (i < len(data_pts)):
            # pdict[] =

if __name__ == "__main__":
    main()
