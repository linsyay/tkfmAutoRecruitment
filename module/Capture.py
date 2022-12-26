import win32gui
import numpy as np
import mss

def get_win_list():
    def callback(hwnd, hwnd_list: list):
        title = win32gui.GetWindowText(hwnd)
        if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title:
            hwnd_list.append((title, hwnd))
        return True
    
    output = []
    
    # map 함수와 비슷한 방식으로 동작
    win32gui.EnumWindows(callback, output)
    return output

def get_win_size(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return left, top, right, bottom

def get_win_image(x1, y1, x2, y2):
    with mss.mss() as sct:
        pos = {"left":x1, "top":y1, "width":x2-x1, "height":y2-y1}
        img = np.array(sct.grab(pos))
    return img