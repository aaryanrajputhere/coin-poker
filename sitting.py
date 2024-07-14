from PIL import ImageGrab
import pytesseract
import cv2
import numpy as np
import time
time.sleep(4)
# Path to tesseract executable (update with your Tesseract-OCR path if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to perform OCR on an image
def ocr_image_sitting(image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    
    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(gray_image)
    
    return text

# Define the coordinates for multiple sets of seats

# Function to count occurrences of 'Take' in a sublist
def count_take(sublist):
    return sum(1 for item in sublist if 'Take' in item)

# Function to extract player names and their seat coordinates from seat sets
def extract_players_with_coords(seats_sets):
    players_with_coords = []

    for set_idx, seats in enumerate(seats_sets):
        print(f"Processing Set {set_idx + 1}:")
        player_with_coords = []
        for i, (left, top, right, bottom) in enumerate(seats):
            # Define the box coordinates (left, top, right, bottom)
            box = (left, top, right, bottom)
            
            # Capture screenshot
            screenshot = ImageGrab.grab(bbox=box)
            
            # Perform OCR on the screenshot
            text = ocr_image_sitting(screenshot)
            
            # Print or use the extracted text
            print(f"Text extracted from seat {i+1} in Set {set_idx + 1}:")
            print(text)
            print("---------------------------")
            
            player_with_coords.append((text, box))  # Collect text and box from each seat
        players_with_coords.append(player_with_coords)
    print("Text extraction complete.")
    return players_with_coords

# Main function to determine final players based on 'Take' occurrences
def get_final_players_with_coords(seats_sets):
    players_with_coords = extract_players_with_coords(seats_sets)
    
    # Initialize variables to track maximum count and corresponding sublist
    max_count = 0
    max_sublist = None
    
    # Iterate through each sublist and find the one with the most 'Take' occurrences
    for sublist in players_with_coords:
        take_count = count_take([item[0] for item in sublist])  # Count 'Take' in player names
        if take_count > max_count:
            max_count = take_count
            max_sublist = sublist
    
    # Return the sublist with the most 'Take' occurrences along with their seat coordinates
    final_players_with_coords = [(player, box) for player, box in max_sublist] if max_sublist else []
    print("Final players list with the most 'Take' occurrences:")
    print(final_players_with_coords)
    return final_players_with_coords

# Example usage:

