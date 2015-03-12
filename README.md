UniMazeGenEX DingoMode 2015
==========================

UniMazeGenEX DingoMode 2015 is a toy built on pygame and pygcurse that generates random displays of ASCII drawing characters. It features various controls to try to give the user a lot of  power, such as changing the colours, the range of characters being drawn, and taking screenshots.

Usage
=====

Requires pygame and python 2. pygcurse is provided.

python runme.py

Controls
========
`1234567890 toggles various characters for display  
~!@#$%^&*() selects only one character to display, corresponding to the above keys  
SPACE toggles space character  
TAB toggles 4 * space character  
ENTER toggles 8 * space character  
BACKSPACE clears all characters to be printed  
B changes current character set (currently Double Pipes, Single Pipes, Card Suits, Numbers, and Shift Row)

-+ decreases/increases automatic sceen refreshing time (goes from 0.1 seconds to 60 seconds on a scale)  
P pauses/unpauses the program completely  
A turns on/off automatic screen refreshing  
G generates a new screen immediately (can be slow with a large screen)

C toggles through preset colour modes  
ARROW KEYS - resizes the window  
F toggles fullscreen mode (window resizing is bad in this mode)

S saves the current screen to an image (saved in /screenshots as a png file with a timestamp filename)  
W randomly selects another control  
ESCAPE ends the program

NOTE: most keys can be held down to be rapidly used, including saving!

History
=======
UniMazeGenEX DingoMode 2015 was originally made in 2013, when it was humbly known as Pipes Generator 2013. It had a short lived second incarnation as UniDisplayEX 2014, but was stopped short due to problems I could not figure out. Hopefully I can get a better handle on it today!