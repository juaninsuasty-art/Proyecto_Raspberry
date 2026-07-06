from grovepi import *
from grove_rgb_lcd import *
import time
import math
import pymysql

# Puerto donde esta conectado el sensor DHT en GrovePi+
dht_sensor_port = 7

# Tipo de sensor:
# 0 = DHT11
# 1 = DHT22
tipo_sensor = 0

# Tiempo entre lecturas
INTERVALO_LECTURA = 60   # 60 segundos = 1 minuto

# Conexion a MariaDB
try:
    db = pymysql.connect(
        host="localhost",
        user="sensor_user",
        password="1234",
        database="sensores12"
    )

    cursor = db.cursor()
    print("Conexion exitosa a MariaDB")

except Exception as e:
    print("ERROR conectando a MariaDB:")
    print(e)

    setRGB(255, 0, 0)
    setText("Error DB")

    exit()


while True:
    try:
        print("Leyendo sensor...")

        temp, hum = dht(dht_sensor_port, tipo_sensor)

        print("Lectura recibida:", temp, hum)

        if (temp is not None and hum is not None and
            not math.isnan(temp) and not math.isnan(hum) and
            0 <= temp <= 50 and
            20 <= hum <= 90):

            print("Temp =", temp, "C  Humedad =", hum, "%")

            t = str(temp)
            h = str(hum)

            setRGB(255, 255, 255)
            setText("Temp:" + t + "C\nHumedad:" + h + "%")

            # Guardar en MariaDB
            sql = "INSERT INTO mediciones (temperatura, humedad) VALUES (%s, %s)"
            valores = (temp, hum)

            cursor.execute(sql, valores)
            db.commit()

            print("Dato guardado en la base de datos")

        else:
            print("Lectura invalida, no se guarda")

            setRGB(255, 0, 0)
            setText("Lectura\ninvalida")

        time.sleep(INTERVALO_LECTURA)

    except (IOError, TypeError) as e:
        print("Error leyendo sensor:")
        print(e)

        setRGB(255, 0, 0)
        setText("Error sensor")

        time.sleep(INTERVALO_LECTURA)

    except pymysql.MySQLError as e:
        print("Error guardando en MariaDB:")
        print(e)

        setRGB(255, 0, 0)
        setText("Error DB")

        time.sleep(INTERVALO_LECTURA)

    except KeyboardInterrupt:
        print("Programa detenido por el usuario")

        cursor.close()
        db.close()

        break