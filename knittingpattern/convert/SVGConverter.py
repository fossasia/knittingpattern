

class SVGConverter(object):
    def __init__(self, file):
        self.file = file

    def __enter__(self):
        pass

    def __exit__(self, type=None, error=None, traceback=None):
        pass
        
    def open(self):
        pass
        
    @property
    def beginning_of_file(self):
        pass
    
    def close(self):
        pass
        
    @property
    def end_of_file(self):
        pass

    def render_at(self, x, y, svg, group_id):
        pass
