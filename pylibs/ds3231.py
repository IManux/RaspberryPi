"""
    developed by iManux
"""
from datetime import datetime
import time
import smbus

"""
SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
DAYS_PER_WEEK = 7
MAX_DAYS_PER_MONTH = 31
MONTHS_PER_YEAR = 12
YEARS_PER_CENTURY = 100

OSCILLATOR_ON_MASK = 0b1<<7
"""
"""
    DY/DT:  If DY/DT is written to logic 0, the alarm will
            be the result of a match with date of the month. If
            DY/DT is written to logic 1, the alarm will be the result of
            a match with day of the week.
    12/24: The DS3231 can be
            run in either 12-hour or 24-hour mode. Bit 6 of the hours
            register is defined as the 12- or 24-hour mode select bit.
            When high, the 12-hour mode is selected. In the 12-hour
            mode, bit 5 is the AM/PM bit with logic-high being PM. In
            the 24-hour mode, bit 5 is the second 10-hour bit (20–23hours). 
"""
class ds3231:

    def __init__(self, twi=1, addr=0x68):
        self.__bus = smbus.SMBus(twi)
        self.__addr_rtc = addr

        self.__SECONDS_PER_MINUTE = 60
        self.__MINUTES_PER_HOUR = 60
        self.__HOURS_PER_DAY = 24
        self.__DAYS_PER_WEEK = 7
        self.__MAX_DAYS_PER_MONTH = 31
        self.__MONTHS_PER_YEAR = 12
        self.__YEARS_PER_CENTURY = 100

        self.__OSCILLATOR_ON_MASK = 0b1<<7
        #REGISTERS PRIVATE
        self.__REG_TM_SECS  = 0x00
        self.__REG_TM_MINS  = 0x01
        self.__REG_TM_HOUR  = 0x02
        self.__REG_TM_DOW   = 0x03
        self.__REG_TM_DATE  = 0x04
        self.__REG_TM_MONTH = 0x05
        self.__REG_TM_YEAR  = 0x06

        self.__REG_A1_SECS = 0x07
        self.__REG_A1_MINS = 0x08
        self.__REG_A1_HOUR = 0x09
        self.__REG_A1_DATE = 0x0A
        self.__REG_A2_MINS = 0x0B
        self.__REG_A2_HOUR = 0x0C
        self.__REG_A2_DATE = 0x0D
        self.__REG_CONTROL = 0x0E   #Control
        self.__REG_CONSTA  = 0x0F   #Control/Status

        #REGISTERS PUBLIC
        self.REG_TM_SECS  = 0x00
        self.REG_TM_MINS  = 0x01
        self.REG_TM_HOUR  = 0x02
        self.REG_TM_DOW   = 0x03
        self.REG_TM_DATE  = 0x04
        self.REG_TM_MONTH = 0x05
        self.REG_TM_YEAR  = 0x06

        self.REG_A1_SECS = 0x07
        self.REG_A1_MINS = 0x08
        self.REG_A1_HOUR = 0x09
        self.REG_A1_DATE = 0x0A
        self.REG_A2_MINS = 0x0B
        self.REG_A2_HOUR = 0x0C
        self.REG_A2_DATE = 0x0D
        self.REG_CONTROL = 0x0E   #Control
        self.REG_CONSTA  = 0x0F   #Control/Status

    def _i2c_write(self, addr, reg, data):
        self.__bus.write_byte_data(addr, reg, data)

    def _i2c_read(self, addr, reg):
        data = self.__bus.read_byte_data(addr, reg)
        return data

    ################
    # DS3231
    ################
    def _clear_alarm_flags(self, b=0):
        if b == 0:
            b = self._i2c_read(self.__addr_rtc, self.__REG_CONSTA)
        b = b & 0xFC
        self._i2c_write(self.__addr_rtc, self.__REG_CONSTA, b)

    def bcd_to_int(self, bcd, n=2):
        """Decode n least significant packed binary coded decimal digits to binary.
        Return binary result.
        n defaults to 2 (BCD digits).
        n=0 decodes all digits.
        """
        return int(('%x' % bcd)[-n:])


    def int_to_bcd(self, x, n=2):
        """
        Encode the n least significant decimal digits of x
        to packed binary coded decimal (BCD).
        Return packed BCD value.
        n defaults to 2 (digits).
        n=0 encodes all digits.
        """
        return int(str(x)[-n:], 0x10)

    def get_datetime(self, century=21, tzinfo=None):
        _secs = self._i2c_read(self.__addr_rtc, self.__REG_TM_SECS)
        _mins = self._i2c_read(self.__addr_rtc, self.__REG_TM_MINS)
        _hour = self._i2c_read(self.__addr_rtc, self.__REG_TM_HOUR)
        #_dow = self._i2c_read(self.__addr_rtc, self.__REG_TM_DOW)
        _date = self._i2c_read(self.__addr_rtc, self.__REG_TM_DATE)
        _year = self._i2c_read(self.__addr_rtc, self.__REG_TM_YEAR)
        _month = self._i2c_read(self.__addr_rtc, self.__REG_TM_MONTH)

        #convert bcd to int
        _secs = self.bcd_to_int(_secs)
        _mins = self.bcd_to_int(_mins)
        _hour = self.bcd_to_int(_hour)
        _date = self.bcd_to_int(_date)
        _month = self.bcd_to_int(_month)
        _year = self.bcd_to_int(_year)
        _year = 100 * (century - 1) + _year

        #year, month, date, hour, mins, secs, millisecons, tzinfo
        return datetime(
            _year, _month, _date, _hour, _mins, _secs, 
            0, tzinfo=tzinfo)

    def get_datetime_tz(self, tz=0):
        ts = self.get_datetime()
        if tz == 0:
            return ts
        ts_seconds = time.mktime(ts.timetuple()) + (tz * 3600)
        ts = datetime.fromtimestamp(ts_seconds)
        return ts

    def system_to_rtc(self):
        _dow = [2, 3, 4, 5, 6, 7, 1]
        _ts = datetime.now()
        _sec = _ts.second
        _min = _ts.minute
        _hour = _ts.hour
        #_day = _ts.weekday() + 1 # 0 is monday, then we have to +1
        _day = _dow[_ts.weekday()]
        _date = _ts.day
        _month = _ts.month
        _year = _ts.year - 2000
        #write registers
        self._i2c_write(self.__addr_rtc, self.__REG_TM_SECS, self.int_to_bcd(_sec))   # second
        self._i2c_write(self.__addr_rtc, self.__REG_TM_MINS, self.int_to_bcd(_min))   # minute
        self._i2c_write(self.__addr_rtc, self.__REG_TM_HOUR, self.int_to_bcd(_hour))  # hour
        self._i2c_write(self.__addr_rtc, self.__REG_TM_DOW, self.int_to_bcd(_day))   # day
        self._i2c_write(self.__addr_rtc, self.__REG_TM_DATE, self.int_to_bcd(_date))  # date
        self._i2c_write(self.__addr_rtc, self.__REG_TM_MONTH, self.int_to_bcd(_month)) # month
        self._i2c_write(self.__addr_rtc, self.__REG_TM_YEAR, self.int_to_bcd(_year))  # year
    
    #set minutes
    def set_alarm1(self, d, h, m, s):
        #print('set_alarm1')
        self._i2c_write(self.__addr_rtc, self.__REG_CONTROL, 0x05) #0x05
        self._i2c_write(self.__addr_rtc, self.__REG_A1_SECS, self.int_to_bcd(s)) #secs
        self._i2c_write(self.__addr_rtc, self.__REG_A1_MINS, self.int_to_bcd(m)) #mins
        self._i2c_write(self.__addr_rtc, self.__REG_A1_HOUR, self.int_to_bcd(h)) #hour
        self._i2c_write(self.__addr_rtc, self.__REG_A1_DATE, self.int_to_bcd(d)) #date
        self._clear_alarm_flags()


    #ALARM 1 MODES
    """
        @brief: Alarm per second
        @return None
    """
    def set_alarm1_mode1(self):

        self.disable_alarm1()
        self.clear_alarm1()

        reg_a1m1 = self._i2c_read(self.__addr_rtc, self.__REG_A1_SECS)
        reg_a1m1 = reg_a1m1 | 0x80
        reg_a1m2 = self._i2c_read(self.__addr_rtc, self.__REG_A1_MINS)
        reg_a1m2 = reg_a1m2 | 0x80
        reg_a1m3 = self._i2c_read(self.__addr_rtc, self.__REG_A1_HOUR)
        reg_a1m3 = reg_a1m3 | 0x80
        reg_a1m4 = self._i2c_read(self.__addr_rtc, self.__REG_A1_DATE)
        reg_a1m4 = reg_a1m4 | 0x80
    
        self._i2c_write(self.__addr_rtc, self.__REG_A1_SECS, reg_a1m1)
        self._i2c_write(self.__addr_rtc, self.__REG_A1_MINS, reg_a1m2)
        self._i2c_write(self.__addr_rtc, self.__REG_A1_HOUR, reg_a1m3)
        self._i2c_write(self.__addr_rtc, self.__REG_A1_DATE, reg_a1m4)

        self.rtc_enable_int() #enable global
        self.enable_alarm1() #enable individual

        return True
    
    """
        @brief: Alarm whe seconds match.
        @param s: seconds between 0 - 59.
        @return 1 if s passed is correct.
    """
    def set_alarmt1_mode2(self, s):

        if s < 0 or s > 59:
            return 0

        self.disable_alarm1()
        self.clear_alarm1()

        reg_a1m2 = self._i2c_read(self.__addr_rtc, self.__REG_A1_MINS)
        reg_a1m2 = reg_a1m2 | 0x80
        reg_a1m3 = self._i2c_read(self.__addr_rtc, self.__REG_A1_HOUR)
        reg_a1m3 = reg_a1m3 | 0x80
        reg_a1m4 = self._i2c_read(self.__addr_rtc, self.__REG_A1_DATE)
        reg_a1m4 = reg_a1m4 | 0x80

        self._i2c_write(self.__addr_rtc, self.__REG_A1_SECS, self.int_to_bcd(s))
        self._i2c_write(self.__addr_rtc, self.__REG_A1_MINS, reg_a1m2)
        self._i2c_write(self.__addr_rtc, self.__REG_A1_HOUR, reg_a1m3)
        self._i2c_write(self.__addr_rtc, self.__REG_A1_DATE, reg_a1m4)

        self.rtc_enable_int() #enable global
        self.enable_alarm1() #enable individual

        return 1

    """
        @brief: Alarm when when minutes and secods match.
        @param m: minutes between 0 - 59.
        @param s: seconds between 0 - 59.
        @return 1 if m, s passed are correct.
    """
    def set_alarm1_mode3(self, m, s):
        print('set_alarm1_minute')

        if m < 0 or m > 59:
            return 0
        if s < 0 or s > 59:
            return 0

        self.disable_alarm1()
        self.clear_alarm1()
        reg_a1m3 = self._i2c_read(self.__addr_rtc, self.__REG_A1_HOUR) #0x09
        reg_a1m3 = reg_a1m3 | 0x80
        reg_a1m4 = self._i2c_read(self.__addr_rtc, self.__REG_A1_DATE) #0x0A
        reg_a1m4 = reg_a1m4 | 0x80

        self._i2c_write(self.__addr_rtc, self.__REG_A1_SECS, self.int_to_bcd(s)) #secs - A1M1
        self._i2c_write(self.__addr_rtc, self.__REG_A1_MINS, self.int_to_bcd(m)) #mins - A1M2
        self._i2c_write(self.__addr_rtc, self.__REG_A1_HOUR, reg_a1m3) #hour - A1M3
        self._i2c_write(self.__addr_rtc, self.__REG_A1_DATE, reg_a1m4) #date - A1M4

        self.rtc_enable_int() #enable global
        self.enable_alarm1() #enable individual

        return 1

    """
        @brief: Alarm when hours, minutes and seconds match
        @param h: minutes between 0 - 23 [format 24].
        @param m: minutes between 0 - 59.
        @param s: seconds between 0 - 59.
        @return 1 if h, m, s passed are correct.
    """
    def set_alarm1_mode4(self, h, m, s):
        print('set_alarm1_hour')
        if h < 0 or h > 23:
            return 0
        if m < 0 or m > 59:
            return 0
        if s < 0 or s > 59:
            return 0

        self.disable_alarm1()
        self.clear_alarm1()
        reg_a1m4 = self._i2c_read(self.__addr_rtc, 0x0A)
        reg_a1m4 = reg_a1m4 | 0x80

        self._i2c_write(self.__addr_rtc, self.__REG_A1_SECS, self.int_to_bcd(s)) #secs - A1M1
        self._i2c_write(self.__addr_rtc, self.__REG_A1_MINS, self.int_to_bcd(m)) #mins - A1M2
        self._i2c_write(self.__addr_rtc, self.__REG_A1_HOUR, self.int_to_bcd(h)) #hour - A1M3
        self._i2c_write(self.__addr_rtc, self.__REG_A1_DATE) #date - A1M4

        self.rtc_enable_int() #enable global
        self.enable_alarm1() #enable individual

        return 1

    """
        @brief: Alarm when date, hours, minutes and seconds match
        @para dt: date between 1 - 31.
        @param h: minutes between 0 - 23 [format 24].
        @param m: minutes between 0 - 59.
        @param s: seconds between 0 - 59.
        @return 1 if dt, h, m, s passed are correct.
    """
    def set_alarm1_mode5(self, dt, h, m, s):
        print('set_alarm1_dow')

        if s < 0 or s > 59:
            return 0
        if m < 0 or m > 59:
            return 0
        if h < 0 or h > 23:
            return 0
        if dt < 1 or dt > 31:
            return 0

        self.disable_alarm1()
        self.clear_alarm1()
        self._i2c_write(self.__addr_rtc, self.__REG_A1_SECS, self.int_to_bcd(s)) #secs - A1M1
        self._i2c_write(self.__addr_rtc, self.__REG_A1_MINS, self.int_to_bcd(m)) #mins - A1M2
        self._i2c_write(self.__addr_rtc, self.__REG_A1_HOUR, self.int_to_bcd(h)) #hour - A1M3
        self._i2c_write(self.__addr_rtc, self.__REG_A1_DATE, self.int_to_bcd(dt)) #date - A1M4

        self.rtc_enable_int() #enable global
        self.enable_alarm1() #enable individual

        return 1
    
    """
        @brief: Alarm when day, hours, minutes and seconds match
        @param d: day of week, between 1 - 7.
        @param h: minutes between 0 - 23 [format 24].
        @param m: minutes between 0 - 59.
        @param s: seconds between 0 - 59.
        @return 1 if d, h, m, s passed are correct.
    """
    def set_alarm1_mode6(self, d, h, m, s):
        print('set_alarm1_dom')

        if s < 0 or s > 59:
            return 0
        if m < 0 or m > 59:
            return 0
        if h < 0 or h > 23:
            return 0
        if d < 1 or d > 7:
            return 0
        
        self.disable_alarm1()
        self.clear_alarm1()
        self._i2c_write(self.__addr_rtc, self.__REG_A1_SECS, self.int_to_bcd(s)) #secs - A1M1
        self._i2c_write(self.__addr_rtc, self.__REG_A1_MINS, self.int_to_bcd(m)) #mins - A1M2
        self._i2c_write(self.__addr_rtc, self.__REG_A1_HOUR, self.int_to_bcd(h)) #hour - A1M3
        self._i2c_write(self.__addr_rtc, self.__REG_A1_DATE, (d | 0x40)) #day - A1M4

        self.rtc_enable_int() #enable global
        self.enable_alarm1() #enable individual

        return 1

    """
        SET ALARM2
    """
    """
        @brief: Alarm once per minute (00 seconds of every minute)
    """
    def set_alarm2_mode1(self):
        print("set_alarm2_mode1")

        self.clear_alarm2()
        self.disable_alarm2()
        self._i2c_write(self.__addr_rtc, self.__REG_A2_MINS, 0x80) #mins - A2M2
        self._i2c_write(self.__addr_rtc, self.__REG_A2_HOUR, 0x80) #hour - A2M3
        self._i2c_write(self.__addr_rtc, self.__REG_A2_DATE, 0x80) #date - A2M4

        self.rtc_enable_int() #enable global
        self.enable_alarm2() #enable individual

    """
        @brief: Alarm when minutes match
        @param m: minutes between 0 - 59.
        @return 1 if m passed are correct.
    """
    def set_alarm2_mode2(self, m):
        print("set_alarm2_mode2")
        if m < 0 or m > 59:
            return False

        self.clear_alarm2()
        self.disable_alarm2()
        self._i2c_write(self.__addr_rtc, self.__REG_A2_MINS, self.int_to_bcd(m)) #secs - A2M2
        self._i2c_write(self.__addr_rtc, self.__REG_A2_HOUR, 0x80) #hour - A2M3
        self._i2c_write(self.__addr_rtc, self.__REG_A2_DATE, 0x80) #date - A2M4

        self.rtc_enable_int() #enable global
        self.enable_alarm2() #enable individual

        return True

    """
        @brief: Alarm when hours and minutes match
        @param h: minutes between 0 - 23 [format 24].
        @param m: minutes between 0 - 59.
        @return 1 if h, m passed are correct.
    """
    def set_alarm2_mode3(self, h, m):
        print("set_alarm2_mode3")
        if h < 0 or h > 23:
            return False
        if m < 0 or m > 59:
            return False

        self.clear_alarm2()
        self.disable_alarm2()
        self._i2c_write(self.__addr_rtc, self.__REG_A2_MINS, self.int_to_bcd(m)) #secs - A2M2
        self._i2c_write(self.__addr_rtc, self.__REG_A2_HOUR, self.int_to_bcd(h)) #hour - A2M3
        self._i2c_write(self.__addr_rtc, self.__REG_A2_DATE, 0x80) #date - A2M4

        self.rtc_enable_int() #enable global
        self.enable_alarm2() #enable individual

        return True

    """
        @brief: Alarm when date, hours and minutes match
        @param dt: date between 1 - 31.
        @param h: minutes between 0 - 23 [format 24].
        @param m: minutes between 0 - 59.
        @return 1 if dt, h, m, s passed are correct.
    """
    def set_alarm2_mode4(self, dt, h, m):
        print("set_alarm2_mode4")
        if dt < 1 or dt > 31:
            return False
        if h < 0 or h > 23:
            return False
        if m < 0 or m > 59:
            return False

        self.clear_alarm2()
        self.disable_alarm2()
        self._i2c_write(self.__addr_rtc, self.__REG_A2_MINS, self.int_to_bcd(m)) #secs - A2M2
        self._i2c_write(self.__addr_rtc, self.__REG_A2_HOUR, self.int_to_bcd(h)) #hour - A2M3
        self._i2c_write(self.__addr_rtc, self.__REG_A2_DATE, self.int_to_bcd(dt)) #date - A2M4

        self.rtc_enable_int() #enable global
        self.enable_alarm2() #enable individual

        return True

    """
        @brief: Alarm when day, hours, and minutes match
        @param d: date between 1 - 7.
        @param h: minutes between 0 - 23 [format 24].
        @param m: minutes between 0 - 59.
        @return 1 if dt, h, m passed are correct.
    """
    def set_alarm2_mode5(self, d, h, m):
        print("set_alarm2_mode5")
        if d < 1 or d > 7:
            return False
        if h < 0 or h > 23:
            return False
        if m < 0 or m > 59:
            return False

        self.clear_alarm2()
        self.disable_alarm2()
        self._i2c_write(self.__addr_rtc, self.__REG_A2_MINS, self.int_to_bcd(m)) #secs - A2M2
        self._i2c_write(self.__addr_rtc, self.__REG_A2_HOUR, self.int_to_bcd(h)) #hour - A2M3
        self._i2c_write(self.__addr_rtc, self.__REG_A2_DATE, (d | 0x40)) #date - A2M4

        self.rtc_enable_int() #enable global
        self.enable_alarm2() #enable individual

        return True

    """
        Alarm1
        - enable, disable, check, clear
    """
    def enable_alarm1(self):
        rg = self._i2c_read(self.__addr_rtc, self.__REG_CONTROL)
        rg = rg | 0x01
        self._i2c_write(self.__addr_rtc, self.__REG_CONTROL, rg) #RC [Control]

    def disable_alarm1(self):
        rg = self._i2c_read(self.__addr_rtc, self.__REG_CONTROL)
        rg = rg & 0xFE
        self._i2c_write(self.__addr_rtc, self.__REG_CONTROL, rg) #RC [Control]

    """
        @brief verify if Alarm1 was trigger
        @return the state of A1F, 0 or 1
    """
    def check_alarm1(self):
        rg = self._i2c_read(self.__addr_rtc, self.__REG_CONSTA)
        return (rg & 0x01)

    def clear_alarm1(self):
        rg = self._i2c_read(self.__addr_rtc, self.__REG_CONSTA)
        rg = rg & 0xFE
        self._i2c_write(self.__addr_rtc, self.__REG_CONSTA, rg) #RCS [Control/Status]

    """
        Alarm2
        - enable, disable, check, clear
    """
    def enable_alarm2(self):
        rg = self._i2c_read(self.__addr_rtc, self.__REG_CONTROL)
        rg = rg | 0x02
        self._i2c_write(self.__addr_rtc, self.__REG_CONTROL, rg) #RC [Control]

    def disable_alarm2(self):
        rg = self._i2c_read(self.__addr_rtc, self.__REG_CONTROL)
        rg = rg & 0xFD
        self._i2c_write(self.__addr_rtc, self.__REG_CONTROL, rg) #RC [Control]

    """
        @brief verify if Alarm2 was trigger
        @return the state of A2F, 0 or 1
    """
    def check_alarm2(self):
        rg = self._i2c_read(self.__addr_rtc, self.__REG_CONSTA)
        return (rg & 0x02)

    def clear_alarm2(self):
        rg = self._i2c_read(self.__addr_rtc, self.__REG_CONSTA)
        rg = rg & 0xFD
        self._i2c_write(self.__addr_rtc, self.__REG_CONSTA, rg) #RCS [Control/Status]
    
    """
        Utils
    """
    def rtc_set_address(self, addr):
        self.__addr_rtc = addr

    def rtc_read_reg(self, rg):
        b = None
        if rg >= 0x00 and rg < 0x10:
            b = self._i2c_read(self.__addr_rtc, rg)
        return b

    def rtc_write_reg(self, rg, value):
        if (rg >= 0x00 and rg < 0x10) and (value >= 0x00 and value <= 0xFF):
            self._i2c_write(self.__addr_rtc, rg, value)
            return True
        return False

    def rtc_enable_int(self):
        rg = self._i2c_read(self.__addr_rtc, self.__REG_CONTROL)
        rg = rg | 0x04
        self._i2c_write(self.__addr_rtc, self.__REG_CONTROL, rg)

    def rtc_disable_int(self):
        rg = self._i2c_read(self.__addr_rtc, self.__REG_CONTROL)
        rg = rg & 0xFB
        self._i2c_write(self.__addr_rtc, self.__REG_CONTROL, rg)

    """
        OLD
    """
    def check_alarms(self):
        reg_status = self._i2c_read(self.__addr_rtc, self.__REG_CONSTA)
        #print('reg_status: ', bin(reg_status))
        return (reg_status & 0x03) #b00000011

    def clear_alarm_flags(self, b=0):
        self._clear_alarm_flags(b)

    def set_alarm_flags(self, b=1):
        self._clear_alarm_flags(b)

