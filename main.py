import pygetwindow as gw
import time
from functions import *
import pyautogui
from sitting import *
from fish import *
import os
window_title = 'CoinPoker - Lobby'  # Update with the exact title of the window
window = None

# Loop through all windows and find the matching title
for w in gw.getWindowsWithTitle(window_title):
    print(w)
    print("---")
    if w.title == window_title:
        window = w
        break

if not window:
    raise Exception(f'Window with title "{window_title}" not found!')

# Get the window coordinates
left, top, right, bottom = window.left, window.top, window.right, window.bottom
# Example usage:
window_title_to_check = "CoinPoker - Lobby"  # Replace with the title of the window you want to check
bbox = (0, 0, 1920, 1080)
time.sleep(2)
previous_text, previous_gray_image = ocr_image(capture_screen(bbox))

while True:   
    if is_window_active(window_title_to_check):
        print(left, top, right, bottom)
        print(f"The window '{window_title_to_check}' is active.")
        current_image = capture_screen(bbox)
        current_text, current_gray_image = ocr_image(current_image)
        cv2.imwrite('plas_gray_img.png', previous_gray_image)
        if current_text != previous_text:
            print("Change detected!")
            previous_text = current_text
        dict = []
        # Get all instances of "PLAY" coordinates
        play_coords = get_text_coordinates(current_gray_image, "Price")
        lets_play_coords = w.left + w.width - 330
        while True:
            blinds_coords = get_text_coordinates(current_gray_image, "BLINDS")
            print(blinds_coords)
            print("Try")
            if blinds_coords != []:
                break
        
        i = 1
        while True:
            
            gap = 37
            blinds_bbox = (blinds_coords[0][0]-50, blinds_coords[0][1]+18 + gap*(i-1) ,blinds_coords[0][0]+120 , blinds_coords[0][1] +18 + gap*i )
            blinds_text , blinds_gray_img = ocr_image(capture_screen(blinds_bbox))
            # cv2.imwrite(f'blinds_gray_img{i}.png', blinds_gray_img)
            blinds_text = replace_characters(blinds_text , '7' , '¥')
            blinds_text = replace_characters(blinds_text , '%' , '¥')
            blinds_text = replace_characters(blinds_text ,  '¥' , ' ' )
            blinds_text = replace_characters(blinds_text , '/' , ' ')
            players_bbox = (blinds_coords[0][0]+120 ,blinds_coords[0][1]+18 + gap*(i-1) , lets_play_coords  , blinds_coords[0][1] +18 + gap*i )
            players_text , players_gray_img = ocr_image(capture_screen(players_bbox))
            cv2.imwrite(f'players_gray_img{i}.png', players_gray_img)
            maximum_players = get_players(f'players_gray_img{i}.png')
            os.remove(f'players_gray_img{i}.png')
            lower_blind , higher_blind = get_blinds(blinds_text)
            
            print(f"Row : {i}")
            details = {
                'lower_blind':lower_blind ,
                'higher_blind':higher_blind ,
                'maximum_players' : maximum_players
            }
            if maximum_players == 7:
                click_when_idle( lets_play_coords , blinds_coords[0][1]+30 + gap*(i-1) ,)
                time.sleep(5)
                final_players = get_final_players_with_coords()
                select_seat(final_players)
            print(details)

            
            if i>=15:
                break
            i += 1
    else:
        print(f"The window '{window_title_to_check}' is inactive.")
    time.sleep(1)
    
       