import board
import displayio
from adafruit_clue import clue
from accelerometer import Accelerometer
from gyroscope import Gyroscope
from distance_sensor_4m import DistanceSensor4M
from twist_sensor import TwistSensor
from haptic_sensor import HapticSensor
from led import LED
import time
import digitalio
# from button import Button


clue_display = clue.simple_text_display(text_scale=1, colors=(clue.WHITE,))
accel = Accelerometer()
gyro = Gyroscope()
dist = DistanceSensor4M()
twi = TwistSensor()
# clue_button = Button()
hap = HapticSensor()


light_red_brake = LED()
light_yellow_left = LED()
light_yellow_right = LED()


light_red_brake = digitalio.DigitalInOut(board.P0)
light_red_brake.direction = digitalio.Direction.OUTPUT
light_red_brake.value = False

light_yellow_right = digitalio.DigitalInOut(board.P3)
light_yellow_right.direction = digitalio.Direction.OUTPUT
light_yellow_left.value = False

light_yellow_left = digitalio.DigitalInOut(board.P7)
light_yellow_left.direction = digitalio.Direction.OUTPUT
light_yellow_left.value = False

while True:
    # hap.trigger_pulse()
    dist.check_distance()
    accel.get_acceleration()
    accel.display_acceleration_values(clue_display)
    gyro.get_ang_vel()
    gyro.display_ang_vel_values(clue_display)
    dist.get_distance_millimeters()
    dist.display_distance(clue_display)
    # twi.twist_sensor()
    # twi.twist_sensor_init()
    twi.detect_twist_direction()
    twi.display_twist_sensor(clue_display)
    # twi.twist_reset()
    # twi.twist_sensor()


    if accel.x > 2 or accel.x < -2:
        light_red_brake.value = True
        time.sleep(2)
        light_red_brake.value = False
    if twi.twist_direction == "left":
        light_yellow_left.value = True
        time.sleep(2)
        light_yellow_left.value = False
        twi.twist_direction = "none"
    if twi.twist_direction == "right":
        light_yellow_right.value = True
        time.sleep(2)
        light_yellow_right.value = False
        twi.twist_direction = "none"



"""light1 = LED()
light2 = LED()

light1 = digitalio.DigitalInOut(board.P0)
light1.direction = digitalio.Direction.OUTPUT

light2 = digitalio.DigitalInOut(board.P1)
light2.direction = digitalio.Direction.OUTPUT

light3 = digitalio.DigitalInOut(board.P7)
light3.direction = digitalio.Direction.OUTPUT

while True:
    # light.turn_on(board.P0)
    light1.value = True
    time.sleep(2)
    # light.turn_off(board.P0)
    light1.value = False
    time.sleep(2)

    light2.value = True
    time.sleep(1)
    light2.value = False
    time.sleep(2)

    light3.value = True
    time.sleep(1)
    light3.value = False
    time.sleep(2)
"""
"""
import microcontroller
import board
import digitalio
import time
a_button = digitalio.DigitalInOut(board.BUTTON_A)
a_button.direction = digitalio.Direction.INPUT
flashlight = digitalio.DigitalInOut(board.WHITE_LEDS)
flashlight.direction = digitalio.Direction.OUTPUT
switch = digitalio.DigitalInOut(board.D0)
switch.direction = digitalio.Direction.OUTPUT
while True:
    switch.value = True
    time.sleep(1)


import microcontroller
import board
import digitalio
import time
a_button = digitalio.DigitalInOut(board.BUTTON_A)
a_button.direction = digitalio.Direction.INPUT
flashlight = digitalio.DigitalInOut(board.WHITE_LEDS)
flashlight.direction = digitalio.Direction.OUTPUT
switch = digitalio.DigitalInOut(board.D0)
switch.direction = digitalio.Direction.OUTPUT
while True:
    if a_button.value:
        flashlight.value = False
        switch.value = False
    else:
        flashlight.value = True
        switch.value = True
    time.sleep(1)
"""















# buttons on Clue board code
"""
    if clue.button_a:
        clue_button.button_a_pressed()
        break
    elif clue.button_b:
        clue_button.button_b_pressed()
        break
    """


# air quality sensor + environmental data code
"""
from adafruit_clue import clue
import adafruit_sgp30
import displayio
import time
import board

sgp30 = adafruit_sgp30.Adafruit_SGP30(board.I2C())
clue_display = clue.simple_text_display(text_scale=1, colors=(clue.WHITE,))
# time.sleep(15)
while True:
"""
"""
    print("Pressure: {:.3f} hPa".format(clue.pressure))
    print("Altitude: {:.1f} m".format(clue.altitude))
    print("Temperature: {:.1f} C".format(clue.temperature))
    print("Humidity: {:.1f} %".format(clue.humidity))
    """
"""
    clue_display[0].text = "Pressure: {:.3f} hPa".format(clue.pressure)
    clue_display[1].text = "Altitude: {:.1f} m".format(clue.altitude)
    clue_display[2].text = "Temperature: {:.1f} C".format(clue.temperature)
    clue_display[3].text = "Humidity: {:.1f} %".format(clue.humidity)



    eCO2, TVOC = sgp30.iaq_measure()
    # print(eCO2)
    # print(TVOC)
    clue_display[4].text = "TVOC" + str(TVOC)
    clue_display[5].text = "eCO2={:5d}".format(eCO2)



    TVOC.text = "TVOC={:5d}".format(TVOC)
    eco2.text = "eCO2={:5d}".format(eCO2)
"""
