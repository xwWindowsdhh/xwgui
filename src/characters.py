import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

_current_hwnd = None
_all_texts = []


def _set_window(hwnd):
    global _current_hwnd
    _current_hwnd = hwnd


def _redraw_all(hdc):
    for text, x, y, color in _all_texts:
        gdi32.SetTextColor(hdc, color)
        gdi32.SetBkMode(hdc, 1)
        
        text_wide = ctypes.c_wchar_p(text)
        gdi32.TextOutW(hdc, x, y, text_wide, len(text))


def characters(text, x, y, color=0x00000000):
    _all_texts.append((text, x, y, color))
