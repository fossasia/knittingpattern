
# attributes

ID = "id"
NAME = "name"
TYPE = "type"
VERSION = "version"

# constants

KNITTING_PATTERN_TYPE = "knitting pattern"

# functions

def to_id(id):
    return tuple(id) if isinstance(id, list) else id
