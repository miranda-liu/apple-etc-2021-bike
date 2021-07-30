from adafruit_clue import clue
import adafruit_sgp30
import time
import board
import displayio

clue_display = clue.simple_text_display(title="SPG30 Sensor!", title_scale=2)

sgp30 = adafruit_sgp30.Adafruit_SGP30(board.I2C())
time.sleep(5)

while True:
    eCO2, TVOC = sgp30.iaq_measure()
    print(eCO2)
    print(TVOC)
    
    clue_display[0].text = "Pressure: {:.3f} hPa".format(clue.pressure)
    clue_display[1].text = "Altitude: {:.1f} m".format(clue.altitude)
    clue_display[2].text = "Temperature: {:.1f} C".format(clue.temperature)
    clue_display[3].text = "Humidity: {:.1f} %".format(clue.humidity)
    clue_display[4].text = "TVOC={:5d}".format(TVOC)
    clue_display[5].text = "eCO2={:5d}".format(eCO2)
    clue_display.show()

