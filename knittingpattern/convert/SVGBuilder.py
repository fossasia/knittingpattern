"""Build SVG files


"""


START_OF_SVG_FILE = """<?xml version="1.0" encoding="UTF-8"?>
<!-- Created with knittingpattern
     https://github.com/AllYarnsAreBeautiful/knittingpattern -->
<svg width="{width}" height="{height}" 
     viewport="{min_x} {min_y} {max_x} {max_y}" >"""
END_OF_SVG_FILE = """</svg>"""
ELEMENT_STRING = """        <g transform=\"translate({x},{y})\">
        {content}
    </g>"""
LAYER_START = """    <g class="row" id="{id}" inkscape:label="{id}"
                      inkscape:groupmode="layer">"""
LAYER_END = """    </g>"""


class SVGBuilder(object):
    """This class builds an SVG to a file.

    The class itself does not know what the objects look like.
    It offers a more convinient interface to build SVG files.

    To place `svg_content` is `(x, y)` position ina layer `layer1` do:

        with SVGBuilder(file) as builder:
            builder.place(x, y, svg_content, "layer1")
    """

    def __init__(self, file, min_x, min_y, max_x, max_y):
        """Initialize this object with the file for the SVG."""
        self._file = file
        self._current_layer = None
        self._min_x = min_x
        self._min_y = min_y
        self._max_x = max_x
        self._max_y = max_y
    
    @property
    def bounding_box(self):
        """Returns (min_x, min_y, max_x, max_y)"""
        return (self._min_x, self._min_y, self._max_x, self._max_y)

    def _write(self, string):
        """Shortcut for writing to the file.

        This should be used instead of `self.file.write()`"""
        self._file.write(string)

    def __enter__(self):
        """Open the builder with the `with` construct."""
        self.open()

    def __exit__(self, type=None, error=None, traceback=None):
        """Close the builder with the `with` construct."""
        self.close()

    def open(self):
        """Start writing to the file."""
        self._write(self._beginning_of_file)

    @property
    def _beginning_of_file(self):
        """This is the beginning of the SVG."""
        return START_OF_SVG_FILE.format(
                width=self._max_x - self._min_x,
                height=self._max_y - self._min_y,
                min_x=self._min_x,
                max_x=self._max_x,
                min_y=self._min_y,
                max_y=self._max_y
            )

    def close(self):
        """Close the SVG tag."""
        if self._current_layer is not None:
            self._close_layer()
        self._write(self._end_of_file)
        self._file.seek(0)

    @property
    def _end_of_file(self):
        """This is the closing tag of the SVG."""
        return END_OF_SVG_FILE

    def place(self, x, y, svg, layer_id):
        """Place the `svg` content at `(x, y)` position in the file, in
        a layer with the id `layer_id`.

        This can be used to place instructions in layers."""
        self._in_layer(layer_id)
        self._write(ELEMENT_STRING.format(x=x, y=y, content=svg))

    def _in_layer(self, layer_id):
        """Assure that we are in a certain layer."""
        if self._current_layer != layer_id:
            if self._current_layer is not None:
                self._close_layer()
            self._open_layer(layer_id)
            self._current_layer = layer_id

    def _open_layer(self, layer_id):
        """Open a layer with the id `layer_id`."""
        self._write(LAYER_START.format(id=layer_id))

    def _close_layer(self):
        """Close a layer."""
        self._write(LAYER_END)


__all__ = [
        "SVGBuilder", "START_OF_SVG_FILE", "END_OF_SVG_FILE",
        "ELEMENT_STRING", "ROW_START", "ROW_END"
    ]
