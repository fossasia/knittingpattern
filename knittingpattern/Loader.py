import json
import os
import sys
from itertools import filterfalse


def do_not_process(object):
    return object
    
def choose_everything(object):
    return True

class ContentLoader(object):
    
    def __init__(self, process=do_not_process, chooses_path=choose_everything):
        self.process = process
        self.chooses_path = chooses_path
        
    def object(self, obj):
        return self.process(obj)

    def string(self, string):
        obj = self.convert_to_processable_object(string)
        return self.object(obj)

    def file(self, file):
        string = file.read()
        return self.string(string)
        
    def convert_to_processable_object(self, string):
        return string

    def path(self, path):
        with open(path) as file:
            return self.file(file)

    def url(self, url, encoding="UTF-8"):
        import urllib.request
        with urllib.request.urlopen(url) as file:
            webpage_content = file.read()
        webpage_content = webpage_content.decode(encoding)
        return self.string(webpage_content)

    def folder(self, folder):
        result = []
        for root, directories, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                if self.chooses_path(path):
                    result.append(self.path(path))
        return result

    def _relative_to_absolute(self, module_location, folder):
        if os.path.isfile(module_location):
            path = os.path.dirname(module_location)
        elif os.path.isdir(module_location):
            path = module_location
        else:
            __import__(module_location)
            module = sys.modules[module_location]
            path = os.path.dirname(module.__file__)
        absolute_path = os.path.join(path, folder)
        return absolute_path

    def relative_folder(self, module, folder):
        folder = self._relative_to_absolute(module, folder)
        return self.folder(folder)

    def relative_file(self, module, file):
        path = self._relative_to_absolute(module, file)
        return self.path(path)
    
    def choose_paths(self, paths):
        return [path for path in paths if self.chooses_path(path)]
        

class JSONLoader(ContentLoader):

    def convert_to_processable_object(self, string):
        return json.loads(string)


        
        


__all__ = ["JSONLoader", "ContentLoader"]
