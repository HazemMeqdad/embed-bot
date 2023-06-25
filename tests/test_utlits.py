
from utlits import convert_theme_color_to_int, int_to_hex

def test_convert_theme_color_to_int():
    assert convert_theme_color_to_int("#FFFFFF") == 16777215
    assert convert_theme_color_to_int("#000000") == 0

def test_int_to_hex():
    assert int_to_hex(16777215) == "#FFFFFF"
    assert int_to_hex(0) == "#000000"
