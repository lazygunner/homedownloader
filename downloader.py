import sys
import subprocess
import os
import re
import time

class Downloader(object):
    pipe = None
    is_downloading = False
    out_dir = "downloads\\"
    lx_path = os.path.join(os.path.dirname(__file__), 'xunlei-lixian/lixian_cli.py').replace('\\', '/')
    current_percent = '0'
    current_speed = '0'
    current_eta = '0'


    def __init__(self, app):
        pass

    def download_link(self, link):
        if self.is_downloading == False:
            self.is_downloading = True
        else:
            return 'is_downloading'

        try:
           
            self.pipe = subprocess.Popen(
                [sys.executable, '-u',self.lx_path, "download", link,\
                "-c", "--output-dir", self.out_dir], shell=False,\
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
                self.pipe.stderr.flush()
            elif re.search(r'.*?completed\..*', data) != None:
                self.current_percent = '100'
                self.pipe = None
                self.is_downloading = False
                return 'finished'
            else:
                pass
            self.pipe.stderr.flush()
            data=self.pipe.stderr.readline()



        
