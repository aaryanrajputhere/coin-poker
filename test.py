from click import run_winapi_click
import pygetwindow as gw

def click_on_blinds_windows(x, y):
    windows = gw.getAllTitles()
    blinds_titles = [title for title in windows if 'Blinds' in title]
    print(blinds_titles)
    if not blinds_titles:
        print("No new window with 'Blinds' in the title found.")
        return

    for title in blinds_titles:
        run_winapi_click(title, x, y)
        print(f"Clicked on '{title}' at ({x}, {y})")

# Example usage
click_on_blinds_windows(1000,650)