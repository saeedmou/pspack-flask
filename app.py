import time
import threading 
from flask import Flask, render_template, request
from urllib.parse import unquote_plus
from sender import send
from server import servercommander
# from switcher import myLED, myLEDOn, myLEDOff, myLED1On, myLED1Off
from switcher import relay, led
import os.path
app = Flask(__name__)

@app.route('/')
def menu():
    ua = request.headers.get("User-Agent", None)
    return render_template("menu.html")


@app.route('/jb')
def index():
    ua = request.headers.get("User-Agent", None)
    try:
        if ua:
            ua_part = ua[ua.index("PlayStation 4/") + len("PlayStation 4/"):]
            ua_part = ua_part[:ua_part.index(")")]
    except ValueError:
        print("Not PS4")
        ua_part = ua
    relay(False)
    return render_template("jb.html", version=ua_part)


@app.route("/relay/<val>")
def relayHandler(val): 
    return relay(val=="on" or val=="1")

@app.route("/led/<int:ind>/<val>")
def ledHandler(ind,val):   
    return led(ind,val=="on" or val=="1")

@app.route("/payload/<pname>")
def payloadsender(pname):
    pname = unquote_plus(pname)
    payloadurl="payload/" +pname
    send(request.remote_addr, 9090, payloadurl)
    print(pname)
    return "OK"

@app.route("/server/<cmd>")
def servercommanderHandler(cmd):
    cmd = unquote_plus(cmd)
    return servercommander(cmd)

@app.route("/log/<msg>")
def log(msg):
    payloadPath='payload/goldhen/GoldHEN-2.2.2/goldhen_2.2.2_900.bin'
    # payloadPath='payload/goldhen/GoldHEN-2.1.1/goldhen_2.1.1_900.bin'
    if(request.args.get('payloadName')):
        print(request.args.get('payloadName'))
        payloadPath=request.args.get('payloadName')
    msg = unquote_plus(msg)
    if "done" in msg or "already" in msg:
        # success message, send HEN
        time.sleep(1)
        relay(False)
        print(f"Sending golden hen to {request.remote_addr}")
        send(request.remote_addr, 9020, payloadPath)
    elif "success!" in msg:
        #Deattach the USB
        time.sleep(1)
        relay(False)
    elif "failed" in msg:
        time.sleep(1)
        relay(False)
    elif "ready" in msg:
        #Attach the USB Flash
        time.sleep(1)
        relay(True)
        start_time = threading.Timer(60,timeoutRelayOff)
        start_time.start()
    print(msg)
    return "OK"

@app.route("/GoldHEN/<fName>")
def GoldHENFunction(fName):
    fName = unquote_plus(fName)
    bPath= "payload/goldhen/GoldHEN-2.2.2/"
    fPath=bPath + fName + '.md'
    file_exists = os.path.exists(fPath)
    if (file_exists):
        f = open(fPath,'r')
        string = ""
        while 1:
            line = f.readline()
            if not line:break
            string += line +"</br>"
        f.close()
    else:
        string = "Not Found!"
    return string

def timeoutRelayOff():         # user defined function which adds +10 to given numbe
    print ("Timeout call")
    relay(False)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    led(2,True)
    app.run(host='0.0.0.0', port=1337)
