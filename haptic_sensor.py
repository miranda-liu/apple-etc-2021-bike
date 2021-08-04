from sparkfun_qwiic_haptic import Sparkfun_Haptic as QuiicHaptic
import board
import displayio
from adafruit_clue import clue
import time

class HapticSensor:

    haptic = QuiicHaptic(board.I2C())

    def test(self):
        while(True):
            self.trigger_pulse()
            time.sleep(1)

    def trigger_pulse(self):
        self.haptic.setVib(127)
        time.sleep(1)
        self.haptic.setVib(0)
        # print("Pulsed")

    def haptic_on(self):
        self.haptic.setVib(127)

    def haptic_off(self):
        self.haptic.setVib(0)
