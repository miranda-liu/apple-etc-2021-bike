import board
import time
from sparkfun_qwiic_vl53l1x import QwiicVL53L1X
from adafruit_clue import clue

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
