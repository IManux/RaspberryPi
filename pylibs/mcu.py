#!/usr/bin/python3
from __future__ import print_function # python 3
import serial
import serial.tools.list_ports as port_list
import threading
import time
import sys

class com:

    #list Port Serial
    def get_all_ports(self):
        ports = list(port_list.comports())
        if len(ports) > 0:
            return ports
        return None
        
    def check_port(self, port=None):
        ret = False
        ports = self.get_all_ports()
        if ports != None and port != None:
            for _port in ports:
                if port.find(_port.device) != -1:
                    ret = True
                    break
        return ret
    
    #is connected?
    def is_connected(self):
        ret = False
        if self.__port != None:
            port_present = self.check_port(self.__port)
            if port_present == True:
                ret = self.__ser.is_open
         
        return ret

    #reconnect
    def reconnect(self):
        ret = False
        if self.__port != None:
            if self.check_port(self.__port) == True:
                if not self.__ser.is_open:
                    try:
                        self.__ser.close()
                        self.__ser.open()
                        if self.__ser.is_open:
                            self.__ser.flushInput()
                            self.__ser.flushOutput()
                            self.__connected = True
                            ret = True
                    except (OSError, serial.SerialException):
                       ret = False

        return ret

    def set_port(self, t_serial):
        if self.is_connected():
            return False

        self.__port - t_serial

        return True

    def set_bauds(self, t_bauds):
        self.__bauds = t_bauds

    def get_port(self):
        return self.__port
    
    def get_bauds(self):
        return self.__bauds

    #begin
    def begin(self):
        ret = 0
        if self.__port != None:
            ret = self.__init_serial_port(self.__port, self.__bauds)
            
        return ret
        
    #init Port Serial
    def __init_serial_port(self, port=None, bauds=9600, timeout=2):
    
        print("initPortSerial")
        self.__connected = False
        
        if port == None:
            return self.__connected

        #if self._check_port(port) == False:
        #    return self.connected
        #process
        self.__ser.port = port
        self.__ser.baudrate = bauds
        self.__ser.parity = serial.PARITY_NONE
        self.__ser.stopbits = serial.STOPBITS_ONE
        self.__ser.timeout = timeout
        try:
            self.__ser.close()
            self.__ser.open()
            if(self.__ser.is_open):
                self.__connected = True
                time.sleep(2)
                self.__ser.flushInput()
                self.__ser.flushOutput()
        except (OSError, serial.SerialException):
            print("port not exist.")
        finally:
            return self.__connected

    #close Port Serial
    def close_serial_port(self):
        result = False
        if self.__port != None:
            if self.check_port(self.__port) == True:
                if self.__ser.is_open: #is it open?
                    self.__ser.close()
                    if self.__ser.is_open: #is it open?
                        self.__connected = True
                    else:
                        self.__connected = False
                    result = self.__connected
        return result

    def inwaiting(self, timeout=1):
        _num_bytes = 0
        _raw_bytes = 0
        _ob = 0
        _timeout = timeout * 1000
        while(_timeout > 0):
            _num_bytes = self.available()
            if _num_bytes > _ob:
                _ob = _num_bytes
                _timeout = 100
            _timeout = _timeout - 1
            time.sleep(0.001)

        return _num_bytes

    def clear_rx(self):
        self.__readLock.acquire()
        self.__ser.flushInput()
        self.__readLock.release()

    def write(self, b):
        self.__readLock.acquire()
        self.__ser.write(b)
        self.__readLock.release()

    def read(self):
        self.__readLock.acquire()
        b = self.__ser.read()
        self.__readLock.release()
        return b

    def read_bytes(self, n):
        self.__readLock.acquire()
        b = bytearray(self.__ser.read(n))
        self.__readLock.release()
        return b

    def available(self):
        self.__readLock.acquire()
        n = self.__ser.inWaiting()
        self.__readLock.release()
        return n

    #return int16
    def bytes_to_int16(self, msb, lsb):
        if sys.version_info[0] < 3:
            if type(msb) == str:
                msb = ord(msb)
            if type(lsb) == str:
                lsb = ord(lsb)
        raw16 = 0
        raw16 = msb
        raw16 = raw16 << 8
        raw16 = raw16 | lsb
        return raw16
    
    def int16_to_bytes(self, b):
        _lsb = b & 0xff
        _msb = (b >> 8) & 0xff
        return _lsb, _msb

    #calculate CRC.
    def calculate_crc16(self, _array, _size):
        if sys.version_info[0] < 3:
            _array = [ord(elem) if type(elem)==str else elem for elem in _array]
        crc = 0xFFFF
        _len = _size - 2

        for i in range(_len):
            crc ^= _array[i]
            j = 8
            while j != 0:
                if (crc & 0x0001) != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
                j = j - 1

        return crc

    def __init__(self, t_serial=None, t_bauds=9600, **kwargs):
        self.__port = t_serial
        self.__bauds = t_bauds #default
        self.__connected = False
        self.__ser = serial.Serial() #self.ser = serial.Serial(t_serial, t_bauds)
        #Mutex
        self.__readLock = threading.Lock()
