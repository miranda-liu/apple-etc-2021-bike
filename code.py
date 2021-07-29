import board
import displayio
from adafruit_clue import clue
from accelerometer import Accelerometer
from gyroscope import Gyroscope
from distance_sensor_4m import DistanceSensor4M

clue_display = clue.simple_text_display(text_scale=1, colors=(clue.WHITE,))
accel = Accelerometer()
gyro = Gyroscope()
dist = DistanceSensor4M()

while True:
    accel.get_acceleration()
    accel.display_acceleration_values(clue_display)

    gyro.get_ang_vel()
    gyro.display_ang_vel_values(clue_display)

    dist.get_distance_millimeters()
    dist.display_distance(clue_display)
