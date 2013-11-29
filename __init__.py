# -*- coding: utf-8 -*-

from flask import Flask




app = Flask(__name__)

def register_blueprints(app):
    from views import indexs
    app.register_blueprint(indexs)

register_blueprints(app)

app.debug = True

if __name__ == '__main__':
    app.run
