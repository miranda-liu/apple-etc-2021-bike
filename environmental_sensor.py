import board
import displayio
from adafruit_clue import clue

class EnvironmentalSensor:
    # humidity, temperature, pressure, altitude

    pressure = -1
    humidity = -1
    temperature = -1
    altitude = -1


    def get_humidity(self):
        self.humidity = clue.humidity


    def get_temperature(self):
        self.temperature = clue.temperature


    def get_pressure(self):
        self.pressure = clue.pressure


    def get_altitude(self):
        self.altitude = clue.altitude
