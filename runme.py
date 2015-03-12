#!/usr/bin/python

# a program that generates and displays random series of unicode pipe characters
# with many options provided for the user to change how they see everything!

# un-comment for compiling [currently broken!]
#import pygame._view
import pygame
pygame.font.init()
from pygame.locals import *

# local pygcurse file
import pygcurse
# local settings file
from settings import *
# python libraries needed
import random, time, sys, copy, os

window = pygcurse.PygcurseWindow()
# disables autoupdate to prevent flickering
window.autoupdate = False

FPS = 30
# clock for limiting program speed
CLOCK = pygame.time.Clock()
pygame.key.set_repeat(200, 50)


def quit():
    # ends the program completely
    pygame.quit()
    sys.exit()


def copy_default_settings():
    # creates a copy of the default settings dict

    settings = {}
    for key, value in DEFAULT_SETTINGS.items():
        settings[key] = copy.deepcopy(value)
    return settings


def set_window_properties(settings):
    # changes the window size to any given values

    global window

    # sets the window size
    window.resize(settings['width'], settings['height'])
    # sets up the fonts
    window.font = pygame.font.SysFont(settings['font'], settings['fontSize'])
    # sets the caption
    pygame.display.set_caption(settings['caption'])


def set_colors(colourInfo):
    # sets the colours for the window

    fg = ()
    bg = ()

    # fg layer, bg layer
    for layer in [0, 2]:
        # R, G, and B channels
        for channel in range(len(colourInfo[layer])):

            minRoll = colourInfo[layer][channel]
            maxRoll = colourInfo[layer + 1][channel]

            roll = random.randint(minRoll, maxRoll)

            if layer == 0: fg += (roll,)
            else: bg += (roll,)

    window.setscreencolors(fg, bg)


def generate(chars, width, height):
    # generates the output of random characters from the list

    # output generated, forced to use a unicode string
    output = u''
    # adds data line by line, to avoid displaying too many chars
    newLine = u''
    numWanted = width * height

    # if there are no chars to select, blank the screen
    if len(chars) == 0:
        output += ' ' * (width * height)

    while len(output) < numWanted:

        roll = random.randint(0, len(chars) - 1)
        char = chars[roll]

        newLine += char

        if len(newLine) >= width:
            # cuts off the extra characters
            output += newLine[:width]
            # puts the extra characters onto the next line
            newLine = newLine[width:]

    return output


