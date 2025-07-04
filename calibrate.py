from pynput.mouse import Listener
import sys
from functions import *
import json
import os
import win32gui

def on_click(x, y, button, pressed):
    global click_count, listener, first_click, second_click
    if pressed:
        print(f"Mouse clicked at ({x}, {y})")
        if click_count == 0:
            first_click = (x, y)
            click_count += 1
        elif click_count == 1:
            second_click = (x, y)
            click_count += 1
            print("Two clicks captured. Exiting...")
            listener.stop()

def calibrate():
    global click_count, listener, first_click, second_click, win_x, win_y
    
    win32gui.EnumWindows(callback, None)

    click_count = 0
    first_click = None
    second_click = None

    print("Listening for two mouse clicks... Press Ctrl+C to exit.")

    try:
        with Listener(on_click=on_click) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    if first_click and second_click:
        return first_click[0] - win_x, first_click[1] - win_y, second_click[0] - win_x, second_click[1] - win_y
    else:
        return None

def save_calibration_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_calibration_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def is_file_empty(filename):
    return os.stat(filename).st_size == 0

def callback(hwnd, extra):
    rect = win32gui.GetWindowRect(hwnd)
    global win_x, win_y

    if win32gui.GetWindowText(hwnd).find("CoinPoker - Lobby") > -1:
        win_x = rect[0]
        win_y = rect[1]
