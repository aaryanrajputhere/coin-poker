from PIL import Image, ImageDraw
import pytesseract
import cv2
import numpy as np
from functions import *
from take_screenshot import *
from click import * 
import tkinter as tk
from fish import *
from PIL import Image, ImageEnhance, ImageFilter
from calibrate import *
import os
import pygetwindow as gw

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path based on your Tesseract installation
# Update this path based on your Tesseract installation

# Google Sheet Skip Players
gc = gspread.oauth(
        credentials_filename='credentials.json',
    authorized_user_filename='authorized_user.json'
)

sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1zgWASElEgB2fG2weHyxfbE7JMsJWMfUsCEh359dhOl4')
worksheet = sht2.worksheet("Sheet1")
skip_players = [item for item in worksheet.col_values(1) if item]
print("Skip Players are : ")
print(skip_players)
skip_players = skip_players[1:]

seats4 =[ [1920/2 - 380 - 180 , 120 , 1920/2 - 380 + 180 , 250],
         [1920/2 + 380 - 180 , 120 , 1920/2 + 380 + 180 , 250],
         [1920/2 + 380 - 180 , 720 , 1920/2 + 380 + 180 , 850],
         [1920/2 - 380 - 180 , 720 , 1920/2 - 380 + 180 , 850],
         ] 


seats7 =[ [1920/2 - 180 , 110 , 1920/2 + 180 , 240],
         [1920/2 + 750 - 180 , 225 , 1920/2 + 750 +  180 , 355],
         [1920/2 + 765 - 180 , 520 , 1920/2 + 765 +  180 , 650],
         [1920/2 + 315 - 180 , 710 , 1920/2 + 315 + 180 , 840],
         [1920/2 - 305 - 180 , 710 , 1920/2 - 305 + 180 , 840],
        [1920/2 - 730 - 180 , 520 , 1920/2 - 730 +  180 , 650],
        [1920/2 - 690 - 180 , 225 , 1920/2 - 690 +  180 , 355]
         ] 


# CODE FOR RANGE INPUT
# def save_data():
#     global data
#     data = []
#     for row in entries:
#         row_data = [entry.get() for entry in row[:4]]
#         players4 = row[2].get()
#         players7 = row[3].get()
#         if players4:
#             data.append(row_data + ["4"])
#         if players7:
#             data.append(row_data + ["7"])
#     print("Saved Data:", data)  # You can replace this with actual save functionality
#     root.destroy()  # Close the application window

# def add_row():
#     row = len(entries) + 1
    
#     lower_blind_entry_low = tk.Entry(root)
#     higher_blind_entry_low = tk.Entry(root)
#     lower_blind_entry_high = tk.Entry(root)
#     higher_blind_entry_high = tk.Entry(root)
#     players4_var = tk.BooleanVar()
#     players7_var = tk.BooleanVar()
    
#     lower_blind_entry_low.grid(row=row, column=0, padx=10, pady=5)
#     higher_blind_entry_low.grid(row=row, column=2, padx=10, pady=5)
#     lower_blind_entry_high.grid(row=row, column=1, padx=10, pady=5)
#     higher_blind_entry_high.grid(row=row, column=3, padx=10, pady=5)
    
#     players4_check = tk.Checkbutton(root, text="4", variable=players4_var)
#     players7_check = tk.Checkbutton(root, text="7", variable=players7_var)
    
#     players4_check.grid(row=row, column=4, padx=5, pady=5)
#     players7_check.grid(row=row, column=5, padx=5, pady=5)
    
#     entries.append([lower_blind_entry_low, higher_blind_entry_low, lower_blind_entry_high , higher_blind_entry_high ,players4_var, players7_var])

# # Create the main window
# root = tk.Tk()
# root.title("Poker Game Settings")
# root.geometry("1920x1080")  # Adjust size as needed

# # Create labels for columns
# tk.Label(root, text="Lower Blind Min").grid(row=0, column=0, padx=10, pady=5)
# tk.Label(root, text="Lower Blind Max").grid(row=0, column=1, padx=10, pady=5)
# tk.Label(root, text="Higher Blind Min").grid(row=0, column=2, padx=10, pady=5)
# tk.Label(root, text="Higher Blind Max").grid(row=0, column=3, padx=10, pady=5)
# tk.Label(root, text="Maximum Players").grid(row=0, column=4, columnspan=2, padx=10, pady=5)

# # Create the initial rows of input boxes
# entries = []
# for i in range(10):
#     add_row()
# # print('---')
# # print(entries)

# # Add the Save button
# save_button = tk.Button(root, text="Save", command=save_data)
# save_button.grid(row=3, column=7, columnspan=2, pady=0)

# # Add the Add Row button
# add_row_button = tk.Button(root, text="Add Row", command=add_row)
# add_row_button.grid(row=4, column=7, columnspan=2, pady=0)

# # Run the main event loop
# root.mainloop()

# # Now data contains the saved information
# print(data)

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
root.geometry("800x600")  # Adjust size as needed

