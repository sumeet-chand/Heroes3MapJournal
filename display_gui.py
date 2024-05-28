import tkinter as tk
from PIL import Image, ImageTk
import os
from download_images import download_images
import urllib.parse

def display_gui(root, SCREEN_WIDTH, SCREEN_HEIGHT, COLS, IMAGE_WIDTH, IMAGE_HEIGHT, SPACING_X, SPACING_Y, base_dirs):
    def update_images():
        # Function to update images
        progress_label.config(text="Rescanning images...")
        root.update()  # Force update of the GUI
        download_images(base_dirs[0], base_dirs[1], update_progress)  # Assuming base_dirs[0] is for overworld and base_dirs[1] is for underground
        load_images()  # Reload images after updating

    def update_progress(status):
        # Function to update progress label
        progress_label.config(text=status)
        root.update()  # Force update of the GUI

    def show_map_name(event, map_name):
        # Function to display the map name
        cleaned_name = map_name.replace('_', ' ').replace(' map auto', '')
        cleaned_name = urllib.parse.unquote(cleaned_name)  # Decode any URL-encoded characters
        map_name_label.config(text=f"Map: {cleaned_name}")

    def load_images():
        # Function to load images into the frame
        for widget in frame.winfo_children():
            widget.destroy()  # Clear existing images

        for base_dir in base_dirs:
            for entry in os.listdir(base_dir):
                path = os.path.join(base_dir, entry)
                if os.path.isfile(path) and path.endswith('.png'):
                    image = Image.open(path)
                    image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
                    photo = ImageTk.PhotoImage(image)
                    label = tk.Label(frame, image=photo)
                    label.image = photo  # Keep a reference to prevent garbage collection
                    label.bind("<Button-1>", lambda event, map_name=os.path.splitext(entry)[0]: show_map_name(event, map_name))
                    row = len(frame.grid_slaves()) // COLS
                    col = len(frame.grid_slaves()) % COLS
                    label.grid(row=row, column=col, padx=SPACING_X, pady=SPACING_Y)

        update_scroll_region()

    def update_scroll_region(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def update_cols(value):
        # Function to update the number of columns
        nonlocal COLS
        COLS = int(value)
        cols_label.config(text=f"Columns: {COLS}")
        load_images()  # Reload images after updating the column count
    
    def update_image_sizes(value):
        # Function to update the image size
        nonlocal IMAGE_WIDTH, IMAGE_HEIGHT
        size = int(value)
        IMAGE_WIDTH = size
        IMAGE_HEIGHT = size
        image_size_label.config(text=f"Image size: {IMAGE_WIDTH}x{IMAGE_HEIGHT}")
        load_images()  # Reload images after updating the image size

    # Initialize GUI components
    canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    load_button = tk.Button(root, text="Rescan Images", command=update_images)
    load_button.pack(pady=5)

    global progress_label  # Declare progress_label as global to access it inside update_images function
    progress_label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 12))
    progress_label.pack(side=tk.BOTTOM, fill=tk.X)

    # Label to display map names
    global map_name_label  # Declare map_name_label as global to access it inside show_map_name function
    map_name_label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 14))
    map_name_label.pack(side=tk.BOTTOM, fill=tk.X)

    # Slider for adjusting the number of columns
    cols_slider = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, label="", command=update_cols, showvalue=False)
    cols_slider.pack()
    cols_label = tk.Label(root, text=f"Columns: {COLS}", font=("Arial", 12))
    cols_label.pack(pady=5)

    # Slider for adjusting the image size
    image_size_slider = tk.Scale(root, from_=100, to=1000, orient=tk.HORIZONTAL, label="", command=update_image_sizes, showvalue=False)
    image_size_slider.pack()
    image_size_label = tk.Label(root, text=f"Image size: {IMAGE_WIDTH}x{IMAGE_HEIGHT}", font=("Arial", 12))
    image_size_label.pack(pady=5)

    # Load initial set of images
    load_images()

    frame.bind("<Configure>", update_scroll_region)
