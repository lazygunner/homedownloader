import sys
import subprocess
import os
import re
import time
import threading

from autodownload import AutoDownload

class Downloader(object):
    pipe = None
    is_downloading = False
    out_dir = "downloads\\"
    lx_path = os.path.join(os.path.dirname(__file__), 'xunlei-lixian/lixian_cli.py').replace('\\', '/')
    current_percent = '0'
    current_speed = '0'
    current_eta = '0'
    current_status = ''


    def __init__(self, app, links, dlock):
        
        self.links = links
        self.dlock = dlock
        self.ad = app.config['AD']
        self.d_thread = threading.Thread(target=self.download_thread,\
            name='download_thread')
    
    def download_thread(self):
        while True:
            if len(self.links.link_list) > 0:
                link_obj = self.links.get_list_top()
                if link_obj.__class__ == type('str'):
                    time.sleep(5)
                else:
                    ret = self.download_link(link_obj)
                    print 'ret:' + ret
                    time.sleep(10)
                    if ret == 'finished':
                        print link_obj
                        if(link_obj['type'] == 'ad'):
                            index_int = int(link_obj['index'])
                            s = index_int / 100
                            e = index_int - s
                            l_s = str(s)
                            l_e = str(e)
                            self.ad.post_download_status(
                                link_obj['show_id'], l_s=l_s, l_e=l_e)
                        else:
                            self.ad.post_dl_completed(link_obj['ed2k_link'])
                        self.links.pop_top()
                        self.pipe = None
                        self.is_downloading = False
                    elif ret == 'no_resp':
                        self.links.pop_top()
                        self.pipe = None
                        self.is_downloading = False

            else:
                print 'empty'
                try:
                    self.dlock.release()
                    time.sleep(10)
                except threading.ThreadError:
                    print 'non lock'
                    time.sleep(10)

    def download_link(self, link_obj):
        print 'download_link'
        if self.is_downloading == False:
            self.is_downloading = True
        else:
            return 'is_downloading'

        link = link_obj['ed2k_link']
        try:
            if re.search(r'http://', link) == None:            
                self.pipe = subprocess.Popen(
                    [sys.executable, '-u',self.lx_path, "download",\
                    link_obj['ed2k_link'], "-c", "--output-dir",\
                    self.out_dir], shell=False,\
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                self.pipe = subprocess.Popen(
                    ["wget", link, "-c", "-P", self.out_dir],\
                    shell=False, stdout=subprocess.PIPE,\
                    stderr= subprocess.PIPE)
        except:
            ret = 'lixian_cli_error'

        #wget status: 28% 123K 20m8s
        pattern = re.compile(
            r'(?P<per>\d{1,2})%\s*(?P<speed>.*?)\s(?P<eta>\w*)'
            )
        data=self.pipe.stderr.readline()
        count = 5
        while data: 
            print 'ori' + data
            
            m = pattern.search(data)
            if m:
                self.current_percent = m.group('per')
                self.current_speed = m.group('speed')
                self.current_eta = m.group('eta')
                self.current_status = 'ing'
                self.pipe.stderr.flush()
            elif re.search(r'\[(?P<size>\d*)/(?P=size)\]', data) != None or\
                    re.search(r'.*?bigger than expected.*?', data) != None:
                print 'fi:' + data
                self.current_percent = '100'
                self.current_status = 'complete'
                return 'finished'
            else:
                self.current_percent = '0'
                self.current_speed = '0'
                self.current_eta = '0'
                self.current_status = 'error'
                print 'error:' + data
            
            self.pipe.stderr.flush()
            data=self.pipe.stderr.readline()

        if data == '':
            return 'no_resp'

        
