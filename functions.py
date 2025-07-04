import pygetwindow as gw
import pywinctl as pwc
from PIL import ImageGrab
import pytesseract
import numpy as np
import cv2
import time
import pyautogui
import re
import csv
from PIL import Image, ImageEnhance, ImageFilter
# Path to tesseract executable
from PIL import Image, ImageDraw
pytesseract.pytesseract.tesseract_cmd = r'D:\opener\opener v2\resources\tesseract\tesseract.exe'  # Update with your Tesseract-OCR path


def capture_screen(bbox):
    screenshot = ImageGrab.grab(bbox=bbox)
    return screenshot

def ocr_image(image):
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_image)
    return text, gray_image



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

    return text

def is_window_active(window_title):
    active_window = gw.getActiveWindow()
    if active_window is not None:
        return active_window.title == window_title
    return False


import pyautogui
import time
def click_when_idle(click_x, click_y ):
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
                    print("hi")
                    time.sleep(0.5)
                   
                    time.sleep(0.1)  # Small delay before clicking
                    pyautogui.click(click_x , click_y)
                    last_position = (x, y)  # Save current position
                    click_made = True  # Set flag to True
                    print("Mouse stationary, moved and clicked.")
                    print(f"Moved and clicked at {click_x}, {click_y}")
            
            prev_x, prev_y = x, y
            time.sleep(0.1)

        if last_position:
            pyautogui.moveTo(last_position[0], last_position[1])  # Move mouse to last position

        print("\nProgram exited.")

    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting.")     

def replace_characters(text, characters_to_replace, replacement_character):
    modified_text = text
    for char in characters_to_replace:
        modified_text = modified_text.replace(char, replacement_character)
        return modified_text

def find_text_in_image(image_path, search_text):
    # Open the image using Pillow
    image = Image.open(image_path)
    image_width, image_height = image.size
    print(f"Image dimensions - Width: {image_width}, Height: {image_height}")
    # Use pytesseract to do OCR on the image and get bounding boxes
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    # Loop through each word found by Tesseract
    for i in range(len(data['text'])):
        if search_text.lower() in data['text'][i].lower():
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            print(f"Found '{search_text}' at ({x}, {y}), width: {w}, height: {h}")
            
            # Optionally, draw a rectangle around the found text
            draw = ImageDraw.Draw(image)
            draw.rectangle([x, y, x + w, y + h], outline="red", width=2)
            return x, y

def find_text_in_coordinates(image_path, coordinates, save_path):
    # Open the image using Pillow
    image = Image.open(image_path)
    
    # Get the dimensions of the image
    image_width, image_height = image.size
    print(f"Image dimensions - Width: {image_width}, Height: {image_height}")

    # Crop the image based on the given coordinates
    left, top, right, bottom = coordinates
    cropped_image = image.crop((left, top, right, bottom))

    
    # Save the cropped image
    cropped_image.save(save_path)
    
    # Use pytesseract to extract text from the cropped image
    text = pytesseract.image_to_string(cropped_image)
    
    # Print the extracted text
    print(f"Extracted text from coordinates {coordinates}:")
    print(text)
   
    return text

last_windows = []

def find_window():
    global last_windows

    all_windows = gw.getAllTitles()
    windows = [x for x in all_windows if x not in last_windows]

    last_windows = all_windows

    print("Open windows:")

    for i, title in enumerate(windows):
        print(f"{i}: '{title}'")

    for title in windows:
        if 'Blinds' in title:
            # Get the window
            window = gw.getWindowsWithTitle(title)[0]
            
            # Restore if minimized
            # if window.isMinimized:
            #     window.restore()
            
            return title
    
    print("No new window with 'Blinds' in the title found.")
    return None

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

def find_text_in_coordinates_players(image_path, coordinates, save_path):
    # Open the image using Pillow
    image = Image.open(image_path)
    
    # Get the dimensions of the image
    image_width, image_height = image.size
    print(f"Image dimensions - Width: {image_width}, Height: {image_height}")

    # Crop the image based on the given coordinates
    left, top, right, bottom = coordinates
    cropped_image = image.crop((left, top, right, bottom))
    
    # Convert the cropped image to grayscale
    grayscale_image = cropped_image.convert("L")
    
    # Convert the grayscale PIL image to a NumPy array
    grayscale_array = np.array(grayscale_image)
    
    # Define the threshold for binarization
    threshold = 210
    
    # Apply the threshold to convert the image to binary
    _, binary_array = cv2.threshold(grayscale_array, threshold, 255, cv2.THRESH_BINARY)
    
    # Apply a median filter to remove noise
    denoised_array = cv2.medianBlur(binary_array, 1)  # Adjust the kernel size as needed
    
    # Convert the denoised NumPy array back to a PIL image
    denoised_image = Image.fromarray(denoised_array)
    
    # Save the preprocessed denoised image
    denoised_image.save(save_path)
    
    # Use pytesseract to extract text from the preprocessed image with PSM 6 (single word)
    custom_config = r'--psm 6'
    text = pytesseract.image_to_string(denoised_image, config=custom_config)
    
    # Print the extracted text
    print(f"Extracted text from coordinates {coordinates}:")
    print(text)
   
    return text

import pygetwindow as gw

def close_window_by_title(window_title):
    # Find the window with the specific title
    window = gw.getWindowsWithTitle(window_title)

    if window:
        # Close the window using pyautogui
        window[0].close()
        print(f"Window '{window_title}' closed.")
    else:
        print(f"Window '{window_title}' not found.")

def read_csv_to_list(file_path):
  
    text_list = []

    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Assuming the text is in the first column
            text_list.append(row[0])

    return text_list

from click import run_winapi_click
import pygetwindow as gw

def click_on_blinds_windows(x, y):
    windows = gw.getAllTitles()
    blinds_titles = [title for title in windows if 'Blinds' in title]

    if not blinds_titles:
        print("No new window with 'Blinds' in the title found.")
        return

    for title in blinds_titles:
        run_winapi_click(title, x, y)
        print(f"Clicked on '{title}' at ({x}, {y})")

# Example usage
