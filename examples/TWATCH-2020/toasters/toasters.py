'''
toasters.py

    An example using bitmap to draw sprites on the
    M5Stack Core Display.

    youtube video: https://youtu.be/0uWsjKQmCpU

    spritesheet from CircuitPython_Flying_Toasters
    https://learn.adafruit.com/circuitpython-sprite-animation-pendant-mario-clouds-flying-toasters
'''

import time
import random
from machine import Pin, SPI
import axp202c
import st7789
import t1,t2,t3,t4,t5

TOASTERS = [t1, t2, t3, t4]
TOAST = [t5]


class toast():
    '''
    toast class to keep track of a sprites locaton and step
    '''
    def __init__(self, sprites, x, y):
        self.sprites = sprites
        self.steps = len(sprites)
        self.x = x
        self.y = y
        self.step = random.randint(0, self.steps-1)
        self.speed = random.randint(2, 5)

    def move(self):
        if self.x <= 0:
            self.speed = random.randint(2, 5)
            self.x = 320-64

        self.step += 1
        self.step %= self.steps
        self.x -= self.speed


def main():
    '''
    Draw and move sprite
    '''
    try:
        # Turn power on display power
        axp = axp202c.PMU()
        axp.enablePower(axp202c.AXP202_LDO2)

        # initialize spi port
        spi = SPI(
            2,
            baudrate=32000000,
            sck=Pin(18, Pin.OUT),
            mosi=Pin(19, Pin.OUT))

        # configure display
        tft = st7789.ST7789(
            spi,
            240,
            240,
            cs=Pin(5, Pin.OUT),
            dc=Pin(27, Pin.OUT),
            backlight=Pin(12, Pin.OUT),
            rotation=2)

        # enable display and clear screen
        tft.init()
        tft.fill(st7789.BLACK)

        # create toast spites in random positions
        sprites = [
            toast(TOASTERS, 320-64, 0),
            toast(TOAST, 320-64*2, 80),
            toast(TOASTERS, 320-64*4, 160)
        ]

        # move and draw sprites
        while True:
            for man in sprites:
                bitmap = man.sprites[man.step]
                tft.fill_rect(
                    man.x+bitmap.WIDTH-man.speed,
                    man.y,
                    man.speed,
                    bitmap.HEIGHT,
                    st7789.BLACK)

                man.move()

                if man.x > 0:
                    tft.bitmap(bitmap, man.x, man.y)
                else:
                    tft.fill_rect(
                        0,
                        man.y,
                        bitmap.WIDTH,
                        bitmap.HEIGHT,
                        st7789.BLACK)

            time.sleep(0.05)

    finally:
        # shutdown spi
        spi.deinit()


main()
