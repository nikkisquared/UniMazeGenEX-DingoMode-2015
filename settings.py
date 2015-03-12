#!/usr/bin/python

# settings for runme.py
# CURRENTLY VERSION 0.7.0!

import pygame
from pygame.locals import *


# TODO: (! means finished- keep track of controls, ~ means SORTA working)

#~ hold down keys (ie (W)ildcard)
    # ARROW KEYS can't be held down??? what's wrong with resize?

#! R to reset all values to default
#! ESC to quit

#! `1234567890 to toggle chars
#! ~!@#$%^&*() keys to select one of above's corresponding chars
#! others to toggle: TAB, SPACE, ENTER
#! B to change character set
#  ? to select all characters
#! BACKSPACE to display nothing

#! - and + to decrease and increase the rate of automatic change, using a scaling system
#! P to pause/continue
#! A to turn on/off automatic refresh mode

#! ARROW KEYS increase / decrease windows' X/Y axises
#! F for full screen
    # AGAIN, RESIZE function is awful here!

#! C to toggle colour mode
#! G to instantly generate a new layout
#! S to save the screen to an image

#! W (Wildcard) to select a mostly random action

#  ? for help/controls (?)
#  ? for freezing colour changes

# add more colour modes
# interpret keypad ? (need to change pygcurse interpret key event)
# why is resize() so annoying

# BIG THINGS:
# M to select these new modes
# U to undo the last selection (!)
# totally wild tile mode- EVERY square is randomly changed
# continuous update mode- change each square randomly, constantly

# BIG WORLD version, where you can scroll around a giant random layout!
# implement an introductory / explanatory menu ?
# [?] key to go back to menu / resume
# seperate window for information output ?


# maximum width allowed
MAXWIDTH = 150
# maximum height allowed
MAXHEIGHT = 75


# dict of preset colour modes, ordered by range of colours
# each position of three refers to the RGB values to be used
# fg-min, fg-max, bg-min, bg-max - fg is 'text', bg is 'fill'
COLOURMODES = {
    #'template': ( (100, 100, 100), (255, 255, 255), (255, 255, 255), (100, 100, 100) )
    'default': ( (128,) * 3, (255,) * 3, (0,) * 3, (127,) * 3 ),

    'bright red': ( (50, 20, 20), (127, 30, 30), (200, 30, 30), (240, 45, 45) ),
    'bright green': ( (20, 50, 20), (30, 127, 30), (30, 200, 30), (45, 240, 45) ),
    'bright blue': ( (20, 20, 50), (30, 30, 127), (30, 30, 200), (45, 45, 240) ),

    'opal': ( (205,) * 3, (225,) * 3, (135,) * 3, (155,) * 3 ),
    'murky': ( (0,) * 3, (30,) * 3, (15,) * 3, (45,) * 3 )
}

# ordered list for colour modes to go through
COLOURMODENAMES = ['default', 'bright red', 'bright green', 'bright blue', 'opal', 'murky']

# list of speed settings to use
SPEED_VALUES = [x / 10.0 for x in range(1, 6)] + [x / 100.0 for x in range(75, 200, 25)] + \
                [x / 100.0 for x in range(200, 500, 50)] + [x for x in range(5, 10)] + \
                [x for x in range(10, 70, 10)]


# various single keys are below

# keys that can be randomly hit
GENERATE = 'G'
COLOURMODE_TOGGLE = 'C'
CHANGE_CHAR_SET = 'B'

# keys that must be manually used
PAUSE = 'P'
WILDCARD = 'W'
FULLSCREEN = 'F'
AUTOREFRESH = 'A'
CLEAR_CHARS = K_BACKSPACE
# NEEDS to be K_r because it is checked seperately from other keys
RESET_SETTINGS = K_r

# keys with a special extra thing
SCREENSHOT = 'S'
SCREENSHOT_FILETYPE = '.PNG'
SCREENSHOT_LOCATION = 'screenshots'


# keys for increasing/decreasing the width/height of the program window
RESIZE_KEYS = [K_LEFT, K_RIGHT, K_UP, K_DOWN]

# keys for controlling the rate of automatic refreshing
TIME_KEYS = ['+', '-']


