'''
Desktop conductor firmware V1
Coded in CircuitPython 
made extremely barebones commands and keybinds
Each key only prints out 1,2,3,4. and the OLED only displays "Example"
Future changes will include media control keybinds and 
more in depth use of the OLED to display information concerning volume or song details.
'''

#import libraries
import board
import digitalio
import time
import busio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_ssd1306 import SSD1306_I2C

#setup simple oled example
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 32, i2c)
oled.fill(0)
oled.text("example", 0, 12, 1)
oled.show()

#keypins which are on the schematic
key_pins = [
    board.D10, #sw1
    board.D9,  #sw2
    board.D8,  #sw3
    board.D2, #rotary encoder pressed
]

keys = []
for pin in key_pins:
    k = digitalio.DigitalInOut(pin)
    k.direction = digitalio.Direction.INPUT
    k.pull = digitalio.PULL.UP #Pull up resistor
    keys.append(k)

kbd = Keyboard(usb_hid.devices)

#make keybinds/values for each key to be associated to.
key_map = {
    0: Keycode.ONE,
    1: Keycode.TWO,
    2: Keycode.THREE,
    3: Keycode.FOUR,
}
#temporary key assignments simplified before deciding real key functions on dedicated board

last_states = [True] * 4
debounce_time = 0.05 


#check for presses and releases etc.
while True:
    for i, key in enumerate(keys):
        current = key.value

        if not current and last_states[i]:
            kbd.press(key_map[i])
        elif current and not last_states[i]:
            kbd.release(key_map[i])
        last_states[i] = current
    time.sleep(debounce_time)
