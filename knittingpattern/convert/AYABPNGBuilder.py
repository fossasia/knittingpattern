"""Convert knitting patterns to png files.

These png files are used to be fed into the ayab-desktop software.
They do not ocntain so much layout information.
They just contain colors."""

class AYABPNGBuilder(object):
    """Convert knitting patterns to png files that onlny contain the color
    information and (x, y) coordinates."""
    
    def __init__(self, file, min_x, max_x, min_y, max_y):
        """Initialize the builder with the file for the PNG.
        
        x ∈ [min_x, max_x) and y ∈ [min_y, max_y) are the bounds of the
        instructions.
        Instructions outside the bounds are not rendered.
        """
        
    def open(self):
        """Start writing to the file."""
        
    def close(self):
        """Stop writing to the file."""
        
    def __enter__(self):
        """`open()` but for the `with` statement."""
        
    def __exit__(self, ty=None, err=None, tb=None):
        """`close()` but for the `with` statement."""

    @staticmethod
    def _convert_color_to_RRGGBB(color):
        """Takes a color such as "#fff" or "blue" and converts it into a 24 bit
        color "#RrGgBb".
        """
        
    def set_pixel(self, x, y, color):
        """Set the pixel at x, y position to color.
        
        If (x, y) is out of the bounds min_x, max_x, min_y, max_y,
        this does not change the image.
        """
    
    def is_in_bounds(self, x, y):
        """Return whether `(x, y)` are inside the bounds of min_x, max_x,
        min_y, max_y.
        """
        
    def set_instruction_in_grid(self, instruction_in_grid):
        """Set the pixel at the position of the instruction to its color.
        
        `instruction_in_grid` must have the following attributes:
        
        - `color` is the color to set the pixel to
        - `x` is the x position of the pixel
        - `y` is the y position of the pixel
        
        Also see `set_pixel()`
        """
    
    def set_instructions_in_grid(self, some_instructions_in_grid):
        """Same as `set_instruction_in_grid()` but with a collection of 
        instructions in grid.
        """


__all__ = ["AYABPNGBuilder"]
