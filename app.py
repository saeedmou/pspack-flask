import os
import time
from flask import Flask, render_template, request
from urllib.parse import unquote_plus
from sender import send
# from switcher import myLED, myLEDOn, myLEDOff, myLED1On, myLED1Off
from switcher import relay, led
app = Flask(__name__)


@app.route('/')
def index():
    ua = request.headers.get("User-Agent", None)
    try:
        if ua:
            ua_part = ua[ua.index("PlayStation 4/") + len("PlayStation 4/"):]
            ua_part = ua_part[:ua_part.index(")")]
    except ValueError:
        print("Not PS4")
        ua_part = ua

    return render_template("index.html", version=ua_part)

@app.route('/menu')
def menu():
    ua = request.headers.get("User-Agent", None)
    return render_template("menu.html")

@app.route("/relay/on")
def relayOnHandler():   
    return relay(True)

@app.route("/relay/off")
def relayOffHandler():   
    return relay(False)

@app.route("/led/1/on")
def led1OnHandler():   
    return led(1,True)

@app.route("/led/1/off")
def led1OffHandler():   
    return led(1,False)

@app.route("/led/2/on")
def led2OnHandler():   
    return led(2,True)

@app.route("/led/2/off")
def led2OffHandler():   
    return led(2,False)

@app.route("/log/<msg>")
def log(msg):
    msg = unquote_plus(msg)
    if "done" in msg or "already" in msg:
        # success message, send HEN
        time.sleep(1)
        print(f"Sending golden hen to {request.remote_addr}")
        #myLED()
        send(request.remote_addr, 9020, "payload/goldhen_2.0b_900.bin")

    print(msg)
    return "OK"

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
    app.run(host='0.0.0.0', port=1337)
