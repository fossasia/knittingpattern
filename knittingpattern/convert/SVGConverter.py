

class SVGConverter(object):

    START_OF_SVG_FILE = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with knittingpattern https://github.com/AllYarnsAreBeautiful/knittingpattern -->
<svg width="0" height="0">"""
    END_OF_SVG_FILE = """</svg>"""
    ELEMENT_STRING = """        <g transform=\"translate({x},{y})\">
            {content}
        </g>"""
    ROW_START = """    <g class="row" id="{id}" inkscape:label="{id}" inkscape:groupmode="layer">"""
    ROW_END = """    </g>"""

    def __init__(self, file):
        self.file = file
        self.current_row = None
    
    def write(self, string):
        print(string)
        self.file.write(string)

    def __enter__(self):
        self.open()

    def __exit__(self, type=None, error=None, traceback=None):
        self.close()
        
    def open(self):
        self.write(self.beginning_of_file)
        
    @property
    def beginning_of_file(self):
        return self.START_OF_SVG_FILE
    
    def close(self):
        if self.current_row is not None:
            self.close_row()
        self.write(self.end_of_file)
        self.file.seek(0)
        
    @property
    def end_of_file(self):
        return self.END_OF_SVG_FILE

    def render_at(self, x, y, svg, row_id):
        self.in_row(row_id)
            
        self.write(self.ELEMENT_STRING.format(
                x= x,
                y= y,
                content= svg
            ))
            
    def in_row(self, row_id):
        if self.current_row != row_id:
            if self.current_row is not None:
                self.close_row()
            self.open_row(row_id)
            self.current_row = row_id

    def open_row(self, row_id):
        self.write(self.ROW_START.format(id = row_id))

    def close_row(self):
        self.write(self.ROW_END)