"""This file lets you convert image files to knitting patterns.

"""
import PIL.Image
from ..Loader import PathLoader
from ..Dumper import JSONDumper
from .load_and_dump import decorate_load_and_dump
import os


@decorate_load_and_dump(PathLoader, JSONDumper)
def convert_image_to_knitting_pattern(path, colors=("white", "black")):
    """Load a image file such as a png bitmap of jpeg file and convert it
    to a :ref:`knitting pattern file <FileFormatSpecification>`.

    :param list colors: a list of strings that should be used as
      :ref:`colors <png-color>`.
    :param str path: ignore this. It is fulfilled by the loeder.

    Example:

    .. code:: python

        convert_image_to_knitting_pattern().path("image.png").path("image.json")
    """
    image = PIL.Image.open(path)
    pattern_id = os.path.splitext(os.path.basename(path))[0]
    rows = []
    connections = []
    pattern_set = {
            "version": "0.1",
            "type": "knitting pattern",
            "comment": {
                "source": path
            },
            "patterns": [
                {
                    "name": pattern_id,
                    "id": pattern_id,
                    "rows": rows,
                    "connections": connections
                }
            ]
        }
    bbox = image.getbbox()
    if not bbox:
        return pattern_set
    white = image.getpixel((0, 0))
    min_x, min_y, max_x, max_y = bbox
    last_row_y = None
    for y in range(min_y, max_y):
        instructions = []
        row = {
                "id": y,
                "instructions": instructions
            }
        rows.append(row)
        for x in range(min_x, max_x):
            if image.getpixel((x, y)) == white:
                color = colors[0]
            else:
                color = colors[1]
            instruction = {"color": color}
            instructions.append(instruction)
        if last_row_y is not None:
            connections.append({
                  "from": {
                    "id": last_row_y
                  },
                  "to": {
                    "id": y
                  }
                })
        last_row_y = y
    return pattern_set


__all__ = ["convert_image_to_knitting_pattern"]
