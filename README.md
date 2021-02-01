CISM
====
Control Interface &amp; Sensor Monitoring

Read temperature and humidity data from DHT22 (AM2302) sensors attached to Raspberry Pi Zeros.  

Publish that data via MQTT to Home Assistant https://www.home-assistant.io/
====

sudo apt update && sudo apt upgrade -y

sudo apt install python3-gpiozero python3-dev python3-pip git libgpiod2 screen mosquitto-clients

sudo python3 -m pip install --upgrade pip setuptools wheel

sudo pip3 install Adafruit_DHT paho-mqtt adafruit-circuitpython-dht pyyaml

cd ~
git clone https://github.com/SWiT/cism.git

# Add "*/5 * * * * python3 /home/pi/cism/cism_cron.py" to cron
crontab -e