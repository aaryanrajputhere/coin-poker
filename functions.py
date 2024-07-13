import pygetwindow as gw
import pywinctl as pwc
from PIL import ImageGrab
import pytesseract
import numpy as np
import cv2
import time
import pyautogui
import re
# Path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update with your Tesseract-OCR path


def capture_screen(bbox):
    screenshot = ImageGrab.grab(bbox=bbox)
    return screenshot

def ocr_image(image):
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_image)
    return text, gray_image


def click_coordinates(x, y):
    # Move the mouse to the specified coordinates and click
    pyautogui.moveTo(x, y)
    pyautogui.click()

def get_text_coordinates(gray_image, search_text):
    # Use pytesseract to get the bounding boxes of all detected words
    data = pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT)
    
    # Initialize coordinates list
    coordinates_list = []
    
    # Iterate over all detected words
    for i, text in enumerate(data['text']):
        if text.lower() == search_text.lower():
            # If the detected word matches the search text, get its bounding box
            x = data['left'][i]
            y = data['top'][i]
            width = data['width'][i]
            height = data['height'][i]
            coordinates = (x, y, width, height)
            coordinates_list.append(coordinates)
    
    return coordinates_list

def get_blinds(text):
   
   numbers = text.strip().split()
  
   if len(numbers) <2:
       lower_blind = 0
       higher_blind = 0
       return lower_blind,higher_blind
   if numbers[0] == 250:
        numbers[0] = 2.50  
   lower_blind = numbers[0]
   higher_blind = numbers[1]
   
   return lower_blind,higher_blind
    

# Example usage:

def extract_data(text, start_symbol, end_symbol):
    start_index = text.find(start_symbol)
    if start_index == -1:
        return None
    
    start_index += len(start_symbol)
    end_index = text.find(end_symbol, start_index)
    if end_index == -1:
        return None
    
    return text[start_index:end_index]

def replace_characters(text, characters_to_replace, replacement_character):
    modified_text = text
    for char in characters_to_replace:
        modified_text = modified_text.replace(char, replacement_character)
        return modified_text

def get_players(img_path):
    image = cv2.imread(img_path)

# Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Save the preprocessed image (optional, for debugging)
    cv2.imwrite('/mnt/data/players_gray_img_preprocessed.png', binary_image)

    # Use Tesseract to do OCR on the preprocessed image
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789/'
    text = pytesseract.image_to_string(binary_image, config=custom_config)
    if "7" in text:
        maximum_players = 7
    elif text == '':
        maximum_players = 0
    else:
        maximum_players = 4
    return maximum_players

def is_window_active(window_title):
    active_window = gw.getActiveWindow()
    if active_window is not None:
        return active_window.title == window_title
    return False


import pyautogui
import time

def click_when_idle(click_x, click_y):
    try:
        prev_x, prev_y = pyautogui.position()
        stationary_time = 0
        click_made = False
        last_position = None
        
        while not click_made:
            x, y = pyautogui.position()
            
            if x != prev_x or y != prev_y:
                print(f"Mouse moving - X: {x}, Y: {y} ", end="\r")
                stationary_time = 0  # Reset stationary time if mouse moves
            else:
                stationary_time += 0.1  # Increment stationary time
                if stationary_time >= 2 and not pyautogui.mouseDown():  # If stationary for 2 seconds and no mouse button is down
                    pyautogui.click(click_x, click_y)  # Perform a mouse click
                    last_position = (x, y)  # Save current position
                    click_made = True  # Set flag to True
                    print("Mouse stationary, clicked.")
            
            prev_x, prev_y = x, y
            time.sleep(0.1)

        if last_position:
            pyautogui.moveTo(last_position[0], last_position[1])  # Move mouse to last position

        print("\nProgram exited.")

    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting.")

