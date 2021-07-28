
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_clue import clue
from adafruit_display_text.label import Label
from appleetc_camperkit.ble import ETCPacket
import board
import displayio
import random
from sparkfun_qwiictwist import Sparkfun_QwiicTwist as QwiicTwist
import terminalio
import time

# The game object contains all the logic and behavior needed to play the game.
#
# This code uses the concept of a "state machine" to support all the behaviors
# of the game. Instead of writing one long function with all the code in it,
# different "states" of the game are broken out into smaller code sections.
#
# The game states roughly match the UI wireframe of the game's design but with
# specific states for each type of game action (press, shake, twist etc.)
#
#                                           (Timer)
#                                              |        +->[PressMe]-+
#                                              v        |            |->[GameSuccess]-+
# [Welcome] -+-------------------------->[GameActive]---+->[ShakeMe]-+                +-+
#    ^       |                             ^   |  ^     |            |->[GameFailure]-+ |
#    |       |                             |   |  |     +->[TwistMe]-+                  |
#    |       |                             |   |  |                                     |
#    |       +-> [WaitForBluetooth]--------+   |  +-------------------------------------+
#    |                                         v
#    +------------------------------------[GameOver]
#
# Each state handles one piece of behavior such as showing the Welcome screen
# or checking for button presses. States can then transition into other states,
# or other events like a timer event may lead to transitions as well.
#
#
class CamperGame:

    def __init__(self, ble):
        # Use the Bluetooth LE object to set up a UART (serial) communication service
        self.uart_service = UARTService()
        self.ble = ble

        # Initialize the graphics we'll show on the display.
        self.display = board.DISPLAY

        #  During gameplay, there are three text fields on the screen:
        #
        #      +---------------+
        #      |     Time      |
        #      |               |
        #      |    *ACTION*   |
        #      |               |
        #      |     Score     |
        #      +---------------+
        #
        self.time_label = Label(terminalio.FONT, text="Time", scale=2)
        self.time_label.anchor_point = (0.5, 0)
        self.time_label.anchored_position = (self.display.width // 2, 0)
        self.action_label = Label(terminalio.FONT, text="Action", scale=3)
        self.action_label.anchor_point = (0.5, 0.5)
        self.action_label.anchored_position = (self.display.width // 2, self.display.height // 3)
        self.score_label = Label(terminalio.FONT, text="Score", scale=2)
        self.score_label.anchor_point = (0.5, 1)
        self.score_label.anchored_position = (self.display.width // 2, self.display.height)
        self.game_playing_display = displayio.Group()
        self.game_playing_display.append(self.time_label)
        self.game_playing_display.append(self.action_label)
        self.game_playing_display.append(self.score_label)

        #  The game over screen has three text fields on the screen, but with different
        #  font sizes and meanings, so we set this up as a different layer on the screen.
        #  (The game over screen is reused for the welcome screen as well to save memory
        #  on the microcontroller.)
        #
        #      +---------------+
        #      |    Welcome    |
        #      |               |
        #      |    *SCORE*    |
        #      |               |
        #      | Instructions  |
        #      +---------------+
        #
        self.game_over_label = Label(terminalio.FONT, text="Welcome", scale=3)
        self.game_over_label.anchor_point = (0.5, 0)
        self.game_over_label.anchored_position = (self.display.width // 2, 0)
        self.game_over_score_label = Label(terminalio.FONT, text="Score", scale=3)
        self.game_over_score_label.anchor_point = (0.5, 0.5)
        self.game_over_score_label.anchored_position = (self.display.width // 2, self.display.height // 2)
        self.game_over_instructions_label = Label(terminalio.FONT, text="Press B to play again")
        self.game_over_instructions_label.anchor_point = (0.5, 1)
        self.game_over_instructions_label.anchored_position = (self.display.width // 2, self.display.height)
        self.game_over_display = displayio.Group()
        self.game_over_display.append(self.game_over_label)
        self.game_over_display.append(self.game_over_score_label)
        self.game_over_display.append(self.game_over_instructions_label)

        # If you don't want sound during the game, set this to False
        self.play_tones = True

        # All of this information is exchanged over Bluetooth to a connected device.
        self.playing = False
        self.game_last_updated = 0
        self.display_last_updated = 0
        self.time_remaining = 0
        self.urgent = False
        self.score = 0

        # Local state of the game.
        self.state = None
        self.states = {}

        # All supported states of the game.
        self.add_state( Welcome() )
        self.add_state( GameActive() )
        self.add_state( GameSuccess() )
        self.add_state( GameFailure() )
        self.add_state( GameOver() )
        self.add_state( PressMe() )
        self.add_state( TwistMe() )
        self.add_state( ShakeMe() )
        self.add_state( WaitForBluetooth() )

        # Go to the Welcome state first.
        self.go_to_state( 'welcome' )

    # Helper function to add a state to the state machine.
    def add_state(self, state):
        self.states[state.name] = state

    # Transition to a state with the given name.
    # Note that when we move between states, we call the exit() function of
    # the previous state and the enter() function of the next state. This lets
    # each state do any cleanup or prep work respectively.
    def go_to_state(self, state_name):
        if self.state:
            self.state.exit(self)
        self.state = self.states[state_name]
        self.state.enter(self)

    # The code.py provided by this example calls the update() function,
    # so we pass this on to the currently selected game state.
    def update(self):
        if self.state:
            self.state.update(self)

    # This function starts the game by setting any variables to the
    # starting values we expect before gameplay begins.
    def start_game(self):
        timestamp = time.monotonic()
        self.time_remaining = 30
        self.score = 0
        self.urgent = False
        self.playing = True
        self.game_last_updated = timestamp
        self.display_last_updated = timestamp
        self.display.show(self.game_playing_display)
        self.go_to_state('game_active')

    # During gameplay, this function is called in a loop no matter
    # what state we're in. This code updates the countdown timer,
    # refreshes the UI, and if the game is over it proceeds directly
    # to the game over state.
    def update_game(self):
        timestamp = time.monotonic()

        # Note that we wait 0.1 seconds between updating the game state.
        # If this value is too low, the board may not be responsive to user
        # inputs. If it's too high, the game may appear laggy even though
        # all inputs are being handled by the game.
        # You might adjust this value depending on how complex the game
        # needs to be.
        time_since_game_last_updated = timestamp - self.game_last_updated
        if time_since_game_last_updated > 0.1:
            self.time_remaining -= time_since_game_last_updated
            if self.time_remaining < 10:
                self.urgent = True
            if self.time_remaining < 0:
                self.go_to_state( 'game_over' )
            self.game_last_updated = timestamp

        # We also add a (longer) delay between UI and Bluetooth updates as these
        # take more time to do than general game updates.
        time_since_display_last_updated = timestamp - self.display_last_updated
        if time_since_display_last_updated > 1.0:
            self.update_display()
            self.update_ble()
            self.display_last_updated = timestamp

    # Updates the UI elements shown on the GameActive screen.
    def update_display(self):
        self.time_label.text = "Time: " + str( int( self.time_remaining ) )
        self.score_label.text = "Score: " + str( self.score )
        # These hex values are used as RGB colors, with 00 being the darkest and FF being the brightest.
        # 0x000000 - black (0, 0, 0)
        # 0xFFFFFF - white (255, 255, 255)
        # 0xDD0000 - somewhat bright red (221, 0, 0)
        # 0x004000 - somewhat dark green (0, 64, 0)
        # 0x990099 - medium magenta (153, 0, 153)
        # You can try other values to see how they look.
        if self.urgent and self.time_label.background_color == 0x000000:
            self.time_label.background_color = 0xDD0000
        elif self.time_label.background_color != 0x000000:
            self.time_label.background_color = 0x000000
        self.display.refresh()

    # Sends the current game variables over Bluetooth.
    # Note that this is a one-way operation right now. If you'd like to receive data
    # back over Bluetooth, check out the Nametag sample for an example of how that works.
    def update_ble(self):
        if self.ble.connected:
            packet = dict()
            packet['state'] = self.state.name
            packet['playing'] = self.playing
            packet['score'] = self.score
            packet['urgent'] = self.urgent
            packet['time_remaining'] = self.time_remaining
            try:
            	self.uart_service.write(ETCPacket(packet).to_bytes())
            except Exception:
                print("Something went wrong")
            	pass

    # This code sets up the structure of the game's state machine.
    # You don't need to modify this - it's declaring a Python class
    # so that every other game state can use some of this code in common.
    class State(object):

        def __init__(self):
            self.last_entered = 0.0
            self.timeout = None

        @property
        def name(self):
            return ''

        def enter(self, machine):
            self.last_entered = time.monotonic()

        def exit(self, machine):
            pass

        # This is a common piece of code which automatically fails a game state
        # if no other state transition happens before the timeout.
        def update(self, machine):
            if machine.playing:
                machine.update_game()
            if machine.playing:
                timestamp = time.monotonic()
                if self.timeout is not None and timestamp - self.last_entered > self.timeout:
                    machine.go_to_state('game_failure')
            return True


class Welcome(CamperGame.State):

    @property
    def name(self):
        return 'welcome'

    def enter(self, machine):
        super().enter(machine)

        machine.game_over_label.text = "Welcome"
        machine.game_over_score_label.text = ""
        machine.game_over_instructions_label.text = "A to start / B to use Bluetooth"
        machine.display.show(machine.game_over_display)

        machine.update_ble()

        if machine.play_tones:
            clue.play_tone(1400, 0.1) # F
            clue.play_tone(1760, 0.1) # A
            clue.play_tone(2100, 0.1) # C
            clue.play_tone(1870, 0.1) # Bb
            clue.play_tone(1760, 0.1) # A
            clue.play_tone(1570, 0.1) # G
            clue.play_tone(1400, 0.5) # F

    def exit(self, machine):
        super().exit(machine)

    def update(self, machine):
        if super().update(machine):
            if clue.button_a:
                machine.start_game()
                machine.go_to_state('game_active')
            elif clue.button_b:
                machine.go_to_state('wait_for_bluetooth')

class GameOver(CamperGame.State):

    @property
    def name(self):
        return 'game_over'

    def enter(self, machine):
        super().enter(machine)
        machine.playing = False
        machine.game_over_label.text = "Game Over"
        machine.game_over_score_label.text = "Score: " + str( machine.score )
        machine.game_over_instructions_label.text = "B to start over"
        machine.display.show(machine.game_over_display)

        machine.update_ble()

        if machine.play_tones:
            clue.play_tone(1400, 0.1) # F
            clue.play_tone(1570, 0.1) # G
            clue.play_tone(1400, 0.1) # F
            clue.play_tone(1320, 0.1) # E
            clue.play_tone(1180, 0.1) # D
            clue.play_tone(1320, 0.1) # E
            clue.play_tone(1400, 0.5) # F

    def exit(self, machine):
        super().exit(machine)

    def update(self, machine):
        if super().update(machine):
            if clue.button_b:
                machine.go_to_state('welcome')


class WaitForBluetooth(CamperGame.State):

    @property
    def name(self):
        return 'wait_for_bluetooth'

    def enter(self, machine):
        super().enter(machine)
        machine.game_over_label.text = "Bluetooth"
        machine.game_over_score_label.text = "Advertising..."
        machine.game_over_instructions_label.text = "Open iOS app to continue"
        machine.display.show(machine.game_over_display)
        advertisement = ProvideServicesAdvertisement(machine.uart_service)
        machine.ble.start_advertising(advertisement)

    def exit(self, machine):
        super().exit(machine)
        print("Bluetooth connected")

    def update(self, machine):
        if super().update(machine):
            if machine.ble.connected:
                machine.start_game()
                machine.go_to_state('game_active')

class GameActive(CamperGame.State):

    @property
    def name(self):
        return 'game_active'

    def enter(self, machine):
        super().enter(machine)

    def exit(self, machine):
        super().exit(machine)

    def update(self, machine):
        if super().update(machine):
            # Randomly picks the next command in the game.
            # If you add another state, its name must also go into this list.
            next_action = random.choice(['press_me', 'shake_me', 'twist_me'])
            machine.go_to_state(next_action)

class GameSuccess(CamperGame.State):

    @property
    def name(self):
        return 'game_success'

    def enter(self, machine):
        super().enter(machine)
        machine.score += 1
        machine.action_label.background_color = 0x00AA00 # medium green (0, 170, 0)
        if machine.play_tones:
            clue.play_tone(1050, 0.1) # C
            clue.play_tone(1400, 0.3) # F
        else:
            time.sleep(0.1)
        machine.action_label.background_color = 0x000000 # black (0, 0, 0)

    def exit(self, machine):
        super().exit(machine)

    def update(self, machine):
        if super().update(machine):
            machine.go_to_state('game_active')


class GameFailure(CamperGame.State):

    @property
    def name(self):
        return 'game_failure'

    def enter(self, machine):
        super().enter(machine)

        machine.action_label.background_color = 0xAA0000 # red (170, 0, 0)
        if machine.play_tones:
            clue.play_tone(1050, 0.2) # C
            clue.play_tone(880, 0.2)  # A
        else:
            time.sleep(0.1)
        machine.action_label.background_color = 0x000000 # black (0, 0, 0)

    def exit(self, machine):
        super().exit(machine)

    def update(self, machine):
        if super().update(machine):
            machine.go_to_state('game_active')

class PressMe(CamperGame.State):

    @property
    def name(self):
        return 'press_me'

    def enter(self, machine):
        super().enter(machine)
        machine.action_label.text = 'Press Me'
        self.timeout = 3.0

    def exit(self, machine):
        super().exit(machine)

    def update(self, machine):
        if super().update(machine):
            # Waits for the B button to be pressed down.
            # You could modify this to wait for a different button, or for both buttons.
            # You can also modify the UI in enter() to say which button it's expecting.
            if clue.button_b:
                machine.go_to_state('game_success')

class ShakeMe(CamperGame.State):

    @property
    def name(self):
        return 'shake_me'

    def enter(self, machine):
        super().enter(machine)
        machine.action_label.text = 'Shake Me'
        self.timeout = 3.0

    def exit(self, machine):
        super().exit(machine)

    def update(self, machine):
        if super().update(machine):
            # Waits for the accelerometer to be shaken.
            # The '15' value here is the shake threshold, check out the Adafruit docs
            # below for a more thorough explanation:
            #
            # https://github.com/adafruit/Adafruit_CircuitPython_CLUE/blob/main/adafruit_clue.py#L381
            #
            # You might have to adjust this if you can't reliably trigger the shake detection,
            # or adjust the game update frequency (the sleep for 0.1 seconds) earlier in this file.
            if clue.shake(shake_threshold=15):
                machine.go_to_state('game_success')

class TwistMe(CamperGame.State):

    def __init__(self):
        super().__init__()
        self.twist = QwiicTwist( board.I2C() )

    @property
    def name(self):
        return 'twist_me'

    def enter(self, machine):
        super().enter(machine)
        self.twist.count = 0
        machine.action_label.text = 'Twist Me'
        self.timeout = 3.0

    def exit(self, machine):
        super().exit(machine)

    def update(self, machine):
        if super().update(machine):
            # This checks for the QwiicTwist module to be turned
            # 10 'clicks' clockwise (to the right).
            # You might change this to look for a random amount of clicks,
            # or to look for counterclockwise values (negative clicks, to the left.)
            #
            # Note that you can also change the RGB color of the QwiicTwist LED
            # or detect when a user presses down on the rotary encoder.
            if self.twist.count > 10:
                machine.go_to_state('game_success')
