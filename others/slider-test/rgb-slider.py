from time import sleep
import board
import digitalio
import busio
import pwmio
import math 

serial=busio.UART(board.GP4, board.GP5, baudrate=9600)#UART1 tx - rx
global page
page: int = 0
global component
component: int = 0
rgb_led = {
    '7': pwmio.PWMOut(board.GP21, frequency=5000, duty_cycle=0),
    '6': pwmio.PWMOut(board.GP20, frequency=5000, duty_cycle=0),
    '5': pwmio.PWMOut(board.GP19, frequency=5000, duty_cycle=0),
}

class RGB:

    def _write_pwm_value(self, serial_value) -> None:
        print(serial_value[6:8])
        """pwm_value = 255 - int(serial_value[6:8], 16)
        print(pwm_value)
        pwm_value = (pwm_value / 255) * 65536
        pwm_value = 1 if pwm_value == 0 else math.ceil(pwm_value) - 1
        print(pwm_value)
        rgb_led[f'{component}'].duty_cycle = pwm_value"""
    
    def update_color(self, serial_value: str) -> None:
        print('cambiando color')
        self._write_pwm_value(serial_value)
        

def define_action(serial_value:bytes, pg, cm):
    temp = str(serial_value)
    print(temp)
    print(pg)
    if not('xff' in temp) and pg == 2:
        RGB().update_color(temp)
        return 2, cm
    page = serial_value[1]
    component = serial_value[2]
    return page, component

if __name__=='__main__':
    while True:
        serial_value = serial.read(8)
        if serial_value != None:
            page, component = define_action(serial_value, page, component)

