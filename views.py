from flask import Blueprint, request, render_template
from homedownloader import app

indexs = Blueprint('index', __name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    print 'haha'
    return render_template('index.html')
    

