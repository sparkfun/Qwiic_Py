#-------------------------------------------------------------------------------
# qwiic_rv8803.py
#
# Python library for the SparkFun Qwiic Real Time Clock Module RV-8803, available here:
# https://www.sparkfun.com/products/16281
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November, 2024
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2024 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#===============================================================================

"""!
qwiic_rv8803.py
============
Python module for the [SparkFun Qwiic RV-8803](https://www.sparkfun.com/products/16281)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_RV-8803_Arduino_Library)
This package can be used with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

# The Qwiic_I2C_Py platform driver is designed to work on almost any Python
# platform, check it out here: https://github.com/sparkfun/Qwiic_I2C_Py
import qwiic_i2c

__version__ = "3.0.0"

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class
# instance. This allows higher level logic to rapidly create a index of Qwiic
# devices at runtine
_DEFAULT_NAME = "Qwiic RV8803"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x32] 

# Seconds between 1970-01-01 and 2000-01-01
_SECONDS_1970_TO_2000 = 946684800

# Date <-> day-count conversion, so the driver doesn't depend on the platform's
# time module (whose epoch and time zone handling differ between platforms).
# These are Howard Hinnant's days_from_civil / civil_from_days algorithms for
# the proleptic Gregorian calendar; days are counted from 1970-01-01.
def _days_from_civil(year, month, day):
    """!
    @return **int** Days from 1970-01-01 to the given date
    """
    if month <= 2:
        year -= 1
    era = year // 400
    yoe = year - era * 400
    doy = (153 * (month + (-3 if month > 2 else 9)) + 2) // 5 + day - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468

def _civil_from_days(days):
    """!
    @return **tuple** (year, month, day) of the date that is days after 1970-01-01
    """
    days += 719468
    era = days // 146097
    doe = days - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    day = doy - (153 * mp + 2) // 5 + 1
    month = mp + (3 if mp < 10 else -9)
    year = yoe + era * 400 + (1 if month <= 2 else 0)
    return (year, month, day)

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicRV8803(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Day constants
    SUNDAY = 0x01
    MONDAY = 0x02
    TUESDAY = 0x04
    WEDNESDAY = 0x08
    THURSDAY = 0x10
    FRIDAY = 0x20
    SATURDAY = 0x40

    # Register names
    REG_RAM = 0x07
    REG_HUNDREDTHS = 0x10
    REG_SECONDS = 0x11
    REG_MINUTES = 0x12
    REG_HOURS = 0x13
    REG_WEEKDAYS = 0x14
    REG_DATE = 0x15
    REG_MONTHS = 0x16
    REG_YEARS = 0x17
    REG_MINUTES_ALARM = 0x18
    REG_HOURS_ALARM = 0x19
    REG_WEEKDAYS_DATE_ALARM = 0x1A
    REG_TIMER0 = 0x1B
    REG_TIMER1 = 0x1C
    REG_EXTENSION = 0x1D
    REG_FLAG = 0x1E
    REG_CONTROL = 0x1F
    REG_HUNDREDTHS_CAPTURE = 0x20
    REG_SECONDS_CAPTURE = 0x21
    REG_OFFSET = 0x2C
    REG_EVENT_CONTROL = 0x2F

    # Enable Bits for Alarm Registers
    ALARM_ENABLE = 7

    # Extension Register Bits
    EXTENSION_TEST = 7
    EXTENSION_WADA = 6
    EXTENSION_USEL = 5
    EXTENSION_TE = 4
    EXTENSION_FD = 2
    EXTENSION_TD = 0

    # Flag Register Bits
    FLAG_UPDATE = 5
    FLAG_TIMER = 4
    FLAG_ALARM = 3
    FLAG_EVI = 2
    FLAG_V2F = 1
    FLAG_V1F = 0

    # Interrupt Control Register Bits
    UPDATE_INTERRUPT = 5
    TIMER_INTERRUPT = 4
    ALARM_INTERRUPT = 3
    EVI_INTERRUPT = 2
    CONTROL_RESET = 0

    # Event Control Bits
    EVENT_ECP = 7
    EVENT_EHL = 6
    EVENT_ET = 4
    EVENT_ERST = 0

    # Possible Settings
    COUNTDOWN_TIMER_FREQUENCY_4096HZ = 0b00
    COUNTDOWN_TIMER_FREQUENCY_64HZ = 0b01
    COUNTDOWN_TIMER_FREQUENCY_1HZ = 0b10
    COUNTDOWN_TIMER_FREQUENCY_1_60TH_HZ = 0b11
    CLOCK_OUT_FREQUENCY_32768HZ = 0b00
    CLOCK_OUT_FREQUENCY_1024HZ = 0b01
    CLOCK_OUT_FREQUENCY_1HZ = 0b10

    COUNTDOWN_TIMER_ON = True
    COUNTDOWN_TIMER_OFF = False
    TIME_UPDATE_1_SECOND = False
    TIME_UPDATE_1_MINUTE = True

    ENABLE_EVI_CALIBRATION = True
    DISABLE_EVI_CALIBRATION = False
    EVI_DEBOUNCE_NONE = 0b00
    EVI_DEBOUNCE_256HZ = 0b01
    EVI_DEBOUNCE_64HZ = 0b10
    EVI_DEBOUNCE_8HZ = 0b11
    RISING_EDGE = True
    FALLING_EDGE = False
    EVI_CAPTURE_ENABLE = True
    EVI_CAPTURE_DISABLE = False
    
    # Vars for time list
    TIME_LIST_LENGTH = 8
    IDX_HUNDREDTHS = 0
    IDX_SECONDS = 1
    IDX_MINUTES = 2
    IDX_HOURS = 3
    IDX_WEEKDAY = 4
    IDX_DATE = 5
    IDX_MONTH = 6
    IDX_YEAR = 7

    def __init__(self, address=None, i2c_bus=None):
        """!
        Constructor

        @param address: **int, optional** The I2C address to use for the device
            If not provided, the default address is used
        @param i2c_bus: **I2CBus, optional** A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.
        """
        # The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
        address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)

        # Use address if provided, otherwise pick the default
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Use the given I2C bus, or the platform's default bus
        self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)

        self._is_12_hour = True # True if 12 hour mode, False if 24 hour mode
        self._time = [0] * self.TIME_LIST_LENGTH # list of bytes for time

    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        return self._i2c.is_device_connected(self.address)

    def begin(self):
        """!
        Initializes this device with default parameters

        @return **bool** Returns `True` if successful, otherwise `False`
        """
        # Confirm device is connected before doing anything
        return self.is_connected()
    
    def set_12_hour(self):
        """!
        Sets the device to 12 hour mode
        """
        self._is_12_hour = True

    def set_24_hour(self):
        """!
        Sets the device to 24 hour mode
        """
        self._is_12_hour = False
    
    def is_12_hour(self):
        """!
        Determines if the device is in 12 hour mode

        @return **bool** `True` if in 12 hour mode, otherwise `False`
        """
        return self._is_12_hour 

    def is_pm(self):
        """!
        Determines if the device is in PM

        @return **bool** Returns true if the microcontroller is in 12 hour mode and the RTC has an hours value greater than or equal to 12 (Noon).
        """
        if self.is_12_hour():
            return self.bcd_to_dec(self._time[self.IDX_HOURS]) >= 12
        
        return False
    
    def string_date_usa(self):
        """!
        Returns the date in MM/DD/YYYY format
        """
        return "{:02}/{:02}/20{:02}".format(self.bcd_to_dec(self._time[self.IDX_MONTH]), self.bcd_to_dec(self._time[self.IDX_DATE]), self.bcd_to_dec(self._time[self.IDX_YEAR]))
    
    def string_date(self):
        """!
        Returns the date in the DD/MM/YYYY format
        """
        return "{:02}/{:02}/20{:02}".format(self.bcd_to_dec(self._time[self.IDX_DATE]), self.bcd_to_dec(self._time[self.IDX_MONTH]), self.bcd_to_dec(self._time[self.IDX_YEAR]))

    def string_time(self):
        """!
        Returns the time in hh:mm:ss (Adds AM/PM if in 12 hour mode)
        """
        if self.is_12_hour():
            hours = self.bcd_to_dec(self._time[self.IDX_HOURS])
            return "{:02}:{:02}:{:02} {}".format(hours if hours <= 12 else hours - 12, 
                                                 self.bcd_to_dec(self._time[self.IDX_MINUTES]), 
                                                 self.bcd_to_dec(self._time[self.IDX_SECONDS]), 
                                                 "PM" if self.is_pm() else "AM")
        
        return "{:02}:{:02}:{:02}".format(self.bcd_to_dec(self._time[self.IDX_HOURS]), 
                                          self.bcd_to_dec(self._time[self.IDX_MINUTES]), 
                                          self.bcd_to_dec(self._time[self.IDX_SECONDS]))

    def string_timestamp(self):
        """!
        Returns the most recent timestamp captured on the EVI pin (if the EVI pin has been configured to capture events)
        """

        hundredths = self._i2c.read_byte(self.address, self.REG_HUNDREDTHS_CAPTURE)
        seconds = self._i2c.read_byte(self.address, self.REG_SECONDS_CAPTURE)

        if self.is_12_hour():
            hours = self.bcd_to_dec(self._time[self.IDX_HOURS])
            return "{:02}:{:02}:{:02}:{:02}{}".format(hours if hours <= 12 else hours - 12, 
                                                       self.bcd_to_dec(self._time[self.IDX_MINUTES]), 
                                                       self.bcd_to_dec(seconds), 
                                                       self.bcd_to_dec(hundredths),
                                                       "PM" if self.is_pm() else "AM",
                                                       )
        else:
            return "{:02}:{:02}:{:02}:{:02}".format(self.bcd_to_dec(self._time[self.IDX_HOURS]), 
                                                    self.bcd_to_dec(self._time[self.IDX_MINUTES]), 
                                                    self.bcd_to_dec(seconds), 
                                                    self.bcd_to_dec(hundredths))
                    
    def string_time_8601(self):
        """!
        Returns timestamp in ISO 8601 format (yyyy-mm-ddThh:mm:ss)
        """
        return "20{:02}-{:02}-{:02}T{:02}:{:02}:{:02}".format(self.bcd_to_dec(self._time[self.IDX_YEAR]), 
                                                              self.bcd_to_dec(self._time[self.IDX_MONTH]), 
                                                              self.bcd_to_dec(self._time[self.IDX_DATE]), 
                                                              self.bcd_to_dec(self._time[self.IDX_HOURS]), 
                                                              self.bcd_to_dec(self._time[self.IDX_MINUTES]), 
                                                              self.bcd_to_dec(self._time[self.IDX_SECONDS]))

    """!
    Below is an optimized python port of the following Arduino c++ function:

    char* RV8803::stringTime8601TZ(char* buffer, size_t len)
    {
        int8_t quarterHours = getTimeZoneQuarterHours();
        char plusMinus = '+';
        if (quarterHours < 0)
        {
            plusMinus = '-';
            quarterHours *= -1;
        }
        uint16_t mins = quarterHours * 15;
        uint8_t tzh = mins / 60;
        uint8_t tzm = mins % 60;
        snprintf(buffer, len, "20%02d-%02d-%02dT%02d:%02d:%02d%c%02d:%02d", BCDtoDEC(_time[TIME_YEAR]), BCDtoDEC(_time[TIME_MONTH]), BCDtoDEC(_time[TIME_DATE]),
                                                                BCDtoDEC(_time[TIME_HOURS]), BCDtoDEC(_time[TIME_MINUTES]), BCDtoDEC(_time[TIME_SECONDS]),
                                                                plusMinus, tzh, tzm);
        return (buffer);
    }
    """
    def string_time_8601_tz(self):
        """!
        Returns timestamp in ISO 8601 format (yyyy-mm-ddThh:mm:ss) and uses timezone corrections
        """
        quarter_hours = self.get_time_zone_quarter_hours()
        plus_minus = '+'
        if quarter_hours < 0:
            plus_minus = '-'
            quarter_hours = quarter_hours * -1
        
        mins = quarter_hours * 15
        tzh = mins // 60
        tzm = mins % 60

        return "20{:02}-{:02}-{:02}T{:02}:{:02}:{:02}{}{:02}:{:02}".format(self.bcd_to_dec(self._time[self.IDX_YEAR]),
                                                                            self.bcd_to_dec(self._time[self.IDX_MONTH]),
                                                                            self.bcd_to_dec(self._time[self.IDX_DATE]),
                                                                            self.bcd_to_dec(self._time[self.IDX_HOURS]),
                                                                            self.bcd_to_dec(self._time[self.IDX_MINUTES]),
                                                                            self.bcd_to_dec(self._time[self.IDX_SECONDS]),
                                                                            plus_minus,
                                                                            tzh,
                                                                            tzm)

    def string_day_of_week(self):
        """!
        Returns the day of the week as a string

        @return **str** The day of the week as a string
        """
        day = self._time[self.IDX_WEEKDAY]
        if day == self.SUNDAY:
            return "Sunday"
        elif day == self.MONDAY:
            return "Monday"
        elif day == self.TUESDAY:
            return "Tuesday"
        elif day == self.WEDNESDAY:
            return "Wednesday"
        elif day == self.THURSDAY:
            return "Thursday"
        elif day == self.FRIDAY:
            return "Friday"
        elif day == self.SATURDAY:
            return "Saturday"
        else:
            return "Invalid Day"
    
    def string_day_of_week_short(self):
        """!
        Return the day of week. Returns "Sun", "Mon" etc

        @return **str** The day of the week as a string
        """
        return self.string_day_of_week()[:3]
    

    def string_date_ordinal(self):
        """!
        Return the ordinal for the date (day of month). Returns "1st", "2nd", "3rd", "4th" etc
        """
        day = self.bcd_to_dec(self._time[self.IDX_DATE])
        if day == 1 or day == 21 or day == 31:
            return "{}st".format(day)
        elif day == 2 or day == 22:
            return "{}nd".format(day)
        elif day == 3 or day == 23:
            return "{}rd".format(day)
        else:
            return "{}th".format(day)

    def string_month(self):
        """!
        Return the name of the month. Returns "January", etc

        @return **str** The month as a string
        """
        month = self.bcd_to_dec(self._time[self.IDX_MONTH])
        if month == 1:
            return "January"
        elif month == 2:
            return "February"
        elif month == 3:
            return "March"
        elif month == 4:
            return "April"
        elif month == 5:
            return "May"
        elif month == 6:
            return "June"
        elif month == 7:
            return "July"
        elif month == 8:
            return "August"
        elif month == 9:
            return "September"
        elif month == 10:
            return "October"
        elif month == 11:
            return "November"
        elif month == 12:
            return "December"
        else:
            return "Invalid Month"
    
    def string_month_short(self):
        """!
        Return the name of the month (short). Returns "Jan", "Feb" etc

        @return **str** The month as a string
        """
        return self.string_month()[:3]
    
    def set_time_list(self, time_list):
        """!
        Sets the time using a list of bytes

        @param time_list: **list** A list of bytes representing the time

        @return **bool** `True` if successful, otherwise `False`
        """
        if len(time_list) != self.TIME_LIST_LENGTH:
            return False
        
        self._time = time_list
        
        # We leave out the hundredths value because it is read only
        self._i2c.write_block(self.address, self.REG_SECONDS, self._time[1:])

        # Set RESET bit to 0 after setting time to make sure seconds don't get stuck.
        self.write_bit(self.REG_CONTROL, self.CONTROL_RESET, 0)

        return True
    
    def set_time(self, seconds, minutes, hours, weekday, date, month, year):
        """!
        Sets the time using individual values

        @param seconds: **int** The seconds value
        @param minutes: **int** The minutes value
        @param hours: **int** The hours value
        @param weekday: **int** The weekday value
        @param date: **int** The date value
        @param month: **int** The month value
        @param year: **int** The year value

        @return **bool** `True` if successful, otherwise `False`
        """

        # Verify input values
        if (seconds < 0 or seconds > 59 or
            minutes < 0 or minutes > 59 or
            hours < 0 or hours > 23 or
            (weekday not in [self.SUNDAY, self.MONDAY, self.TUESDAY, self.WEDNESDAY, self.THURSDAY, self.FRIDAY, self.SATURDAY]) or
            date < 1 or date > 31 or
            month < 1 or month > 12):
            return False

        self._time[self.IDX_SECONDS] = self.dec_to_bcd(seconds)
        self._time[self.IDX_MINUTES] = self.dec_to_bcd(minutes)
        self._time[self.IDX_HOURS] = self.dec_to_bcd(hours)
        self._time[self.IDX_WEEKDAY] = weekday # One bit per day, not BCD
        self._time[self.IDX_DATE] = self.dec_to_bcd(date)
        self._time[self.IDX_MONTH] = self.dec_to_bcd(month)
        self._time[self.IDX_YEAR] = self.dec_to_bcd(year - 2000)

        self.set_time_list(self._time)

        return True

    def set_epoch(self, value, use_1970s_epoch=True, time_zone_quarter_hours=0):
        """!
        Sets time using UNIX Epoch time.
        If time_zone_quarter_hours is non-zero, update RV8803_RAM. Add the zone to the epoch before setting

        @param value: **int** The epoch time
        @param use_1970s_epoch: **bool** If `True`, count from 1970-01-01 (Unix epoch), otherwise from 2000-01-01
        @param time_zone_quarter_hours: **int** The time zone offset in 15 minute increments
        """

        tz_offset = self.get_time_zone_quarter_hours() * 15 * 60

        if time_zone_quarter_hours != 0:
            self.set_time_zone_quarter_hours(time_zone_quarter_hours)
            tz_offset = time_zone_quarter_hours * 15 * 60

        value += tz_offset

        self.set_local_epoch(value, use_1970s_epoch)


    def set_local_epoch(self, value, use_1970s_epoch = True):
        """!
        Set the local epoch - without adding the time zone

        @param value: **int** The epoch time
        @param use_1970s_epoch: **bool** If `True`, count from 1970-01-01 (Unix epoch), otherwise from 2000-01-01
        """
        value = int(value)
        if not use_1970s_epoch:
            value += _SECONDS_1970_TO_2000

        days, seconds = divmod(value, 86400)
        year, month, date = _civil_from_days(days)

        self._time[self.IDX_SECONDS] = self.dec_to_bcd(seconds % 60)
        self._time[self.IDX_MINUTES] = self.dec_to_bcd((seconds // 60) % 60)
        self._time[self.IDX_HOURS] = self.dec_to_bcd(seconds // 3600)
        self._time[self.IDX_DATE] = self.dec_to_bcd(date)
        self._time[self.IDX_WEEKDAY] = 1 << ((days + 4) % 7) # 1970-01-01 was a Thursday; bit 0 is Sunday
        self._time[self.IDX_MONTH] = self.dec_to_bcd(month)
        self._time[self.IDX_YEAR] = self.dec_to_bcd(year - 2000)

        self.set_time_list(self._time)
    
    def set_hundredths_to_zero(self):
        """!
        Sets the hundredths value to zero by setting then clearing RESET bit in CONTROL register (see App-Manual page 43)
        """
        self.write_bit(self.REG_CONTROL, self.CONTROL_RESET, 1)
        self.write_bit(self.REG_CONTROL, self.CONTROL_RESET, 0)
    
    def set_seconds(self, value):
        """!
        Sets the seconds value

        @param value: **int** The seconds value

        @return **bool** `True` if successful, otherwise `False`
        """
        if value < 0 or value > 59:
            return False

        self._time[self.IDX_SECONDS] = self.dec_to_bcd(value)
        self.set_time_list(self._time)
        return True
    
    def set_minutes(self, value):
        """!
        Sets the minutes value

        @param value: **int** The minutes value

        @return **bool** `True` if successful, otherwise `False`
        """
        if value < 0 or value > 59:
            return False

        self._time[self.IDX_MINUTES] = self.dec_to_bcd(value)
        self.set_time_list(self._time)
        return True
    
    def set_hours(self, value):
        """!
        Sets the hours value

        @param value: **int** The hours value

        @return **bool** `True` if successful, otherwise `False`
        """
        if value < 0 or value > 23:
            return False

        self._time[self.IDX_HOURS] = self.dec_to_bcd(value)
        self.set_time_list(self._time)
        return True
    
    def set_date(self, value):
        """!
        Sets the date value

        @param value: **int** The date value

        @return **bool** `True` if successful, otherwise `False`
        """
        if value < 1 or value > 31:
            return False

        self._time[self.IDX_DATE] = self.dec_to_bcd(value)
        self.set_time_list(self._time)
        return True

    def set_weekday(self, value):
        """!
        Sets the weekday value

        @param value: **int** The weekday value
            Allowable Values:
                - SUNDAY
                - MONDAY
                - TUESDAY
                - WEDNESDAY
                - THURSDAY
                - FRIDAY
                - SATURDAY

        @return **bool** `True` if successful, otherwise `False`
        """
        if value not in [self.SUNDAY, self.MONDAY, self.TUESDAY, self.WEDNESDAY, self.THURSDAY, self.FRIDAY, self.SATURDAY]:
            return False

        self._time[self.IDX_WEEKDAY] = value # One bit per day, not BCD
        self.set_time_list(self._time)
        return True
    
    def set_month(self, value):
        """!
        Sets the month value

        @param value: **int** The month value

        @return **bool** `True` if successful, otherwise `False`
        """
        if value < 1 or value > 12:
            return False

        self._time[self.IDX_MONTH] = self.dec_to_bcd(value)
        self.set_time_list(self._time)
        return True
    
    def set_year(self, value):
        """!
        Sets the year value

        @param value: **int** The year value (specify full year, including the "20" prefix i.e. 2024 rather than 24)

        @return **bool** `True` if successful, otherwise `False`
        """
        self._time[self.IDX_YEAR] = self.dec_to_bcd(value - 2000)
        self.set_time_list(self._time)
        return True

    def set_time_zone_quarter_hours(self, quarter_hours):
        """!
        Sets the time zone in quarter hours

        @param quarter_hours: **int** The time zone offset in 15 minute increments

        @return **bool** `True` if successful, otherwise `False`
        """
        # verify signed 8 bit integer input
        if quarter_hours < -128 or quarter_hours > 127:
            return False

        # convert to unsigned
        if quarter_hours < 0:
            quarter_hours = 256 + quarter_hours

        self._i2c.write_byte(self.address, self.REG_RAM, quarter_hours)
        return True

    def get_time_zone_quarter_hours(self):
        """!
        Gets the time zone in quarter hours

        @return **int** The time zone offset in 15 minute increments
        """
        unsigned = self._i2c.read_byte(self.address, self.REG_RAM)
        return unsigned if unsigned < 128 else unsigned - 256

    def update_time(self):
        """!
        Updates the time by reading the time from the RTC and storing it in the time list.

        Move the hours, mins, sec, etc registers from RV-8803 into the _time array
        Needs to be called before printing time or date
        We do not protect the GPx registers. They will be overwritten. The user has plenty of RAM if they need it.
        """

        self._time = list(self._i2c.read_block(self.address, self.REG_HUNDREDTHS, self.TIME_LIST_LENGTH))
        # If hundredths are at 99 or seconds are at 59, read again to make sure we didn't accidentally skip a second/minute
        if self._time[self.IDX_HUNDREDTHS] == 0x99 or self._time[self.IDX_SECONDS] == 0x59:
            rollover_time = list(self._i2c.read_block(self.address, self.REG_HUNDREDTHS, self.TIME_LIST_LENGTH))
            # If the reading for hundredths has rolled over, then our new data is correct, otherwise, we can leave the old data.
            if self.bcd_to_dec(self._time[self.IDX_HUNDREDTHS]) > self.bcd_to_dec(rollover_time[self.IDX_HUNDREDTHS]):
                self._time = rollover_time
    
    def get_hundredths(self):
        """!
        Gets the byte value for hundredths

        @return **int** The hundredths
        """
        return self.bcd_to_dec(self._time[self.IDX_HUNDREDTHS])

    def get_seconds(self):
        """!
        Gets the byte value for seconds

        @return **int** The seconds
        """
        return self.bcd_to_dec(self._time[self.IDX_SECONDS])

    def get_minutes(self):
        """!
        Gets the byte value for minutes

        @return **int** The minutes
        """
        return self.bcd_to_dec(self._time[self.IDX_MINUTES])

    def get_hours(self):
        """!
        Gets the byte value for hours, automatically converts to 12 hour mode if necessary

        @return **int** The hours
        """
        hours = self.bcd_to_dec(self._time[self.IDX_HOURS])
        if self.is_12_hour() and (hours > 12):
            hours -= 12
            
        return hours

    def get_date(self):
        """!
        Gets the byte value for date

        @return **int** The date
        """
        return self.bcd_to_dec(self._time[self.IDX_DATE])

    def get_weekday(self):
        """!
        Gets the byte value for weekday. Compare against the day constants inherent to this class.

        @return **int** The weekday
        """
        return self._time[self.IDX_WEEKDAY] # One bit per day, not BCD

        # TODO: The arduino lib converts the weekday read to 0-6, this isn't really necessary if user always compares against the day constants
        #       but if we want that functionality, we can add it with this:
        # weekday = self._time[self.IDX_WEEKDAY]
        # for i in range (7):
        #     if weekday & (1 << i):
        #         return i

    def get_month(self):
        """!
        Gets the byte value for month

        @return **int** The month
        """
        return self.bcd_to_dec(self._time[self.IDX_MONTH])

    def get_year(self):
        """!
        Gets the byte value for year. Automatically adds 2000 to the year.

        @return **int** The year
        """
        return self.bcd_to_dec(self._time[self.IDX_YEAR]) + 2000

    def get_epoch(self, use_1970s_epoch=True):
        """!
        Get the epoch - with the time zone subtracted (i.e. return UTC epoch)

        @param use_1970s_epoch: **bool** If `True`, count from 1970-01-01 (Unix epoch), otherwise from 2000-01-01

        @return **int** The epoch time
        """
        local_epoch = self.get_local_epoch(use_1970s_epoch)
        return local_epoch - (self.get_time_zone_quarter_hours() * 15 * 60)
        

    def get_local_epoch(self, use_1970s_epoch=True):
        """!
        Get the local epoch - without subtracting the time zone

        @param use_1970s_epoch: **bool** If `True`, count from 1970-01-01 (Unix epoch), otherwise from 2000-01-01

        @return **int** The epoch time
        """

        days = _days_from_civil(self.bcd_to_dec(self._time[self.IDX_YEAR]) + 2000,
                                self.bcd_to_dec(self._time[self.IDX_MONTH]),
                                self.bcd_to_dec(self._time[self.IDX_DATE]))
        t = (days * 86400
             + self.bcd_to_dec(self._time[self.IDX_HOURS]) * 3600
             + self.bcd_to_dec(self._time[self.IDX_MINUTES]) * 60
             + self.bcd_to_dec(self._time[self.IDX_SECONDS]))

        if not use_1970s_epoch:
            t -= _SECONDS_1970_TO_2000
        
        return t

    
    def get_hundredths_capture(self):
        """!
        Gets the byte value for hundredths capture

        @return **int** The hundredths capture
        """
        return self.bcd_to_dec(self._i2c.read_byte(self.address, self.REG_HUNDREDTHS_CAPTURE))
    
    def get_seconds_capture(self):
        """!
        Gets the byte value for seconds capture

        @return **int** The seconds capture
        """
        return self.bcd_to_dec(self._i2c.read_byte(self.address, self.REG_SECONDS_CAPTURE))
    
    def set_calibration_offset(self, ppm):
        """!
        Sets the calibration offset in parts per million (ppm)

        Under the hood, the offset is a two's complement value with a range of -32 to + 31. See App-Manual page 22 for more information.

        @param ppm: **float** The calibration offset in parts per million
        """

        integer_offset = int(ppm / 0.238)
        
        if integer_offset < 0:
            integer_offset += 64

        self._i2c.write_byte(self.address, self.REG_OFFSET, integer_offset)

    def get_calibration_offset(self):
        """!
        Gets the calibration offset in parts per million

        @return **int** The calibration offset in parts per million
        """
        value = self._i2c.read_byte(self.address, self.REG_OFFSET)
        if value > 32:
            value -= 64
        return value * 0.238

    def set_evi_debounce_time(self, debounce_time):
        """!
        Sets the EVI debounce time

        @param debounce_time: **int** The debounce time
        """
        self.write_two_bits(self.REG_EVENT_CONTROL, self.EVENT_ET, debounce_time)

    def set_evi_calibration(self, evi_calibration):
        """!
        Sets the EVI calibration

        @param evi_calibration: **bool** The EVI calibration
        """
        self.write_bit(self.REG_EVENT_CONTROL, self.EVENT_ERST, evi_calibration)

    def set_evi_edge_detection(self, edge):
        """!
        Sets the EVI edge detection

        @param edge: **bool** The edge detection
        """
        self.write_bit(self.REG_EVENT_CONTROL, self.EVENT_EHL, edge)

    def set_evi_event_capture(self, capture):
        """!
        Sets the EVI event capture

        @param capture: **bool** The event capture
        """
        self.write_bit(self.REG_EVENT_CONTROL, self.EVENT_ECP, capture)

    def get_evi_debounce_time(self):
        """!
        Gets the EVI debounce time

        @return **int** The debounce time
        """
        return self.read_two_bits(self.REG_EVENT_CONTROL, self.EVENT_ET)

    def get_evi_calibration(self):
        """!
        Gets the EVI calibration

        @return **bool** The EVI calibration
        """
        return self.read_bit(self.REG_EVENT_CONTROL, self.EVENT_ERST)

    def get_evi_edge_detection(self):
        """!
        Gets the EVI edge detection

        @return **bool** The edge detection
        """
        return self.read_bit(self.REG_EVENT_CONTROL, self.EVENT_EHL)

    def get_evi_event_capture(self):
        """!
        Gets the EVI event capture

        @return **bool** The event capture
        """
        return self.read_bit(self.REG_EVENT_CONTROL, self.EVENT_ECP)

    def set_countdown_timer_enable(self, timer_state):
        """!
        Sets the countdown timer enable

        @param timer_state: **bool** The timer state
        """
        self.write_bit(self.REG_EXTENSION, self.EXTENSION_TE, timer_state)

    def set_countdown_timer_frequency(self, countdown_timer_frequency):
        """!
        Sets the countdown timer frequency

        @param countdown_timer_frequency: **int** The countdown timer frequency
        """
        self.write_two_bits(self.REG_EXTENSION, self.EXTENSION_TD, countdown_timer_frequency)
    
    def set_countdown_timer_clock_ticks(self, clock_ticks):
        """!
        Sets the countdown timer clock ticks

        @param clock_ticks: **int** The clock ticks
        """
        # First handle the upper bit, as we need to preserve the GPX bits
        value = self._i2c.read_byte(self.address, self.REG_TIMER1)
        value &= ~(0b00001111)  # Clear the least significant nibble
        value |= (clock_ticks >> 8)
        self._i2c.write_byte(self.address, self.REG_TIMER1, value)
        value = clock_ticks & 0x00FF
        self._i2c.write_byte(self.address, self.REG_TIMER0, value)
    
    def get_countdown_timer_clock_ticks(self):
        """!
        Gets the countdown timer clock ticks

        @return **int** The countdown timer clock ticks
        """
        value = self._i2c.read_byte(self.address, self.REG_TIMER1) << 8
        value |= self._i2c.read_byte(self.address, self.REG_TIMER0)
        return value
    
    def set_clock_out_timer_frequency(self, clock_out_timer_frequency):
        """!
        Sets the clock out timer frequency

        @param clock_out_timer_frequency: **int** The clock out timer frequency
        """
        self.write_bit(self.REG_EXTENSION, self.EXTENSION_FD, clock_out_timer_frequency)

    def get_countdown_timer_enable(self):
        """!
        Gets the countdown timer enable

        @return **bool** The countdown timer enable
        """
        return self.read_bit(self.REG_EXTENSION, self.EXTENSION_TE)

    def get_countdown_timer_frequency(self):
        """!
        Gets the countdown timer frequency

        @return **int** The countdown timer frequency
        """
        return self.read_two_bits(self.REG_EXTENSION, self.EXTENSION_TD)

    def get_clock_out_timer_frequency(self):
        """!
        Gets the clock out timer frequency

        @return **int** The clock out timer frequency
        """
        return self.read_two_bits(self.REG_EXTENSION, self.EXTENSION_FD)

    def set_periodic_time_update_frequency(self, time_update_frequency):
        """!
        Sets the periodic time update frequency

        @param time_update_frequency: **bool** The time update frequency
        """
        self.write_bit(self.REG_EXTENSION, self.EXTENSION_USEL, time_update_frequency)

    def get_periodic_time_update_frequency(self):
        """!
        Gets the periodic time update frequency

        @return **bool** The periodic time update frequency
        """
        return self.read_bit(self.REG_EXTENSION, self.EXTENSION_USEL)

    def set_items_to_match_for_alarm(self, minute_alarm, hour_alarm, weekday_alarm, date_alarm):
        """!
        Set Alarm Mode controls which parts of the time have to match for the alarm to trigger.
        When the RTC matches a given time, make an interrupt fire.
        Setting a bit to 1 means that the RTC does not check if that value matches to trigger the alarm.

        Alarm goes off with match of second, minute, hour, etc

        @param minute_alarm: **bool** If `True`, the alarm will trigger on a match of the minutes
        @param hour_alarm: **bool** If `True`, the alarm will trigger on a match of the hours
        @param weekday_alarm: **bool** If `True`, the alarm will trigger on a match of the weekday
        @param date_alarm: **bool** If `True`, the alarm will trigger on a match of the date
        """
        self.write_bit(self.REG_MINUTES_ALARM, self.ALARM_ENABLE, not minute_alarm)  # For some reason these bits are active low
        self.write_bit(self.REG_HOURS_ALARM, self.ALARM_ENABLE, not hour_alarm)
        self.write_bit(self.REG_WEEKDAYS_DATE_ALARM, self.ALARM_ENABLE, not weekday_alarm)
        self.write_bit(self.REG_EXTENSION, self.EXTENSION_WADA, date_alarm)
        if date_alarm:  # enabling both weekday and date alarm will default to a date alarm
            self.write_bit(self.REG_WEEKDAYS_DATE_ALARM, self.ALARM_ENABLE, not date_alarm)

    def set_alarm_minutes(self, minute):
        """!
        Sets the alarm minutes

        @param minute: **int** The minute value
        """
        value = self._i2c.read_byte(self.address, self.REG_MINUTES_ALARM)
        value &= (1 << self.ALARM_ENABLE)  # clear everything but enable bit
        value |= self.dec_to_bcd(minute)
        self._i2c.write_byte(self.address, self.REG_MINUTES_ALARM, value)

    def set_alarm_hours(self, hour):
        """!
        Sets the alarm hours

        @param hour: **int** The hour value
        """
        value = self._i2c.read_byte(self.address, self.REG_HOURS_ALARM)
        value &= (1 << self.ALARM_ENABLE)  # clear everything but enable bit
        value |= self.dec_to_bcd(hour)
        self._i2c.write_byte(self.address, self.REG_HOURS_ALARM, value)

    def set_alarm_weekday(self, weekday):
        """!
        Sets the alarm weekday

        @param weekday: **int** The weekday value
        """
        value = self._i2c.read_byte(self.address, self.REG_WEEKDAYS_DATE_ALARM)
        value &= (1 << self.ALARM_ENABLE)  # clear everything but enable bit
        value |= 0x7F & weekday
        self._i2c.write_byte(self.address, self.REG_WEEKDAYS_DATE_ALARM, value)

    def set_alarm_date(self, date):
        """!
        Sets the alarm date

        @param date: **int** The date value
        """
        value = self._i2c.read_byte(self.address, self.REG_WEEKDAYS_DATE_ALARM)
        value &= (1 << self.ALARM_ENABLE)  # clear everything but enable bit
        value |= self.dec_to_bcd(date)
        self._i2c.write_byte(self.address, self.REG_WEEKDAYS_DATE_ALARM, value)
    
    def enable_hardware_interrupt(self, source):
        """!
        Enables the hardware interrupt for the given source

        Given a bit location, enable the interrupt
        Allowable sources: 
            UPDATE_INTERRUPT
            TIMER_INTERRUPT
            ALARM_INTERRUPT
            EVI_INTERRUPT
            CONTROL_RESET

        @param source: **int** The interrupt source
        """
        if source not in [self.UPDATE_INTERRUPT, self.TIMER_INTERRUPT, self.ALARM_INTERRUPT, self.EVI_INTERRUPT, self.CONTROL_RESET]:
            return

        value = self._i2c.read_byte(self.address, self.REG_CONTROL)
        value |= (1 << source)  # Set the interrupt enable bit
        self._i2c.write_byte(self.address, self.REG_CONTROL, value)

    def disable_hardware_interrupt(self, source):
        """!
        Disables the hardware interrupt for the given source
        Allowable sources: 
            UPDATE_INTERRUPT
            TIMER_INTERRUPT
            ALARM_INTERRUPT
            EVI_INTERRUPT
            CONTROL_RESET

        @param source: **int** The interrupt source
        """
        if source not in [self.UPDATE_INTERRUPT, self.TIMER_INTERRUPT, self.ALARM_INTERRUPT, self.EVI_INTERRUPT, self.CONTROL_RESET]:
            return
        value = self._i2c.read_byte(self.address, self.REG_CONTROL)
        value &= ~(1 << source)  # Clear the interrupt enable bit
        self._i2c.write_byte(self.address, self.REG_CONTROL, value)

    def disable_all_interrupts(self):
        """!
        Disables all hardware interrupts
        """
        value = self._i2c.read_byte(self.address, self.REG_CONTROL)
        value &= 1  # Clear all bits except for Reset
        self._i2c.write_byte(self.address, self.REG_CONTROL, value)

    def get_interrupt_flag(self, flag_to_get):
        """!
        Gets the interrupt flag for the given source

        @param flag_to_get: **int** The interrupt flag to get

        @return **bool** The value of the interrupt flag
        """
        flag = self._i2c.read_byte(self.address, self.REG_FLAG)
        flag &= (1 << flag_to_get)
        flag = flag >> flag_to_get
        return flag != 0

    def clear_all_interrupt_flags(self):
        """!
        Clears all interrupt flags
        """
        self._i2c.write_byte(self.address, self.REG_FLAG, 0b00000000)  # Write all 0's to clear all flags

    def clear_interrupt_flag(self, flag_to_clear):
        """!
        Clears the interrupt flag for the given source

        @param flag_to_clear: **int** The interrupt flag to clear
        """
        value = self._i2c.read_byte(self.address, self.REG_FLAG)
        value &= ~(1 << flag_to_clear)  # Clear flag
        self._i2c.write_byte(self.address, self.REG_FLAG, value)

    def get_alarm_minutes(self):
        """!
        Gets the alarm minutes

        @return **int** The alarm minutes
        """
        return self.bcd_to_dec(self._i2c.read_byte(self.address, self.REG_MINUTES_ALARM) & 0x7F)

    def get_alarm_hours(self):
        """!
        Gets the alarm hours

        @return **int** The alarm hours
        """
        return self.bcd_to_dec(self._i2c.read_byte(self.address, self.REG_HOURS_ALARM) & 0x7F)

    def get_alarm_weekday(self):
        """!
        Gets the alarm weekday

        @return **int** The alarm weekday mask (one bit per day, as set_alarm_weekday() takes)
        """
        return self._i2c.read_byte(self.address, self.REG_WEEKDAYS_DATE_ALARM) & 0x7F

    def get_alarm_date(self):
        """!
        Gets the alarm date

        @return **int** The alarm date
        """
        return self.bcd_to_dec(self._i2c.read_byte(self.address, self.REG_WEEKDAYS_DATE_ALARM) & 0x7F)


    # Helper Functions
    def dec_to_bcd(self, val):
        """!
        Converts decimal to binary coded decimal

        @param val: The decimal value to convert

        @return **int** The binary coded decimal
        """
        if (val < 0) or (val > 255):
            return 0
        
        return ( (val // 10) * 16) + (val % 10)
    
    def bcd_to_dec(self, val):
        """!
        Converts binary coded decimal to decimal

        @param val: The binary coded decimal value to convert

        @return **int** The decimal value
        """
        return ( (val // 16) * 10) + (val % 16)
    
    def write_bit(self, reg, bit, val):
        """!
        Writes a bit to a register

        @param reg: **int** The register to write to
        @param bit: **int** The bit to write
        @param val: **bool** The value to write
        """
        data = self._i2c.read_byte(self.address, reg)

        data &= ~(1 << bit)
        
        if val:
            data |= (1 << bit)

        self._i2c.write_byte(self.address, reg, data)
    
    def write_two_bits(self, reg, bit, val):
        """!
        Writes two bits to a register

        @param reg: **int** The register to write to
        @param bit: **int** The bit to write
        @param val: **int** The value to write
        """
        data = self._i2c.read_byte(self.address, reg)

        data &= ~(3 << bit)
        data |= (val << bit)

        self._i2c.write_byte(self.address, reg, data)
    
    def read_bit(self, reg, bit):
        """!
        Reads a bit from a register

        @param reg: **int** The register to read from
        @param bit: **int** The bit to read

        @return **bool** The value of the bit
        """
        data = self._i2c.read_byte(self.address, reg)
        return (data & (1 << bit)) != 0

    def read_two_bits(self, reg, bit):
        """!
        Reads two bits from a register

        @param reg: **int** The register to read from
        @param bit: **int** The bit to read

        @return **int** The value of the bits
        """
        data = self._i2c.read_byte(self.address, reg)
        return (data & (3 << bit)) >> bit
    