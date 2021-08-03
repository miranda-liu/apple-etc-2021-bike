import board
import time
from adafruit_clue import clue
import digitalio



class LED:
    def turn_on(self):
        self.value = True # sends 3.3V to pin

    def turn_off(self):
        # self = digitalio.DigitalInOut(pin)
        # self.direction = digitalio.Direction.OUTPUT
        self.value = False # sends 0V to pin

    # def brightness_control():


