import Adafruit_DHT
import paho.mqtt.client as paho
import os
import time
import cism

#DHT_SENSOR = Adafruit_DHT.DHT11
#DHT_SENSOR = Adafruit_DHT.DHT22
DHT_SENSOR = Adafruit_DHT.AM2302

# MQTT details
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883

# Output file name
LOGFILE = "/home/pi/cism.csv"
DEGREE = "F" # F or C

sensor = cism.CismSensor("Garden 1", 4, 0, 0)

def on_publish(client,userdata,result):             #create function for callback
    print("data published.")
    #print(userdata)
    #print(result)
    #print("\n");
    pass

def on_disconnect(client, userdata, rc):
   print("client disconnected ok")

    
client1 = paho.Client("control1")                   #create client object
client1.on_publish = on_publish                     #assign function to callback
client1.connect(MQTT_BROKER, MQTT_PORT)              #establish connection

try:
    f = open(LOGFILE, 'a+')
    if os.stat(LOGFILE).st_size == 0:
            f.write('DateTime,Sensor,Temperature(*'+DEGREE+'),Humidity(%)\r\n')
except:
    pass
    
humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, sensor.gpiopin)
if DEGREE == "F":
    temperature = temperature * (9 / 5) + 32

if humidity is not None and temperature is not None:
    ret = client1.publish("temperature","{0:0.1f}".format(temperature))
    ret = client1.publish("humidity","{0:0.1f}".format(humidity))
    f.write('{0},{1},{2:0.1f},{3:0.1f}\r\n'.format(time.strftime('%Y-%m-%d %H:%M:%S'), sensor.name, temperature, humidity))
else:
    ret = client1.publish(sensor.name,"FAILED")
    print("Failed to retrieve data from sensor")
    
   
client1.on_disconnect = on_disconnect
client1.disconnect()

