#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013 Julian Metzler
# See the LICENSE file for the full license.

"""
This is a rather chaotic collection of examples. Use at your own risk :-)
"""

import argparse
import os
import psutil
import pylcd
import time
from subprocess import check_output


PINMAP = {
    'RS': 7,
    'E': 8,
    'D4': 17,
    'D5': 18,
    'D6': 27,
    'D7': 22,
    'LED': 101,
}

INPUT_PINMAP = {
	'UP': 4,
	'LEFT': 23,
	'RIGHT': 102,
	'DOWN': 9,
        'READY': 101,
        'ERROR': 101,
        'OK': 10,  
}



CHARMAP = {
	0: (
		0b01110,
		0b10001,
		0b10111,
		0b11001,
		0b10111,
		0b10001,
		0b01110,
		0b00000,
	),
	1: (
		0b10010,
		0b00100,
		0b01001,
		0b10010,
		0b00100,
		0b01001,
		0b10010,
		0b00100,
	),
	2: (
		0b01001,
		0b00100,
		0b10010,
		0b01001,
		0b00100,
		0b10010,
		0b01001,
		0b00100,
	),
	3: (
		0b10101,
		0b01010,
		0b10101,
		0b01010,
		0b10101,
		0b01010,
		0b10101,
		0b01010,
	),
	4: (
		0b01010,
		0b10101,
		0b01010,
		0b10101,
		0b01010,
		0b10101,
		0b01010,
		0b10101,
	),
	5: (
		0b11111,
		0b11111,
		0b11111,
		0b11111,
		0b11111,
		0b11111,
		0b11111,
		0b11111,
	),
	6: (
		0b11111,
		0b10001,
		0b10101,
		0b10101,
		0b10101,
		0b10101,
		0b10001,
		0b11111,
	),
	7: (
		0b00000,
		0b01110,
		0b01010,
		0b01010,
		0b01010,
		0b01010,
		0b01110,
		0b00000,
	),
}


#CHARMAP = None

