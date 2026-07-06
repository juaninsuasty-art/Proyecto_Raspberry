from grovepi import *
from grove_rgb_lcd import *
import time

dht_sensor_port = 7 #Connet de DHt sensor to port 7


while True:
    try:
        temp,hum = dht(dht_sensor_port,0)


        print("temp =", temp, "C\thumadity", hum, "%")
        t = str(temp)
        h = str(hum)


        setRGB(255,255,255)
        setText("Temp:" + t + "C " + "Humedad :" + h + "%")

        time.sleep(1)

    except (IOError,TypeError) as e:
        print("Error", e)
        time.sleep(1)