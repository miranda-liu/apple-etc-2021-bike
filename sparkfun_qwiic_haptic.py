from time import sleep
from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice

QWIIC_TWIST_ADDR = const(0x4A) # default I2C Address or 5A
QWIIC_TWIST_ID = const(0xE0) # value returned by id register

class Sparkfun_Haptic:
    """CircuitPython class for the Sparkfun QwiicTwist RGB Rotary Encoder"""

    def __init__(self, i2c, address=QWIIC_TWIST_ADDR, debug=False):
        """Initialize Qwiic Twist for i2c communication."""
        print("Searching for haptic")
        self._device = I2CDevice(i2c, address)
        print("Found Haptic")
        #save handle to i2c bus in case address is changed
        self._i2c = i2c
        self._debug = debug
        # self._write_register8(0xF7, 3)
        # self._write_register8(0xF8, 1)
        self._write_register8(0x22, 0x21)

# public properites (read-only)

    #0-127
    def setVib(self, vib):
        if vib < 0:
            return False; 
        if vib > 127:
            return False; 
        self._write_register8(0x23, vib)


# private methods

    def _read_register8(self, addr):
        # print("Reading Registored Address")
        # Read and return a byte from the specified 8-bit register address.
        with self._device as device:
            device.write(bytes([addr & 0xFF]))
            result = bytearray(1)
            device.readinto(result)
            if self._debug:
                print("$%02X => %s" % (addr, [hex(i) for i in result]))
            return result[0]

    def _write_register8(self, addr, value):
        # Write a byte to the specified 8-bit register address
        with self._device as device:
            device.write(bytes([addr & 0xFF, value & 0xFF]))
            if self._debug:
                print("$%02X <= 0x%02X" % (addr, value))

    def _read_register16(self, addr):
        # Read and return a 16-bit value from the specified 8-bit register address.
        with self._device as device:
            device.write(bytes([addr & 0xFF]))
            result = bytearray(2)
            device.readinto(result)
            if self._debug:
                print("$%02X => %s" % (addr, [hex(i) for i in result]))
            return (result[1] << 8) | result[0]

    def _write_register16(self, addr, value):
        # Write a 16-bit big endian value to the specified 8-bit register
        with self._device as device:
            # write LSB then MSB
            device.write(bytes([addr & 0xFF,
                                value & 0xFF,
                                (value >> 8) & 0xFF]))
            if self._debug:
                print("$%02X <= 0x%02X" % (addr, value & 0xFF))
                print("$%02X <= 0x%02X" % (addr, (value >> 8) &0xFF))

    def _write_register24(self, addr, value):
        # Write a byte to the specified 8-bit register address
        with self._device as device:
            device.write(bytes([addr & 0xFF,
                                (value >> 16) & 0xFF,
                                (value >> 8) & 0xFF,
                                value & 0xFF]))
            if self._debug:
                print("$%02X <= 0x%02X" % (addr, (value >> 16) &0xFF))
                print("$%02X <= 0x%02X" % (addr, (value >> 8) &0xFF))
                print("$%02X <= 0x%02X" % (addr, value & 0xFF))
