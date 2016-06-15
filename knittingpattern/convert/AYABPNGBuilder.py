"""Convert knitting patterns to png files.

These png files are used to be fed into the ayab-desktop software.
They only contain which meshes will be knit with a contrast color.
They just contain colors."""
import webcolors
import PIL.Image


class AYABPNGBuilder(object):
    """Convert knitting patterns to png files that onlny contain the color
    information and (x, y) coordinates."""

    def __init__(self, min_x, min_y, max_x, max_y,
                 default_color="white"):
        """Initialize the builder with the file for the PNG.

        x in [min_x, max_x) and y in [min_y, max_y) are the bounds of the
        instructions.
        Instructions outside the bounds are not rendered.
        Any Pixel that is not set has the `default_color`.
        """
        self._min_x = min_x
        self._min_y = min_y
        self._max_x = max_x
        self._max_y = max_y
        self._default_color = default_color
        self._image = PIL.Image.new(
                "RGB", (max_x - min_x, max_y - min_y),
                self._convert_to_image_color(default_color)
            )

    def write_to_file(self, file):
        """Writes the png to the file."""
        self._image.save(file, format="PNG")

    @staticmethod
    def _convert_color_to_RRGGBB(color):
        """Takes a color such as "#fff" or "blue" and converts it into a 24 bit
        color "#RrGgBb".
        """
        if not color.startswith("#"):
            rgb = webcolors.html5_parse_legacy_color(color)
            hex = webcolors.html5_serialize_simple_color(rgb)
        else:
            hex = color
        return webcolors.normalize_hex(hex)

    def _convert_RRGGBB_to_image_color(self, rrggbb):
        """Returns the color that is used by the image."""
        return webcolors.hex_to_rgb(rrggbb)

    def _convert_to_image_color(self, color):
        """Returns a color thet can be used by the image."""
        rgb = self._convert_color_to_RRGGBB(color)
        return self._convert_RRGGBB_to_image_color(rgb)

    def _set_pixel_and_convert_color(self, x, y, color):
        """Set the pixel but convert the color before."""
        if color is None:
            return
        color = self._convert_color_to_RRGGBB(color)
        self._set_pixel(x, y, color)

    def _set_pixel(self, x, y, color):
        """Set the color of the pixel.

        `color` must be a valid color in the form of "#rrggbb".
        If you need to convert color, use `_set_pixel_and_convert_color()`.
        """
        if not self.is_in_bounds(x, y):
            return
        rgb = self._convert_RRGGBB_to_image_color(color)
        x -= self._min_x
        y -= self._min_y
        self._image.putpixel((x, y), rgb)

    def set_pixel(self, x, y, color):
        """Set the pixel at x, y position to color.

        If (x, y) is out of the bounds min_x, max_x, min_y, max_y,
        this does not change the image.
        """
        self._set_pixel_and_convert_color(x, y, color)

    def is_in_bounds(self, x, y):
        """Return whether `(x, y)` are inside the bounds of min_x, max_x,
        min_y, max_y.
        """
        lower = self._min_x <= x and self._min_y <= y
        upper = self._max_x > x and self._max_y > y
        return lower and upper

    def set_color_in_grid(self, color_in_grid):
        """Set the pixel at the position of the `color_in_grid` to its color.

        `color_in_grid` must have the following attributes:

        - `color` is the color to set the pixel to
        - `x` is the x position of the pixel
        - `y` is the y position of the pixel

        Also see `set_pixel()`
        """
        self._set_pixel_and_convert_color(
                color_in_grid.x, color_in_grid.y, color_in_grid.color
            )

    def set_colors_in_grid(self, some_colors_in_grid):
        """Same as `set_color_in_grid()` but with a collection of
        colors in grid.
        """
        for color_in_grid in some_colors_in_grid:
            self._set_pixel_and_convert_color(
                    color_in_grid.x, color_in_grid.y, color_in_grid.color
                )

    @property
    def default_color(self):
        """Returns the color of the pixels that are not set.

        You can set this color by passing it to the constructor.
        """
        return self._default_color


__all__ = ["AYABPNGBuilder"]
