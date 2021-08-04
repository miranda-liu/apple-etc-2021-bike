import board
import time
import pwmio
from adafruit_clue import clue
# from distance_sensor_4m import DistanceSensor4M


buzzer = pwmio.PWMOut(board.SPEAKER, frequency=440, duty_cycle= 0, variable_frequency=True)
SPEAKER_ON  = 0x7FFF
SPEAKER_OFF = 0x0000
# dist = DistanceSensor4M()

class CBoard():
    def get_note(self, scale_degree, octave):
        ptonic_scale_c = [[32, 36, 41, 49, 55],
                [65, 73, 82, 98, 110],
                [130, 146, 164, 196, 220],
                [261, 293, 329, 392, 440],
                [522, 586, 658, 784, 880],
                [1044, 1172, 1316, 1568, 1760]]
        return ptonic_scale_c[octave][scale_degree]

    def play_sounds(self):
        buzzer.frequency = self.get_note(3, 0)


    def close_enough(self):
        #if dist.get_distance_feet() < 1:
        buzzer.duty_cycle = SPEAKER_ON
        self.play_sounds()
        time.sleep(2)
        buzzer.duty_cycle = SPEAKER_OFF















"""
def get_note(scale_degree, octave):
    Get note from Pentatonic Scale in C. From C1 to C6
        scale_degree : Selects the corresponding note in the scale by scale position
        octave : Selects which octave, octave = 0 corresponds to the C1 octave
​
    # These lists of integers represent the frequencies of the notes in the C Pentatonic scale separated by octave
    ptonic_scale_c =    [[32, 36, 41, 49, 55],
                        [65, 73, 82, 98, 110],
                        [130, 146, 164, 196, 220],
                        [261, 293, 329, 392, 440],
                        [522, 586, 658, 784, 880],
                        [1044, 1172, 1316, 1568, 1760]]
​
    return ptonic_scale_c[octave][scale_degree]
​
def value2note(val):
   Map notes in scale to linear value from 0 to 255
    note = 30 * val // 256 #
    scale_degree = note % 5 # modulus operator will wrap result from 0 to 4
    octave = note // 5 # octave will count up every 5 notes
    return scale_degree, octave
#Definitions to remember what a value represents
SPEAKER_ON  = 0x7FFF # Speaker will be on when the duty cycle is 50% or 0xFFFF/2 = 0x7FFF
SPEAKER_OFF = 0x0000  # Speaker will be off if the duty cycle is 0% or 0x0000
​
#Run this piece of code while True is True, so forever...
while True:
​
    # Tones can only be head if...
    if clue.button_a: # Button A is pressed
        buzzer.duty_cycle = SPEAKER_ON
    else: # Otherwise...
        buzzer.duty_cycle = SPEAKER_OFF #Stay on Mute
​
    # Read any sensor and keep the value between 0 and 255
    # For example, the proximity sensor...
    proximity = clue.proximity & 0xFF #Read Proximity Sensor and keep value between 0 and 255
    scale_degree, octave = value2note(proximity) # Convert value to note
    # print(scale_degree,octave, proximity)
    buzzer.frequency = get_note(scale_degree, octave) #Play selected note in speaker by setting the pulse frequency equal to the note's frequency
    time.sleep(0.1) # Wait here for 0.1 seconds before repeating loop
"""
