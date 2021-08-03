import board
import time
from sparkfun_qwiic_vl53l1x import QwiicVL53L1X
from adafruit_clue import clue
from haptic_sensor import HapticSensor
from twist_sensor import TwistSensor
from clue_board import CBoard
from accelerometer import Accelerometer
# from led import LED


hap = HapticSensor()
twi = TwistSensor()
cboard = CBoard()
accel = Accelerometer()
# light = LED()


class DistanceSensor4M:


    # distance sensor returns in millimeters


    distanceMM = -1
    ToF = QwiicVL53L1X(clue._i2c)
    ToF.sensor_init()

    def get_distance_millimeters(self):
        # ToF = QwiicVL53L1X(clue._i2c)
        # ToF.sensor_init()
        #if (ToF.sensor_init() == None):					 # Begin returns 0 on a good init
         #   print("Sensor online!\n")
        self.ToF.start_ranging()	# Write configuration bytes to initiate measurement
        time.sleep(.005)
        self.distanceMM = self.ToF.get_distance() # Get the result of the measurement from the sensor
        time.sleep(.005)
        self.ToF.stop_ranging()
        #distanceInches = self.distanceMM / 25.4
        #distanceFeet = distanceInches / 12.0
        #print("Distance(mm): %s" % (self.distanceMM))


    def get_distance_centimeters(self):
        self.get_distance_millimeters()
        distanceCM = self.distanceMM * 10
        return distanceCM


    def get_distance_meters(self):
        self.get_distance_millimeters()
        distanceM = self.distanceMM * 100
        return distanceM


    def get_distance_inches(self):
        self.get_distance_millimeters()
        distanceIN = self.distanceMM / 25.4
        return distanceIN


    def get_distance_feet(self):
        self.get_distance_millimeters()
        distanceFT = self.distanceMM / 305
        return distanceFT


    def display_distance(self, clue_display):
        clue_display[11].text = "Distance sensor"
        clue_display[12].text = "Millimeters: {:.2f}".format(self.distanceMM)
        clue_display[13].text = "Feet: {:.2f}".format(self.get_distance_feet())

        clue_display.show()

    def check_distance(self):
        if self.get_distance_feet() < 1 and self.get_distance_inches() > 6:
            for i in range(3):
                twi.flash_color_blue()
                # cboard.close_enough()
        if self.get_distance_inches() < 6:
          #  hap.trigger_pulse()
            # cboard.close_enough()
            print("yay")

"""
    def configure_LEDs(self):
        switch0 = digitalio.DigitalInOut(board.D0) # red brake lights
        switch1 = digitalio.DigitalInOut(board.D1) # yellow turn signal - left
        switch2 = digitalio.DigitalInOut(board.D2) # yellow turn signal - right
"""
"""
    def turn_on_LEDs(self, switch0, switch1, switch2):
        if accel.x > 5:
            switch0 = True
            # turn on red LEDs
            time.sleep(5) # move this outside class
            # turn off red LEDs

        if twi.detect_twist_direction() == "left":
            switch1 = True
            # turn on left yellow LEDs
            time.sleep(5)
            # turn off left yellow LEDs


        if twi.detect_twist_direction() == "right":
            switch2 = True
            # turn on right yellow LEDs
            time.sleep(5)
            # turn off right yellow LEDs
    """

















"""
    print("VL53L1X Qwiic Test\n")
    ToF = QwiicVL53L1X(clue._i2c)
    if (ToF.sensor_init() == None): # Begin returns 0 on a good init
        print("Sensor online!\n")
    while True:
        try:
            ToF.start_ranging()	# Write configuration bytes to initiate measurement
            time.sleep(.005)
            distance = ToF.get_distance() # Get the result of the measurement from the sensor
            time.sleep(.005)
            ToF.stop_ranging()
            distanceInches = distance / 25.4
            distanceFeet = distanceInches / 12.0
            print("Distance(mm): %s Distance(ft): %s" % (distance, distanceFeet))
        except Exception as e:
            print(e)
    """
