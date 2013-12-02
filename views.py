from flask import Blueprint, request, render_template
from homedownloader import app
import json

indexs = Blueprint('index', __name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/check', methods=['GET'])
def check():
    dl = app.config['DL']
    status = {}
    status['per'] = dl.current_percent
    status['speed'] = dl.current_speed
    status['eta'] = dl.current_eta
    status['status'] = dl.current_status

    return json.dumps(status)
    

