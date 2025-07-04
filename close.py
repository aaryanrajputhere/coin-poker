import pygetwindow as gw
def minimize_window_by_title(window_title):
    try:
        # Get the window by its title
        window = gw.getWindowsWithTitle(window_title)[0]
        
        # Minimize the window
        if window:
            window.minimize()
            print(f'Window "{window_title}" minimized.')
        else:
            print(f'Window "{window_title}" not found.')
    except IndexError:
        print(f'No window with title "{window_title}" found.')


minimize_window_by_title('C:\WINDOWS\system32\cmd.exe')