# Create labels for columns
tk.Label(root, text="Lower Blind").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Higher Blind").grid(row=0, column=1, padx=10, pady=5)
tk.Label(root, text="Maximum Players").grid(row=0, column=2, columnspan=2, padx=10, pady=5)

# Create the initial rows of input boxes
entries = []
for i in range(10):
    add_row()

# Auto - Sitting Button
auto_sitting_var = tk.BooleanVar()
auto_sitting = tk.Checkbutton(root, text="Auto - Sitting" , variable=auto_sitting_var)
auto_sitting.grid(row = 3 , column = 7 , columnspan= 2 , pady = 0)
# Add Row button
add_row_button = tk.Button(root, text="Add Row", command=add_row)
add_row_button.grid(row=4, column=7, columnspan=2, pady=0)

# Save button
save_button = tk.Button(root, text="Save", command=save_data)
save_button.grid(row=5, column=7, columnspan=2, pady=0)

# Run the main event loop
root.mainloop()

# Now data contains the saved information
print(data)

calibration_file = 'calibration_data.json'

if not os.path.exists(calibration_file) or is_file_empty(calibration_file):
    print("Calibrate Blinds Position")
    print("Click on the top left corner of the first blind field, then the bottom right corner")
    blindx1, blindy1, blindx2, blindy2 = calibrate()
    gap1 = blindy2 - blindy1
    print("Calibrate Players Position")
    print("Click on the top left corner of the first players field, then the bottom right corner")
    playersx1, playersy1, playersx2, playersy2 = calibrate()
    gap2 = playersy2 - playersy1
    print("Calibrate Buttons Position")
    print("Click on the top left corner of the first let's play button, then the bottom right corner")
    buttonx1, buttony1, buttonx2, buttony2 = calibrate()
    gap3 = buttony2 - buttony1


    calibration_data = {
        'blind': [blindx1, blindy1, blindx2, blindy2],
        'gap1': gap1,
        'players': [playersx1, playersy1, playersx2, playersy2],
        'gap2': gap2,
        'button': [buttonx1, buttony1, buttonx2, buttony2],
        'gap3': gap3
    }
    
    save_calibration_data(calibration_file, calibration_data)
else:
    calibration_data = load_calibration_data(calibration_file)
    blindx1, blindy1, blindx2, blindy2 = calibration_data['blind']
    gap1 = calibration_data['gap1']
    playersx1, playersy1, playersx2, playersy2 = calibration_data['players']
    gap2 = calibration_data['gap2']
    buttonx1, buttony1, buttonx2, buttony2 = calibration_data['button']
    gap3 = calibration_data['gap3']

