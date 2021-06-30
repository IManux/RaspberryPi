#!/usr/bin/python3
"""
    file: exserial1.py
    brief: script display the string received
"""
import time
import mcu

uart = mcu.com('/dev/ttyACM0')

if uart.begin():
    print ('init uart ok')

while True:
    if uart.is_connected():
        n = uart.available()
        if n > 0:
            rs = uart.read_bytes(n) #bytearray
            ds = rs.decode() #options: utf-8, iso-8859-1. utf-8 [default]
            print (ds)
    time.sleep(1)
