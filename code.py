import board
import displayio
from adafruit_clue import clue
from accelerometer import Accelerometer
from gyroscope import Gyroscope
from distance_sensor_4m import DistanceSensor4M
from twist_sensor import TwistSensor
# from button import Button

clue_display = clue.simple_text_display(text_scale=1, colors=(clue.WHITE,))
accel = Accelerometer()
gyro = Gyroscope()
dist = DistanceSensor4M()
twi = TwistSensor()
# clue_button = Button()


while True:
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
