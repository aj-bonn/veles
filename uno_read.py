import serial
import numpy as np
import time
from datetime import datetime


# Arduino Variables
ha_ard = serial.Serial(port = '/dev/cu.usbmodem1301', baudrate = 9600, timeout = 0.1) # Arduino 1
# hu_ard = serial.Serial(port = '', baudrate = 9600, timeout = 0.1) # Arduino 2
# so_ard = serial.Serial(port = '', baudrate = 9600, timeout = 0.1) # Arduino 3
# si_ard = serial.Serial(port = '', baudrate = 9600, timeout = 0.1) # Arduino 4

def main():
    print("Ran code")

# might not need this
def write_data(ard):
    pdata = []
    pdata.append(ard.readline())

    f = open("plant_data.txt", "a")
    for plant in pdata:
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
            pdict[] =

def convert_


    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")

if __name__ == "__main__":
    main()
