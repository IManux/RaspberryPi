import time
import mcu

uart = mcu.com('/dev/ttyACM0') #bauds default: 9600

if uart.begin():
    print ('init uart ok')

while True:
    if uart.is_connected():
        msg = 'Testintg exserial2.py\n'
        uart.write(msg.encode())
        time.sleep(3)
