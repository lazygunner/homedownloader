# -*- coding: utf-8 -*-

from flask import Flask
from models import Links
from downloader import Downloader
from autodownload import AutoDownload
import threading

app = Flask(__name__)

app.config['UPDATE_URL'] = 'http://tv.xdream.info/download/'

links = Links(app)
dlock = threading.Lock()
dlock.acquire()


def register_blueprints(app):
    from views import indexs
    app.register_blueprint(indexs)

register_blueprints(app)

def threads():
    ad = AutoDownload(app, links, dlock)
    dl = Downloader(app, links, dlock)
    dl.d_thread.start()
    ad.a_thread.start()
    app.config['DL'] = dl

threads()

app.debug=False
app.use_reload=False
if __name__ == '__main__':
    app.run()

