#!/usr/bin/python
#
#
from flask import Flask, render_template, request, jsonify
from subprocess import check_output
import logging
import subprocess
from multiprocessing import Process, Value, Array, Manager
import os, sys

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
counter = 0
attackOne = False
attackTwo = True

#########################################    FLASK WEB SERVER  #######################################
#####################################################################################################
####################################################################################################
####################################################################################################
######################################################################################################
######################################################################################################

counter = 0
attackOne = False
attackTwo = True
FLAGS = ""

### Start the web interface control###################################
#def website():
#    
#    pass


app = Flask(__name__)

####### main HTML file / template ###################################
@app.route("/")
def Index():
    return render_template("index.html", uptime=GetUptime())


@app.route("/_KARMA")
def _KARMA():
    global FLAGS

   ### Not great as does not take into account that KARMA's is enabled from LCD
    state = request.args.get('state')
    if state=="on":
        print "on"
        p = subprocess.Popen("/rasberryPwnPi/hostapd-1.0-karma/hostapd/hostapd_cli -p /var/run/hostapd karma_enable", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        if p_status == 0:
            FLAGS[1] = True
        
    else:
        print "off"
        p = subprocess.Popen("/rasberryPwnPi/hostapd-1.0-karma/hostapd/hostapd_cli -p /var/run/hostapd karma_disable", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        FLAGS[1] = False
        
        

    return ""


@app.route("/_SSLSTRIP")
def _SSLSTRIP():
    global FLAGS
    retCode = ""
    state = request.args.get('state')
    if state == "on" and FLAGS[1] == True:
        print "on"
        retCode = subprocess.call(["/rasberryPwnPi/scripts/sslstrip_enable.sh"])
        print retCode
        FLAGS[2] = True
        
    else:
        print "off"
        if FLAGS[2] == True:
            retCode = subprocess.call(["/rasberryPwnPi/scripts/sslstrip_disable.sh"])
            
        print retCode
        FLAGS[2] = False


    return ""



@app.route("/_PARSE")
def _PARSE():
    os.system("sudo python /rasberryPwnPi/scripts/log_ex.py %s %s %s %s" % (" /rasberryPwnPi/logPi/sslstrip.log "," -t ", " -o "," /var/www/ssllog/ssllog"))
    
    
    #state = request.args.get('state')
    #if state == "on" :
    #    print "hello"     
    #else:
    #    print "off"
    return ""



# ajax GET call this function periodically to read button state
# the state is sent back as json data


@app.route("/sslstrip_state")
def sslstrip_state():
    if  FLAGS[2] == True:
        state = "On"
    else:
        state = "Off"
    return jsonify(currentState=state)





@app.route("/karma_state")
def _karma_state():    
    global FLAGS

    
    if  FLAGS[1] == True:
        state = "Broadcast On"
    else:
        state = "Broadcast Off"
        
    print "Deeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeebugggggggggggggggggggggggggg"
    print FLAGS
    print hex(id(FLAGS[1]))
    return jsonify(currentState=state)





def GetUptime():
    output = check_output(["uptime"])
    uptime = output[output.find("up"):output.find("user")-5]
    return uptime


###########################  MAIN ###############################################
#################################################################################
#################################################################################

def main(dictionary):
    global FLAGS
    FLAGS = dictionary
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
    
# run the webserver on standard port 80, requires sudo
if __name__ == "__main__":
    main()