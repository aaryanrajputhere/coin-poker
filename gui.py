import tkinter as tk

def save_data():
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
save_button.grid(row=3, column=7, columnspan=2, pady=20)

# Add the Add Row button
add_row_button = tk.Button(root, text="Add Row", command=add_row)
add_row_button.grid(row=4, column=7, columnspan=2, pady=20)

# Run the main event loop
root.mainloop()


