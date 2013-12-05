# -*- coding: utf-8 -*-

from flask import Flask
from models import Links
from downloader import Downloader
from autodownload import AutoDownload
import threading

app = Flask(__name__)

app.config['UPDATE_URL'] = 'http://tv.xdream.info/download/'
app.config['AD_USERNAME'] = 'gymgunner@gmail.com'
app.config['AD_PASSWORD'] = '880420'

links = Links(app)
dlock = threading.Lock()
dlock.acquire()


def register_blueprints(app):
    from views import indexs
    app.register_blueprint(indexs)

register_blueprints(app)

def threads():
    ad = AutoDownload(app, links, dlock)
    app.config['AD'] = ad
    dl = Downloader(app, links, dlock)
    app.config['DL'] = dl
    dl.d_thread.start()
    ad.a_thread.start()

threads()

app.debug=False
app.use_reload=False
if __name__ == '__main__':
    app.run()