# dict of keys, and their shifted states, for single character selections
SINGLECHARS = {
    '~': '`', '!': '1', '@': '2', '#': '3', '$': '4', '%': '5',
    '^': '6', '&': '7', '*': '8', '(': '9', ')': '0'
}


# dicts of chars to use, referenced by the key that toggles them

# two spaced apart pipe-like lines
DOUBLEPIPES = {
        # four-way connector
        '`': u"\u256C",
        # corner pieces: top-left, top-right, bottom-left, bottom-right
        '1': u"\u2554", '2': u"\u2557", '3': u"\u255A", '4': u"\u255D",
        # t-sections: no top, no right, no bottom, no left
        '5': u"\u2566", '6': u"\u2563", '7': u"\u2569", '8': u"\u2560",
        # two-way connectors: top-bottom, left-right; four-way connector
        '9': u"\u2550", '0': u"\u2551"
}

# single pipe-like lines
SINGLEPIPES = {
        # four-way connector
        '`': u"\u253C",
        # corner pieces: top-left, top-right, bottom-left, bottom-right
        '1': u"\u250C", '2': u"\u2510", '3': u"\u2514", '4': u"\u2518",
        # t-sections: no top, no right, no bottom, no left
        '5': u"\u252C", '6': u"\u2524", '7': u"\u2534", '8': u"\u251C",
        # two-way connectors: top-bottom, left-right; four-way connector
        '9': u"\u2502", '0': u"\u2500"
}

# playing card suits
CARDSUITS = {
        # black filled: heart, diamond, club, spades
        '`': u"\u2665", '1': u"\u2666", '2': u"\u2663", '3': u"\u2660",
        # white filled: heart, diamond, club, spades - WON'T DISPLAY :(
        #'4': u"\u2661",'5': u"\u2662", '6': u"\u2667", '7': u"\u2664",
        # nothing... yet
        #'8': u"\u", '9': u"\u", '0': u"\u"
}

# just some numbers
NUMBERS = {
    '`': u"`", '1': u"1", '2': u"2", '3': u"3",
    '4': u"4", '5': u"5", '6': u"6", '7': u"7", 
    '8': u"8", '9': u"9", '0': u"0"
}

# shift row of numbers
SHIFT_ROW = {
    '`': u"~", '1': u"!", '2': u"@", '3': u"#",
    '4': u"$", '5': u"%", '6': u"^", '7': u"&", 
    '8': u"*", '9': u"(", '0': u")"
}

# curved corners and some diagonal lines... don't seem to work???
CURVES_DIAGONALS = {
    # curved corners: top-left, top-right, bottom-left, bottom-right
    '`': u"\u256D", '1': u"\u256E", '2': u"\u256F", '3': u"\u2570",
    # diagonals: bottom-left to upper-right, upper-left to bottom-right
    '4': u"\u2571", '5': u"\u2572",
    # four way diagonal
    '6': u"\u2573",
    # nothing... yet
    #'7': u"\u", '8': u"\u", '9': u"\u", '0': u"\u"
}

# the space, newline, and tab characters are always included
EXTRACHARS = {' ': " ", '\t': " " * 4, '\r': " " * 8}

CHAR_SETS = [DOUBLEPIPES, SINGLEPIPES, CARDSUITS, 
            NUMBERS, SHIFT_ROW]


# refers to all keys that would be interesting to be randomly pressed
WILD_KEYS = SINGLECHARS.values() + TIME_KEYS #+ RESIZE_KEYS
WILD_KEYS += [GENERATE, COLOURMODE_TOGGLE, CHANGE_CHAR_SET, ' ']


# stores the default settings
DEFAULT_SETTINGS = {

    # program window height / x size
    'width': 80,
    # program window width / y size
    'height': 25,
    # window caption
    'caption': "UNIDISPLAYEX 2015 - a Nikki production",
    # fullscreen status
    'fullscreen': False,

    # displayed font type
    'font': 'courier',
    # displayed font size
    'fontSize': 15,

    # how long, in seconds, until generating a new screen
    'speed': 4,
    # if the screen should automatically refresh
    'autoRefresh': True,
    # if the screen should never refresh
    'pause': False,

    # chosen arrangement of colours
    'colourMode': COLOURMODENAMES[0],

    # current char set to be used
    'charSet': CHAR_SETS[0],
    # list of chars to display to the screen
    'charsToUse': CHAR_SETS[0].values()
}