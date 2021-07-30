import board
import displayio
from adafruit_clue import clue

# key diff between Python and Java classes
    # Java --> accessing property methods --> variable = something
    # Python --> accessing properties with self.____

class Accelerometer:


    # acceleration values
    x = 0
    y = 0
    z = 0

    # alert
    acceleration_alert = False

    def get_acceleration(self):
        self.x, self.y, self.z = clue.acceleration


    def display_acceleration_values(self, clue_display):
        clue_display[0].text = "Acceleration"
        clue_display[1].text = "X: {:.2f}".format(self.x)
        clue_display[2].text = "Y: {:.2f}".format(self.y)
        clue_display[3].text = "Z: {:.2f}".format(self.z)

        clue_display.show()


    def collision_acceleration(self):
        if self.x > 18:
            # clue_display[5].text = "Impact detected"
            acceleration_alert = True
        # else:
            # clue_display[5].text = "No impact"
