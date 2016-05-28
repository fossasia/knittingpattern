import json
import urllib

class Loader(object):

    def __init__(self, process):
        self.process = process

    def object(self, obj):
        return self.process(obj)

    def string(self, json_string):
        obj = json.loads(json_string)
        return self.object(obj)

    def file(self, file):
        obj = json.load(file)
        return self.object(obj)

    def path(self, path):
        with open(path) as file:
            return self.file(file)

    def url(self, url, encoding="UTF-8"):
        import urllib.request
        with urllib.request.urlopen(url) as file:
            json = file.read()
        json = json.decode(encoding)
        return self.string(json)