import re
import webcolors
def int_to_hex(color_int):
    if color_int is None:
        return '#000000' 
    else:
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

def test_convert_theme_color_to_int():
    assert convert_theme_color_to_int("#FFFFFF") == 16777215
    assert convert_theme_color_to_int("#000000") == 0

def test_int_to_hex():
    assert int_to_hex(16777215) == "#FFFFFF"
    assert int_to_hex(0) == "#000000"
