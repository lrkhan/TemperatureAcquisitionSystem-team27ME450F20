import serial
import time
import datetime
import gspread

# SetUp for Google Sheets - commented out
gc = gspread.service_account(filename="credentials.json")
sh = gc.open_by_key('1KxQs-sXtK4b5pK-4ShMgG22hfLjVjQGQMqZ2yrzcFQU')

# Adruino Communication Line
ser = serial.Serial('/dev/ttyACM0', 1200)

# output file info
date = str(datetime.date.today())
dtime = str(datetime.datetime.now())
path = "./saveData/"
outFile = path + (date + ".csv")
printFILE = open(outFile, "a")
index = 0
cellIndex = 1

# print the top info
def printTOP():
    top = "\nTime, CH00, CH01, CH02, CH03, CH04, CH05, CH06, CH07, CH08, CH09\n"
    printFILE.write(top)
    print(top)

def topFile():
    print('\n',dtime)
    printFILE.write(dtime)
    printTOP()

def printData(dateIN, readIN, celIN):
    output = str(dateIN) + "," + str(readIN) 
    printFILE.write(output + "\n")
    write2sheet(output, celIN)
    print(dateIN,',',readIN)

# google info
# creates and selects new sheet with [name]
def createSheet(name):
    ws = sh.worksheet(name)
    return ws

# checks to see if sheet is already made and makes or itterates over the title
def sheet():
    title ="Current"
    return createSheet(title) 

# writes header to row 1 if no header present
def header():
    header = ["Index", "Ch0","Ch1","Ch2","Ch3","Ch4","Ch5","Ch6","Ch7","Ch8","Ch9"]
    head = worksheet.row_values(1)
    if head != header:
        worksheet.insert_row(header, 1)

# write data
def write2sheet(data, row):
    info = list(map(float, data.split(",")))
    worksheet.insert_row(info, row)

try:
    worksheet = sheet()
    header()
    topFile()
    ser.readline()
    while True:
        if ser.in_waiting > 0:
            index += 1
            cellIndex += 1
            output = str(ser.readline())
            output = output[2:-5]
            printData(index, output, cellIndex)
            time.sleep(2)
            output = str(ser.readline())
            output = str(ser.readline())
            output = str(ser.readline())


finally:
    printFILE.close()
    print("\nProgram Terinated")