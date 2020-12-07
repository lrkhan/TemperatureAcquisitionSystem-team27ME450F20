import serial
import time
import datetime

ser = serial.Serial('/dev/ttyACM0', 1200)

# output file info
date = str(datetime.date.today())
path = "./saveData/"
outFile = path + (date + ".csv")
printFILE = open(outFile, "a")

# print the top info
def printTOP():
    top = "\nTime, CH00, CH01, CH02, CH03, CH04, CH05, CH06, CH07, CH08, CH09"
    printFILE.write(top)
    print(top)

def topFile():
    print('\n',date)
    printFILE.write(date)
    printTOP()

def printData(dateIN, readIN):
    printFILE.write(dateIN + ", " + readIN + "\n")
    print(dateIN,',',readIN)


try:
    topFile()
    ser.readline()
    while True:
        if ser.in_waiting > 0:
            dateTIME = str(datetime.datetime.now())
            output = str(ser.readline())
            output = output[2:-5]
            printData(dateTIME, output)



finally:
    printFILE.close()
    print("\nProgram Terinated")