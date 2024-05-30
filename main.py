import tkinter as tk
from PIL import Image, ImageTk
import os
import urllib.parse
import requests
import re

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 720
COLS = 1
IMAGE_WIDTH = 300
IMAGE_HEIGHT = 300
SPACING_X = 20
SPACING_Y = 20
base_dirs = ["Heroes3overworldImages", "Heroes3undergroundImages"]
root = tk.Tk()
root.title("Heroes 3 Map Liker")

# Load the icon image
icon_path = "assets/beholder.png"
icon = tk.PhotoImage(file=icon_path)
root.iconphoto(False, icon)

# load icon for favouriting
star_texture_path = "assets/star.png"

# create directories if they dont exist
for base_dir in base_dirs:
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

# triggered on software startup if no image dir's or on rescan button to scrap all images
def download_images(base_dir, underground_dir, progress_callback=None):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    if not os.path.exists(underground_dir):
        os.makedirs(underground_dir)

    url = "https://heroes.thelazy.net/index.php/List_of_maps"
    response = requests.get(url)

    map_info = {}
    map_name_tags = response.text.split('<td style="text-align:center;">')[1:]

    total_maps = len(map_name_tags) // 2
    current_map = 0

    for i in range(0, len(map_name_tags), 2):
        map_name_tag = map_name_tags[i + 1]
        map_name = re.search(r'title="(.*?)"', map_name_tag).group(1)
        map_link = "https://heroes.thelazy.net" + re.search(r'href="(.*?)"', map_name_tag).group(1)
        map_info[map_name] = map_link

    for map_name, map_link in map_info.items():
        current_map += 1
        progress = f"Downloading new images progress: {current_map}/{total_maps}"
        print(progress)
        
        if progress_callback:
            progress_callback(progress)
        
        print(f"Map page URL: {map_link}")  # Print the map page URL
        image_url = map_link + "#/media/File:" + map_name.replace(" ", "_") + "_map_auto.png"
        print(f"Processing image URL: {image_url}")

        image_response = requests.get(image_url)
        img_tags = re.findall(r'<img.+?src="([^"]+)"', image_response.text)
        if img_tags:
            for img_tag in img_tags:
                if "underground" not in img_tag:
                    match = re.search(r'/images/(.*?)map_auto.png', img_tag)
                    if match:
                        download_link = "https://heroes.thelazy.net/images/" + match.group(1) + "map_auto.png"
                        download_link = download_link.replace("/thumb", "")
                        filename = os.path.join(base_dir, os.path.basename(download_link))
                        download_image(download_link, filename)
                else:
                    match = re.search(r'/images/(.*?)map_auto.png', img_tag)
                    if match:
                        download_link = "https://heroes.thelazy.net/images/" + match.group(1) + "map_auto.png"
                        download_link = download_link.replace("/thumb", "")
                        filename = os.path.join(underground_dir, os.path.basename(download_link))
                        download_image(download_link, filename)
        else:
            print("No download link found.")

    print("Completed processing for all maps.")
    if progress_callback:
        progress_callback("Rescanning complete!")

# works with download_images to downlaod the scrapped image
def download_image(image_url, save_path):
    if os.path.exists(save_path):
        print(f"Image already exists: {save_path}")
    else:
        try:
            response = requests.get(image_url)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded: {save_path}")
        except Exception as e:
            print(f"Failed to download image from {image_url}: {str(e)}")

# software GUI
def display_gui(root, SCREEN_WIDTH, SCREEN_HEIGHT, COLS, IMAGE_WIDTH, IMAGE_HEIGHT, SPACING_X, SPACING_Y, base_dirs):
    def update_images():
        progress_label.config(text="Rescanning images...")
        root.update()  # Force update of the GUI
        download_images(base_dirs[0], base_dirs[1], update_progress)
        load_images()

    def update_progress(status):
        progress_label.config(text=status)
        root.update()

    def show_map_name(event, map_name):
        cleaned_name = map_name.replace('_', ' ').replace(' map auto', '')
        cleaned_name = urllib.parse.unquote(cleaned_name)
        map_name_label.config(text=f"Map: {cleaned_name}")

    def load_images():
        for widget in frame.winfo_children():
            widget.destroy()

        for base_dir in base_dirs:
            for entry in os.listdir(base_dir):
                path = os.path.join(base_dir, entry)
                if os.path.isfile(path) and path.endswith('.png'):
                    image = Image.open(path)
                    image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
                    photo = ImageTk.PhotoImage(image)
                    label = tk.Label(frame, image=photo)
                    label.image = photo
                    label.bind("<Button-1>", lambda event, map_name=os.path.splitext(entry)[0]: show_map_name(event, map_name))
                    row = len(frame.grid_slaves()) // COLS
                    col = len(frame.grid_slaves()) % COLS
                    label.grid(row=row, column=col, padx=SPACING_X, pady=SPACING_Y)

        update_scroll_region()

    def update_scroll_region(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def update_cols(value):
        nonlocal COLS
        COLS = int(value)
        cols_label.config(text=f"Columns: {COLS}")
        load_images()

    def update_image_sizes(value):
        nonlocal IMAGE_WIDTH, IMAGE_HEIGHT
        size = int(value)
        IMAGE_WIDTH = size
        IMAGE_HEIGHT = size
        image_size_label.config(text=f"Image size: {IMAGE_WIDTH}x{IMAGE_HEIGHT}")
        load_images()

    canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    canvas.grid(row=0, column=0, columnspan=2, sticky="nsew")

    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=2, sticky="ns")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    load_images()

    frame.bind("<Configure>", update_scroll_region)

    # Create control frame
    control_frame = tk.Frame(root)
    control_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

    # Rescan Images button
    load_button = tk.Button(control_frame, text="Rescan Images", command=update_images)
    load_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    # Slider for adjusting the number of columns
    cols_slider = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL, label="", command=update_cols, showvalue=False)
    cols_slider.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    cols_label = tk.Label(control_frame, text=f"Columns: {COLS}", font=("Arial", 12))
    cols_label.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    # Slider for adjusting the image size
    image_size_slider = tk.Scale(control_frame, from_=100, to=1000, orient=tk.HORIZONTAL, label="", command=update_image_sizes, showvalue=False)
    image_size_slider.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
    image_size_label = tk.Label(control_frame, text=f"Image size: {IMAGE_WIDTH}x{IMAGE_HEIGHT}", font=("Arial", 12))
    image_size_label.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

    # Progress label
    global progress_label
    progress_label = tk.Label(control_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 12))
    progress_label.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

    # Map name label
    global map_name_label
    map_name_label = tk.Label(control_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 14))
    map_name_label.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

    # Configure column and row resizing behavior for the control frame
    control_frame.grid_columnconfigure(0, weight=1)

    # Configure column and row resizing behavior for the root window
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)

display_gui(root, SCREEN_WIDTH, SCREEN_HEIGHT, COLS, IMAGE_WIDTH, IMAGE_HEIGHT, SPACING_X, SPACING_Y, base_dirs)

root.mainloop()