while True:
    window_title = 'CoinPoker - Lobby'
    take_screenshot(window_title , "lobby.bmp")
    bmp_to_jpg("lobby.bmp" , "lobby.jpg")
    window = None

    # Loop through all windows and find the matching title
    for w in gw.getWindowsWithTitle(window_title):
        print(w)
        print("---")
        if w.title == window_title:
            window = w
            break
    print(w.top ,w.right)    

    # Example usage
    image_path = 'lobby.jpg'  # Update this with the path to your image
    search_text = 'BLINDS'    # Update this with the text you want to find


    image = Image.open(image_path)
    image_width, image_height = image.size
    # blinds_coords  = (x - 15 , y + 16 , x + 500 , image_height - 50 )
    # blinds_text = find_text_in_coordinates(image_path, blinds_coords, f'blinds.png')

    for i in range(15):
        blinds_coords = (blindx1 , blindy1 + gap1*i  , blindx2 , blindy2 +gap1*i )
        
        blinds_text = find_text_in_coordinates(image_path, blinds_coords, f'blinds/blinds{i}.png')
        
        blinds_text = replace_characters(blinds_text, '7', '¥')
        blinds_text = replace_characters(blinds_text, '%', '¥')
        blinds_text = replace_characters(blinds_text, '¥', ' ')
        blinds_text = replace_characters(blinds_text, '/', ' ')
        blinds_text = replace_characters(blinds_text, 'F', ' ')
        blinds_text = replace_characters(blinds_text, '#', ' ')
   
        values = blinds_text.split()
        try:
            lower_blind = float(values[0])
            higher_blind = float(values[1])
            # print(lower_blind , higher_blind)
            player_coords  = (playersx1 , playersy1 + gap2 * i , playersx2   , playersy2  + gap2 * i )
            player_text = find_text_in_coordinates(image_path, player_coords, f'players/players{i}.png')
            player_text = get_players(f'players/players{i}.png')
            # print(f"players : {player_text}")
            if len(values) == 0:
                continue
            if "7" in player_text:
                maximum_players = 7
            else:
                maximum_players = 4
            
            details = {
                'lower_blind':lower_blind ,
                'higher_blind':higher_blind ,
                'maximum_players' : maximum_players
            }
            print(details)
            # titles = all_tables()
            # print(titles)
            # for title in titles:
            #     run_winapi_click(title)
            for det in data:
                # if int(det[0]) <= int(details['lower_blind']) <= int(det[2]) and int(det[1]) <= int(details['higher_blind']) <= int(det[3]) and int(details['maximum_players']) == int(det[4]):
                if details['lower_blind'] == int(det[0]) and details['higher_blind'] == int(det[1]) and details['maximum_players'] == int(det[2]):   
                    print("-----------------------------")
                    print(f"Table Found with {det}")
                    print("-----------------------------")
                    run_winapi_click(window_title , (buttonx1 + buttonx2) / 2, (buttony1 + buttony2) / 2 + i * gap3)
                    run_winapi_click(window_title , (buttonx1 + buttonx2) / 2, (buttony1 + buttony2) / 2 + i * gap3)
                    time.sleep(2)
                    table_window_title = find_window()
                    print(f"Auto - Sitting : {auto_sitting_var.get()}")
                    print(f"Maximizing All Windows...")
                    
                    if table_window_title != None  and auto_sitting_var.get():
                       
                        table_window = gw.getWindowsWithTitle(table_window_title)[0]
                        table_window.maximize()
                        click_on_blinds_windows(1000,650)
                        print("-------------------------------")
                        print(f"Reading all the players present from {table_window_title}")
                        print("-------------------------------")
                        # run_winapi_click(table_window_title , 510 , 365)
                        take_screenshot(table_window_title , "table.bmp")
                        bmp_to_jpg("table.bmp" , "table.jpg")
                        table_img = "table.jpg"
                        # if maximum_players == 4 :
                        #     seats = seats4
                        # else:
                        #     seats = seats7
                        final_players = []
                        if "4 Max" in table_window_title:
                            seats =seats4
                        else:
                            seats = seats7
                        i = 0
                        for  coords in seats:
                                save_path = f"seats/seat{i}.jpg"
                                text = find_text_in_coordinates_players(table_img , coords , save_path)
                                player = [text , coords]
                                final_players.append(player)
                                i+=1
                        print(final_players)
                        final_players = trim_player_names(final_players)
                        print(final_players)
                        flag = 0 
                        for index, player in enumerate(final_players):
                            for skip_player in skip_players:
                                if skip_player in player[0]:
                                    print('------------------------------------------------------------------')
                                    print('Skip Player Found.')
                                    close_window_by_title(table_window_title)
                                    print('------------------------------------------------------------------')
                                    flag = 1
                        if flag == 0:             
                            fish_indices = is_fish(final_players , fishes)
                            print(final_players)
                            if len(fish_indices) == 0 :
                                print("No fish found")
                                continue
                            fish_index = fish_indices[0]
                            seat_coords = take_seat(fish_index , final_players)
                        
                            run_winapi_click(table_window_title , seat_coords[0] , seat_coords[1] )
                else :
                    print("-----------------------------")
                    print(f"Table with {det} not found.")
                    print("-----------------------------")
            click_on_blinds_windows(480, 400)

        except ValueError:
            print("Conversion error: Could not convert values to float.")
        except IndexError:
            print("Index error: Not enough elements in the 'values' list.")
               
    # rows = [row.strip() for row in blinds_text.split("\n") if row.strip()]
   
    # length = len(rows)
    # if length % 2 != 0: 
    #     rows.append("1/7") 
    # length = len(rows)

    # midpoint = (length // 2)
    # for i in range(0 , midpoint):
    #     row = rows[i]
    #     row = replace_characters(row, '7', '¥')
    #     row = replace_characters(row, '%', '¥')
    #     row = replace_characters(row, '¥', ' ')
    #     row = replace_characters(row, '/', ' ')
    #     row = replace_characters(row, 'F', ' ')
    #     row = replace_characters(row, '#', ' ')
    #     values = row.split()
    #     lower_blind = float(values[0])  
    #     higher_blind = float(values[1]) 
    #     if lower_blind == 250.0:
    #         lower_blind = 2.5
        
    #     if "7" in rows[i+midpoint]:
    #         maximum_players = 7
    #     else:
    #         maximum_players = 4

    #     details = {
    #         'lower_blind':lower_blind ,
    #         'higher_blind':higher_blind ,
    #         'maximum_players' : maximum_players
    #     }
    #     print(details)
    #     for det in data:
    #             if details['lower_blind'] == int(det[0]) and details['higher_blind'] == int(det[1]) and details['maximum_players'] == int(det[2]):
    #                 run_winapi_click(1300 , 220 + 30 *i)
                
    #                 table_img = "sitting7.jpg"
                    
    #                 if maximum_players == 4 :
    #                     seats = seats4
    #                 else:
    #                     seats = seats7
    #                 final_players = []
    #                 i = 0
    #                 for  coords in seats:
    #                         save_path = f"seats/seat{i}.jpg"
    #                         text = find_text_in_coordinates(image_path , coords , save_path)
    #                         player = [text , coords]
    #                         final_players.append(player)
    #                         i+=1
    #                 final_players = trim_player_names(final_players)
    #                 fish_indices = is_fish(final_players , fishes)
    #                 print(final_players)
    #                 if len(fish_indices) == 0 :
    #                     print("No fish found")
    #                     continue
    #                 fish_index = fish_indices[0]
    #                 take_seat(fish_index , final_players)

                
                
            
        
            
      

    time.sleep(10)    