import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# 按钮默认尺寸
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 25

_all_buttons = []
_pressed_button = None  # 当前被按下的按钮索引


def _redraw_all_buttons(hdc):
    """绘制所有按钮"""
    for i, btn in enumerate(_all_buttons):
        text, x, y, bg_color, text_color = btn
        is_pressed = (_pressed_button == i)

        if is_pressed:
            # 按下状态：内凹效果
            # 右边和下边 - 白色（阴影）
            _draw_line(hdc, x + BUTTON_WIDTH - 1, y + 1, x + BUTTON_WIDTH - 1, y + BUTTON_HEIGHT - 1, 0x00FFFFFF)
            _draw_line(hdc, x + 1, y + BUTTON_HEIGHT - 1, x + BUTTON_WIDTH - 1, y + BUTTON_HEIGHT - 1, 0x00FFFFFF)
            # 左边和上边 - 深灰（阴影）
            _draw_line(hdc, x, y, x, y + BUTTON_HEIGHT - 1, 0x00808080)
            _draw_line(hdc, x, y, x + BUTTON_WIDTH - 1, y, 0x00808080)
        else:
            # 正常状态：外凸效果
            # 左边和上边 - 白色（高光）
            _draw_line(hdc, x, y, x, y + BUTTON_HEIGHT - 1, 0x00FFFFFF)
            _draw_line(hdc, x, y, x + BUTTON_WIDTH - 1, y, 0x00FFFFFF)
            # 右边和下边 - 深灰（阴影）
            _draw_line(hdc, x + BUTTON_WIDTH - 1, y, x + BUTTON_WIDTH - 1, y + BUTTON_HEIGHT - 1, 0x00808080)
            _draw_line(hdc, x, y + BUTTON_HEIGHT - 1, x + BUTTON_WIDTH - 1, y + BUTTON_HEIGHT - 1, 0x00808080)

        # 按钮背景
        _fill_rect(hdc, x + 1, y + 1, x + BUTTON_WIDTH - 1, y + BUTTON_HEIGHT - 1, bg_color)

        # 绘制文字（居中，按下时稍微偏移）
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
    """绘制直线"""
    pen = gdi32.CreatePen(0, 1, color)
    old_pen = gdi32.SelectObject(hdc, pen)

    gdi32.MoveToEx(hdc, x1, y1, None)
    gdi32.LineTo(hdc, x2, y2)

    gdi32.SelectObject(hdc, old_pen)
    gdi32.DeleteObject(pen)


def _fill_rect(hdc, left, top, right, bottom, color):
    """填充矩形"""
    brush = gdi32.CreateSolidBrush(color)

    rect = wintypes.RECT(left, top, right, bottom)
    user32.FillRect(hdc, ctypes.byref(rect), brush)

    gdi32.DeleteObject(brush)


def _set_pressed(x, y, pressed):
    """设置按钮按下状态"""
    global _pressed_button

    if pressed:
        # 检查哪个按钮被按下
        for i, btn in enumerate(_all_buttons):
            bx, by = btn[1], btn[2]
            if bx <= x <= bx + BUTTON_WIDTH and by <= y <= by + BUTTON_HEIGHT:
                _pressed_button = i
                # 强制重绘
                user32.InvalidateRect(user32.GetForegroundWindow(), None, 0)
                return
    else:
        if _pressed_button is not None:
            _pressed_button = None
            # 强制重绘
            user32.InvalidateRect(user32.GetForegroundWindow(), None, 0)


def _is_over_button(x, y):
    """检查鼠标是否在按钮上"""
    for btn in _all_buttons:
        bx, by = btn[1], btn[2]
        if bx <= x <= bx + BUTTON_WIDTH and by <= y <= by + BUTTON_HEIGHT:
            return True
    return False


def button(text, x, y, bg_color=0x00C0C0C0, text_color=0x00000000):
    """
    添加按钮（有点击效果，无功能）

    参数:
        text: 按钮文字
        x: 按钮左上角 x 坐标
        y: 按钮左上角 y 坐标
        bg_color: 背景颜色，默认浅灰色 (0x00C0C0C0)
        text_color: 文字颜色，默认黑色 (0x00000000)
    """
    _all_buttons.append((text, x, y, bg_color, text_color))
