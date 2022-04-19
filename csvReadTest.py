import csv
import urllib.request
import time

# ------- Setup the URL for Thingspeak.com Data Cloud --------
baseURL = 'http://api.thingspeak.com/update?key=9H44G9OF897TOOPJ'

file = open('E:/EVENT1.csv')

csvreader = csv.reader(file)

rows = []
for row in csvreader:
    rows.append(row)

count = 0
for row in rows:
    # ------- Send Sensor Data to the Cloud -----------
    f = urllib.request.urlopen(
        baseURL + '&field1=' + str(row[0]) + '&field2=' + str(row[1]) + '&field3=' + str(row[2]) + '&field4=' + str(row[3]))
    f.read()
    f.close()
    print('Iteration: ' + str(count))
    count = count + 1
    time.sleep(15)
