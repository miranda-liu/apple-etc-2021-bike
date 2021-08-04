from sparkfun_qwiictwist import Sparkfun_QwiicTwist as QwiicTwist
import board
import displayio
from adafruit_clue import clue
import time

IS_BUTTON_CLICKED = 0x4 #(1 << 2) since we are getting back reg values
IS_BUTTON_PRESSED = 0x2 #(1 << 1) since we are getting back reg values

class TwistSensor:


    twist_count = 0
    twist = QwiicTwist( board.I2C() )
    twist_direction = "none"
    twist_sensor_pressed = False
    twist_sensor_clicked = False


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
        if self.twist.count > 2 and self.twist.count < 10:
            print("twisted right")
            self.twist.count = 0
            self.change_color_red()
            time.sleep(0.7)
            self.change_color_reset()
            self.twist_direction = "right"

        elif self.twist.count< -2 and self.twist.count >-10:
            print("twisted left")
            self.twist.count = 0
            self.change_color_green()
            time.sleep(0.7)
            self.change_color_reset()
            self.twist_direction = "left"

    def turn_on_red_brake_lights(self):
        if self.twist.count >= 10:
            # print("pressed v2")
            self.twist.count = 0
            self.change_color_blue()
            time.sleep(0.7)
            self.change_color_reset()
            return True


    def change_color_red(self):
        self.twist.set_color(230, 32, 25)

    def change_color_green(self):
        self.twist.set_color(25, 230, 49)

    def change_color_blue(self):
        self.twist.set_color(107, 228, 255)

    def change_color_orange(self):
        self.twist.set_color(255, 163, 64)

    def flash_color_blue(self):
        self.change_color_blue()
        # time.sleep(0.5)
        # self.change_color_reset()
        # time.sleep(0.5)


    def change_color_reset(self):
        self.twist.set_color(255, 255, 255)

    def detect_pressed(self):
        if self.twist.pressed == IS_BUTTON_PRESSED:
            self.twist_sensor_pressed = True
            self.change_color_blue()
            time.sleep(0.5)
            self.change_color_reset()


    def detect_clicked(self):
        if self.twist.clicked == IS_BUTTON_CLICKED:
        # click = self.twist.clicked
            self.twist_sensor_clicked = True
            self.change_color_red()
            time.sleep(0.5)
            self.change_color_reset()
            return True

    """
    def detect_pressed(self):
        if self.twist.pressed == IS_BUTTON_PRESSED:
            # time.sleep(0.5) # Adjust time to press detection as long as needed
            # if self.twist.pressed == IS_BUTTON_PRESSED:
            return True



    """


"""
from sparkfun_qwiictwist import Sparkfun_QwiicTwist as QwiicTwist
import board
import displayio
from adafruit_clue import clue
import time

IS_BUTTON_CLICKED = 0x4 #(1 << 2) since we are getting back reg values
IS_BUTTON_PRESSED = 0x2 #(1 << 1) since we are getting back reg values


class TwistSensor:


    twist_count = 0
    twist = QwiicTwist( board.I2C() )
    twist_direction = "none"
    twist_sensor_pressed = False


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

    def detect_pressed(self):
        if self.twist.pressed == IS_BUTTON_PRESSED:
            time.sleep(0.5) # Adjust time to press detection as long as needed
            if self.twist.pressed == IS_BUTTON_PRESSED:
                return True

    def detect_clicked(self):
        if self.twist.clicked == IS_BUTTON_CLICKED:
            return True

"""


