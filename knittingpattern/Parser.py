
# attributes

ID = "id"
NAME = "name"
TYPE = "type"
VERSION = "version"

# constants

KNITTING_PATTERN_TYPE = "knitting pattern"


class ParsingError(ValueError):
    pass


class Parser(object):

    def __init__(self, knitting_context):
        self.knitting_context = knitting_context

    @staticmethod
    def to_id(id):
        return tuple(id) if isinstance(id, list) else id

    def error(self, text):
        raise self.knitting_context.ParsingError(text)

    def parse(self, values):
        self.values = values
        self.create_pattern_collection()
        self.fill_pattern_collection()
        self.create_pattern_set()
        return self.pattern_set

    def create_pattern_collection(self):
        self.pattern_collection = self.knitting_context.PatternCollection()

    def fill_pattern_collection(self):
        pattern = self.values.get("pattern", [])
        for pattern_to_parse in pattern:
            parsed_pattern = self.new_pattern(pattern_to_parse)
            self.pattern_collection.append(parsed_pattern)

    def parse_row(self, values):
        id = self.to_id(values[ID])
        return self.knitting_context.Row(id)

    def new_pattern(self, base):
        rows = self.knitting_context.RowCollection()
        for row in base.get("rows", []):
            rows.append(self.parse_row(row))
        id = self.to_id(base[ID])
        name = base[NAME]
        return self.knitting_context.Pattern(id, name, rows)

    def get_type(self):
        if TYPE not in self.values:
            self.error("No pattern type given but should be "
                       "\"{}\"".format(KNITTING_PATTERN_TYPE))
        type = self.values[TYPE]
        if type != KNITTING_PATTERN_TYPE:
            self.error("Wrong pattern type. Type is \"{}\" "
                       "but should be \"{}\""
                       "".format(type, KNITTING_PATTERN_TYPE))
        return type

    def get_version(self):
        return self.values[VERSION]

    def create_pattern_set(self):
        type = self.get_type()
        version = self.get_version()
        pattern = self.pattern_collection
        self.pattern_set = self.knitting_context.PatternSet(
                                    type, version, pattern)


__all__ = ["PatternParser"]
