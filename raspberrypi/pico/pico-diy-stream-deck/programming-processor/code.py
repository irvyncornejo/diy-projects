"""
Description: DIY Stream Deck
Board: Raspberry Pi Pico with rp2040
Display: NX3224T024 yellow = Rx | Blue = Tx
"""
from time import sleep
import board
import pwmio
import digitalio
import busio
import rotaryio
import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

#Objects
keyboard=Keyboard(usb_hid.devices)
consumer_control=ConsumerControl(usb_hid.devices)
serial=busio.UART(board.GP4, board.GP5, baudrate=9600)#UART1 tx - rx

max_values_led = 65535
steps = 20
step = max_values_led // steps 

colors = {
    '5': {
        'color': 'red',
        'value': 65535
    },
    '6': {
        'color':'green',
        'value': 65535
    },
    '7': {
        'color':'blue',
        'value': 65535
    }
}

rgb_led = {
    'blue': pwmio.PWMOut(board.GP21, frequency=5000, duty_cycle=0),
    'green': pwmio.PWMOut(board.GP20, frequency=5000, duty_cycle=0),
    'red': pwmio.PWMOut(board.GP19, frequency=5000, duty_cycle=0),
}

class RGB:
    
    def __init__(self):
        self.off_value = 65535
    
    @staticmethod
    def select_color(color):
        for led in color.keys():
            rgb_led[led].duty_cycle = color[led]
            
    def change_color(self, color:str, step:int) -> None:
        led = rgb_led[color]
        led.duty_cycle = int(step)
            
    def off_rgb(self) -> None:
        rgb_led['blue'].duty_cycle = self.off_value
        rgb_led['green'].duty_cycle = self.off_value
        rgb_led['red'].duty_cycle = self.off_value
    

def get_operating_system(page: int ,component: int) -> str:
    pass

def define_action(page: int, component: int) -> None:
    if page==0 and component==1:
        consumer_control.send(ConsumerControlCode.VOLUME_INCREMENT)
    if page==0 and component==2:
        consumer_control.send(ConsumerControlCode.VOLUME_DECREMENT)
    if page==0 and component==3:
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.G)
    if page==0 and component==4:
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.Y)
    if page==0 and component==6:
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.S)
    if page==1 and component==2:
        keyboard.send(Keycode.WINDOWS, Keycode.E)
    if page==1 and component==4:
        keyboard.send(Keycode.WINDOWS, Keycode.I)
    if page==0 and component==6:
        keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.A)
    if page==2:
        update_value = lambda component, value : colors[component].update({'value': value})
        component = str(component)
        color = colors[component]['color']
        value_color = colors[component]['value'] - step
        if value_color > 0:
            update_value(component, value_color)
            rgb.change_color(color, value_color)
        else:
            update_value(component, max_values_led)
            rgb.change_color(color, max_values_led)
    

if __name__ == '__main__':
    rgb = RGB()
    rgb.off_rgb()
    
    while True:
        try:
            data=serial.read(7)#number of bytes b'e\x00\x02\x01\xff\xff\xff'
            if len(data) == 7:
                print(data)
                define_action(data[1], data[2])
        except Exception as e:
            #print(f'error --> {e}')
            pass