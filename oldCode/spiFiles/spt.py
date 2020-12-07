import time
import datetime
import spidev

# const values /dev/spidev{bus}.{cs}
bus = 0
cs = 0

#create spi obj and set speed to 1.2 MHz
spi = spidev.SpiDev(bus, cs)
spi.max_speed_hz = 1200000

def channelERR(channel):
    error = "The channel chosen is not valid"
    
    if (channel > 15) or (channel < 0):
        print(error)
        return True
    else:
        return False

def getCHAN():
    chan = (input("Select a Channel (0 - 15): "))
    
    while channelERR(int(chan)) == True:
      chan = (input("Select a Channel (0 - 15): "))
    
    # Convert to int
    chan = int(chan)

    return chan

def readADC(channel, vref=3.3):
    
    #DIN msg
    stdMsg = 0b0000100000100100
    chanMSG = 128*channel
    msg = stdMsg + chanMSG
    # send bits and a few extra to get the data we need 
    reply = spi.xfer2([msg, 0b00000000])
    
    # combining the return bits to one bin number
    adc = 0
    for n  in reply:
        adc = (adc << 8) + n
    
    # removes 2 lsb = 0
    adc = adc >> 2
    
    # adds zeros to remove 0bXXX - XXX represents a return channel 
    adc = bin(adc)[5:].zfill(8)
    adc = int(adc,2)
    
    voltage = (vref * adc) /1024
    
    return (voltage)

def printTime():
    print(datetime.datetime.now(),end='')

def printTOP():
    print("Time, CH00, CH01, CH02, CH03, CH04, CH05, CH06, CH07, CH08, CH09, CH10, CH11, CH12, CH13, CH14, CH15")

def printVal(val):
    print(val, end='')

try:
    # number of channels being used
     nChan = getCHAN()
     
     printTOP()

     while True:
        adcVals = [0]*16
        
        # print time
        printTime()

        # read in vals
        for i in range(nChan+1):
            adcVals[i] = readADC(i)

        for value in adcVals:
            print(', ',end='')
            printVal(value)
        
        print("")

        time.sleep(0.5)

finally:
    spi.close()
