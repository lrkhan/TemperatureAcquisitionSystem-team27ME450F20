#this file is is used to test specific parts of the code without the SPI library
import datetime

date = str(datetime.date.today())

print(date)

path = "./saveData/"
outFile = path + (date + ".csv") 
print(outFile)

#f = open(file, a)