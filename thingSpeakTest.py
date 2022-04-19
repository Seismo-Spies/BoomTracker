import time
import urllib.request
import random

# ------- Setup the URL for Thingspeak.com Data Cloud --------

baseURL = 'http://api.thingspeak.com/update?key=I738P3JF6A0UGU8H'

def NumGen():
    num = random.randint(0, 9)
    return num


for x in range(10):
    # ------- Send Sensor Data to the Cloud -----------
    f = urllib.request.urlopen(baseURL + '&field1=' +
                               str(time.time()) + '&field2=' + str(NumGen()))
    f.read()
    f.close()
    print("Iteration: " + str(x))

    # ------ 20 second timer --------
    time.sleep(20)
