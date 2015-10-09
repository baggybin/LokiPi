#!/usr/bin/python
#########################################
################### Jonathan OBrien #####
# Waterford Institute of Technology #####
#########################################
#########################################
#
# pyLCD UI menu library from https://github.com/Mezgrman/pyLCD
# Wiring GPIO interaction from https://github.com/WiringPi/WiringPi-Python
# psutil
# Netifaces
# WIFI
# 


###################### Module Imports #################
#######################################################
#######################################################
import string 
import psutil
import pylcd
import time
import os, sys
from multiprocessing import Process
from wifi import Cell, Scheme
from wifi.exceptions import ConnectionError
from threading import Thread
import subprocess
import netifaces

    
    
### ASCII Character Generation ########################
#######################################################
inputCharacters = string.printable
inputCharacters = " " + inputCharacters
b =  ('Back','Delete')
fullList = list(b)
inputCharacters = tuple(inputCharacters)
for x in inputCharacters:
    fullList.append(x)      
########################################################
########################################

############## FLAGS ###################
########################################

### will use these to test if incompatible funtions are operating
###

FLAG_KARMA_WE = False
FLAG_KARMA_WW = False
FLAG_SSLSTRIP = False
FLAG_wan = False
FLAG_Evil = False
FLAG_DNS = True
choice = ""


########################### GPIO PIN MAPPINGS ####################
############################################################

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


############################### Progress BAR --- NEEDS ALTERATION ########################

#def progressbar():
#    x =0.0
#    bar = ui.progress_bar("Scanning...", fraction = x, char = "*")
#    while x < 1.0:
#        x += 1.0 / 16.
#        bar.update(fraction = x)
#        time.sleep(1.0)



