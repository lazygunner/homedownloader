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
                    print link_obj
                    time.sleep(5)
                else:
                    ret = self.download_link(link_obj)
                    print ret
                    if ret == 'finished':
                        if(self.link_obj['type'] == 'ad'):
                            index_int = int(link_obj['index'])
                            s = index_int / 100
                            e = index_int - s
                            l_s = str(s)
                            l_e = str(e)
                            self.ad.post_download_status(
                                link_obj['show_id'], l_s=l_s, l_e=l_e)

                        self.links.pop()

            else:
                print 'empty'
                try:
                    self.dlock.release()
                except threading.ThreadError:
                    print 'non lock'
                    time.sleep(10)

    def download_link(self, link_obj):
        print 'download_link'
        if self.is_downloading == False:
            self.is_downloading = True
        else:
            return 'is_downloading'

        try:
           
            self.pipe = subprocess.Popen(
                [sys.executable, '-u',self.lx_path, "download",\
                link_obj['ed2k_link'], "-c", "--output-dir",\
                self.out_dir], shell=False,\
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            ret = 'lixian_cli_error'

        #wget status: 28% 123K 20m8s
        pattern = re.compile(
            r'(?P<per>\d{1,2})%\s*(?P<speed>.*?)\s(?P<eta>\w*)'
            )
        data=self.pipe.stderr.readline()
        while data: 
#            print data
            m = pattern.search(data)
            if m:
                self.current_percent = m.group('per')
                self.current_speed = m.group('speed')
                self.current_eta = m.group('eta')
                self.current_status = 'ing'
                self.pipe.stderr.flush()
            elif re.search(r'.*?completed\..*', data) != None:
                self.current_percent = '100'
                self.pipe = None
                self.is_downloading = False
                self.current_status = 'complete'
                return 'finished'
            else:
                self.current_percent = '0'
                self.current_speed = '0'
                self.current_eta = '0'
                self.current_status = 'error'
            
            self.pipe.stderr.flush()
            data=self.pipe.stderr.readline()



        
