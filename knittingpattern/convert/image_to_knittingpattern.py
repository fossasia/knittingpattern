"""This file lets you convert image files to knitting patterns.

"""


import PIL.Image
import json
from knittingpattern.Loader import PathLoader
from knittingpattern.Dumper import JSONDumper
import os


def _load_and_save(path):
    image = PIL.Image.open(path)
    def save():
        id = os.path.splitext(os.path.basename(path))[0]
        rows = []
        connections = []
        pattern_set = {
                "version" : "0.1",
                "type" : "knitting pattern",
                "comment" : {
                    "source": path
                },
                "patterns": [
                    {
                        "name" : id, 
                        "id" : id, 
                        "rows" : rows,
                        "connections": connections
                    }
                ]
            }
        bbox = image.getbbox()
        assert bbox
        min_x, min_y, max_x, max_y = bbox
        last_row_y = None
        for y in range(min_y, max_y):
            instructions = []
            row = {
                    "id" : y,
                    "instructions" : instructions
                }
            rows.append(row)
            for x in range(min_x, max_x):
                color = image.getpixel((x, y))
                instruction = {"type": "knit", "color": color}
                instructions.append(instruction)
            if last_row_y is not None:
                connections.append({
                      "from" : {
                        "id" : last_row_y
                      }, 
                      "to" : {
                        "id" : y
                      }
                    })
            last_row_y = y
        return pattern_set
    return JSONDumper(save)

convert_image_to_knitting_pattern = PathLoader(_load_and_save)
    

__all__ = ["convert_image_to_knitting_pattern"]