# pi-pico-macropad
A Macropad concept created with a Raspberry Pi Pico and a Pimoroni Pico RGB Keypad

What you need:
- Raspberry Pi Pico
- Pimoroni Pico RGB Keypad

Could also be done with the Keybow 2040 if you want mechanical keys and easier setup, albeit at a higher pice tag


Dependencies:
- CircuitPython

Stuff in the lib folder:
- adafruit_hid (folder)
- pmk (folder)
- adafruit_dotstar

adafruit_hid has the following:
- consumer_control.mpy
- consumer_control_code.mpy
- keyboard.mpy
- keyboard_layout_base.mpy
- keyboard_layout_us.mpy
- keycode.mpy
- mouse.mpy

Libraries go in the lib folder

code.py goes in the root directory of Circuitpython.


How to use:
The keypad has multiple layers to it. In the default mode, the mode shift modifier key will be a dim red color.

Press and hold the modifier key to choose a mode, it will turn gold to indicate this. You will need to hold it while you select a mode, otherwise it will revert back to the selected mode once you press any key.

The modes are as follows:
- [Red] Idle (only modifier key is active)
- [Cyan] 8x8 Phone Dial pad
- [Green] Media transport keys (implemented, but the keycodes do not appear to work)
- [Violet] Macros (F13-F24)

In any mode, the modifier key will always be in the top right.

In 8x8 mode, the blue keys are the numpad. Top Left is 1, bottom right is 9.
On the bottom row, the keys are *, 0, #.
The right column has Hang Up [Red], Answer Call [Green], Highlight text to dial [White]

In Media Transport Control mode, the column is as follows:
- [Violet] Next
- [Green] Play/Pause
- [Red] Stop
- [Blue] Previous
