"""Functions for color conversion."""
import webcolors


def convert_color_to_rrggbb(color):
    """The color in "#RRGGBB" format.

    :return: the :attr:`color` in "#RRGGBB" format
    """
    if not color.startswith("#"):
        rgb = webcolors.html5_parse_legacy_color(color)
        hex_color = webcolors.html5_serialize_simple_color(rgb)
    else:
        hex_color = color
    return webcolors.normalize_hex(hex_color)

__all__ = ["convert_color_to_rrggbb"]
