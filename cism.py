class CismSensor:
    def __init__(self, name = "Sensor", pin = 4, toffset = 0, hoffset = 0):
        self.name = name
        self.gpiopin = pin
        self.toffset = toffset
        self.hoffset = hoffset