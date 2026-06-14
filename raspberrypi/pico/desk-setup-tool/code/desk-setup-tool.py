from gpiopico import NextionDisplay, RGB

display = NextionDisplay(uart_number=0, tx=16, rx=17)
rgb = RGB(pin_red=18, pin_blue=19, pin_green=20, inverted_logic=True)

class App:
    def __init__(self)->None:
        pass
    def defineAction(self, buffer):
        print(buffer)
        if isinstance(buffer, bytes):
            color = buffer.decode('UTF-8')
            rgb.define_color(color_hex=color)

if __name__=='__main__':
    app = App()
    while True:
        buffer = display.read()
        if buffer:
            app.defineAction(buffer)    

