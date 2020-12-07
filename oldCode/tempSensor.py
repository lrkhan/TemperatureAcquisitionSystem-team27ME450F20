import time
import datetime
import spidev
import math

# const values /dev/spidev{bus}.{cs}
bus = 0
cs = 0
bits = math.pow(2,12)

# create spi obj and set speed to 1.2 MHz
spi = spidev.SpiDev(bus, cs)
spi.max_speed_hz = 1200000000

# output file info
date = str(datetime.date.today())
path = "./saveData/"
outFile = path + (date + ".csv")
printFILE = open(outFile, "a")

# check to see if channel is in range
def channelERR(channel):
    error = "The channel chosen is not valid"
    
    if (channel > 15) or (channel < 0):
        print(error)
        return True
    else:
        return False

# get channel(s) from user
def getCHAN():
    chan = (input("Select a Channel (0 - 15): "))
    
    while channelERR(int(chan)) == True:
      chan = (input("Select a Channel (0 - 15): "))
    
    # Convert to int
    chan = int(chan)

    return chan

# send bits and recieve bits from ADC (returns float) 
def readADC(channel, vref=3.3):
    # resistor values
    res = [998, 994, 996, 984, 984, 984, 1001, 991, 994, 998]

    #DIN msg
    stdMsg = 0b0000100001000100
    chanMSG = 128*channel
    msg = stdMsg + chanMSG
    # send bits and a few extra to get the data we need 
    reply = spi.xfer2([msg, 0b0000000000])
    
    # combining the return bits to one bin number
    adc = 0
    for n  in reply:
        adc = (adc << 10) + n

    return adc

    # adds zeros to remove 0bXXX - XXX represents a return channel 
    adc = bin(adc)[4:].zfill(8)
    adc = int(adc,2)
    return adc
    voltage = (vref * adc) / bits
    rSys = 994 #res[channel]

    if voltage == 0:
        return 0
    r = (rSys * (vref - voltage) ) / voltage

    return voltage

    # Steinheart Model Constants
    A = 0.02324341278
    B = -0.003600335913
    C = 0.00001511095903

    # temp calcs
    temp = A + (B * math.log(r)) + (C * math.pow((math.log(r)), 3))
    temp = 1/temp
    temp = temp - 273.15

    return (temp)

# print the time
def printTime():
    return str(datetime.datetime.now())
    print(time,end='')
    printFILE.write(time)

# print the top info
def printTOP():
    top = "Time, CH00, CH01, CH02, CH03, CH04, CH05, CH06, CH07, CH08, CH09, CH10, CH11, CH12, CH13, CH14, CH15\n"
    printFILE.write(top)
    print(top)

# print the values read form the adc
def printVal(val):
    printFILE.write(str(val))
    print(val, end='')

# where the code runs
try:
    # number of channels being used
     nChan = getCHAN()
     
     # prints top informational section
     printTOP()
    
     #ADC config
     config = 0b1000000000000000
     spi.writebytes2([config])
     
     while True:
        adcVals = [0]*16
        
        # print time
        printTime()
        
        # read in vals
        for i in range(nChan+1):
            adcVals[i] = readADC(i)
        
        # print to comand line and write to file
        for value in adcVals:
            printFILE.write(', ')
            print(', ',end='')
            
            printVal(value)
        
        # finish this line and move on to new data
        printFILE.write("\n")
        print("")
        
        # delay timer
        time.sleep(1)

# closing statements
finally:
    spi.close()
    printFILE.close()
