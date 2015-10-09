#!/usr/bin/python
#
#
# HD44870 UI menu library from https://github.com/Mezgrman/pyLCD
# Wiring GPIO interaction from https://github.com/WiringPi/WiringPi-Python

import string 
import psutil
import pylcd
import time
import os
from multiprocessing import Process
from wifi import Cell, Scheme
#import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_UP)



#######################################################
inputCharacters = string.printable
inputCharacters = " " + inputCharacters
b =  ('Back','Delete')
fullList = list(b)
inputCharacters = tuple(inputCharacters)
for x in inputCharacters:
    fullList.append(x)      
########################################################


# Dictionary mapping pins on LCD to RasberryPi GPIO
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


# DisplayUI class Instantiation for the HD44780 LCD, RPi.GPIO with personal mappings  
display = pylcd.hd44780.Display(backend = pylcd.hd44780.GPIOBackend, pinmap = PINMAP, lines = 4, columns = 20)
ui = pylcd.hd44780.DisplayUI(display, pylcd.hd44780.GPIOInput, input_kwargs = {'pinmap': INPUT_PINMAP})
# Sends Clear command to the LCD 0b00000001
display.clear()

ui.message( " Welcome ", align = 'center', wrap = False, duration = 1)



try:
   while True:
      res = ui.list_dialog("...Menu...", ( "Wireless Connetion", "Clock", "System info", "Quit"), align = 'center')
      
      if res[1] == "Enter Security key":
              password = ""  
              while True:
                     ####could make sub sub levels for inputing UPPER/lower/symbols/Number seperatley
                     
                    pres = ui.list_dialog(password, list(fullList), align = 'center')
                    #password.join(ires[1])
                    password = password + str(pres[1])
                    if pres[1] == "Back":
                       password = password.strip('Back')
                       break
 
      if res[1] == "Wireless Connetion":
              password = ""  
              while True:
               
                  
                     ####could make sub sub levels for inputing UPPER/lower/symbols/Number seperatley
                    wres = ui.list_dialog(password, list(fullList), align = 'center')
                    #password.join(ires[1])
                    
                    if wres[1]  != "Delete" and wres[1] != "Back":
                         password = password + str(wres[1])
                         
                    if wres[1] == "Delete":
                        password = password[:-1]
   
                    
                    if wres[1] == "Back":
                       print password
                       break            
        
         
      elif res[1] == "Clock":
         try:
            #clockkey = None
            #while clockkey == None:
            while true:
            
               data = time.strftime("%a, %d.%m.%Y\n%H:%M:%S")
               ui.message(data, align = 'center')
               
               #p = Process(target=clockupdate, args=())
               #p.start()
               #p.join()
               # Hack to get this code to return to previous menu
               # Due to my 4x20 charater display onyl having 4 input buttons
               #GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_UP)
               #GPIO.wait_for_edge(23, GPIO.FALLING)
               #
               # ended up causing more issue
               
               time.sleep(1)
               if ui.input.return_back()== True:
                  break
               #clockkey = ui.input.read_key()
               #clockkey = display.digitalRead(PIN_LEFT)
                  
         except KeyboardInterrupt:
            pass

      elif res[1] == "System info":
              while True:
                      ires = ui.list_dialog("System info", ( "Disk space", "Memory", "Back"), align = 'center')
                                    
                      if ires[1] == "Disk space":
                              try:
                                      key = None
                                      while True and key == None:
                                              space = os.statvfs("/")
                                              free = (space.f_bavail * space.f_frsize) / 1024.0 / 1024.0
                                              total = (space.f_blocks * space.f_frsize) / 1024.0 / 1024.0
                                              data = "Total\t%.2fMB\nFree\t%.2fMB" % (total, free)
                                              ui.message(data)
                                              time.sleep(1)
                                              if ui.input.return_back()== True:
                                                 break
                              except KeyboardInterrupt:
                                      pass
                                    
                      elif ires[1] == "Memory":
                              try:
                                      key = None
                                      while True and key == None:
                                              mem = psutil.phymem_usage()
                                              free = mem[2] / 1024.0 / 1024.0
                                              total = mem[0] / 1024.0 / 1024.0
                                              data = "Total\t%.2fMB\nFree\t%.2fMB" % (total, free)
                                              ui.message(data, duration = 0.001)
                                              #key = ui.input.read_key()
                                              
                                              if ui.input.return_back()== True:
                                                 break
                                                
                              except KeyboardInterrupt:
                                      pass
                      

                                    
                                      
                      elif ires[1] == "Back":
                              break

except:
   raise
finally:
   ui.shutdown()
   display.shutdown()
 