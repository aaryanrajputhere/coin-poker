import subprocess
from PIL import Image
import os

# Define the command as a list of strings
def take_screenshot(window_title , image_path):
    command = ["winapi/winapi.exe", "--screenshot", "--window", window_title , "--name" , image_path]

    # Run the command
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Command output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)
        print("Command output (if any):", e.stdout)
    except Exception:
        print("An error occurred")


def bmp_to_jpg(bmp_path, jpg_path):
       
    try:
        # Open the BMP file
        with Image.open(bmp_path) as img:
            # Save as JPG
            img.convert("RGB").save(jpg_path, "JPEG")
            print(f"Converted {bmp_path} to {jpg_path}")
    except IOError as e:
        print(f"Error converting {bmp_path}:", e)
