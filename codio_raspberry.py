from grovepi import *
from grove_rgb_lcd import *
import time

dht_sensor_port = 7 #Connet de DHt sensor to port 7


while True:
    try:
        temp,hum = dht(dht_sensor_port,0)

        print ("temp =", temp, "C\thumadity", hum, "%")
        t = str(temp)
        h = str(hum)

        setRGB(0,128,64)
        setRGB(0,255,0)
        setText("Temp:" + t + "C " + "Humidity :" + h + "%")

    except (IOError,TypeError) as e:
        print ("Error")