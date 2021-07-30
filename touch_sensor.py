from sparkfun_Touch import Sparkfun_Touch as QwiicTouch
import board
import displayio
from adafruit_clue import clue
import time

class TouchSensor:

    touch = QwiicTouch( board.I2C() )

    def get_vals(self):
        vals = self.touch.readVal()
        for itr, i in enumerate(vals):
            if i == 127:
                vals[itr] = True
            else:
                vals[itr] = False
        return vals

    def get_back_button(self):
        return self.get_vals()[0]

    def get_middle_button(self):
        return self.get_vals()[1]
        
    def get_front_button(self):
        return self.get_vals()[2]

    def display_button_states(self, clue_display):
        clue_display[16].text = "Touch sensor"
        clue_display[17].text = "Vals: {:}".format(self.get_vals())
        clue_display.show()

    