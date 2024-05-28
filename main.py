import tkinter as tk
from display_gui import display_gui
import os

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 720
COLS = 3
IMAGE_WIDTH = 300
IMAGE_HEIGHT = 300
SPACING_X = 20
SPACING_Y = 20
base_dirs = ["Heroes3OverworldImages", "Heroes3UndergroundImages"]

root = tk.Tk()
root.title("Heroes 3 Map Liker")

# Load the icon image
icon_path = "assets/beholder.png"
icon = tk.PhotoImage(file=icon_path)
root.iconphoto(False, icon)

# create directories if they dont exist
for base_dir in base_dirs:
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

display_gui(root, SCREEN_WIDTH, SCREEN_HEIGHT, COLS, IMAGE_WIDTH, IMAGE_HEIGHT, SPACING_X, SPACING_Y, base_dirs)
root.mainloop()
