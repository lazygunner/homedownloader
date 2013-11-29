from downloader import Downloader
import threading
import time

class Test(object):
    
    def __init__(self):
        self.dl = None
    
    def check_thread(self):
        while True:
            print self.dl.current_percent + '%  ' + self.dl.current_speed + '  ' + self.dl.current_eta
            time.sleep(5)

    def test(self):
        app = ''
        self.dl = Downloader(app)
    
        t = threading.Thread(target=self.check_thread, args=())
        t.start()

        ret = self.dl.download_link('ed2k://|file|%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8.The.Big.Bang.Theory.S07E09.%E4%B8%AD%E8%8B%B1%E5%AD%97%E5%B9%95.HDTVrip.1024X576.mkv|227921591|6aabbc235565b45935da37f1485d157f|h=zxig5py6v4bde4ygwrzbjuvptrfttitw|/')

        print 'error:' + ret

t = Test()
t.test()
