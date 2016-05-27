import json


__version__ = '0.0.1'


TYPE = "type"
VERSION = "version"
KNITTING_PATTERN_TYPE = "knitting pattern"


class KnittingPattern(object):

    def __init__(self, pattern):
        self.pattern = pattern
        if TYPE not in self.pattern:
            raise ValueError("No pattern type given but should be "
                             "\"{}\"".format(KNITTING_PATTERN_TYPE))
        if self.type != KNITTING_PATTERN_TYPE:
            raise ValueError("Wrong pattern type. Type is \"{}\" "
                             "but should be \"{}\""
                             "".format(self.type, KNITTING_PATTERN_TYPE))

    @property
    def version(self):
        return self.pattern[VERSION]

    @property
    def type(self):
        return self.pattern[TYPE]

    @classmethod
    def load_from_object(cls, obj):
        return cls(obj)

    @classmethod
    def load_from_string(cls, json_string):
        obj = json.loads(json_string)
        return cls.load_from_object(obj)

    @classmethod
    def load_from_file(cls, file):
        obj = json.load(file)
        return cls.load_from_object(obj)

    @classmethod
    def load_from_path(cls, path):
        with open(path) as file:
            return cls.load_from_file(file)

    @classmethod
    def load_from_url(cls, url, encoding="UTF-8"):
        import urllib.request
        with urllib.request.urlopen(url) as file:
            json = file.read()
        json = json.decode(encoding)
        return cls.load_from_string(json)


load_from_object = KnittingPattern.load_from_object
load_from_string = KnittingPattern.load_from_string
load_from_file = KnittingPattern.load_from_file
load_from_path = KnittingPattern.load_from_path
load_from_url = KnittingPattern.load_from_url
