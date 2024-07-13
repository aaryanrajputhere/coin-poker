import pyautogui
from test import *
from functions import *
def trim_player_names(final_players):
    trimmed_final_players = []
    for player, coords in final_players:
        trimmed_name = player.split('\n')[0]  # Extract text up to the first newline
        trimmed_final_players.append((trimmed_name, coords))
    return trimmed_final_players

final_players = [ ('Take\nSeat\n', (1700, 162, 1900, 230)), ('Take\nSeat\n', (1712, 368, 1912, 440)), ('Take\nSeat\n', (1459, 500, 1689, 570)), ('John\nSeat\n', (1147, 499, 1347, 569)), ('Take\nSeat\n', (921, 372, 1121, 442)), ('Take\nSeat\n', (938, 168, 1138, 238)),('Chattahoochee\n¥ 8,000.00\n', (1308, 90, 1508, 160))]


def is_fish(final_players, fishes):
    
    fish_indices = []
    for index, player in enumerate(final_players):
        for fish in fishes:
            if fish in player[0]:
                print(f"{player} at index {index} is a fish")
                fish_indices.append(index)
    return fish_indices
   



final_players = trim_player_names(final_players)
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



def select_seat(final_players):
    fishes = [
    "Sashimi123",
    "Madvin",
    "John",
    "Alice",
    "Bob",
    "Eve",
    "Michael",
    "Sophia",
    "David",
    "Emily",
    "James",
    "Olivia",
    "Chattahoochee",
    "omaha4rollz"
    ]
    final_players = trim_player_names(final_players)
    fish_index = is_fish(final_players , fishes)
    if len(fish_index)>=1:
        fish_index = fish_index[0]
        seat_to_take = take_seat(fish_index, final_players)
        x = (seat_to_take[0] + seat_to_take[2]) / 2
        y = (seat_to_take[1] + seat_to_take[3]) / 2
        click_when_idle(x, y)
        print(f"Clicked at - (x: {x}, y: {y})")
    else:
        print("No Fish found")
        

