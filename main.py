import time
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import usb_hid

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

for x in range(0, 5):
    led.value = False
    time.sleep(0.2)
    led.value = True
    time.sleep(0.2)

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

PINS = ["D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7"]
keys = {}

for pin in PINS:
    key = DigitalInOut(getattr(board, pin))
    key.direction = Direction.INPUT
    key.pull = Pull.UP
    keys[pin] = key

""" 
    EDIT THE LIST BELOW 

    The below list is arranged in the same way Suspad is arranged.
    Here are the things you can set - 
    1. A Keycode: (This will simply send that keycode)
        eg Keycode.F18
    2. A List of Keycodes: (This will send the below keycodes in quick succession)
        eg [Keycode.LALT, Keycode.TAB]
    3. A String: (This will trigger GUI (WIN / CMD depending on OS) + SPACE, write the string, and then hit enter)
        eg "chrome"

    Example keymap - 

    key_map = [
        Keycode.F12, "brave", Keycode.F14, Keycode.F15,
        Keycode.F16, [Keycode.LALT, Keycode.TAB], Keycode.F18, "discord",
    ]
"""
key_map = [
    Keycode.F12, Keycode.F13, Keycode.F14, Keycode.F15,
    Keycode.F16, Keycode.F17, Keycode.F18, Keycode.F19,
]


def open_app(app):
    # Will work for both Windows and Mac, however you will need "PowerToys Run" on Windows
    kbd.send(Keycode.GUI, Keycode.SPACE)
    time.sleep(0.2)
    layout.write(app)
    time.sleep(0.2)
    kbd.send(Keycode.ENTER)


while True:
    for idx, pin in enumerate(PINS):
        if not keys[pin].value:
            led.value = False  # led on

            input = key_map[idx]
            if isinstance(input, list):
                kbd.send(*input)
            elif isinstance(input, str):
                open_app(input)
            else:
                kbd.send(input)

            time.sleep(0.2)
            led.value = True  # led off
