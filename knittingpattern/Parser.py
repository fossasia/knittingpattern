
# attributes

ID = "id"
NAME = "name"
TYPE = "type"
VERSION = "version"
INSTRUCTIONS = "instructions"
SAME_AS = "same as"

# constants

KNITTING_PATTERN_TYPE = "knitting pattern"


class ParsingError(ValueError):
    pass


class Parser(object):

    def __init__(self, knitting_context):
        self.knitting_context = knitting_context
        self.instruction_library = self.knitting_context.DefaultInstructions()
        self._id_cache = {}

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
        inheritance = []
        if SAME_AS in values:
            _id = self.to_id(values[SAME_AS])
            object = self._id_cache[_id]
            inheritance.append(object)
        row = self.knitting_context.Row(id, values, inheritance)
        for instruction_specification in row.get(INSTRUCTIONS, []):
            instruction = self.instruction(row, instruction_specification)
            row.instructions.append(instruction)
        self._id_cache[id] = row
        return row
        
    def instruction(self, row, instruction_specification):
        whole_instruction_specification = \
            self.instruction_library.as_instruction(instruction_specification)
        return self.knitting_context.InstructionInRow(
                        row, whole_instruction_specification)

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
