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

# Find the window by title
window_title = 'CoinPoker - Lobby'  # Update with the exact title of the window
window = None

# Loop through all windows and find the matching title
for w in gw.getWindowsWithTitle(window_title):
    print(w)
    if w.title == window_title:
        window = w
        break

if not window:
    raise Exception(f'Window with title "{window_title}" not found!')

# Get the window coordinates
left, top, right, bottom = window.left, window.top, window.right, window.bottom
print(left , top  , right , bottom)
bbox = (0, 0, 1920, 1080)
print(bbox)
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
    pattern = r'¥ ?(\d+\.\d+) */¥ ?(\d+\.\d+)'

    # Match the pattern in the text
    matches = re.search(pattern, text)

    if matches:
        lower_blind = float(matches.group(1))  # ¥5.00
        higher_blind = float(matches.group(2))  # 10.00
       
        
        print(f"lower_blind: {lower_blind}")
        print(f"higher_blind: {higher_blind}")
     
    else:
        lower_blind = ''
        higher_blind = ''

    return lower_blind , higher_blind


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
    current_players = 0
    max_players = 0
    if len(text) < 2 :
        return current_players , max_players
    current_players = text[0]
    max_players = text[1]
    if max_players == 1 :
        max_players = 4
    print(f'{current_players} , {max_players}')
    return current_players , max_players

previous_text, previous_gray_image = ocr_image(capture_screen(bbox))

while True:
    current_image = capture_screen(bbox)
    current_text, current_gray_image = ocr_image(current_image)
    
    if current_text != previous_text:
        print("Change detected!")
        previous_text = current_text
    dict = []
    # Get all instances of "PLAY" coordinates
    play_coords = get_text_coordinates(current_gray_image, "PLAY")
    if play_coords:

        for coord in play_coords:
            x, y, width, height = coord
            click_x = x + left + width // 2  # Adjust click_x relative to the screen
            click_y = y + top + height // 2  # Adjust click_y relative to the screen
            print(f"'LET'S PLAY' found at coordinates: (x: {click_x}, y: {click_y})")
            blinds_box = (1000 , click_y - 18 , 1170 , click_y + 18)
            print(blinds_box)
            blinds_text , blinds_gray_img = ocr_image(capture_screen(blinds_box))
            blinds_text = replace_characters(blinds_text , '7' , '¥')
            blinds_text = replace_characters(blinds_text , '%' , '¥')
            lower_blind , higher_blind = get_blinds(blinds_text)
            players_box = (1240 , click_y - 20 , 1300 , click_y + 20)
            print(players_box)
            players_text , players_gray_img = ocr_image(capture_screen(players_box))
            cv2.imwrite('players_gray_img.png', players_gray_img)
            current_players , maximum_players = get_players('players_gray_img.png')
            print(players_text)
            details = {
                    'lower_blind':lower_blind ,
                    'higher_blind':higher_blind ,
                    'current_players' : current_players,
                    'maximum_players' : maximum_players
            }
            dict.append(details)
        print("'LET'S PLAY' not found.")
    
    print(dict)
    # Wait before capturing again
    time.sleep(1)