def run():
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--mode', choices = ['stats', 'text', 'textpad', 'interactive', 'music'], default = 'interactive')
	parser.add_argument('-t', '--text', default = "Hello world!")
	parser.add_argument('-c', '--cursor', action = 'store_true')
	parser.add_argument('-cb', '--cursor-blink', action = 'store_true')
	parser.add_argument('-s', '--scroll', action = 'store_true')
	parser.add_argument('-sd', '--scroll-delay', type = float, default = 0.25)
	parser.add_argument('-si', '--skip-init', action = 'store_true')
	parser.add_argument('-a', '--align', choices = ['left', 'center', 'right'], default = 'left')
	args = parser.parse_args()
	
	display = pylcd.hd44780.Display(backend = pylcd.GPIOBackend, pinmap = PINMAP, charmap = CHARMAP, lines = 4, columns = 20, skip_init = args.skip_init, debug = False)
	display.set_display_enable(cursor = args.cursor, cursor_blink = args.cursor_blink)
	display.clear()
	display.home()
	ui = pylcd.hd44780.DisplayUI(display, pylcd.hd44780.GPIOInput, input_kwargs = {'pinmap': INPUT_PINMAP})
	ui.message(chr(0) + " 2013 Mezgrman\nwww.mezgrman.de", align = 'center', wrap = False, duration = 2.5)
	
	try:
		if args.mode == 'interactive':
			while True:
				res = ui.list_dialog("Welcome!", ("Textpad mode", "Clock", "System info", "Demos", "Settings", "Quit"), align = 'center')
				if res[1] == "Textpad mode":
					ui.clear()
					try:
						while True:
							char = ui.input.read_key()
							if char:
								display.write(char)
					except KeyboardInterrupt:
						pass
					ui.clear()
					
					
					
				elif res[1] == "Clock":
					try:
						while True:
							data = time.strftime("%a, %d.%m.%Y\n%H:%M:%S")
							ui.message(data, align = 'center')
							time.sleep(1)
						
							if ui.input.return_back()== True:
								break
							
					except KeyboardInterrupt:
						break
					
					
					
				elif res[1] == "System info":
					while True:
						ires = ui.list_dialog("System info", ("Load average", "Disk space", "Memory", "Back"), align = 'center')
						if ires[1] == "Load average":
							try:
								while True:
									with open("/proc/loadavg", 'r') as f:
										loadavg = f.read()
									data = "* LOAD AVERAGE *\n" + "  ".join(loadavg.split()[:3])
									ui.message(data, align = 'center')
									time.sleep(5)
							except KeyboardInterrupt:
								pass
						elif ires[1] == "Disk space":
							try:
								while True:
									space = os.statvfs("/")
									free = (space.f_bavail * space.f_frsize) / 1024.0 / 1024.0
									total = (space.f_blocks * space.f_frsize) / 1024.0 / 1024.0
									data = "Total\t%.2fMB\nFree\t%.2fMB" % (total, free)
									ui.message(data)
									time.sleep(5)
							except KeyboardInterrupt:
								pass
						elif ires[1] == "Memory":
							try:
								while True:
									mem = psutil.phymem_usage()
									free = mem[2] / 1024.0 / 1024.0
									total = mem[0] / 1024.0 / 1024.0
									data = "Total\t%.2fMB\nFree\t%.2fMB" % (total, free)
									ui.message(data, duration = 5.0)
							except KeyboardInterrupt:
								pass
						elif ires[1] == "Back":
							break
				elif res[1] == "Demos":
					while True:
						dres = ui.list_dialog("Demos", ("Progress bar", "Input dialog", "Check dialog", "Custom chars", "Back"), align = 'center')
						if dres[1] == "Progress bar":
							x = 0.0
							bar = ui.progress_bar("Testing...", fraction = x, char = "*")
							while x < 1.0:
								x += 1.0 / 16.0
								bar.update(fraction = x)
							time.sleep(1.5)
							ui.message("Done :)", align = 'center', duration = 3.0)
						elif dres[1] == "Input dialog":
							name = ui.input_dialog("Your name?")
							ui.message("Hello %s!" % name, align = 'center', duration = 3.0)
						elif dres[1] == "Check dialog":
							selected = ui.multiple_choice_dialog("Which?", ("rrerr", "SooS", "MeeM", "M. D'Avis"))
							ui.message("%s!" % ", ".join([str(item[1]) for item in selected]), align = 'center', duration = 3.0)
						elif dres[1] == "Custom chars":
							for i in range(8):
								ui.message(chr(i) * 16 + "\n" + chr(i) * 16, align = 'center', duration = 1.0)
						elif dres[1] == "Back":
							break
				elif res[1] == "Settings":
					while True:
						sres = ui.list_dialog("Settings", ("Brightness", "Back"), align = 'center')
						if sres[1] == "Brightness":
							count = ui.slider_dialog("Brightness", 0, 1023, step = 5, big_step = 100, value = ui.display.brightness, onchange = ui.dim, onchange_kwargs = {'animate': False})
							ui.dim(count)
						elif sres[1] == "Back":
							break
				elif res[1] == "Quit":
					ui.message("Bye! :-)", align = 'center')
					time.sleep(1)
					ui.clear()
					ui.dim(0, duration = 0.65)
					break
		elif args.mode == 'music':
			while True:
				data = check_output(['mocp', '--info'])
				if "FATAL_ERROR" in data:
					string = "Not running"
				else:
					metadata = [line.split(": ") for line in data.splitlines()]
					metadata = dict([(line[0], ": ".join(line[1:])) for line in metadata])
					string = "%(Artist)s\n%(Title)s" % metadata
				display.write(string, align = 'center')
				time.sleep(5)
		elif args.mode == 'textpad':
			while True:
				char = ui.input.read_key()
				if char:
					display.write(char)
		elif args.mode == 'text':
			text = args.text.replace("\\n", "\n")
			display.write(text, align = args.align)
			while args.scroll and len(args.text) > display.column_count:
				display.scroll()
				time.sleep(args.scroll_delay)
		elif args.mode == 'stats':
			while True:
				with open("/proc/loadavg", 'r') as f:
					loadavg = f.read()
				data = "* LOAD AVERAGE *\n" + "  ".join(loadavg.split()[:3])
				display.write(data, update = True, align = args.align)
				time.sleep(5)
	except KeyboardInterrupt:
		pass
	except:
		raise
	finally:
		ui.shutdown()
		display.shutdown()

run()
