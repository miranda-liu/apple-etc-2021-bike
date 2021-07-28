import board
import displayio
from adafruit_clue import clue
from qwiic_VL53L1X import QwiicVL53L1X as Distance

# from sparkfun_qwiictwist import Sparkfun_QwiicTwist as QwiicTwist

clue_display = clue.simple_text_display(text_scale=3, colors=(clue.WHITE,))
clue_display[0].text = "Hello"

mySensor = qwiic_VL53L1X.QwiicVL53L1X()
mySensor.SensorInit()

while True:
    clue_display.show()
    x, y, z = clue.acceleration

    clue_display[2].text = "X: {:.2f}".format(x)
    clue_display[3].text = "Y: {:.2f}".format(y)
    clue_display[4].text = "Z: {:.2f}".format(z)

    ToF.StartRanging()						 # Write configuration bytes to initiate measurement
    time.sleep(.005)
    distance = ToF.GetDistance()	 # Get the result of the measurement from the sensor
    time.sleep(.005)
    ToF.StopRanging()

    clue_display[5].text = distance

# try to increase # of times the acceleration sensor is getting data

