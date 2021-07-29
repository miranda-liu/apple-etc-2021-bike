from adafruit_clue import clue
import adafruit_sgp30
import time
import board
import displayio

clue_display = clue.simple_text_display(text_scale=1, colors=(clue.WHITE,))

sgp30 = adafruit_sgp30.Adafruit_SGP30(board.I2C())
time.sleep(15)

while True:
    print("Pressure: {:.3f} hPa".format(clue.pressure))
    print("Altitude: {:.1f} m".format(clue.altitude))
    print("Temperature: {:.1f} C".format(clue.temperature))
    print("Humidity: {:.1f} %".format(clue.humidity))

    eCO2, TVOC = sgp30.iaq_measure()
    print(eCO2)
    print(TVOC)
    clue_display[0].text = "TVOC={:5d}".format(TVOC)
    clue_display[1].text = "eCO2={:5d}".format(eCO2)
    print("--------------------------------")

