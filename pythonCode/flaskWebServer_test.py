#!/usr/bin/python
#
#
from flask import Flask, render_template, request, jsonify
from subprocess import check_output
import logging
import subprocess
from multiprocessing import Process, Value, Array, Manager


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
FLAG_KARMA_BROADCAST =""

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
    global FLAG_KARMA_BROADCAST
   
   
   ### Not great as does not take into account that KARMA's is enabled from LCD
    state = request.args.get('state')
    if state=="on":
        print "on"
        p = subprocess.Popen("/rasberryPwnPi/hostapd-1.0-karma/hostapd/hostapd_cli -p /var/run/hostapd karma_enable", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        if p_status == 0:
            FLAG_KARMA_BROADCAST[1] = True
        
    else:
        print "off"
        p = subprocess.Popen("/rasberryPwnPi/hostapd-1.0-karma/hostapd/hostapd_cli -p /var/run/hostapd karma_disable", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        FLAG_KARMA_BROADCAST[1] = False
        
        

    return ""


@app.route("/_ATT2")
def __ATT2():
    global counter
    global attackTwo
    state = request.args.get('state')
    if state == "on":
        counter+=1
        attackTwo = True
    else:
        counter-=1
        attackTwo = False
    print attackTwo
    print counter
    return ""
    
# ajax GET call this function periodically to read button state
# the state is sent back as json data


@app.route("/currentState")
def _currentState():
    if  attackTwo == True:
        state = "Attack On"
    else:
        state = "Attack Off"
    return jsonify(currentState=state)


@app.route("/karma_state")
def _karma_state():    
    global FLAG_KARMA_BROADCAST

    
    if  FLAG_KARMA_BROADCAST[1] == True:
        state = "Broadcast On"
    else:
        state = "Broadcast Off"
        
    print "Deeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeebugggggggggggggggggggggggggg"
    print FLAG_KARMA_BROADCAST
    print hex(id(FLAG_KARMA_BROADCAST))
    return jsonify(currentState=state)

def GetUptime():
    output = check_output(["uptime"])
    uptime = output[output.find("up"):output.find("user")-5]
    return uptime

def main(dictionary):
    global FLAG_KARMA_BROADCAST
    FLAG_KARMA_BROADCAST = dictionary
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
    
# run the webserver on standard port 80, requires sudo
if __name__ == "__main__":
    main()