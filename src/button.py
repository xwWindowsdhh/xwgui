import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

BUTTON_WIDTH = 80
BUTTON_HEIGHT = 25

_all_buttons = []
_pressed_button = None


def _redraw_all_buttons(hdc):
    """绘制所有按钮"""
    for i, btn in enumerate(_all_buttons):
        text, x, y, bg_color, text_color = btn
        is_pressed = (_pressed_button == i)

        if is_pressed:
            _draw_line(hdc, x + BUTTON_WIDTH - 1, y + 1, x + BUTTON_WIDTH - 1, y + BUTTON_HEIGHT - 1, 0x00FFFFFF)
            _draw_line(hdc, x + 1, y + BUTTON_HEIGHT - 1, x + BUTTON_WIDTH - 1, y + BUTTON_HEIGHT - 1, 0x00FFFFFF)
            _draw_line(hdc, x, y, x, y + BUTTON_HEIGHT - 1, 0x00808080)
            _draw_line(hdc, x, y, x + BUTTON_WIDTH - 1, y, 0x00808080)
        else:
            _draw_line(hdc, x, y, x, y + BUTTON_HEIGHT - 1, 0x00FFFFFF)
            _draw_line(hdc, x, y, x + BUTTON_WIDTH - 1, y, 0x00FFFFFF)
            _draw_line(hdc, x + BUTTON_WIDTH - 1, y, x + BUTTON_WIDTH - 1, y + BUTTON_HEIGHT - 1, 0x00808080)
            _draw_line(hdc, x, y + BUTTON_HEIGHT - 1, x + BUTTON_WIDTH - 1, y + BUTTON_HEIGHT - 1, 0x00808080)

        _fill_rect(hdc, x + 1, y + 1, x + BUTTON_WIDTH - 1, y + BUTTON_HEIGHT - 1, bg_color)

        gdi32.SetTextColor(hdc, text_color)
        gdi32.SetBkMode(hdc, 1)

        text_width = len(text) * 8
        text_x = x + (BUTTON_WIDTH - text_width) // 2
        text_y = y + (BUTTON_HEIGHT - 16) // 2

        if is_pressed:
            text_x += 1
            text_y += 1

        text_wide = ctypes.c_wchar_p(text)
        gdi32.TextOutW(hdc, text_x, text_y, text_wide, len(text))


def _draw_line(hdc, x1, y1, x2, y2, color):
    pen = gdi32.CreatePen(0, 1, color)
    old_pen = gdi32.SelectObject(hdc, pen)

    gdi32.MoveToEx(hdc, x1, y1, None)
    gdi32.LineTo(hdc, x2, y2)

    gdi32.SelectObject(hdc, old_pen)
    gdi32.DeleteObject(pen)


def _fill_rect(hdc, left, top, right, bottom, color):
    brush = gdi32.CreateSolidBrush(color)

    rect = wintypes.RECT(left, top, right, bottom)
    user32.FillRect(hdc, ctypes.byref(rect), brush)

    gdi32.DeleteObject(brush)


def _set_pressed(x, y, pressed):
    global _pressed_button

    if pressed:
        for i, btn in enumerate(_all_buttons):
            bx, by = btn[1], btn[2]
            if bx <= x <= bx + BUTTON_WIDTH and by <= y <= by + BUTTON_HEIGHT:
                _pressed_button = i
                user32.InvalidateRect(user32.GetForegroundWindow(), None, 0)
                return
    else:
        if _pressed_button is not None:
            _pressed_button = None
            user32.InvalidateRect(user32.GetForegroundWindow(), None, 0)


def _is_over_button(x, y):
    for btn in _all_buttons:
        bx, by = btn[1], btn[2]
        if bx <= x <= bx + BUTTON_WIDTH and by <= y <= by + BUTTON_HEIGHT:
            return True
    return False


def button(text, x, y, bg_color=0x00C0C0C0, text_color=0x00000000):
    _all_buttons.append((text, x, y, bg_color, text_color))
