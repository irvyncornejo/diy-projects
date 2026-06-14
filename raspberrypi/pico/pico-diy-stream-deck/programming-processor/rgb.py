import time
import board
import pwmio

rgb = {
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
            rgb[led].duty_cycle = color[led]
    
    def turn_on(self, color) -> None:
        self.off_rgb() 
        if type(color) == str:
            led = rgb[color]
            for i in range(100):
                if i < 50:
                    led.duty_cycle = int(i * 2 * 65535 / 100)
                else:
                    led.duty_cycle = 65535 - int((i - 50) * 2 * 65535 / 100)
                time.sleep(0.05)
        else:
            self.select_color(color)
    
    def blink_rgb(self, color=None) -> None:
        for i in range(100):
            if i < 50:
                rgb['blue'].duty_cycle = int(i * 2 * 65535 / 100)
                rgb['green'].duty_cycle = int(i * 2 * 65535 / 100)
                rgb['red'].duty_cycle = int(i * 2 * 65535 / 100)
            else:
                rgb['blue'].duty_cycle = 65535 - int((i - 50) * 2 * 65535 / 100)
                rgb['green'].duty_cycle = 65535 - int((i - 50) * 2 * 65535 / 100)
                rgb['red'].duty_cycle = 65535 - int((i - 50) * 2 * 65535 / 100)
            time.sleep(0.01)
            
    def off_rgb(self) -> None:
        rgb['blue'].duty_cycle = self.off_value
        rgb['green'].duty_cycle = self.off_value
        rgb['red'].duty_cycle = self.off_value
    
    