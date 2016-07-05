"""Convert knitting patterns to png files.

These png files are used to be fed into the ayab-desktop software.
They only contain which meshes will be knit with a contrast color.
They just contain colors.
"""
import webcolors
import PIL.Image
from .color import convert_color_to_rrggbb


class AYABPNGBuilder(object):
    """Convert knitting patterns to png files that only contain the color
    information and ``(x, y)`` coordinates.

    .. _png-color:

    Througout this class the term `color` refers to either

    - a valid html5 color name such as ``"black"``, ``"white"``
    - colors of the form ``"#RGB"``, ``"#RRGGBB"`` and ``"#RRRGGGBBB"``

    """

    def __init__(self, min_x, min_y, max_x, max_y,
                 default_color="white"):
        """Initialize the builder with the bounding box and a default color.

        .. _png-builder-bounds:

        ``min_x <= x < max_x`` and ``min_y <= y < max_y`` are the bounds of the
        instructions.
        Instructions outside the bounds are not rendered.
        Any Pixel that is not set has the :paramref:`default_color`.

        :param int min_x: the lower bound of the x coordinates
        :param int max_x: the upper bound of the x coordinates
        :param int min_y: the lower bound of the y coordinates
        :param int max_y: the upper bound of the y coordinates
        :param default_color: a valid :ref:`color <png-color>`
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
        """write the png to the file

        :param file: a file-like object
        """
        self._image.save(file, format="PNG")

    @staticmethod
    def _convert_color_to_rrggbb(color):
        """takes a :ref:`color <png-color>` and converts it into a 24 bit
        color "#RRGGBB"

        """
        return convert_color_to_rrggbb(color)

    def _convert_rrggbb_to_image_color(self, rrggbb):
        """:return: the color that is used by the image"""
        return webcolors.hex_to_rgb(rrggbb)

    def _convert_to_image_color(self, color):
        """:return: a color that can be used by the image"""
        rgb = self._convert_color_to_rrggbb(color)
        return self._convert_rrggbb_to_image_color(rgb)

    def _set_pixel_and_convert_color(self, x, y, color):
        """set the pixel but convert the color before."""
        if color is None:
            return
        color = self._convert_color_to_rrggbb(color)
        self._set_pixel(x, y, color)

    def _set_pixel(self, x, y, color):
        """set the color of the pixel.

        :param color: must be a valid color in the form of "#RRGGBB".
          If you need to convert color, use `_set_pixel_and_convert_color()`.
        """
        if not self.is_in_bounds(x, y):
            return
        rgb = self._convert_rrggbb_to_image_color(color)
        x -= self._min_x
        y -= self._min_y
        self._image.putpixel((x, y), rgb)

    def set_pixel(self, x, y, color):
        """set the pixel at ``(x, y)`` position to :paramref:`color`

        If ``(x, y)`` is out of the :ref:`bounds <png-builder-bounds>`
        this does not change the image.

        .. seealso:: :meth:`set_color_in_grid`
        """
        self._set_pixel_and_convert_color(x, y, color)

    def is_in_bounds(self, x, y):
        """
        :return: whether ``(x, y)`` is inside the :ref:`bounds
          <png-builder-bounds>`
        :rtype: bool
        """
        lower = self._min_x <= x and self._min_y <= y
        upper = self._max_x > x and self._max_y > y
        return lower and upper

    def set_color_in_grid(self, color_in_grid):
        """Set the pixel at the position of the :paramref:`color_in_grid`
        to its color.

        :param color_in_grid: must have the following attributes:

          - ``color`` is the :ref:`color <png-color>` to set the pixel to
          - ``x`` is the x position of the pixel
          - ``y`` is the y position of the pixel

        .. seealso:: :meth:`set_pixel`, :meth:`set_colors_in_grid`
        """
        self._set_pixel_and_convert_color(
                color_in_grid.x, color_in_grid.y, color_in_grid.color
            )

    def set_colors_in_grid(self, some_colors_in_grid):
        """Same as :meth:`set_color_in_grid` but with a collection of
        colors in grid.

        :param iterable some_colors_in_grid: a collection of colors in grid for
          :meth:`set_color_in_grid`
        """
        for color_in_grid in some_colors_in_grid:
            self._set_pixel_and_convert_color(
                    color_in_grid.x, color_in_grid.y, color_in_grid.color
                )

    @property
    def default_color(self):
        """:return: the :ref:`color <png-color>` of the pixels that are not set

        You can set this color by passing it to the :meth:`constructor
        <__init__>`.
        """
        return self._default_color


__all__ = ["AYABPNGBuilder"]
