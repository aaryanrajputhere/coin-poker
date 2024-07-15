import pygetwindow as gw
import time
from functions import *
import pyautogui
from sitting import *
from fish import *
import os
import tkinter as tk
seats_sets7= [
    [
        (1308, 90, 1508, 160),      # Top-left seat
        (1700, 162, 1900, 230),     # Top-right seat
        (1712, 368, 1912, 440),     # Middle-right seat
        (1459, 500, 1689, 570),     # Bottom-right seat
        (1147, 499, 1347, 569),     # Bottom-left seat
        (921, 372, 1121, 442),      # Middle-left seat
        (938, 168, 1138, 238)       # Another seat
    ],
    [
        (1305, 381, 1505, 451),      # Top-left seat
        (1700, 460, 1900, 530),     # Top-right seat
        (1712, 671, 1912, 741),     # Middle-right seat
        (1459, 802, 1689, 872),     # Bottom-right seat
        (1147, 802, 1347, 872),     # Bottom-left seat
        (921, 670, 1121, 740),      # Middle-left seat
        (938, 460, 1138, 530)       # Another seat
    ],
    [
        (412, 90, 612, 160),      # Top-left seat
        (805, 162, 1005, 230),     # Top-right seat
        (813, 368, 1013, 440),     # Middle-right seat
        (572, 500, 772, 570),     # Bottom-right seat
        (247, 499, 447, 569),     # Bottom-left seat
        (36, 372, 236, 442),      # Middle-left seat
        (47, 168, 247, 238)       # Another seat
    ],
    [
        (412, 380, 612, 450),      # Top-left seat
        (805, 455, 1005, 525),     # Top-right seat
        (813, 670, 1013, 741),     # Middle-right seat
        (572, 802, 772, 872),      # Bottom-right seat
        (247, 802, 447, 872),      # Bottom-left seat
        (36, 670, 236, 740),       # Middle-left seat
        (47, 460, 247, 530)        # Another seat
    ],
]
seats_sets4= [
    [
        (1100, 95, 1300, 165),      
        (1515, 95, 1715, 165),     
        (1515, 515, 1715, 585),     
        (1100, 515, 1300, 585),     

    ],
    [
        (214, 93, 414, 163),      
        (612, 93, 812, 163),     
        (612, 515, 812, 585),     
        (214, 515, 414, 585),     

    ],
    [
        (1100, 380, 1300, 450),      
        (1515, 380, 1715, 450),     
        (1515, 800, 1715, 870),     
        (1100, 800, 1300, 870),     

    ],
    [
        (214, 380, 414, 450),      
        (612, 380, 812, 450),     
        (612, 800, 812, 870),     
        (214, 800, 414, 870),     

    ],
]

def save_data():
    global data
    data = []
    for row in entries:
        row_data = [entry.get() for entry in row[:2]]
        players4 = row[2].get()
        players7 = row[3].get()
        if players4:
            data.append(row_data + ["4"])
        if players7:
            data.append(row_data + ["7"])
    print("Saved Data:", data)  # You can replace this with actual save functionality
    root.destroy()  # Close the application window

def add_row():
    row = len(entries) + 1
    
    lower_blind_entry = tk.Entry(root)
    higher_blind_entry = tk.Entry(root)
    players4_var = tk.BooleanVar()
    players7_var = tk.BooleanVar()
    
    lower_blind_entry.grid(row=row, column=0, padx=10, pady=5)
    higher_blind_entry.grid(row=row, column=1, padx=10, pady=5)
    
    players4_check = tk.Checkbutton(root, text="4", variable=players4_var)
    players7_check = tk.Checkbutton(root, text="7", variable=players7_var)
    
    players4_check.grid(row=row, column=2, padx=5, pady=5)
    players7_check.grid(row=row, column=3, padx=5, pady=5)
    
    entries.append([lower_blind_entry, higher_blind_entry, players4_var, players7_var])

# Create the main window
root = tk.Tk()
root.title("Poker Game Settings")
root.geometry("600x400")  # Adjust size as needed

# Create labels for columns
tk.Label(root, text="Lower Blind").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Higher Blind").grid(row=0, column=1, padx=10, pady=5)
tk.Label(root, text="Maximum Players").grid(row=0, column=2, columnspan=2, padx=10, pady=5)

# Create the initial rows of input boxes
entries = []
for i in range(10):
    add_row()

# Add the Save button
save_button = tk.Button(root, text="Save", command=save_data)
save_button.grid(row=3, column=7, columnspan=2, pady=0)

# Add the Add Row button
add_row_button = tk.Button(root, text="Add Row", command=add_row)
add_row_button.grid(row=4, column=7, columnspan=2, pady=0)

# Run the main event loop
root.mainloop()

# Now data contains the saved information
print(data)

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
            try:
                lower_blind = int(float(lower_blind))
                higher_blind = int(float(higher_blind))
            except:
                pass
            print(f"Row : {i}")
            details = {
                'lower_blind':lower_blind ,
                'higher_blind':higher_blind ,
                'maximum_players' : maximum_players
            }
            if maximum_players == 7:
                seats_sets = seats_sets7
            elif maximum_players == 4:
                seats_sets = seats_sets4
            for det in data:
                if details['lower_blind'] == int(det[0]) and details['higher_blind'] == int(det[1]) and details['maximum_players'] == int(det[2]):
                    click_when_idle( lets_play_coords , blinds_coords[0][1]+30 + gap*(i-1) ,)
                    time.sleep(5)
                    final_players = get_final_players_with_coords(seats_sets)
                    select_seat(final_players)
            
           

            if i>=15:
                break
            i += 1
    else:
        print(f"The window '{window_title_to_check}' is inactive.")
    time.sleep(1)
