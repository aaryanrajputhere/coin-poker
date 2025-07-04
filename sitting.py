from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'D:\opener\opener v2\resources\tesseract\tesseract.exe'  # Update this path based on your Tesseract installation

def find_text_in_coordinates(image_path, coordinates, save_path):
    # Open the image using Pillow
    image = Image.open(image_path)
    
    # Get the dimensions of the image
    image_width, image_height = image.size
    print(f"Image dimensions - Width: {image_width}, Height: {image_height}")

    # Crop the image based on the given coordinates
    left, top, right, bottom = coordinates
    cropped_image = image.crop((left, top, right, bottom))

    
    # Save the cropped image
    cropped_image.save(save_path)
    
    # Use pytesseract to extract text from the cropped image
    text = pytesseract.image_to_string(cropped_image)
    
    # Print the extracted text
    print(f"Extracted text from coordinates {coordinates}:")
   
    return text

image_path = "sitting7.jpg"
save_path = "test.jpg"
seats4 = [(210, 100 , 410 , 170),
         (615, 100 , 815 , 170),
         (615, 515 , 815 , 585),
         (210, 515 , 410 , 585),
         
         ]

seats7 = [
        (412, 90, 612, 160),      # Top-left seat
        (805, 162, 1005, 230),     # Top-right seat
        (813, 368, 1013, 440),     # Middle-right seat
        (572, 500, 772, 570),     # Bottom-right seat
        (247, 499, 447, 569),     # Bottom-left seat
        (36, 372, 236, 442),      # Middle-left seat
        (47, 168, 247, 238) 
]

    

