import board
import displayio
from adafruit_clue import clue

class Gyroscope:


     # angular velocity values
    x = 0
    y = 0
    z = 0


    def get_ang_vel(self):
        self.x, self.y, self.z = clue.gyro


    def display_ang_vel_values(self, clue_display):
        clue_display[7].text = "Gyroscope: angular velocity"
        clue_display[8].text = "X: {:.2f}".format(self.x)
        clue_display[9].text = "Y: {:.2f}".format(self.y)
        clue_display[10].text = "Z: {:.2f}".format(self.z)

        clue_display.show()


    def collision_gyroscope(self):
        if self.x > 18:
            clue_display[11].text = "Impact detected"
        else:
            clue_display[11].text = "No impact"