def user_options(keyEvent, settings, nextScreen):
    # runs through and applies options enacted by the user

    # tries to convert the key event into a string character
    char = pygcurse.interpretkeyevent(keyEvent)
    # if it is convertible, it sets it to the key
    if char: key = char.upper()
    # otherwise, it just uses the keyEvent's key
    else: key = keyEvent.key

    # if the screen should be refreshed
    refresh = False
    # DEBUG! if the list of characters to be displayed should be shown
    showDisplayChars = False

    # chooses a totally random option
    if key == WILDCARD:
        roll = random.randint(0, len(WILD_KEYS) - 1)
        key = WILD_KEYS[roll]
        print key

    # pauses/unpauses the program
    if key == PAUSE:
        settings['pause'] = not settings['pause']

    # turns automatic screen refresh on/off
    elif key == AUTOREFRESH:
        settings['autoRefresh'] = not settings['autoRefresh']


    # time controls
    elif key in TIME_KEYS:

        position = SPEED_VALUES.index(settings['speed'])

        # if the action is slowing down the refresh rate
        if key == TIME_KEYS[0] or key == K_EQUALS and (KMOD_SHIFT):
            position += 1
            action = '+'
        # or if the action is speeding it up
        else:
            position -= 1
            action = '-'

        # moves position around to valid values
        if position < 0: position = 0
        if position >= len(SPEED_VALUES): position = len(SPEED_VALUES) - 1

        settings['speed'] = SPEED_VALUES[position]
        speed = settings['speed']

        # the time to the next screen is larger than the new speed
        if action == '-' and nextScreen > speed:
            nextScreen = speed
        elif action == '+' and nextScreen < speed:
            difference = speed - nextScreen
            nextScreen += difference / 2


    # changes the current character set to the next
    elif key == CHANGE_CHAR_SET:

        # gets the numeric position of the current colour mode
        current = CHAR_SETS.index(settings['charSet'])
        # finds the position of the /next/ colour mode, going back to 1 if len
        settings['charSet'] = CHAR_SETS[ (current + 1) % len(CHAR_SETS) ]
        # puts in all of the new chars
        settings['charsToUse'] = settings['charSet'].values()

        showDisplayChars = True
        refresh = True

    # blanks chars to display
    elif key == CLEAR_CHARS:

        settings['charsToUse'] = []
        showDisplayChars = True
        refresh = True

    # selects/deselects a character for displaying
    elif key in settings['charSet'] or key in EXTRACHARS:

        char = settings['charSet'].get(key, None)
        if char == None: char = EXTRACHARS[key]

        # removes the selected 
        if char in settings['charsToUse']:
            settings['charsToUse'].remove(char)
        else:
            settings['charsToUse'].append(char)

        showDisplayChars = True
        refresh = True

    # selects/deselects only one charater for displaying
    elif key in SINGLECHARS:

        # retrives the corresponding un-shifted key, if it exists
        char = settings['charSet'].get(SINGLECHARS[key])

        # makes sure the selection is valid
        if char != None:
            settings['charsToUse'] = [char]
            showDisplayChars = True
            refresh = True

    # DEBUG TERMINAL OUTPUT
    if showDisplayChars:

        data = []
        for k, v in settings['charSet'].items():
            if v in settings['charsToUse']:
                data.append(k)
        print data


    # toggles what colour mode the screen is in
    elif key == COLOURMODE_TOGGLE:

        # gets the numeric position of the current colour mode
        current = COLOURMODENAMES.index(settings['colourMode'])
        # finds the position of the /next/ colour mode, going back to 1 if len
        settings['colourMode'] = COLOURMODENAMES[ (current + 1) % len(COLOURMODENAMES) ]

        refresh = True


    # toggles the full screen setting
    elif key == FULLSCREEN:

        settings['fullscreen'] = not settings['fullscreen']
        window.fullscreen = settings['fullscreen']

        # updates the window so it will be immediately displayed in full screen
        window.update()

    # resizes the window
    elif key in RESIZE_KEYS:

        # defaults to nothing, in case an action isn't possible
        change = (0, 0)

        # saves reference space
        action = RESIZE_KEYS.index(key)

        # creates the appropiate difference tuple, if possible
        if action == 0 and settings['width'] > 1: change = (-1, 0)
        elif action == 1 and settings['width'] < MAXWIDTH: change = (1, 0)
        elif action == 2 and settings['height'] > 1: change = (0, -1)
        elif action == 3 and settings['height'] < MAXHEIGHT: change = (0, 1)

        # applies the size changes
        settings['width'] += change[0]
        settings['height'] += change[1]

        set_window_properties(settings)
        refresh = True

    # saves the screen to an image
    elif key == SCREENSHOT:

        # makes the screenshot folder if it doesn't already exist
        if not os.path.exists(SCREENSHOT_LOCATION):
            os.makedirs(SCREENSHOT_LOCATION)

        # removes period from time.time() result
        filename = str(time.time()).replace('.', '')
        filename = "./%s/%s%s" % (SCREENSHOT_LOCATION, filename, SCREENSHOT_FILETYPE)

        pygame.image.save(window._surfaceobj, filename)


    # user wants to refresh the screen, or it needs to be done now
    if key == GENERATE or refresh:
        nextScreen = 0

    return settings, nextScreen


def display_screen(settings):
    # displays a screen of characters to the user
    
    nextScreen = settings['speed']

    set_colors(COLOURMODES[ settings['colourMode'] ])

    # blanks the window display
    window.fill('')
    # resets cursor position
    window.cursorx = 0
    window.cursory = 0

    # generates extra output, just to be sure to fill the screen
    output = generate(settings['charsToUse'], settings['width'], settings['height'])

    # writes output to the window
    window.write(output, autoScroll=False)
    # finally updates the window, displaying it to the user
    window.update()

    return nextScreen

def main():
    # the main program, runs everything from here

    # if all variables need to be set/reset
    reset = True

    # time until the next screen is displayed automatically
    nextScreen = 0
    # the system time when the screen was changed last
    lastTime = 0

    # loops until user quit
    while True:

        # if the settings need to be re-initialized
        if reset:
            reset = False
            settings = copy_default_settings()
            set_window_properties(settings)
            # force the next screen to display
            nextScreen = 0
        
        # slows down processing speed a little
        CLOCK.tick(FPS)

        # if the screen should automatically refresh
        if settings['autoRefresh']:

            # gets the difference in time since the last loop
            timeDiff = time.time() - lastTime
            # applies time difference to the time remaining
            nextScreen -= timeDiff
            # saves the exact time for the next loop
            lastTime = time.time()

        # if it is time to display another screen
        if nextScreen <= 0 and not settings['pause']:
            nextScreen = display_screen(settings)

        for event in pygame.event.get():

            # user quit
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                quit()

            # if the user pressed a key
            if event.type == KEYDOWN:

                print pygcurse.interpretkeyevent(event)
                
                # looks through user options
                settings, nextScreen = user_options(event, settings, nextScreen)

                # reset settings to def
                if event.key == RESET_SETTINGS:
                    reset = True

# runs the program
main()