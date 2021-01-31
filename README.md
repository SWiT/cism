CISM
====

Control Interface &amp; Sensor Monitoring

Read temperature and humidity data from DHT22 (AM2302) sensors attached to Raspberry Pi Zeros.  

Publish that data via MQTT to Home Assistyant https://www.home-assistant.io/

sudo apt update && sudo apt upgrade -y

sudo apt install python3-gpiozero python3-dev python3-pip git libgpiod2

sudo python3 -m pip install --upgrade pip setuptools wheel

sudo pip3 install Adafruit_DHT paho-mqtt adafruit-circuitpython-dht

sudo apt install mosquitto mosquitto-clients

sudo systemctl enable mosquitto

cd ~
git clone git@github.com:SWiT/cism.git


pip3 install adafruit-circuitpython-dht

sudo apt-get install libgpiod2