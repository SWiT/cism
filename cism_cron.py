import Adafruit_DHT
import paho.mqtt.client as paho
import os
import time
import cism
import yaml

with open("config.yaml", 'r') as stream:
    try:
        cfg = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
    
MQTT_USER = cfg['mqtt']['user']
MQTT_PASS = cfg['mqtt']['pass']
MQTT_BROKER = cfg['mqtt']['broker']['address']
MQTT_PORT = cfg['mqtt']['broker']['port']
LOGFILE = cfg['logfile']
DEGREE = cfg['degree']
SENSORS = []
for s in cfg['sensors']:
    SENSORS.append(cism.Sensor(s['name'], s['gpiopin'], s['toffset'], s['hoffset']))

#DHT_SENSOR = Adafruit_DHT.DHT11
#DHT_SENSOR = Adafruit_DHT.DHT22
DHT_SENSOR = Adafruit_DHT.AM2302   

def on_publish(client,userdata,result):             #create function for callback
    print("data published.")
    pass

def on_disconnect(client, userdata, rc):
   print("client disconnected ok")

    
mqttclient = paho.Client("connection01")               #create client object
mqttclient.username_pw_set(MQTT_USER, MQTT_PASS)
mqttclient.on_publish = on_publish                     #assign function to callback
mqttclient.connect(MQTT_BROKER, MQTT_PORT)              #establish connection

# Create the log file if empty.
f = open(LOGFILE, 'a+')
if os.stat(LOGFILE).st_size == 0:
    f.write('DateTime,Name,Temperature(*'+DEGREE+'),Humidity(%)\r\n')
    
# Read each of the sensors data
for sensor in SENSORS:
    
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, sensor.gpiopin)
    
    if DEGREE == "F":
        temperature = temperature * (9 / 5) + 32

    if humidity is not None and temperature is not None:
        # Publish the data
        ret = mqttclient.publish(sensor.name+"/temperature","{0:0.1f}".format(temperature))
        ret = mqttclient.publish(sensor.name+"/humidity","{0:0.1f}".format(humidity))
        f.write('{0},{1},{2:0.1f},{3:0.1f}\r\n'.format(time.strftime('%Y-%m-%d %H:%M:%S'), sensor.name, temperature, humidity))
    else:
        ret = mqttclient.publish(sensor.name,"FAILED")
        print("Failed to retrieve data from sensor")
    
   
mqttclient.on_disconnect = on_disconnect
mqttclient.disconnect()

