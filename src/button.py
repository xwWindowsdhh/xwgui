import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# 按钮默认尺寸
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 25

_all_buttons = []


def _redraw_all_buttons(hdc):
    """绘制所有按钮"""
    for text, x, y, bg_color, text_color in _all_buttons:
        # 绘制按钮背景（3D效果）
        # 外边框 - 黑色
        _draw_rect(hdc, x, y, x + BUTTON_WIDTH, y + BUTTON_HEIGHT, 0x00000000)
        
        # 按钮背景 - 浅灰色
        _fill_rect(hdc, x + 1, y + 1, x + BUTTON_WIDTH - 1, y + BUTTON_HEIGHT - 1, 0x00C0C0C0)
        
        # 绘制文字（居中）
        gdi32.SetTextColor(hdc, text_color)
        gdi32.SetBkMode(hdc, 1)
        
        # 计算文字居中位置
        text_width = len(text) * 8  # 粗略估算
        text_x = x + (BUTTON_WIDTH - text_width) // 2
        text_y = y + (BUTTON_HEIGHT - 16) // 2
        
        text_wide = ctypes.c_wchar_p(text)
        gdi32.TextOutW(hdc, text_x, text_y, text_wide, len(text))


def _draw_rect(hdc, left, top, right, bottom, color):
    """绘制矩形边框"""
    pen = gdi32.CreatePen(0, 1, color)  # PS_SOLID = 0
    old_pen = gdi32.SelectObject(hdc, pen)
    
    gdi32.MoveToEx(hdc, left, top, None)
    gdi32.LineTo(hdc, right, top)
    gdi32.LineTo(hdc, right, bottom)
    gdi32.LineTo(hdc, left, bottom)
    gdi32.LineTo(hdc, left, top)
    
    gdi32.SelectObject(hdc, old_pen)
    gdi32.DeleteObject(pen)


def _fill_rect(hdc, left, top, right, bottom, color):
    """填充矩形"""
    brush = gdi32.CreateSolidBrush(color)
    
    rect = wintypes.RECT(left, top, right, bottom)
    user32.FillRect(hdc, ctypes.byref(rect), brush)
    
    gdi32.DeleteObject(brush)


def button(text, x, y, bg_color=0x00C0C0C0, text_color=0x00000000):
    """
    添加按钮
    
    参数:
        text: 按钮文字
        x: 按钮左上角 x 坐标
        y: 按钮左上角 y 坐标
        bg_color: 背景颜色，默认浅灰色 (0x00C0C0C0)
        text_color: 文字颜色，默认黑色 (0x00000000)
    """
    _all_buttons.append((text, x, y, bg_color, text_color))
