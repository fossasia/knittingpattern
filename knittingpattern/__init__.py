import json


__version__ = '0.0.1'


class KnittingPattern(object):

    def __init__(self, pattern):
        self.pattern = pattern

    @property
    def version(self):
        return self.pattern["version"]

    @property
    def type(self):
        return self.pattern["type"]

    @classmethod
    def load_from_object(cls, obj):
        return cls(obj)

    @classmethod
    def load_from_string(cls, json_string):
        return cls.load_from_object(json.loads(json_string))

    @classmethod
    def load_from_file(cls, file):
        return cls.load_from_object(json.load(file))

    @classmethod
    def load_from_path(cls, path):
        with open(path) as file:
            return cls.load_from_file(file)


load_from_object = KnittingPattern.load_from_object
load_from_string = KnittingPattern.load_from_string
load_from_file = KnittingPattern.load_from_file
load_from_path = KnittingPattern.load_from_path
