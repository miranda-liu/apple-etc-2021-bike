# imports
import displayio
import terminalio
from adafruit_clue import clue

# QUESTIONS
    # How do we set up the code for an external or already on the board sensor?
    # Where do we find the lib files for these sparkfun sensors?
    # How can we split up each sensor into its own .py file for organization? Or is there a better way we can organize this?
    # How can we send signals between the Clue boards and the breadboard that was in the Arduino green plastic box kit?
        # Bluetooth?
        # Wires?

# accelerometer (on board) (back of bike)
    # sense when there is a sudden change in speed --> sends signal for brake lights to breadboard on back of bike
    # in conjunction with gyroscope, sense collisions/falls



# gyroscope (on board) (back of bike)
    # sense when there is a sudden change in rotation --> sense collision (in conjunction with accelerometer)
    # sends signal to alert biker (phone, sounds from the board, maybe use the lights as well, or the screen of the Clue board)



# distance sensor (4m, off board) (back of bike)
    # sense an approaching object --> when the approaching object passes a certain threshold --> sends signal for some type of alert for the biker
    # sends signal to alert biker (phone, sounds from the board, maybe use the lights as well, or the screen of the Clue board)



# LIDAR sensor (on board) (back of bike)
    # use it to back up the distance sensor



# button A/B (on board) (front of bike)
    # sense user input for R/L turn signals --> sends signal for turn signal to breadboard on back of bike



# capacitive touch slider (off board) (front of bike)
    # sense user input for R/L turn signals --> sends signal for turn signal to breadboard on back of bike



