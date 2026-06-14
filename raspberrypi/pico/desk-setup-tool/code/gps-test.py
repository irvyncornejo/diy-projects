from umachine import Pin, UART

from time import sleep, time

class GPSModule:
    def __init__(self, tx:int, rx:int):
        self._module = UART(1, baudrate=9600, tx=Pin(tx), rx=Pin(rx))
        ##self._module.init(bits=8, parity=None, stop=1)
        print(self._module)
        
    def read(self):
        ##buff = bytearray(255)
        buff = self._module.read()
        if buff:       
            print(buff)
    


if __name__=='__main__':
    gps_module = GPSModule(4, 5)
    
    while True:
        gps_module.read()

