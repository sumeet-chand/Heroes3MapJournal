# /Heroes3MapLiker.py

import tkinter as tk
from PIL import Image, ImageTk
from typing import Dict
import os
from display_gui import display_gui

SCREEN_WIDTH: int = 1100
SCREEN_HEIGHT: int = 720
COLS: int = 1
IMAGE_WIDTH: int = 300
IMAGE_HEIGHT: int = 300
SPACING_X: int = 20
SPACING_Y: int = 20
root = tk.Tk()
root.title("Heroes 3 Map Liker")
assets_directory = "assets"
map_images_dir = os.path.join(assets_directory, "map_images")

def set_window_icon():
    """
    Set the icon for the Tkinter GUI window.

    Opens an image file specified by `icon_path`, resizes it to (32, 32) if necessary, 
    and sets it as the window icon.

    Args:
        icon_path (str): The file path to the icon image.

    Returns:
        None
    """
    icon_path = Image.open("assets/view_earth.png")  # Open the image
    icon_path = icon_path.resize((32, 32))  # Resize the image if required
    icon = ImageTk.PhotoImage(icon_path)  # Convert the image to a PhotoImage
    root.iconphoto(False, icon) # set as software window icon

def load_asset_images(directory: str) -> Dict[str, ImageTk.PhotoImage]:
    """
    Load all asset images from a directory, resize them to (32, 32), and return a dictionary of PhotoImage objects.

    Args:
        directory (str): The directory path containing the images.

    Returns:
        dict: A dictionary containing PhotoImage objects with filenames (without extension) as keys.
    """
    photo_images = {}
    for filename in os.listdir(directory):
        if filename.endswith(('.png', '.gif', '.jpg', '.jpeg')):
            path = os.path.join(directory, filename)
            try:
                name = os.path.splitext(filename)[0]  # Extract filename without extension
                image = Image.open(path)  # Load the image
                image = image.resize((32, 32))  # Resize the image
                photo_images[name] = ImageTk.PhotoImage(image)  # Load image and store it in the dictionary
            except Exception as e:
                print(f"Error loading image {path}: {e}")
    return photo_images

photo_images: Dict[str, ImageTk.PhotoImage] = load_asset_images(assets_directory)

def create_directories_if_missing():
    """
    Create directories to hold scrapped map images if they dont exist
    Returns:
        None
    """
    # create image directory if they don't exist
    if not os.path.exists(map_images_dir):
        os.makedirs(map_images_dir)

set_window_icon()
create_directories_if_missing()
display_gui(root, SCREEN_WIDTH, SCREEN_HEIGHT, COLS, IMAGE_WIDTH, IMAGE_HEIGHT, SPACING_X, SPACING_Y, map_images_dir, photo_images)

root.mainloop()
