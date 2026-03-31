import ctypes
from ctypes import wintypes
import characters
import button

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

gdi32 = ctypes.windll.gdi32

WS_OVERLAPPEDWINDOW = 0x00CF0000
SW_SHOW = 1
WM_CLOSE = 0x0010
WM_DESTROY = 0x0002
WM_QUIT = 0x0012
WM_SIZE = 0x0005
WM_PAINT = 0x000F
CS_HREDRAW = 0x0002
CS_VREDRAW = 0x0001
COLOR_WINDOW = 5

_current_window = None


LPARAM = ctypes.c_longlong
WPARAM = ctypes.c_uint64
LRESULT = ctypes.c_longlong


user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, WPARAM, LPARAM]
user32.DefWindowProcW.restype = LRESULT

user32.DestroyWindow.argtypes = [wintypes.HWND]
user32.DestroyWindow.restype = wintypes.BOOL

user32.PostQuitMessage.argtypes = [ctypes.c_int]
user32.PostQuitMessage.restype = None


def _window_proc(hwnd, msg, wparam, lparam):
    try:
        if msg == WM_CLOSE:
            user32.DestroyWindow(hwnd)
            return 0
        elif msg == WM_DESTROY:
            user32.PostQuitMessage(0)
            return 0
        elif msg == WM_PAINT:
            ps = PAINTSTRUCT()
            hdc = user32.BeginPaint(hwnd, ctypes.byref(ps))
            
            gdi32.SetTextColor(hdc, 0x00000000)
            gdi32.SetBkMode(hdc, 1)
            
            characters._redraw_all(hdc)
            button._redraw_all_buttons(hdc)
            
            user32.EndPaint(hwnd, ctypes.byref(ps))
            return 0
        return user32.DefWindowProcW(hwnd, msg, wparam, lparam)
    except KeyboardInterrupt:
        user32.DestroyWindow(hwnd)
        return 0


WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, WPARAM, LPARAM)


class WNDCLASSW(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HCURSOR),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]


class PAINTSTRUCT(ctypes.Structure):
    _fields_ = [
        ("hdc", wintypes.HDC),
        ("fErase", wintypes.BOOL),
        ("rcPaint", wintypes.RECT),
        ("fRestore", wintypes.BOOL),
        ("fIncUpdate", wintypes.BOOL),
        ("rgbReserved", ctypes.c_byte * 32),
    ]


def window(title, width, height, x=None, y=None):
    global _current_window
    
    hInstance = kernel32.GetModuleHandleW(None)
    
    wc = WNDCLASSW()
    wc.style = CS_HREDRAW | CS_VREDRAW
    wc.lpfnWndProc = WNDPROC(_window_proc)
    wc.hInstance = hInstance
    wc.hbrBackground = ctypes.c_void_p(COLOR_WINDOW + 1)
    wc.lpszClassName = "xwguiWindow"
    
    user32.RegisterClassW(ctypes.byref(wc))
    
    if x is None:
        screen_width = user32.GetSystemMetrics(0)
        x = (screen_width - width) // 2
    if y is None:
        screen_height = user32.GetSystemMetrics(1)
        y = (screen_height - height) // 2
    
    hwnd = user32.CreateWindowExW(
        0,
        "xwguiWindow",
        title,
        WS_OVERLAPPEDWINDOW,
        x, y, width, height,
        0, 0, hInstance, 0
    )
    
    user32.ShowWindow(hwnd, SW_SHOW)
    user32.UpdateWindow(hwnd)
    
    _current_window = hwnd
    
    hdc = user32.GetDC(hwnd)
    gdi32.SetTextColor(hdc, 0x00000000)
    gdi32.SetBkMode(hdc, 1)
    
    characters._redraw_all(hdc)
    button._redraw_all_buttons(hdc)
    
    user32.ReleaseDC(hwnd, hdc)
    
    try:
        _run_message_loop()
    except KeyboardInterrupt:
        user32.DestroyWindow(hwnd)
    
    return hwnd


def _run_message_loop():
    msg = wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))
