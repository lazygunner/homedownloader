import sys
import threading 

class Links(object):
    
    def __init__(self, app):
        self.link_list = []
        self.llock = threading.Lock()

    # add the links from autodownloader
    def add_links_from_ad(self, links):
        self.llock.acquire()
        for link in links:
            link['type'] = 'ad'
            self.link_list.append(link)
        self.llock.release()

    def get_list_top(self):
        try:
            self.llock.acquire()
            print len(self.link_list)
            link_obj = self.link_list.pop(0)
            if(link_obj['type'] == 'ad'):
                link = link_obj['ed2k_link']
                if(link != ''):
                    #reinsert the link to list to prevent lost
                    self.link_list.insert(0, link_obj)
                else:
                    link_obj = 'invalid_link'
            else:
                link_obj = 'invalid_type'
        except:
            link_obj = 'list_empty'
            print "Unexpected error:", sys.exc_info()
        finally:
            self.llock.release()
            return link_obj
    
    # after the download finished of the top link
    def pop_top(self):
        return links.pop(0)
