from sparkfun_qwiictwist import Sparkfun_QwiicTwist as QwiicTwist
import board
import displayio
from adafruit_clue import clue
import time

class TwistSensor:


    twist_count = 0
    twist = QwiicTwist( board.I2C() )
    twist_direction = "none"


    def twist_sensor_init(self):
        # self.twist_count = self.twist.count
        self.twist_count = 0


    def twist_reset(self):
        self.twist_count = 0


    def display_twist_sensor(self, clue_display):
        clue_display[15].text = "Twist sensor"
        clue_display[16].text = "Twist count: {:}".format(self.twist.count)
        clue_display.show()


    def detect_twist_direction(self):
        if self.twist.count > 5:
            print("twisted right")
            self.twist.count = 0
            self.change_color_red()
            time.sleep(1.5)
            self.change_color_reset()
            self.twist_direction = "right"

        elif self.twist.count< -5:
            print("twisted left")
            self.twist.count = 0
            self.change_color_green()
            time.sleep(1.5)
            self.change_color_reset()
            self.twist_direction = "left"


    def change_color_red(self):
        self.twist.set_color(230, 32, 25)

    def change_color_green(self):
        self.twist.set_color(25, 230, 49)

    def change_color_blue(self):
        self.twist.set_color(107, 228, 255)

    def flash_color_blue(self):
        self.change_color_blue()
        time.sleep(0.5)
        self.change_color_reset()
        time.sleep(0.5)


    def change_color_reset(self):
        self.twist.set_color(255, 255, 255)