def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)
    
    
################################################# ROUGE  ##################################
###########################################################################################################
############################################################################################################
def rouge():
    global FLAG_KARMA_WE 
    global FLAG_KARMA_WW
    global FLAG_SSLSTRIP
    global FLAG_wan 
    global FLAG_Evil
    global FLAG_DNS
    global ui
    global display
    try:
       while True:

          res = ui.list_dialog("...Menu...", ( "Wireless Scan", "KARMA", "Evil Twin" ,"Extras", "System info", "Quit", "Shutdown" ), align = 'center')
          
        ################################################# KARMA ############################################################
        ####################################################################################################################
        #####################################################################################################################
        #####################################################################################################################
        
          if res[1] == "KARMA":
                  
                  while True:
                        wres = ui.list_dialog("<<<KARMA>>>", ("Karma_we", "Karma_ww" ,"Terminate KARMA", "<-Back"), align = 'center')
                                            
                        if wres[1] == "Karma_we":
                            
                            if FLAG_KARMA_WE or FLAG_KARMA_WW == True:
                                ui.message("Already Enabled!!!!", align = 'center', duration = 1.5)
                                break
                            
                            print "here"
                            ui.message("Starting KARMA", align = 'center', duration = 1.5)
                            retCode = subprocess.call(["/rasberryPwnPi/scripts/karma_we.sh"])
                            ### Do check on return code to enable flag or not
                            ############
                            ## make sure that the WLAN1 interface has IP
                            try:
                                addr = netifaces.ifaddresses("wlan1")   
                            except Exception, e:
                                ui.message("Access Issue", align = 'center', duration = 10)
                            if netifaces.AF_INET in addr == False:
                                ui.message("Wlan1 IP Error", align = 'center', duration = 10)
                                subprocess.call(["/rasberryPwnPi/scripts/karma_wlan1_retry.sh"])
                                break  
                            
                            FLAG_KARMA_WE = True
                        
                        
                        
                        
                        elif wres[1] == "Karma_ww":
                            if FLAG_KARMA_WE or FLAG_KARMA_WW == True:
                                ui.message("Already Enabled!!!!", align = 'center', duration = 1.5)
                                break
                            
                            ui.message("Starting KARMA", align = 'center', duration = 1.5)
                            retCode = subprocess.call(["/rasberryPwnPi/scripts/karma_ww.sh"])
                            
    
                            try:
                                addr = netifaces.ifaddresses("wlan1")   
                            except Exception, e:
                                ui.message("Access Issue", align = 'center', duration = 10)
                            if netifaces.AF_INET in addr == False:
                                ui.message("Wlan1 IP Error", align = 'center', duration = 10)
                                subprocess.call(["/rasberryPwnPi/scripts/karma_wlan1_retry.sh"])
                                break                        
                        
                            FLAG_KARMA_WW = True
                        
                            
                        elif wres[1] == "Terminate KARMA":
                           ui.message("Killing KARMA", align = 'center', duration = 1.5)
                           retCode = subprocess.call(["/rasberryPwnPi/scripts/karma_WE_CLEAN.sh"])
                           FLAG_KARMA_WE = False
                           FLAG_KARMA_WW = False
                           
    
                           
                        elif wres[1] == "<-Back":
                           break
    
        #########################################################  EXTRA ATTACK Features #######################################################################
        ########################################################################################################################################################
        #######################################################################################################################################################
          if res[1] == "Extras":
                
                
                
                ##################################################### SSLStrip Transparent Proxy ##############################################################
                ###############################################################################################################################################
                ##############################################################################################################################################
                
                  while True:
                        exres = ui.list_dialog("<<<Extras>>>", ("SSLstrip", "DNSspoof", "<-Back"), align = 'center')
                        
                        if exres[1] == "SSLstrip":
                                while True:
                                      sslres = ui.list_dialog("<<<SSLStrip>>>", ("SSLstrip", "Terminate SSLstrip", "Parse SSL LOG", "Delete HTTP Logs", "<-Back"), align = 'center')
    
                                      if sslres[1] == "SSLstrip":
                                          if FLAG_SSLSTRIP == True:
                                              ui.message("SSLstrip\nEnabled Already", align = 'center', duration = 2.0)
                                              break
                                          
                                          elif FLAG_KARMA_WE == False and FLAG_KARMA_WW == False and FLAG_Evil == False:
                                              ui.message("Enable KARMA !!!!!", align = 'center', duration = 2.0)
                                              break
                  
                                          ui.message("Starting SSLstrip", align = 'center', duration = 1.5)
                                          retCode = subprocess.call(["/rasberryPwnPi/scripts/sslstrip_enable.sh"])
                                          FLAG_SSLSTRIP = True
                                          
                                         
                                      elif sslres[1] == "Terminate SSLstrip":
                                         ui.message("Killing SSLstrip", align = 'center', duration = 1.5)
                                         retCode = subprocess.call(["/rasberryPwnPi/scripts/sslstrip_disable.sh"])
                                         FLAG_SSLSTRIP = False
                                      
                                      elif sslres[1] == "Parse SSL LOG":
                                          ui.message("Parsing !!", align = 'center', duration = 1.5)
                                          #subprocess.call("python /root/scripts/log_ex.py /root/logPi/sslstrip.log  -o /var/www/ssllog/index.html")
                                          os.system("sudo python /rasberryPwnPi/scripts/log_ex.py %s %s %s %s" % (" /rasberryPwnPi/logPi/sslstrip.log "," -t ", " -o "," /var/www/ssllog/ssllog"))
                                          ui.message("Access at LOCALHOST:666", align = 'center', duration = 1.5)
                                          print
                                     
                                      elif  sslres[1] == "Delete HTTP Logs":
                                         print "attempting deletion" 
                                         retCode = subprocess.call(["/rasberryPwnPi/scripts/sslstrip_del_html.sh"])                
                                         print retCode
                                         print "Return Code"
                                        
                                      elif sslres[1] == "<-Back":
                                         break
    
                        elif exres[1] == "DNSspoof":
                                while True:
                                      dnsres = ui.list_dialog("<<<DNSspoofing>>>", ("Enable", "Disable", "Universal", "<-Back"), align = 'center')
    
                                      if dnsres[1] == "Enable":
                                        ui.message("Enabling DNSspoof", align = 'center', duration = 1.5)
                                        subprocess.call(["cp" , "/etc/dnsmasq.hosts.empty", "/etc/dnsmasq.hosts"])
                                        subprocess.call(["cp" , "/etc/dnsmasq.hosts.specific", "/etc/dnsmasq.hosts"])
                                        if FLAG_Evil and FLAG_KARMA_WE and FLAG_KARMA_WW == False:
                                            break                                    
                                        subprocess.call(["service" , "dnsmasq", "restart"])
                                        
                                      elif dnsres[1] == "Disable":
                                        ui.message("Disabling DNSspoof", align = 'center', duration = 1.5)
                                        ####echo wouldnt work
                                        #subprocess.call(["echo" , "   ", " > ", "/etc/dnsmasq.hosts"])
                                        subprocess.call(["cp" , "/etc/dnsmasq.hosts.empty", "/etc/dnsmasq.hosts"])
                                        if FLAG_Evil and FLAG_KARMA_WE and FLAG_KARMA_WW == False:
                                            break  
                                        subprocess.call(["service" , "dnsmasq", "restart"])
    
                                      elif dnsres[1] == "Universal":
                                        ui.message("Feature not/nImplemented", align = 'center', duration = 1.5)
    
                                      elif dnsres[1] == "<-Back":
                                         break
                         
                         
                                       
                        elif exres[1] == "<-Back":
                            break
          
          ############################################ Evil Twin attampts ##############################################################
          ##########################################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!######################################
          ########################################## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ########################################
          
          elif res[1] == "Evil Twin":
                while True:
                    etres = ui.list_dialog("<<<EvilTwin>>>", ("Evil Twin1","Evil Twin2", "Tear-Down", "<-Back"), align = 'center')
                    
                    if etres[1] == "Evil Twin1":
                        ui.message("Scanning <->", align = 'center', duration = 0.5)
                        try:
                            cells = Cell.all('wlan0')
                        except Exception, e:
                            print e.message
                            ui.message("Interface Init Err", align = 'center', duration = 1.5)
                            break    
                         
                           
                        ssids = []
                    
                        for x in range (0,len(cells)):
                            ssids.append(cells[x].ssid)
                    
                        cres = ui.list_dialog("Results", list(ssids), align = 'center')
    
                        if cres[1]:
                            choice = cres[1]
                            try:
                                index = [ x.ssid for x in cells ].index(choice)
                            except ValueError:
                                index = -1
                    
                        evilMac =  cells[index].address
                        evilSSID = str(cells[index].ssid)
                        evilChan = cells[index].channel
                    
                        print evilMac
                        print evilChan
                        print evilSSID
                        #retCode = subprocess.call(["/root/scripts/evilTwin_Start.sh",evilSSID,evilMac,evilChan ])
                        retCode = os.system("sh /rasberryPwnPi/scripts/evilTwin_Start.sh %s %s %s" % (evilSSID,evilMac,evilChan))
                        #print retCode
                        FLAG_Evil = True
                    
                    
                    elif etres[1] == "Evil Twin2":
                          while True:
                              ui.message("Scanning <->", align = 'center', duration = 0.5)
                              try:
                                  cells = Cell.all('wlan0')
                              except Exception, e:
                                  ui.message("Interface Init Err", align = 'center', duration = 1.5)
                                  print e.message
                                  break 
                                     
                              ssids = []
                              
                              for x in range (0,len(cells)):
                                  ssids.append(cells[x].ssid)
                              
                              cres = ui.list_dialog("Results", list(ssids), align = 'center')
              
                              if cres[1]:
                                  choice = cres[1]
                                  try:
                                      index = [ x.ssid for x in cells ].index(choice)
                                  except ValueError:
                                      index = -1
                              
                              evilMac =  cells[index].address
                              evilSSID = str(cells[index].ssid)
                              evilChan = cells[index].channel
                              
                              print evilMac
                              print evilChan
                              print evilSSID
                              #retCode = subprocess.call(["/root/scripts/evilTwin_Start.sh",evilSSID,evilMac,evilChan ])
                              ui.message("Cloning Initilised", align = 'center', duration = 0.5)
                              retCode = os.system("sh /rasberryPwnPi/scripts/evilTwin_Start2.sh %s %s %s" % (evilSSID,evilMac,evilChan))
                              FLAG_Evil = True
                              print retCode                
                              break
                    
                    elif etres[1] == "Tear-Down":
                        ui.message("Tear-Down Started", align = 'center', duration = 0.5)
                        subprocess.call(["/rasberryPwnPi/scripts/evilTwin_TearDown.sh"])
                        FLAG_Evil = False
                        break
                    
                    elif etres[1] == "<-Back":
                           break
                        
                        
          ################################################## WAN CONNECTION ###############################################
          ##################################################   Wireless     ###############################################
          ###################################################################################################################
          ##################################################################################################################
          
          elif res[1] == "Wireless Scan":
                  while True:
                        
                        ####could make sub sub levels for inputing UPPER/lower/symbols/Number seperatley
                        wsres = ui.list_dialog("Wirless Menu", ("Scan","Check_IP", "Back" ), align = 'center')
                        #password.join(ires[1])
                        
                        
                        
                        ######################################## Active Interface IP Check #################################
                        ###################################################################################################
                        
                        if wsres[1] ==  "Check_IP":
                            
                            ifaces = netifaces.interfaces()
                            ifaces.append('Back')
                            while True:
                                    ifres = ui.list_dialog("Interfaces", (ifaces), align = 'center')
                                    if ifres[1] != "Back":
                                        choice = ifres[1]
                                        try:
                                            addr = netifaces.ifaddresses(choice)[2][0]['addr']
                                            ui.message(addr, align = 'center', duration = 3.5)
                                        except Exception, e:
                                            ui.message("No IP", align = 'center', duration = 3.5)
                                            print "Iface Has no address"
                                    if ifres[1] == "Back":        
                                        break
                                    
                                
                        ################################################ AP SCANNING ##########################################
                        #######################################################################################################
                        ## option for initiating scanning of AP's
                        
                        if wsres[1]  == "Scan":
                            ui.message("Scanning <->", align = 'center', duration = 0.5)
                            try:
                                cells = Cell.all('wlan0')
                            except Exception, e:
                                print e.message
                                break 
                                   
                            ssids = []
                            
                            for x in range (0,len(cells)):
                                ssids.append(cells[x].ssid)
                            
                            cres = ui.list_dialog("Results", list(ssids), align = 'center')
    
                            if cres[1]:
                                choice = cres[1]
                                try:
                                    index = [ x.ssid for x in cells ].index(choice)
                                except ValueError:
                                    index = -1
                                    
            
                                
                                if Scheme.find('wlan0', choice):
                                    print "Found"
                                    ui.message("Found Previous Entry\nAttemting", align = 'Left', duration = 1.5) 
                                    #### !!!!!!!!!!!!!!!!!!!!!! add code for a re-entry of Key
                                    ## Retreieve Scheme for processing
                                    scheme = Scheme.find('wlan0', choice)
                                    try:
                                        result = scheme.activate()
                                    except Exception as e:
                                        print "Exception Activating Found Scheme"
                                        ui.message("Failed, >>>>>> Deleted", align = 'center', duration = 2.5)
                                        scheme.delete() 
                                    break
                            
                            ##########################################################################################################
                               #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!~~~~~~~~~~~~~~###########################
                               #######################################################################################################
                               ################################# HARD CODED KEYS Here#################################################
                               
                                if cells[index].ssid == "TNCAP071FA6":
                                    scheme = Scheme.for_cell('wlan0', choice, cells[index], "5788C9870Bpissy8189?reality")
                                    scheme.save()
                                    try:
                                        ui.message("Attempting Ceonnection \n Please wait", align = 'Left', duration = 1.5)
                                        scheme.activate()
                                        break
                                    except Exception, e:
                                        print "Already Connected, Or Error"
                                        scheme.delete()
    
                                    
                                
                                ### If choice is ENCYPTED 
                                elif cells[index].encrypted:
                                    ui.message("AP Encypted - Enter Key", align = 'center', duration = 1.5)
                                    password = ""  
                                    while True:
                                    ####could make sub sub levels for inputing UPPER/lower/symbols/Number seperatley
                                        wres = ui.list_dialog(password, list(fullList), align = 'center')
                            
                                # Enters and stores characters generated from list
                                # allows deletion 
                                        if wres[1]  != "Delete" and wres[1] != "Back":
                                          password = password + str(wres[1])
                             
                                        if wres[1] == "Delete":
                                           password = password[:-1]
                       
                                        if wres[1] == "Back":
                                          print password
                                          break
                                        
                                    ui.message("Attempting \n Please wait", align = 'Left', duration = 1.5)
                                    scheme = Scheme.for_cell('wlan0', choice, cells[index], password)
                                    scheme.save()
                                    try:
                                        scheme.activate()
                                    except Exception, e:
                                        print e.message
                                        scheme.delete()
      
            
                                elif not cells[index].encrypted:
                                    ui.message("Attempting Ceonnection \n Please wait", align = 'Left', duration = 1.5)
                                    scheme = Scheme.for_cell('wlan0', choice, cells[index])
                                    scheme.save()
                                    try:
                                        scheme.activate()
                                    except Exception, e:
                                        scheme.delete()
    
                                print index
                                print choice
                                break
                        
    
                        elif wsres[1] == "Back":
                           break          
             
    
    
    
    ########################################################### SYSTEM INFORMATION #######################################################
          elif res[1] == "System info":
                  while True:
                          ires = ui.list_dialog("System info", ( "Memory","Clock", "Check_IP", "Back"), align = 'center')
                                        
                                        
                          if ires[1] == "Memory":
                                  try:
                                          key = None
                                          while True and key == None:
                                                  mem = psutil.phymem_usage()
                                                  free = mem[2] / 1024.0 / 1024.0
                                                  total = mem[0] / 1024.0 / 1024.0
                                                  
                                                  ## display and convert KB to MB
                                                  data = "Total\t%.2fMB\nFree\t%.2fMB" % (total, free)
                                                 
    
                                                  ui.message(data, duration = 0.001)
                                                  #key = ui.input.read_key()
                                                  if ui.input.return_back()== True:
                                                     break
                                                    
                                  except KeyboardInterrupt:
                                          pass
                                        
                        ########### CHECK CLOCK BECAUSE THERE IS NO RTC --- may add use of NTP here #########################
             
                          elif ires[1] == "Clock":
                                 try:
                                      while True:
                
                                            data = time.strftime("%a, %d.%m.%Y\n%H:%M:%S")
                                            ui.message(data, align = 'center')               
                                            time.sleep(1)
                                            if ui.input.return_back()== True:
                                                break
                                 except KeyboardInterrupt:
                                     pass                          
                          
    
                          elif ires[1] ==  "Check_IP":
                            
                                ifaces = netifaces.interfaces()
                                ifaces.append('Back')
                                while True:
                                        ifres = ui.list_dialog("Interfaces", (ifaces), align = 'center')
                                        if ifres[1] != "Back":
                                            choice = ifres[1]
                                            try:
                                                addr = netifaces.ifaddresses(choice)[2][0]['addr']
                                                ui.message(addr, align = 'center', duration = 3.5)
                                            except Exception, e:
                                                ui.message("No IP", align = 'center', duration = 3.5)
                                                print "Iface Has no address"
                                        if ifres[1] == "Back":        
                                            break
    
             
                          elif ires[1] == "Back":
                                  break
        
    ################################################## QUIT --- NEEDs to be changed to SYS Shutdown ############################
    ############################################################################################################################
          elif res[1] == "Quit":
            ui.message("Exiting!!!!", align = 'center')
            time.sleep(2)
            ui.clear()
            main()
        
          elif res[1] == "Shutdown":
            ui.message("Shutting Down!", align = 'center')
            time.sleep(1.5)
            ui.clear()
            subprocess.call(["poweroff" , "-i"])
            subprocess.call(["service" , "raspberrypwnpi", "stop"])
            
    
    except:
       raise
    finally:
       ui.shutdown()
       display.shutdown()
    pass

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
                                         #~~~~~      Main     ~~~~~#
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
#                                       ~
#       .M,                 +M         ~
#       :MMMM               MMMM,       ~
#       MM .M             M  MM:       ~
#       .MM.  M           M   MM        ~
#       .MMM                .MMM        ~
#         MM,               MMM.        ~
#         MMM.              MMM         ~
#          MMM            .MMM          ~
#          +M+MMMMMMMM,7MM MM           ~
#           MMM ? ,MMM.MMM MM           ~
#           .MM MM .M DMIMMM            ~
#            MMMMMMMMMM, MMM            ~
#           .M$MM +MMMM MNM,            ~
#            MMMMMMMMM.MMMMN            ~
#            N.OM.MM=MM MM .            ~
#            ...  .. .    :.            ~
#             N           O             ~
#             NM        .M~             ~
#            .8.       MM              ~
#              M..     MM.              ~
#               MM      M               ~
#               .=    .M                ~
#                                       ~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    mainres = ui.list_dialog("<<<<<LokiPi>>>>>", ( "Rouge", "WEP" ,"Reverse Backdoor"), align = 'center')

        
    if mainres[1] == "Rouge":
        rouge()
    
    elif mainres[1] == "WEP":
        main()
        print "WEP"
    
    else:
        restart()
        print "backdoor"
    
    


if __name__ == "__main__":
    main()
    

