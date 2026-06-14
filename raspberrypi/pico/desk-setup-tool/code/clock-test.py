from umachine import I2C, Pin
from utime import sleep
from urtc import DS1307

class ClockDS1307:
    def __init__(
        self,
        i2c_number:int,
        pin_scl:int,
        pin_sda:int,
        freq=400000,
        auto_config:bool=False
    )->None:
        self._i2c = I2C(i2c_number, scl=Pin(pin_scl), sda=Pin(pin_sda), freq=freq)
        try:
            self._rtc = DS1307(self._i2c)
            self._now = self._config(auto_config)
            self._rtc.datetime(self._now)
        except (ValueError, ImportError) as e:
            print(e)
        
    def _config(self, auto_config:bool)->tuple:
        year = int(input("Year : "))
        month = int(input("month (Jan --> 1 , Dec --> 12): "))
        date = int(input("date : "))
        day = int(input("day (1 --> monday , 2 --> Tuesday ... 0 --> Sunday): "))
        hour = int(input("hour (24 Hour format): "))
        minute = int(input("minute : "))
        second = int(input("second : "))
        return (year, month, date, day, hour, minute,second, 0)
    
    def read_datetime(self, format_return:str='tuple')->tuple:
        if format_return != 'tuple':
            (year,month,date,day,hour,minute,second,p1) = self._rtc.datetime()
            try:
                formats = {
                    'str': f'{year}-{month}-{date}|{hour}:{minute}:{second}',
                    'mapping': {
                        'year': year,
                        'month': month,
                        'date': date,
                        'day': day,
                        'hour': hour,
                        'minute': minute,
                        'second': second
                    }
                }
                return formats[format_return]
            except KeyError:
                return self._rtc.datetime()
        return self._rtc.datetime()

clock = ClockDS1307(0,1,0)

while True:
    sleep(1)
    print(clock.read_datetime('mapping'))


