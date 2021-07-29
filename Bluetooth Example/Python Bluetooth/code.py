# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# CircuitPython Bluefruit LE Connect Plotter Example

import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_clue import clue

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

def sendData(dataToSend):
    uart_server.write(dataToSend)
    print("Sent Data: " + dataToSend)

button_a_active = False
button_b_active = False

def checkButtonState():
    global button_a_active
    if button_a_active == False and clue.button_a:
        sendData("Sample Data to send")
        button_a_active = True
    if button_a_active == True and clue.button_a == False:
        button_a_active = False
            

# def recieveData(): 
    # def run():
    #     while ble.connected:
    #         if uart_server.in_waiting:
    #             print(uart_server.read)
    #             # packet = Packet.from_stream(uart_server)
    #             # print(packet.color)
    # threading.Thread(target=run, args=())

# def periodicDataSend():
#     def run():
#         while ble.connected:
#             strToSend = "{},{}\n".format(time.time(), time.time())
#             sendData(strToSend)
#             time.sleep(0.1)
#     threading.Thread(target=run, args=())

while True:
    # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    print("Connected to central!")
    ble.stop_advertising()
    # recieveData()
    # periodicDataSend()
    while ble.connected:
        while uart_server.in_waiting:
            rxData = uart_server.read()
            if rxData:
                try:
                    result = str(eval(rxData))
                except Exception as e:
                    result = repr(e)
            print("Recieved>" + rxData.decode() + "<")
        # strToSend = "{},{}".format(time.time(), time.time())
        checkButtonState()
        # sendData(strToSend)
        time.sleep(.1)
    print("Disconnected from central!")