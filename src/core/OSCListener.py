import time
from .tinyoscquery.query import OSCQueryBrowser, OSCQueryClient

class OSCListener:
    def __init__(self):
        browser = OSCQueryBrowser()
        time.sleep(2) # Wait for discovery
        self.service_info = browser.find_service_by_name("VRChat-Client")
        self.client = OSCQueryClient(self.service_info)

    def getHostInfo(self):
        return  self.client.get_host_info()
        
    def getAvatarID(self):
        node = self.client.query_node("/avatar/change")
        return node.value[0]
    
    def getMuteSelf(self):
        node = self.client.query_node("/avatar/parameters/MuteSelf")
        return node.value[0]
