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
import time

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class
# instance. This allows higher level logic to rapidly create a index of Qwiic
# devices at runtine
_DEFAULT_NAME = "Qwiic RV8803"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x32] 

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicRV8803(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Day constants
    kSunday = 0x01
    kMonday = 0x02
    kTuesday = 0x04
    kWednesday = 0x08
    kThursday = 0x10
    kFriday = 0x20
    kSaturday = 0x40

    # Register names
    kRegRAM = 0x07
    kRegHundredths = 0x10
    kRegSeconds = 0x11
    kRegMinutes = 0x12
    kRegHours = 0x13
    kRegWeekdays = 0x14
    kRegDate = 0x15
    kRegMonths = 0x16
    kRegYears = 0x17
    kRegMinutesAlarm = 0x18
    kRegHoursAlarm = 0x19
    kRegWeekdaysDateAlarm = 0x1A
    kRegTimer0 = 0x1B
    kRegTimer1 = 0x1C
    kRegExtension = 0x1D
    kRegFlag = 0x1E
    kRegControl = 0x1F
    kRegHundredthsCapture = 0x20
    kRegSecondsCapture = 0x21
    kRegOffset = 0x2C
    kRegEventControl = 0x2F

    # Enable Bits for Alarm Registers
    kAlarmEnable = 7

    # Extension Register Bits
    kExtensionTest = 7
    kExtensionWada = 6
    kExtensionUsel = 5
    kExtensionTe = 4
    kExtensionFd = 2
    kExtensionTd = 0

    # Flag Register Bits
    kFlagUpdate = 5
    kFlagTimer = 4
    kFlagAlarm = 3
    kFlagEvi = 2
    kFlagV2f = 1
    kFlagV1f = 0

    # Interrupt Control Register Bits
    kUpdateInterrupt = 5
    kTimerInterrupt = 4
    kAlarmInterrupt = 3
    kEviInterrupt = 2
    kControlReset = 0

    # Event Control Bits
    kEventEcp = 7
    kEventEhl = 6
    kEventEt = 4
    kEventErst = 0

    # Possible Settings
    kCountdownTimerFrequency4096Hz = 0b00
    kCountdownTimerFrequency64Hz = 0b01
    kCountdownTimerFrequency1Hz = 0b10
    kCountdownTimerFrequency1_60thHz = 0b11
    kClockOutFrequency32768Hz = 0b00
    kClockOutFrequency1024Hz = 0b01
    kClockOutFrequency1Hz = 0b10

    kCountdownTimerOn = True
    kCountdownTimerOff = False
    kTimeUpdate1Second = False
    kTimeUpdate1Minute = True

    kEnableEviCalibration = True
    kDisableEviCalibration = False
    kEviDebounceNone = 0b00
    kEviDebounce256Hz = 0b01
    kEviDebounce64Hz = 0b10
    kEviDebounce8Hz = 0b11
    kRisingEdge = True
    kFallingEdge = False
    kEviCaptureEnable = True
    kEviCaptureDisable = False
    
    # Vars for time list
    kTimeListLength = 8
    kIdxHundredths = 0
    kIdxSeconds = 1
    kIdxMinutes = 2
    kIdxHours = 3
    kIdxWeekday = 4
    kIdxDate = 5
    kIdxMonth = 6
    kIdxYear = 7

    # Indices into localtime() struct_time/returned tuple
    kTmYear = 0
    kTmMonth = 1
    kTmMDay = 2
    kTmHour = 3
    kTmMinute = 4
    kTmSecond = 5
    kTmWDay = 6
    kTmYDay = 7
    kTmIsDST = 8 # Note, IsDST is implemented in CircuitPython but not in MicroPython

    def __init__(self, address=None, i2c_driver=None):
        """!
        Constructor

        @param int, optional address: The I2C address to use for the device
            If not provided, the default address is used
        @param I2CDriver, optional i2c_driver: An existing i2c driver object
            If not provided, a driver object is created
        """

        # Use address if provided, otherwise pick the default
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver
        
        self._is12Hour = True # True if 12 hour mode, False if 24 hour mode
        self._time = [0] * self.kTimeListLength # list of bytes for time

        # Some platforms (CircuitPython, RasPi) have time.struct_time objects with tm_isdst while others (MicroPython) do not
        # This check will save whether the platform has tm_isdst or not
        self._hasIsDst = False
        if len(time.localtime()) > 8:
            self._hasIsDst = True
        
    def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        return self._i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

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
        self._is12Hour = True

    def set_24_hour(self):
        """!
        Sets the device to 24 hour mode
        """
        self._is12Hour = False
    
    def is_12_hour(self):
        """!
        Determines if the device is in 12 hour mode

        @return **bool** `True` if in 12 hour mode, otherwise `False`
        """
        return self._is12Hour 

    def is_PM(self):
        """!
        Determines if the device is in PM

        @return **bool** Returns true if the microcontroller is in 12 hour mode and the RTC has an hours value greater than or equal to 12 (Noon).
        """
        if self.is_12_hour():
            return self.bcd_to_dec(self._time[self.kIdxHours]) >= 12
        
        return False
    
    def string_date_usa(self):
        """!
        Returns the date in MM/DD/YYYY format
        """
        return "{:02}/{:02}/20{:02}".format(self.bcd_to_dec(self._time[self.kIdxMonth]), self.bcd_to_dec(self._time[self.kIdxDate]), self.bcd_to_dec(self._time[self.kIdxYear]))
    
    def string_date(self):
        """!
        Returns the date in the DD/MM/YYYY format
        """
        return "{:02}/{:02}/20{:02}".format(self.bcd_to_dec(self._time[self.kIdxDate]), self.bcd_to_dec(self._time[self.kIdxMonth]), self.bcd_to_dec(self._time[self.kIdxYear]))

    def string_time(self):
        """!
        Returns the time in hh:mm:ss (Adds AM/PM if in 12 hour mode)
        """
        if self.is_12_hour():
            hours = self.bcd_to_dec(self._time[self.kIdxHours])
            return "{:02}:{:02}:{:02} {}".format(hours if hours <= 12 else hours - 12, 
                                                 self.bcd_to_dec(self._time[self.kIdxMinutes]), 
                                                 self.bcd_to_dec(self._time[self.kIdxSeconds]), 
                                                 "PM" if self.is_PM() else "AM")
        
        return "{:02}:{:02}:{:02}".format(self.bcd_to_dec(self._time[self.kIdxHours]), 
                                          self.bcd_to_dec(self._time[self.kIdxMinutes]), 
                                          self.bcd_to_dec(self._time[self.kIdxSeconds]))

    def string_timestamp(self):
        """!
        Returns the most recent timestamp captured on the EVI pin (if the EVI pin has been configured to capture events)
        """

        hundredths = self._i2c.readByte(self.address, self.kRegHundredthsCapture)
        seconds = self._i2c.readByte(self.address, self.kRegSecondsCapture)

        if self.is_12_hour():
            hours = self.bcd_to_dec(self._time[self.kIdxHours])
            return "{:02}:{:02}:{:02}:{:02}{}".format(hours if hours <= 12 else hours - 12, 
                                                       self.bcd_to_dec(self._time[self.kIdxMinutes]), 
                                                       self.bcd_to_dec(seconds), 
                                                       self.bcd_to_dec(hundredths),
                                                       "PM" if self.is_PM() else "AM",
                                                       )
        else:
            return "{:02}:{:02}:{:02}:{:02}".format(self.bcd_to_dec(self._time[self.kIdxHours]), 
                                                    self.bcd_to_dec(self._time[self.kIdxMinutes]), 
                                                    self.bcd_to_dec(seconds), 
                                                    self.bcd_to_dec(hundredths))
                    
    def string_time_8601(self):
        """!
        Returns timestamp in ISO 8601 format (yyyy-mm-ddThh:mm:ss)
        """
        return "20{:02}-{:02}-{:02}T{:02}:{:02}:{:02}".format(self.bcd_to_dec(self._time[self.kIdxYear]), 
                                                              self.bcd_to_dec(self._time[self.kIdxMonth]), 
                                                              self.bcd_to_dec(self._time[self.kIdxDate]), 
                                                              self.bcd_to_dec(self._time[self.kIdxHours]), 
                                                              self.bcd_to_dec(self._time[self.kIdxMinutes]), 
                                                              self.bcd_to_dec(self._time[self.kIdxSeconds]))

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
    def string_time_8601_TZ(self):
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

        return "20{:02}-{:02}-{:02}T{:02}:{:02}:{:02}{}{:02}:{:02}".format(self.bcd_to_dec(self._time[self.kIdxYear]),
                                                                            self.bcd_to_dec(self._time[self.kIdxMonth]),
                                                                            self.bcd_to_dec(self._time[self.kIdxDate]),
                                                                            self.bcd_to_dec(self._time[self.kIdxHours]),
                                                                            self.bcd_to_dec(self._time[self.kIdxMinutes]),
                                                                            self.bcd_to_dec(self._time[self.kIdxSeconds]),
                                                                            plus_minus,
                                                                            tzh,
                                                                            tzm)

    def string_day_of_week(self):
        """!
        Returns the day of the week as a string

        @return **str** The day of the week as a string
        """
        day = self._time[self.kIdxWeekday]
        if day == self.kSunday:
            return "Sunday"
        elif day == self.kMonday:
            return "Monday"
        elif day == self.kTuesday:
            return "Tuesday"
        elif day == self.kWednesday:
            return "Wednesday"
        elif day == self.kThursday:
            return "Thursday"
        elif day == self.kFriday:
            return "Friday"
        elif day == self.kSaturday:
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
        day = self.bcd_to_dec(self._time[self.kIdxDate])
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
        month = self._time[self.kIdxMonth]
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

        @param list time_list: A list of bytes representing the time

        @return **bool** `True` if successful, otherwise `False`
        """
        if len(time_list) != self.kTimeListLength:
            return False
        
        self._time = time_list
        
        # We leave out the hundredths value because it is read only
        self._i2c.writeBlock(self.address, self.kRegSeconds, self._time[1:])

        # Set RESET bit to 0 after setting time to make sure seconds don't get stuck.
        self.write_bit(self.kRegControl, self.kControlReset, 0)

        return True
    
    def set_time(self, seconds, minutes, hours, weekday, date, month, year):
        """!
        Sets the time using individual values

        @param int seconds: The seconds value
        @param int minutes: The minutes value
        @param int hours: The hours value
        @param int weekday: The weekday value
        @param int date: The date value
        @param int month: The month value
        @param int year: The year value

        @return **bool** `True` if successful, otherwise `False`
        """

        # Verify input values
        if (seconds < 0 or seconds > 59 or
            minutes < 0 or minutes > 59 or
            hours < 0 or hours > 23 or
            (weekday not in [self.kSunday, self.kMonday, self.kTuesday, self.kWednesday, self.kThursday, self.kFriday, self.kSaturday]) or
            date < 1 or date > 31 or
            month < 1 or month > 12):
            return False

        self._time[self.kIdxSeconds] = self.dec_to_bcd(seconds)
        self._time[self.kIdxMinutes] = self.dec_to_bcd(minutes)
        self._time[self.kIdxHours] = self.dec_to_bcd(hours)
        self._time[self.kIdxWeekday] = self.dec_to_bcd(weekday)
        self._time[self.kIdxDate] = self.dec_to_bcd(date)
        self._time[self.kIdxMonth] = self.dec_to_bcd(month)
        self._time[self.kIdxYear] = self.dec_to_bcd(year - 2000)

        self.set_time_list(self._time)

        return True

    def set_epoch(self, value, use1970sEpoch=True, timeZoneQuarterHours=0):
        """!
        Sets time using UNIX Epoch time.
        If timeZoneQuarterHours is non-zero, update RV8803_RAM. Add the zone to the epoch before setting

        @param int value: The epoch time
        @param bool use1970sEpoch: If `True`, the epoch is in the 1970s
        @param int timeZoneQuarterHours: The time zone offset in 15 minute increments
        """

        tz_offset = self.get_time_zone_quarter_hours() * 15 * 60

        if timeZoneQuarterHours != 0:
            self.set_time_zone_quarter_hours(timeZoneQuarterHours)
            tz_offset = timeZoneQuarterHours * 15 * 60

        value += tz_offset

        self.set_local_epoch(value, use1970sEpoch)


    def set_local_epoch(self, value, use1970sEpoch = True):
        """!
        Set the local epoch - without adding the time zone

        @param int value: The epoch time
        @param bool use1970sEpoch: If `True`, the epoch is in the 1970s
        """
        if not use1970sEpoch:
            value += 946684800
        
        # TODO: MicroPython has time.gmtime() while CircuitPython does not. Both have time.localtime(). Since neither really has timezone support, 
        #       the output or time.gmtime() is equivalent to time.localtime() for both. However, RaspberryPi likely has explicit timezone support, so we might have to 
        #       add a check for that.
        tmp = time.localtime(value)
        
        self._time[self.kIdxSeconds] = self.dec_to_bcd(tmp[self.kTmSecond])
        self._time[self.kIdxMinutes] = self.dec_to_bcd(tmp[self.kTmMinute])
        self._time[self.kIdxHours] = self.dec_to_bcd(tmp[self.kTmHour])
        self._time[self.kIdxDate] = self.dec_to_bcd(tmp[self.kTmMDay])
        self._time[self.kIdxWeekday] = self.dec_to_bcd(1 << tmp[self.kTmWDay])
        self._time[self.kIdxMonth] = self.dec_to_bcd(tmp[self.kTmMonth])
        self._time[self.kIdxYear] = self.dec_to_bcd(tmp[self.kTmYear] - 2000)

        self.set_time_list(self._time)
    
    def set_hundredths_to_zero(self):
        """!
        Sets the hundredths value to zero by setting then clearing RESET bit in CONTROL register (see App-Manual page 43)
        """
        self.write_bit(self.kRegControl, self.kControlReset, 1)
        self.write_bit(self.kRegControl, self.kControlReset, 0)
    
    def set_seconds(self, value):
        """!
        Sets the seconds value

        @param int value: The seconds value

        @return **bool** `True` if successful, otherwise `False`
        """
        if value < 0 or value > 59:
            return False

        self._time[self.kIdxSeconds] = self.dec_to_bcd(value)
        self.set_time_list(self._time)
        return True
    
    def set_minutes(self, value):
        """!
        Sets the minutes value

        @param int value: The minutes value

        @return **bool** `True` if successful, otherwise `False`
        """
        if value < 0 or value > 59:
            return False

        self._time[self.kIdxMinutes] = self.dec_to_bcd(value)
        self.set_time_list(self._time)
        return True
    
    def set_hours(self, value):
        """!
        Sets the hours value

        @param int value: The hours value

        @return **bool** `True` if successful, otherwise `False`
        """
        if value < 0 or value > 23:
            return False

        self._time[self.kIdxHours] = self.dec_to_bcd(value)
        self.set_time_list(self._time)
        return True
    
    def set_date(self, value):
        """!
        Sets the date value

        @param int value: The date value

        @return **bool** `True` if successful, otherwise `False`
        """
        if value < 1 or value > 31:
            return False

        self._time[self.kIdxDate] = self.dec_to_bcd(value)
        self.set_time_list(self._time)
        return True

    def set_weekday(self, value):
        """!
        Sets the weekday value

        @param int value: The weekday value
            Allowable Values:
                - kSunday
                - kMonday
                - kTuesday
                - kWednesday
                - kThursday
                - kFriday
                - kSaturday

        @return **bool** `True` if successful, otherwise `False`
        """
        if value not in [self.kSunday, self.kMonday, self.kTuesday, self.kWednesday, self.kThursday, self.kFriday, self.kSaturday]:
            return False

        self._time[self.kIdxWeekday] = self.dec_to_bcd(value)
        self.set_time_list(self._time)
        return True
    
    def set_month(self, value):
        """!
        Sets the month value

        @param int value: The month value

        @return **bool** `True` if successful, otherwise `False`
        """
        if value < 1 or value > 12:
            return False

        self._time[self.kIdxMonth] = self.dec_to_bcd(value)
        self.set_time_list(self._time)
        return True
    
    def set_year(self, value):
        """!
        Sets the year value

        @param int value: The year value (specify full year, including the "20" prefix i.e. 2024 rather than 24)

        @return **bool** `True` if successful, otherwise `False`
        """
        self._time[self.kIdxYear] = self.dec_to_bcd(value - 2000)
        self.set_time_list(self._time)
        return True

    def set_time_zone_quarter_hours(self, quarter_hours):
        """!
        Sets the time zone in quarter hours

        @param int quarter_hours: The time zone offset in 15 minute increments

        @return **bool** `True` if successful, otherwise `False`
        """
        # verify signed 8 bit integer input
        if quarter_hours < -128 or quarter_hours > 127:
            return False

        # convert to unsigned
        if quarter_hours < 0:
            quarter_hours = 256 + quarter_hours

        self._i2c.writeByte(self.address, self.kRegRAM, quarter_hours)
        return True

    def get_time_zone_quarter_hours(self):
        """!
        Gets the time zone in quarter hours

        @return **int** The time zone offset in 15 minute increments
        """
        unsigned = self._i2c.readByte(self.address, self.kRegRAM)
        return unsigned if unsigned < 128 else unsigned - 256

    def update_time(self):
        """!
        Updates the time by reading the time from the RTC and storing it in the time list.

        Move the hours, mins, sec, etc registers from RV-8803 into the _time array
        Needs to be called before printing time or date
        We do not protect the GPx registers. They will be overwritten. The user has plenty of RAM if they need it.
        """

        self._time = list(self._i2c.readBlock(self.address, self.kRegHundredths, self.kTimeListLength))
        # If hundredths are at 99 or seconds are at 59, read again to make sure we didn't accidentally skip a second/minute
        if self._time[self.kIdxHundredths] == 0x99 or self._time[self.kIdxSeconds] == 0x59:
            rollover_time = list(self._i2c.readBlock(self.address, self.kRegHundredths, self.kTimeListLength))
            # If the reading for hundredths has rolled over, then our new data is correct, otherwise, we can leave the old data.
            if self.bcd_to_dec(self._time[self.kIdxHundredths]) > self.bcd_to_dec(rollover_time[self.kIdxHundredths]):
                self._time = rollover_time
    
    def get_hundredths(self):
        """!
        Gets the byte value for hundredths

        @return **int** The hundredths
        """
        return self.bcd_to_dec(self._time[self.kIdxHundredths])

    def get_seconds(self):
        """!
        Gets the byte value for seconds

        @return **int** The seconds
        """
        return self.bcd_to_dec(self._time[self.kIdxSeconds])

    def get_minutes(self):
        """!
        Gets the byte value for minutes

        @return **int** The minutes
        """
        return self.bcd_to_dec(self._time[self.kIdxMinutes])

    def get_hours(self):
        """!
        Gets the byte value for hours, automatically converts to 12 hour mode if necessary

        @return **int** The hours
        """
        hours = self.bcd_to_dec(self._time[self.kIdxHours])
        if self.is_12_hour() and (hours > 12):
            hours -= 12
            
        return hours

    def get_date(self):
        """!
        Gets the byte value for date

        @return **int** The date
        """
        return self.bcd_to_dec(self._time[self.kIdxDate])

    def get_weekday(self):
        """!
        Gets the byte value for weekday. Compare against the day constants inherent to this class.

        @return **int** The weekday
        """
        return self.bcd_to_dec(self._time[self.kIdxWeekday])
        
        # TODO: The arduino lib converts the weekday read to 0-6, this isn't really necessary if user always compares against the day constants
        #       but if we want that functionality, we can add it with this:
        # weekday = self._time[self.kIdxWeekday]
        # for i in range (7):
        #     if weekday & (1 << i):
        #         return i

    def get_month(self):
        """!
        Gets the byte value for month

        @return **int** The month
        """
        return self.bcd_to_dec(self._time[self.kIdxMonth])

    def get_year(self):
        """!
        Gets the byte value for year. Automatically adds 2000 to the year.

        @return **int** The year
        """
        return self.bcd_to_dec(self._time[self.kIdxYear]) + 2000

    def get_epoch(self, use1970sEpoch=True):
        """!
        Get the epoch - with the time zone subtracted (i.e. return UTC epoch)

        @param bool use1970sEpoch: If `True`, the epoch is in the 1970s

        @return **int** The epoch time
        """
        local_epoch = self.get_local_epoch(use1970sEpoch)
        return local_epoch - (self.get_time_zone_quarter_hours() * 15 * 60)
        

    def get_local_epoch(self, use1970sEpoch=True):
        """!
        Get the local epoch - without subtracting the time zone

        @param bool use1970sEpoch: If `True`, the epoch is in the 1970s

        @return **int** The epoch time
        """

        tm = [0] * 8
        tm[self.kTmSecond] = self.bcd_to_dec(self._time[self.kIdxSeconds])
        tm[self.kTmMinute] = self.bcd_to_dec(self._time[self.kIdxMinutes])
        tm[self.kTmHour] = self.bcd_to_dec(self._time[self.kIdxHours])
        tm[self.kTmMDay] = self.bcd_to_dec(self._time[self.kIdxDate])
        tm[self.kTmMonth] = self.bcd_to_dec(self._time[self.kIdxMonth])
        tm[self.kTmYear] = self.bcd_to_dec(self._time[self.kIdxYear]) + 2000
        tm[self.kTmWDay] = 0
        tm[self.kTmYDay] = 0

        if self._hasIsDst:
            tm.append(-1) 

        t = time.mktime(tuple(tm))

        if not use1970sEpoch:
            t -= 946684800
        
        return t

    
    def get_hundredths_capture(self):
        """!
        Gets the byte value for hundredths capture

        @return **int** The hundredths capture
        """
        return self.bcd_to_dec(self._i2c.readByte(self.address, self.kRegHundredthsCapture))
    
    def get_seconds_capture(self):
        """!
        Gets the byte value for seconds capture

        @return **int** The seconds capture
        """
        return self.bcd_to_dec(self._i2c.readByte(self.address, self.kRegSecondsCapture))
    
    def set_calibration_offset(self, ppm):
        """!
        Sets the calibration offset in parts per million (ppm)

        Under the hood, the offset is a two's complement value with a range of -32 to + 31. See App-Manual page 22 for more information.

        @param float ppm: The calibration offset in parts per million
        """

        integerOffset = int(ppm / 0.238)
        
        if integerOffset < 0:
            integerOffset += 64

        self._i2c.writeByte(self.address, self.kRegOffset, integerOffset)

    def get_calibration_offset(self):
        """!
        Gets the calibration offset in parts per million

        @return **int** The calibration offset in parts per million
        """
        value = self._i2c.readByte(self.address, self.kRegOffset)
        if value > 32:
            value -= 64
        return value * 0.238

    def set_evi_debounce_time(self, debounce_time):
        """!
        Sets the EVI debounce time

        @param int debounce_time: The debounce time
        """
        self.write_two_bits(self.kRegEventControl, self.kEventEt, debounce_time)

    def set_evi_calibration(self, evi_calibration):
        """!
        Sets the EVI calibration

        @param bool evi_calibration: The EVI calibration
        """
        self.write_bit(self.kRegEventControl, self.kEventErst, evi_calibration)

    def set_evi_edge_detection(self, edge):
        """!
        Sets the EVI edge detection

        @param bool edge: The edge detection
        """
        self.write_bit(self.kRegEventControl, self.kEventEhl, edge)

    def set_evi_event_capture(self, capture):
        """!
        Sets the EVI event capture

        @param bool capture: The event capture
        """
        self.write_bit(self.kRegEventControl, self.kEventEcp, capture)

    def get_evi_debounce_time(self):
        """!
        Gets the EVI debounce time

        @return **int** The debounce time
        """
        return self.read_two_bits(self.kRegEventControl, self.kEventEt)

    def get_evi_calibration(self):
        """!
        Gets the EVI calibration

        @return **bool** The EVI calibration
        """
        return self.read_bit(self.kRegEventControl, self.kEventErst)

    def get_evi_edge_detection(self):
        """!
        Gets the EVI edge detection

        @return **bool** The edge detection
        """
        return self.read_bit(self.kRegEventControl, self.kEventEhl)

    def get_evi_event_capture(self):
        """!
        Gets the EVI event capture

        @return **bool** The event capture
        """
        return self.read_bit(self.kRegEventControl, self.kEventEcp)

    def set_countdown_timer_enable(self, timer_state):
        """!
        Sets the countdown timer enable

        @param bool timer_state: The timer state
        """
        self.write_bit(self.kRegExtension, self.kExtensionTe, timer_state)

    def set_countdown_timer_frequency(self, countdown_timer_frequency):
        """!
        Sets the countdown timer frequency

        @param int countdown_timer_frequency: The countdown timer frequency
        """
        self.write_two_bits(self.kRegExtension, self.kExtensionTd, countdown_timer_frequency)
    
    def set_countdown_timer_clock_ticks(self, clock_ticks):
        """!
        Sets the countdown timer clock ticks

        @param int clock_ticks: The clock ticks
        """
        # First handle the upper bit, as we need to preserve the GPX bits
        value = self._i2c.readByte(self.address, self.kRegTimer1)
        value &= ~(0b00001111)  # Clear the least significant nibble
        value |= (clock_ticks >> 8)
        self._i2c.writeByte(self.address, self.kRegTimer1, value)
        value = clock_ticks & 0x00FF
        self._i2c.writeByte(self.address, self.kRegTimer0, value)
    
    def get_countdown_timer_clock_ticks(self):
        """!
        Gets the countdown timer clock ticks

        @return **int** The countdown timer clock ticks
        """
        value = self._i2c.readByte(self.address, self.kRegTimer1) << 8
        value |= self._i2c.readByte(self.address, self.kRegTimer0)
        return value
    
    def set_clock_out_timer_frequency(self, clock_out_timer_frequency):
        """!
        Sets the clock out timer frequency

        @param int clock_out_timer_frequency: The clock out timer frequency
        """
        self.write_bit(self.kRegExtension, self.kExtensionFd, clock_out_timer_frequency)

    def get_countdown_timer_enable(self):
        """!
        Gets the countdown timer enable

        @return **bool** The countdown timer enable
        """
        return self.read_bit(self.kRegExtension, self.kExtensionTe)

    def get_countdown_timer_frequency(self):
        """!
        Gets the countdown timer frequency

        @return **int** The countdown timer frequency
        """
        return self.read_two_bits(self.kRegExtension, self.kExtensionTd)

    def get_clock_out_timer_frequency(self):
        """!
        Gets the clock out timer frequency

        @return **int** The clock out timer frequency
        """
        return self.read_two_bits(self.kRegExtension, self.kExtensionFd)

    def set_periodic_time_update_frequency(self, time_update_frequency):
        """!
        Sets the periodic time update frequency

        @param bool time_update_frequency: The time update frequency
        """
        self.write_bit(self.kRegExtension, self.kExtensionUsel, time_update_frequency)

    def get_periodic_time_update_frequency(self):
        """!
        Gets the periodic time update frequency

        @return **bool** The periodic time update frequency
        """
        return self.read_bit(self.kRegExtension, self.kExtensionUsel)

    def set_items_to_match_for_alarm(self, minuteAlarm, hourAlarm, weekdayAlarm, dateAlarm):
        """!
        Set Alarm Mode controls which parts of the time have to match for the alarm to trigger.
        When the RTC matches a given time, make an interrupt fire.
        Setting a bit to 1 means that the RTC does not check if that value matches to trigger the alarm.

        Alarm goes off with match of second, minute, hour, etc

        @param bool minuteAlarm: If `True`, the alarm will trigger on a match of the minutes
        @param bool hourAlarm: If `True`, the alarm will trigger on a match of the hours
        @param bool weekdayAlarm: If `True`, the alarm will trigger on a match of the weekday
        @param bool dateAlarm: If `True`, the alarm will trigger on a match of the date
        """
        self.write_bit(self.kRegMinutesAlarm, self.kAlarmEnable, not minuteAlarm)  # For some reason these bits are active low
        self.write_bit(self.kRegHoursAlarm, self.kAlarmEnable, not hourAlarm)
        self.write_bit(self.kRegWeekdaysDateAlarm, self.kAlarmEnable, not weekdayAlarm)
        self.write_bit(self.kRegExtension, self.kExtensionWada, dateAlarm)
        if dateAlarm:  # enabling both weekday and date alarm will default to a date alarm
            self.write_bit(self.kRegWeekdaysDateAlarm, self.kAlarmEnable, not dateAlarm)

    def set_alarm_minutes(self, minute):
        """!
        Sets the alarm minutes

        @param int minute: The minute value
        """
        value = self._i2c.readByte(self.address, self.kRegMinutesAlarm)
        value &= (1 << self.kAlarmEnable)  # clear everything but enable bit
        value |= self.dec_to_bcd(minute)
        self._i2c.writeByte(self.address, self.kRegMinutesAlarm, value)

    def set_alarm_hours(self, hour):
        """!
        Sets the alarm hours

        @param int hour: The hour value
        """
        value = self._i2c.readByte(self.address, self.kRegHoursAlarm)
        value &= (1 << self.kAlarmEnable)  # clear everything but enable bit
        value |= self.dec_to_bcd(hour)
        self._i2c.writeByte(self.address, self.kRegHoursAlarm, value)

    def set_alarm_weekday(self, weekday):
        """!
        Sets the alarm weekday

        @param int weekday: The weekday value
        """
        value = self._i2c.readByte(self.address, self.kRegWeekdaysDateAlarm)
        value &= (1 << self.kAlarmEnable)  # clear everything but enable bit
        value |= 0x7F & weekday
        self._i2c.writeByte(self.address, self.kRegWeekdaysDateAlarm, value)

    def set_alarm_date(self, date):
        """!
        Sets the alarm date

        @param int date: The date value
        """
        value = self._i2c.readByte(self.address, self.kRegWeekdaysDateAlarm)
        value &= (1 << self.kAlarmEnable)  # clear everything but enable bit
        value |= self.dec_to_bcd(date)
        self._i2c.writeByte(self.address, self.kRegWeekdaysDateAlarm, value)
    
    def enable_hardware_interrupt(self, source):
        """!
        Enables the hardware interrupt for the given source

        Given a bit location, enable the interrupt
        Allowable sources: 
            kUpdateInterrupt
            kTimerInterrupt
            kAlarmInterrupt
            kEviInterrupt
            kControlReset

        @param int source: The interrupt source
        """
        if source not in [self.kUpdateInterrupt, self.kTimerInterrupt, self.kAlarmInterrupt, self.kEviInterrupt, self.kControlReset]:
            return

        value = self._i2c.readByte(self.address, self.kRegControl)
        value |= (1 << source)  # Set the interrupt enable bit
        self._i2c.writeByte(self.address, self.kRegControl, value)

    def disable_hardware_interrupt(self, source):
        """!
        Disables the hardware interrupt for the given source
        Allowable sources: 
            kUpdateInterrupt
            kTimerInterrupt
            kAlarmInterrupt
            kEviInterrupt
            kControlReset

        @param int source: The interrupt source
        """
        if source not in [self.kUpdateInterrupt, self.kTimerInterrupt, self.kAlarmInterrupt, self.kEviInterrupt, self.kControlReset]:
            return
        value = self._i2c.readByte(self.address, self.kRegControl)
        value &= ~(1 << source)  # Clear the interrupt enable bit
        self._i2c.writeByte(self.address, self.kRegControl, value)

    def disable_all_interrupts(self):
        """!
        Disables all hardware interrupts
        """
        value = self._i2c.readByte(self.address, self.kRegControl)
        value &= 1  # Clear all bits except for Reset
        self._i2c.writeByte(self.address, self.kRegControl, value)

    def get_interrupt_flag(self, flag_to_get):
        """!
        Gets the interrupt flag for the given source

        @param int flag_to_get: The interrupt flag to get

        @return **bool** The value of the interrupt flag
        """
        flag = self._i2c.readByte(self.address, self.kRegFlag)
        flag &= (1 << flag_to_get)
        flag = flag >> flag_to_get
        return flag != 0

    def clear_all_interrupt_flags(self):
        """!
        Clears all interrupt flags
        """
        self._i2c.writeByte(self.address, self.kRegFlag, 0b00000000)  # Write all 0's to clear all flags

    def clear_interrupt_flag(self, flag_to_clear):
        """!
        Clears the interrupt flag for the given source

        @param int flag_to_clear: The interrupt flag to clear
        """
        value = self._i2c.readByte(self.address, self.kRegFlag)
        value &= ~(1 << flag_to_clear)  # Clear flag
        self._i2c.writeByte(self.address, self.kRegFlag, value)

    def get_alarm_minutes(self):
        """!
        Gets the alarm minutes

        @return **int** The alarm minutes
        """
        return self.bcd_to_dec(self._i2c.readByte(self.address, self.kRegMinutesAlarm))

    def get_alarm_hours(self):
        """!
        Gets the alarm hours

        @return **int** The alarm hours
        """
        return self.bcd_to_dec(self._i2c.readByte(self.address, self.kRegHoursAlarm))

    def get_alarm_weekday(self):
        """!
        Gets the alarm weekday

        @return **int** The alarm weekday
        """
        return self.bcd_to_dec(self._i2c.readByte(self.address, self.kRegWeekdaysDateAlarm))

    def get_alarm_date(self):
        """!
        Gets the alarm date

        @return **int** The alarm date
        """
        return self.bcd_to_dec(self._i2c.readByte(self.address, self.kRegWeekdaysDateAlarm))


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

        @param int reg: The register to write to
        @param int bit: The bit to write
        @param bool val: The value to write
        """
        data = self._i2c.readByte(self.address, reg)

        data &= ~(1 << bit)
        
        if val:
            data |= (1 << bit)

        self._i2c.writeByte(self.address, reg, data)
    
    def write_two_bits(self, reg, bit, val):
        """!
        Writes two bits to a register

        @param int reg: The register to write to
        @param int bit: The bit to write
        @param int val: The value to write
        """
        data = self._i2c.readByte(self.address, reg)

        data &= ~(3 << bit)
        data |= (val << bit)

        self._i2c.writeByte(self.address, reg, data)
    
    def read_bit(self, reg, bit):
        """!
        Reads a bit from a register

        @param int reg: The register to read from
        @param int bit: The bit to read

        @return **bool** The value of the bit
        """
        data = self._i2c.readByte(self.address, reg)
        return (data & (1 << bit)) != 0

    def read_two_bits(self, reg, bit):
        """!
        Reads two bits from a register

        @param int reg: The register to read from
        @param int bit: The bit to read

        @return **int** The value of the bits
        """
        data = self._i2c.readByte(self.address, reg)
        return (data & (3 << bit)) >> bit
    