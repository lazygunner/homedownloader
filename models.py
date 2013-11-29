

class Links(objects):
    
    def __init__(self):
        self.link_list = []

    # add the links from autodownloader
    def add_links_from_ad(self, links):
        self.link_list.append(map(lambda link:link['type']='ad', links))

    def get_list_top():
        try:
            link_obj = links.pop(0)
            if(link_obj['type'] == 'ad'):
                link = link_obj['ed2k_link']
                if(link != ''):
                    #reinsert the link to list to prevent lost
                    links.insert(0, link)
                    return link
                else:
                    return 'invalid_link'
             else:
                return 'invalid_type'

         except:
            return 'list_empty'
    
    # after the download finished of the top link
    def pop_top():
        return links.pop(0)
