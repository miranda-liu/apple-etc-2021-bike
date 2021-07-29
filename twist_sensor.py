from sparkfun_qwiictwist import Sparkfun_QwiicTwist as QwiicTwist
import board
import displayio
from adafruit_clue import clue

class TwistSensor:

    twist_count = -1
    twist = QwiicTwist( board.I2C() )

    def twist_sensor(self):
        self.twist_count = self.twist.count

    def display_twist_sensor(self, clue_display):
        clue_display[15].text = "Twist sensor"
        clue_display[16].text = "Twist count: {:}".format(self.twist_count)
        clue_display.show()



