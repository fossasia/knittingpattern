"""In this module you can find the parsing of knitting pattern structures

"""
# attributes

ID = "id"  #: the id of a row, an instruction or a pattern
NAME = "name"  #: the name of a row
TYPE = "type"  #: the type of an instruction or the knitting pattern set
VERSION = "version"  #: the version of a knitting pattern set
INSTRUCTIONS = "instructions"  #: the instructions in a row
SAME_AS = "same as"  #: pointer to a inherit from
PATTERNS = "patterns"  #: the patterns in the knitting pattern set
ROWS = "rows"  #: the rows inside a pattern
CONNECTIONS = "connections"  #: the connections in a pattern
FROM = "from"  #: the position and row a connection comes from
TO = "to"  #: the position and row a connection goes to
START = "start"  #: the mesh index the connection starts at
#: the default mesh index the connection starts at if none is given
DEFAULT_START = 0
MESHES = "meshes"  #: the number of meshes of a connection
COMMENT = "comment"  #: a comment of a row, an instruction, anything

# constants

#: the default type of the knitting pattern set
KNITTING_PATTERN_TYPE = "knitting pattern"


class ParsingError(ValueError):
    """This Error is raised if there is an error during the parsing for
    :class:`~knittingpattern.Parser.Parser`"""
    pass


class Parser(object):
    """parse a knitting pattern set and anything in it"""

    def __init__(self, specification):
        """Create a parser with a specification

        :param specification: the types and classes to use for the resulting
          object structure, preferably a
          :class:`knittingpattern.ParsingSpecification.ParsingSpecification`

        """
        self._specification = specification
        self._start()

    def _start(self):
        """initialize the parsing process"""
        self._instruction_library = self._specification.DefaultInstructions()
        self._id_cache = {}
        self._pattern_set = None

    @staticmethod
    def _to_id(id):
        """:return: a hashable object"""
        return tuple(id) if isinstance(id, list) else id

    def _error(self, text):
        """:raises: a specified ParsingError

        :param str text: the text to include in the error message
        """
        raise self._specification.ParsingError(text)

    def knitting_pattern_set(self, values):
        """parses a
        :class:`~knittingpattern.KnittingPatternSet.KnittingPatternSet`

        :param dict value: the specification of the knitting pattern set
        :rtype: knittingpattern.KnittingPatternSet.KnittingPatternSet
        :raises knittingpattern.KnittingPatternSet.ParsingError: if
          :paramref:`value` does not fulfill the :ref:`specification
          <FileFormatSpecification>`.

        """
        self._start()
        pattern_collection = self._new_pattern_collection()
        self._fill_pattern_collection(pattern_collection, values)
        self._create_pattern_set(pattern_collection, values)
        return self._pattern_set

    def _new_pattern_collection(self):
        """:return: a new specified PatternCollection for
          :meth:`knitting_pattern_set`"""
        return self._specification.PatternCollection()

    def _new_row_collection(self):
        """:return: a new specified RowCollection for
          :meth:`pattern`"""
        return self._specification.RowCollection()

    def _fill_pattern_collection(self, pattern_collection, values):
        """fills a pattern collection"""
        pattern = values.get(PATTERNS, [])
        for pattern_to_parse in pattern:
            parsed_pattern = self._pattern(pattern_to_parse)
            pattern_collection.append(parsed_pattern)

    def _row(self, values):
        """parses a row"""
        id = self._to_id(values[ID])
        inheritance = []
        if SAME_AS in values:
            _id = self._to_id(values[SAME_AS])
            object = self._id_cache[_id]
            inheritance.append(object)
        row = self._specification.Row(id, values, inheritance)
        for instruction_ in row.get(INSTRUCTIONS, []):
            instruction = self._instruction(row, instruction_)
            row.instructions.append(instruction)
        self._id_cache[id] = row
        return row

    def _instruction(self, row, instruction_):
        """parses an instruction"""
        whole_instruction_ = \
            self._instruction_library.as_instruction(instruction_)
        return self._specification.InstructionInRow(
                        row, whole_instruction_)

    def _pattern(self, base):
        """parses a pattern"""
        rows = self._rows(base.get(ROWS, []))
        self._connect_rows(base.get(CONNECTIONS, []))
        id = self._to_id(base[ID])
        name = base[NAME]
        return self._specification.Pattern(id, name, rows)

    def _rows(self, spec):
        """parses a collection of rows"""
        rows = self._new_row_collection()
        for row in spec:
            rows.append(self._row(row))
        return rows

    def _connect_rows(self, connections):
        """connects the parsed rows"""
        for connection in connections:
            from_row_id = self._to_id(connection[FROM][ID])
            from_row = self._id_cache[from_row_id]
            from_row_mesh_index = connection[FROM].get(START, DEFAULT_START)
            to_row_id = self._to_id(connection[TO][ID])
            to_row = self._id_cache[to_row_id]
            to_row_mesh_index = connection[TO].get(START, DEFAULT_START)
            meshes = min(from_row.number_of_produced_meshes,
                         to_row.number_of_produced_meshes)
            number_of_meshes = connection.get(MESHES, meshes)
            from_row._produce_number_of_meshes_for_row(
                    from_row_mesh_index,
                    from_row_mesh_index + number_of_meshes,
                    to_row,
                    to_row_mesh_index
                )

    def _get_type(self, values):
        """returns the type of a knitting pattern set"""
        if TYPE not in values:
            self._error("No pattern type given but should be "
                        "\"{}\"".format(KNITTING_PATTERN_TYPE))
        type = values[TYPE]
        if type != KNITTING_PATTERN_TYPE:
            self._error("Wrong pattern type. Type is \"{}\" "
                        "but should be \"{}\""
                        "".format(type, KNITTING_PATTERN_TYPE))
        return type

    def _get_version(self, values):
        """::return: the version of :paramref:`values`"""
        return values[VERSION]

    def _create_pattern_set(self, pattern, values):
        """Creates a new pattern set."""
        type = self._get_type(values)
        version = self._get_version(values)
        comment = values.get(COMMENT)
        self._pattern_set = self._specification.PatternSet(
                type, version, pattern, comment
            )

__all__ = ["Parser", "ID", "NAME", "TYPE", "VERSION", "INSTRUCTIONS",
           "SAME_AS", "PATTERNS", "ROWS", "CONNECTIONS", "FROM", "TO", "START",
           "DEFAULT_START", "MESHES", "COMMENT", "ParsingError"]
