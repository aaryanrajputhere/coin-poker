import gspread
from functions import *
def trim_player_names(final_players):
    trimmed_final_players = []
    for player, coords in final_players:
        player = replace_characters(player, '@', '')
        player = replace_characters(player, ' ', '')
        player = replace_characters(player, '.', '')
        player = replace_characters(player, ',', '')
        for i in range(9):
            player = replace_characters(player, f'{i}', '')
        trimmed_name = player.split('\n')[0]  # Extract text up to the first newline
        trimmed_final_players.append((trimmed_name, coords))
    return trimmed_final_players


fishes = []

def load_fishes():
    global fishes

    gc = gspread.oauth(
            credentials_filename='credentials.json',
        authorized_user_filename='authorized_user.json'
    )

    sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1zgWASElEgB2fG2weHyxfbE7JMsJWMfUsCEh359dhOl4')
    worksheet = sht2.worksheet("Sheet1")
    fishes = [item for item in worksheet.col_values(1) if item]

    print(fishes)

def is_fish(final_players, fishes):
    if len(fishes) == 0:
        load_fishes()
    
    print(fishes)
    fish_indices = []
    for index, player in enumerate(final_players):
        
        for fish in fishes:
            if fish in player[0]:
                print(f"{player} at index {index} is a fish")
                fish_indices.append(index)
    return fish_indices

def take_seat(fish_index, final_players):
    n = len(final_players)

    # Check the seats in circular order starting from fish_index + 1
    for i in range(1, n):
        index = (fish_index + i) % n
        if "Take" in final_players[index][0]:
            print(f"Take this seat: {final_players[index][1]} (at index {index})")
            return final_players[index][1]

    # If no empty seat is found
    print("No empty seat found")
    return None
