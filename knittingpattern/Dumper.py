

class ContentDumper(object):

    def __init__(self, on_dump):
        self.on_dump = on_dump
    
    def string(self):
        pass
        
class DumpToString(object):
    
    def prefers_string(self):
        return True
        
    def prefers_file(self):
        return False


class DumpToFile(object):
    
    def prefers_string(self):
        return False
        
    def prefers_file(self):
        return True
