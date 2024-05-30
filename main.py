import tkinter as tk
from PIL import Image, ImageTk
import os
import urllib.parse
import requests
import re
import platform

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

# create directories if they don't exist
for base_dir in base_dirs:
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

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

def display_gui(root, SCREEN_WIDTH, SCREEN_HEIGHT, COLS, IMAGE_WIDTH, IMAGE_HEIGHT, SPACING_X, SPACING_Y, base_dirs):
    # rescan images button progress label
    def update_images():
        progress_label.config(text="Rescanning images...")
        root.update()  # Force update of the GUI
        download_images(base_dirs[0], base_dirs[1], update_progress)
        load_images()

    # rescan images button progress label
    def update_progress(status):
        progress_label.config(text=status)
        root.update()

    # show map name when clicking image on label
    def show_map_name(event, map_name):
        cleaned_name = map_name.replace('_', ' ').replace(' map auto', '')
        cleaned_name = urllib.parse.unquote(cleaned_name)
        map_name_label.config(text=f"Map: {cleaned_name}")

    # load all images again, called usually after every gui change e.g. changing columns, load new state
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

    # bind scroll bar GUI element to canvas
    def update_scroll_region(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    # columns count slider
    def update_cols(value):
        nonlocal COLS
        COLS = int(value)
        cols_label.config(text=f"Columns: {COLS}")
        load_images()

    # image size slider
    def update_image_sizes(value):
        nonlocal IMAGE_WIDTH, IMAGE_HEIGHT
        size = int(value)
        IMAGE_WIDTH = size
        IMAGE_HEIGHT = size
        image_size_label.config(text=f"Image size: {IMAGE_WIDTH}x{IMAGE_HEIGHT}")
        load_images()

    # like image
    def like_image():
        print("Liked image: ")
    
    # open Heroes 3 launcher, start game and navigate to chosen map settings
    def play_map():
        print("Starting map: ")

    # reset all settings back to normal
    def reset_settings():
        COLS = 1
        IMAGE_WIDTH = 300
        IMAGE_HEIGHT = 300

    # Keyboard input handling
    def on_key_press(event):
        if event.keysym == "Up":
            canvas.yview_scroll(-1, "units")
        if event.keysym == "Down":
            canvas.yview_scroll(1, "units")
        if event.keysym == "Left":
            canvas.xview_scroll(-1, "units")
        if event.keysym == "Right":
            canvas.xview_scroll(1, "units")

    canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    canvas.grid(row=0, column=0, columnspan=2, sticky="nsew")

    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=2, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    # if MacOS use touchpad scrolling else default
    def on_mouse_wheel(event):
        if platform.system() == "Darwin":  # Check if the platform is macOS
            canvas.yview_scroll(int(-1 * event.delta), "units")  # Adjust the scrolling for macOS touchpads
        else:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")  # For other platforms, use the original scrolling behavior
    canvas.bind_all("<MouseWheel>", lambda event: on_mouse_wheel(event)) # bind event MouseWheel to function on_mouse_wheel

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    load_images()

    frame.bind("<Configure>", update_scroll_region)

    # Bind all key presses to the on_key_press function
    canvas.bind_all("<KeyPress>", on_key_press)

    # Create control frame GUI elements are the rows after it
    control_frame = tk.Frame(root)
    control_frame.grid(row=1, column=0, columnspan=7, sticky="ew")

    # Like map button
    like_button = tk.Button(control_frame, text="like", command=like_image)
    like_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # Play map button
    play_button = tk.Button(control_frame, text="Play Map", command=play_map)
    play_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # Rescan Images button
    load_button = tk.Button(control_frame, text="Rescan Images", command=update_images)
    load_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # filter row 3 - sort
    liked_checkbox = tk.Checkbutton(control_frame, text="Liked Maps", command=load_images)
    liked_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    name_descending_checkbox = tk.Checkbutton(control_frame, text="Descending map name", command=load_images)
    name_descending_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    name_ascending_checkbox = tk.Checkbutton(control_frame, text="Ascending map name", command=load_images)
    name_ascending_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox


    # filter row 3 - expansion
    restoration_checkbox = tk.Checkbutton(control_frame, text="Restoration of Erathia", command=load_images)
    restoration_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    armageddons_checkbox = tk.Checkbutton(control_frame, text="Armageddons Blade", command=load_images)
    armageddons_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    shadow_checkbox = tk.Checkbutton(control_frame, text="Shadow of Death", command=load_images)
    shadow_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    hota_checkbox = tk.Checkbutton(control_frame, text="Horn of the Abyss", command=load_images)
    hota_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    # filter row 4 - map sizes

    small_maps_checkbox = tk.Checkbutton(control_frame, text="S", command=load_images)
    small_maps_checkbox.grid(row=3, column=1, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    medium_maps_checkbox = tk.Checkbutton(control_frame, text="M", command=load_images)
    medium_maps_checkbox.grid(row=3, column=2, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    large_maps_checkbox = tk.Checkbutton(control_frame, text="L", command=load_images)
    large_maps_checkbox.grid(row=3, column=3, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    extra_large_maps_checkbox = tk.Checkbutton(control_frame, text="XL", command=load_images)
    extra_large_maps_checkbox.grid(row=3, column=4, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    gigantic_maps_checkbox = tk.Checkbutton(control_frame, text="G", command=load_images)
    gigantic_maps_checkbox.grid(row=3, column=5, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    underground_maps_checkbox = tk.Checkbutton(control_frame, text="Underground", command=load_images)
    underground_maps_checkbox.grid(row=3, column=6, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    # filters row 4 - difficulty

    easy_checkbox = tk.Checkbutton(control_frame, text="Easy", command=load_images)
    easy_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    medium_maps_checkbox = tk.Checkbutton(control_frame, text="Medium", command=load_images)
    medium_maps_checkbox.grid(row=3, column=1, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    hard_maps_checkbox = tk.Checkbutton(control_frame, text="Hard", command=load_images)
    hard_maps_checkbox.grid(row=3, column=2, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    expert_maps_checkbox = tk.Checkbutton(control_frame, text="Expert", command=load_images)
    expert_maps_checkbox.grid(row=3, column=1, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    impossible_maps_checkbox = tk.Checkbutton(control_frame, text="Impossible", command=load_images)
    impossible_maps_checkbox.grid(row=3, column=2, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox


    # filters row 5 - win conditions

    acquire_artifact_checkbox = tk.Checkbutton(control_frame, text="Acquire Artifact", command=load_images)
    acquire_artifact_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    defeat_monster_checkbox = tk.Checkbutton(control_frame, text="Defeat Monster", command=load_images)
    defeat_monster_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    survive_checkbox = tk.Checkbutton(control_frame, text="Survive time", command=load_images)
    survive_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    standard_checkbox = tk.Checkbutton(control_frame, text="Standard", command=load_images)
    standard_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    build_grail_checkbox = tk.Checkbutton(control_frame, text="Build Grail", command=load_images)
    build_grail_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    eliminate_monsters_checkbox = tk.Checkbutton(control_frame, text="Eliminiate all Monsters", command=load_images)
    eliminate_monsters_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    transport_artifact_checkbox = tk.Checkbutton(control_frame, text="Transport Artifact", command=load_images)
    transport_artifact_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    no_conditions_checkbox = tk.Checkbutton(control_frame, text="Liked Maps", command=load_images)
    no_conditions_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    no_conditions_checkbox = tk.Checkbutton(control_frame, text="Liked Maps", command=load_images)
    no_conditions_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    no_conditions_checkbox = tk.Checkbutton(control_frame, text="Liked Maps", command=load_images)
    no_conditions_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    no_conditions_checkbox = tk.Checkbutton(control_frame, text="Liked Maps", command=load_images)
    no_conditions_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    no_conditions_checkbox = tk.Checkbutton(control_frame, text="Liked Maps", command=load_images)
    no_conditions_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    no_conditions_checkbox = tk.Checkbutton(control_frame, text="Liked Maps", command=load_images)
    no_conditions_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    no_conditions_checkbox = tk.Checkbutton(control_frame, text="Liked Maps", command=load_images)
    no_conditions_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox


    # filters row 6 - lose conditions

    no_conditions_checkbox = tk.Checkbutton(control_frame, text="None", command=load_images)
    no_conditions_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    lose_hero_checkbox = tk.Checkbutton(control_frame, text="Lose a specific Hero", command=load_images)
    lose_hero_checkbox.grid(row=3, column=1, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    lose_town_checkbox = tk.Checkbutton(control_frame, text="Lose a specific Town", command=load_images)
    lose_town_checkbox.grid(row=3, column=2, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    time_expire_checkbox = tk.Checkbutton(control_frame, text="Time Expires", command=load_images)
    time_expire_checkbox.grid(row=3, column=3, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox


    # filters row 7

    # filters row 8

    # Slider for adjusting the number of columns
    cols_slider = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL, label="", command=update_cols, showvalue=False)
    cols_slider.grid(row=4, column=0, padx=5, pady=5, sticky="ew", columnspan=7)
    cols_label = tk.Label(control_frame, text=f"Columns: {COLS}", font=("Arial", 12))
    cols_label.grid(row=5, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # Slider for adjusting the image size
    image_size_slider = tk.Scale(control_frame, from_=100, to=1000, orient=tk.HORIZONTAL, label="", command=update_image_sizes, showvalue=False)
    image_size_slider.grid(row=6, column=0, padx=5, pady=5, sticky="ew", columnspan=7)
    image_size_label = tk.Label(control_frame, text=f"Image size: {IMAGE_WIDTH}x{IMAGE_HEIGHT}", font=("Arial", 12))
    image_size_label.grid(row=7, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # Reset settings button
    reset_button = tk.Button(control_frame, text="Reset settings", command=reset_settings)
    reset_button.grid(row=8, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # Progress label
    global progress_label
    progress_label = tk.Label(control_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 12))
    progress_label.grid(row=9, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # Map name label
    global map_name_label
    map_name_label = tk.Label(control_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 14))
    map_name_label.grid(row=10, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # Configure column resizing behavior for the control frame
    # so column span in gui elements represents the column to fill out to
    # the below weighting means that each column is the same width
    control_frame.grid_columnconfigure(0, weight=1)
    control_frame.grid_columnconfigure(1, weight=1)
    control_frame.grid_columnconfigure(2, weight=1)
    control_frame.grid_columnconfigure(3, weight=1)
    control_frame.grid_columnconfigure(4, weight=1)
    control_frame.grid_columnconfigure(5, weight=1)
    control_frame.grid_columnconfigure(6, weight=1)

    # Configure column and row resizing behavior for the root window
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)

display_gui(root, SCREEN_WIDTH, SCREEN_HEIGHT, COLS, IMAGE_WIDTH, IMAGE_HEIGHT, SPACING_X, SPACING_Y, base_dirs)

root.mainloop()
