
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

    def knitting_pattern_set(self, values):
        pattern_collection = self.new_pattern_collection()
        self.fill_pattern_collection(pattern_collection, values)
        self.create_pattern_set(pattern_collection, values)
        return self.pattern_set

    def new_pattern_collection(self):
        return self.knitting_context.PatternCollection()

    def new_row_collection(self):
        return self.knitting_context.RowCollection()

    def fill_pattern_collection(self, pattern_collection, values):
        pattern = values.get("pattern", [])
        for pattern_to_parse in pattern:
            parsed_pattern = self.pattern(pattern_to_parse)
            pattern_collection.append(parsed_pattern)

    def row(self, values):
        id = self.to_id(values[ID])
        return self.knitting_context.Row(id)

    def pattern(self, base):
        rows = self.new_row_collection()
        for row in base.get("rows", []):
            rows.append(self.row(row))
        id = self.to_id(base[ID])
        name = base[NAME]
        return self.knitting_context.Pattern(id, name, rows)

    def get_type(self, values):
        if TYPE not in values:
            self.error("No pattern type given but should be "
                       "\"{}\"".format(KNITTING_PATTERN_TYPE))
        type = values[TYPE]
        if type != KNITTING_PATTERN_TYPE:
            self.error("Wrong pattern type. Type is \"{}\" "
                       "but should be \"{}\""
                       "".format(type, KNITTING_PATTERN_TYPE))
        return type

    def get_version(self, values):
        return values[VERSION]

    def create_pattern_set(self, pattern, values):
        type = self.get_type(values)
        version = self.get_version(values)
        self.pattern_set = self.knitting_context.PatternSet(
                                    type, version, pattern)


__all__ = ["PatternParser"]
