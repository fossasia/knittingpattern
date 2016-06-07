from ..Loader import ContentLoader
import os

class Instruction(object):
    
    def __init__(self, spec):
        self._spec = spec
        self.load_image = ContentLoader(
                self._set_raw_image, 
                self._chooses_file
            )
        
    @property
    def type(self):
        return self._spec["type"]
    
    def _set_raw_image(self, image):
        self.raw_image = image
        
    def _chooses_file(self, path):
        return path.endswith(self.type + ".svg")