
import requests
import json
import threading


class AutoDownload(object):
    
    def __init__(self, app, links, dlock):
        self.links = links
        self.dlock = dlock
        self.uri = app.config['UPDATE_URL']
        self.username = app.config['AD_USERNAME']
        self.password = app.config['AD_PASSWORD']
        self.a_thread = threading.Thread(target=self.auto_thread,\
            name='auto_thread')
        self.headers = {"Content-Type":"application/json"}
    def get_updates(self):
        #data = json.dumps({"email":"gymgunner@gmail.com"})

        r = requests.get(self.uri + 'download/', auth=(self.username, self.password))
        
        if(r.status_code == 200):
            updates = json.loads(r.text)
        else:
            updates = []

        return updates
        
    def post_download_status(self, show_id, l_e, l_s):
        data = json.dumps({"l_s":l_s, "l_e":l_e})
        r = requests.post(self.uri + 'download/' + show_id, data=data, headers=self.headers, auth=(self.username, self.password))
        if r.status_code != 404:
            return 'update_ok'
    
    def post_dl_completed(self, link):
        data = json.dumps({'link':link})
        print self.uri + ' ' + data
        r = requests.post(self.uri + 'completed/', data=data, headers=self.headers, auth=(self.username, self.password))
        print r.text
        if r.status_code != 404:
                return 'complete'

    def auto_thread(self):
        while True:
            self.dlock.acquire()
            print 'auto down'
            updates = self.get_updates()
            print updates
            self.links.add_links_from_ad(updates)
            
