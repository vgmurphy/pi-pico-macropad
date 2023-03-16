from pmk import PMK
# from pmk.platform.keybow2040 import Keybow2040 as Hardware          # for Keybow 2040
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware  # for Pico RGB Keypad Base

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

import time

# Set up Keybow
hardware = Hardware()
pmk = PMK(hardware)
keys = pmk.keys
kbd = Keyboard(usb_hid.devices)

time_interval = 0.25
time_last_fired = time.monotonic()
time_elapsed = 0

key = keys[0]

#Configure layers
modifier = keys[15]
action1 = keys[3]
action2 = keys[2]
action3 = keys[1]
action4 = keys[0]

layer = 0
ignore = 0

#Set layer by holding modifier button

################
#Layer LED Setup
################

#layer 0 is default, indicated by dim red modifier
def layer0():
    pmk.set_led(15, 25, 0, 0)
    for i in range(0, 14):
        pmk.set_led(i, 0, 0, 0)
        
#layer 1 is 8x8 key combinations for work. Indicated by cyan modifier
def layer1():
    pmk.set_led(15, 0, 110, 110) #modifier
    pmk.set_led(14, 110, 110, 110) #highlight to call button
    pmk.set_led(13, 0, 110, 0) #answer
    pmk.set_led(12, 110, 0, 0) #decline
    
    #dialpad
    # *
    pmk.set_led(0, 50, 0, 70)
    # #
    pmk.set_led(8, 50, 0, 70)
    #numeric buttons
    for i in range(1, 8):
        pmk.set_led(i, 0, 0, 70)
    for i in range(9, 12):
        pmk.set_led(i, 0, 0, 70)

#layer 2 is media playback controls. Indicated by green modifier
def layer2():
    pmk.set_led(15, 0, 128, 0) #modifier
    
    pmk.set_led(0, 0, 0, 128) #next
    pmk.set_led(1, 128, 0, 0) #stop
    pmk.set_led(2, 0, 128, 0) #Play/Pause
    pmk.set_led(3, 128, 0, 128) #previous
    
    for i in range(5, 15): #unused
        clear_keys(i)

#layer 3 is macro buttons [F13-F24], for use with AutoHotkey and stuff. Indicated by purple modifier
def layer3():
    pmk.set_led(15, 128, 0, 128) #modifier
    
    for i in range(0, 12): #functions
        pmk.set_led(i, 30, 0, 128)
        
    for i in range(13, 15): #unused
        clear_keys(i)

#layer shows available layer options
def modifier_layer():
    pmk.set_led(15, 255, 255, 0) #modifier
    pmk.set_led(0, 255, 0, 255) #function
    pmk.set_led(1, 0, 255, 0) #media
    pmk.set_led(2, 0, 255, 255) #8x8
    pmk.set_led(3, 255, 0, 0) #dark mode
    
    for i in range(4, 15): #unused
        clear_keys(i)

#blank unnecessary keys
def clear_keys(k):
    pmk.set_led(k, 0, 0, 0)
    
#layer handler decision matrix
def layer_tree(l):
    if l == 0:
        layer0()
    elif l == 1:
        layer1()
    elif l == 2:
        layer2()
    elif l == 3:
        layer3()
    
        
#################################################        
#Layer Functions, set code to None if not defined
#################################################
        
#layer 1
layer1_btn = [Keycode.KEYPAD_ASTERISK, Keycode.KEYPAD_SEVEN, Keycode.KEYPAD_FOUR, Keycode.KEYPAD_ONE,
              Keycode.KEYPAD_ZERO, Keycode.KEYPAD_EIGHT, Keycode.KEYPAD_FIVE, Keycode.KEYPAD_TWO,
              None, Keycode.KEYPAD_NINE, Keycode.KEYPAD_SIX, Keycode.KEYPAD_THREE,
              None, None, None, None]
        
#layer 2
layer2_btn = [ConsumerControlCode.SCAN_NEXT_TRACK, ConsumerControlCode.STOP, ConsumerControlCode.PLAY_PAUSE, ConsumerControlCode.SCAN_PREVIOUS_TRACK,
              None, None, None, None,
              None, None, None, None,
              None, None, None, None]

#layer 3
layer3_btn = [Keycode.F22, Keycode.F19, Keycode.F16, Keycode.F13,
              Keycode.F23, Keycode.F20, Keycode.F17, Keycode.F14,
              Keycode.F24, Keycode.F21, Keycode.F18, Keycode.F15,
              None, None, None, None]

####################################
#start default layer from power loss
layer0()

while True:
    # Always remember to call keybow.update() on every iteration of your loop!
    pmk.update()
    
    for key in keys:
        if key.pressed:
            time_elapsed = time.monotonic() - time_last_fired
            if time_elapsed > time_interval:
                time_last_fired = time.monotonic()
                time_elapsed = 0

                #begin layer decision tree
                #modifier key
                if modifier.held:
                    modifier_layer()
                    ignore = 1 #set to ignore other functions when a layer is held
                    
                elif pmk.on_release(modifier): #return to layer
                    layer_tree(layer)
                    ignore = 0
                    
                #layer selection menu
                if modifier.held and action1.pressed:
                    layer = 0
                    layer0()
                elif modifier.held and action2.pressed:
                    layer = 1
                    layer1()
                elif modifier.held and action3.pressed:
                    layer = 2
                    layer2()
                elif modifier.held and action4.pressed:
                    layer = 3
                    layer3()
                        
                #Use ignore variable to determine if it is safe to handle inputs
                if ignore == 0:
                    #functions for layers
                    if key != modifier:
                        if layer == 1:
                            keycode = layer1_btn[key.number]
                            if keycode != None:
                                kbd.send(keycode)
                            #custom 8x8 shortcuts
                            elif key.number == 8:
                                kbd.send(Keycode.SHIFT, Keycode.THREE)
                            elif key.number == 12:
                                kbd.send(Keycode.CONTROL, Keycode.LEFT_SHIFT, Keycode.H) #hangup
                            elif key.number == 13:
                                kbd.send(Keycode.CONTROL, Keycode.LEFT_SHIFT, Keycode.A) #answer
                            elif key.number == 14:
                                kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.EIGHT) #highlight to dial/open dialpad
                                #kbd.send(Keycode.BACKSPACE)
                        elif layer == 2:
                            keycode = layer2_btn[key.number]
                            if keycode != None:
                                kbd.send(keycode)
                        elif layer == 3:
                            keycode = layer3_btn[key.number]
                            if keycode != None:
                                kbd.send(keycode)
                        kbd.release_all()