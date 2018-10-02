import smtplib
from flask import Flask, request
from flask_cors import CORS
from datetime import datetime
from flask import jsonify


app = Flask(__name__)
CORS(app)
user_notified = False
temp_notify_high = 50.0
temp_notify_low = 10.0
temperature = 15
LED = False
cell_number = '5153210875'
cell_carrier = "verizon"
gateway_lookup = {"verizon": "vtext.com", "at&t": "txt.att.net", "sprint": "pm.sprint.com", "t-mobile": "tmomail.net"}
last_post_time = datetime.now()


@app.route('/cell/<cell>', methods=["POST"])
def set_cell(cell):
    global cell_number
    cell_number = str(cell)
    return 'true'


@app.route('/carrier/<carrier>', methods=["POST"])
def set_carrier(carrier):
    if str(carrier) in gateway_lookup:
        global cell_carrier
        cell_carrier = str(carrier)
        print("CONTAIN")
        return 'true'
    print("EXCLUDE")
    return 'false'


@app.route('/cell', methods=["GET"])
def get_cell():
    return str(cell_number)


@app.route('/carrier', methods=["GET"])
def get_carrier():
    res = {"name": cell_carrier}
    return jsonify(res)

def text_message(message):
    address = str(cell_number) + "@" + gateway_lookup[cell_carrier]
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login("frontendlab138", '$2854888')
    server.sendmail('frontendlab138@gmail.com',  address, message)
    server.quit()



@app.route('/temp', methods=["GET"])
def get_temp():
    diff = datetime.now() - last_post_time
    print(diff.seconds)
    if diff.seconds > 4:
        return "405"
    return str(temperature)


@app.route('/temp/<thermometer>', methods=["POST"])
def set_temp(thermometer):
    global last_post_time
    last_post_time = datetime.now()
    global temperature
    global user_notified
    if thermometer == 'blah':
        thermometer = 404
    temperature = float(thermometer)
    if not temperature == 404:
        if temperature < temp_notify_low or temperature > temp_notify_high:
            if not user_notified:
                text_message("Warning, temperature out of range!\nCurrent temp: " + str(temperature) + "\nCurrent Range:"
                             + str(temp_notify_low) + " to " + str(temp_notify_high))
                user_notified = True
        else:
            user_notified = False
    return 'true'


@app.route('/led', methods=["POST", "GET"])
def led():
    global LED
    if request.method == 'POST':
        if LED:
            LED = False
            return '0'
        else:
            LED = True
            return '1'
    if request.method == 'GET':
        if LED:
            return '1'
        else:
            return '0'


@app.route('/min/<minapi>', methods=["POST"])
def minapi(minapi):
    global temp_notify_low
    if request.method == 'POST':
        temp_notify_low = float(minapi)
        return 'true'


@app.route('/max/<maxapi>', methods=["POST"])
def maxapi(maxapi):
    global temp_notify_high
    if request.method == 'POST':
        temp_notify_high = float(maxapi)
        return 'true'


@app.route('/max', methods=["GET"])
def get_max():
    return str(temp_notify_high)


@app.route('/min', methods=["GET"])
def get_min():
    return str(temp_notify_low)

if __name__ == '__main__':
    app.run(host='0.0.0.0')


