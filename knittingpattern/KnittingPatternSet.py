import json
from .PatternParser import PatternParser

TYPE = "type"
VERSION = "version"
KNITTING_PATTERN_TYPE = "knitting pattern"

class KnittingPatternSet(object):

    def __init__(self, pattern_set):
        self.pattern_set = pattern_set
        if TYPE not in self.pattern_set:
            raise ValueError("No pattern type given but should be "
                             "\"{}\"".format(KNITTING_PATTERN_TYPE))
        if self.type != KNITTING_PATTERN_TYPE:
            raise ValueError("Wrong pattern type. Type is \"{}\" "
                             "but should be \"{}\""
                             "".format(self.type, KNITTING_PATTERN_TYPE))
        self._pattern = self._parse()

    @property
    def version(self):
        return self.pattern_set[VERSION]

    @property
    def type(self):
        return self.pattern_set[TYPE]

    @property
    def pattern(self):
        return self._pattern

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

    def _parse(self):
        parser = PatternParser(self, self.pattern_set)
        return parser.parse()

            
__all__ = ["KnittingPatternSet"]
