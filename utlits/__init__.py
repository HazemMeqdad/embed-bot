import re
import webcolors
from .logger import CustomFormatter;
from .compiler import videoSchema, json_compiler, embed_schema;
def int_to_hex(color_int):
    return f"#{color_int:06X}"

def convert_theme_color_to_int(theme_color):
    try:
        if theme_color.startswith("#"):
            theme_color = theme_color[1:]  # Remove the '#' prefix if present
            rgb_color = webcolors.hex_to_rgb(theme_color)
        elif theme_color.startswith("rgb(") or theme_color.startswith("rgba("):
            color_values = re.findall(r'\d+', theme_color)
            rgb_color = tuple(int(value) for value in color_values[:3])
        else:
            return None

        intColor = int(rgb_color[0]) << 16 | int(rgb_color[1]) << 8 | int(rgb_color[2])
        return intColor
    except (ValueError, AttributeError):
        return None
