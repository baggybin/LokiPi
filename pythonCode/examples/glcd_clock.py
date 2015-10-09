#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013 Julian Metzler
# See the LICENSE file for the full license.

"""
Script to display a clock on a GLCD
"""

import datetime
import math
import sys
import time
import hd44870 


# Pin map for Register Select, Enable, 4 Data lines (LED AND RW n/a)
PINMAP = {
    'RS': 7,
    'RW': 3,
    'E': 8,
    'D4': 17,
    'D5': 18,
    'D6': 27,
    'D7': 22,
    'LED': 101,
}

# input pinmap including making 10 both ok and down, also include
# unused LEDs 101 for Library compatability

INPUT_PINMAP = {
        'UP': 4,
        'LEFT': 23,
        'RIGHT': 10,
        'DOWN': 9,
        'READY': 101,
        'ERROR': 101,
        'OK': 10,  
}

WEEKDAYS = (
	"Monday",
	"Tuesday",
	"Wednesday",
	"Thursday",
	"Friday",
	"Saturday",
	"Sunday",
)

def main():
	display = hd44780.Display(backend = pylcd.GPIOBackend, pinmap = PINMAP, debug = False)
	draw = pylcd.hd44780.DisplayDraw(display)
	display.commit(full = True)
	old_minute = -1
	
	while True:
		now = datetime.datetime.now()
		
		if now.minute != old_minute:
			old_minute = now.minute
			if now.hour >= 20 and now.hour < 22:
				display.set_brightness(100)
			elif now.hour >= 22:
				display.set_brightness(10)
			elif 0 <= now.hour < 7:
				display.set_brightness(1)
			else:
				display.set_brightness(1023)
			
			display.clear()
			draw.analog_clock(32, 32, 31, now.hour, now.minute, has_lines = True, fill = True, clear = False)
			draw.text(WEEKDAYS[now.weekday()], ('center', 56, 127), 2, 14, "/home/pi/.fonts/truetype/timesbd.ttf")
			draw.line(64, 18, 127, 18)
			draw.function_plot(lambda x: math.sin(x), 64, 127, 18, 1.0, 0, 62.8)
			draw.text("%02i:%02i" % (now.hour, now.minute), ('center', 64, 127), 'middle', 25, "/home/pi/.fonts/truetype/timesbd.ttf")
			draw.line(64, 45, 127, 45)
			draw.function_plot(lambda x: math.sin(x), 64, 127, 45, 1.0, 0, 62.8)
			draw.text("%02i.%02i.%04i" % (now.day, now.month, now.year), ('center', 64, 127), ('bottom', 0, 61), 14, "/home/pi/.fonts/truetype/timesbd.ttf")
			display.commit()
			time_needed = (datetime.datetime.now() - now).total_seconds()
			print "%.2f seconds needed to redraw" % time_needed
		time.sleep(1)

if __name__ == "__main__":
	main()
