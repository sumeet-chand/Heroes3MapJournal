import tkinter as tk
from PIL import Image, ImageTk
from typing import List, Dict
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
base_dirs = ["overworld_map_images", "underground_map_images"]
root = tk.Tk()
root.title("Heroes 3 Map Liker")
image_paths = [
    "assets/star.png",
    "icons/dif_easy.gif",
    "icons/dif_expert.gif",
    "icons/dif_hard.gif",
    "icons/dif_impossible.gif",
    "icons/dif_normal.gif",
    "icons/ls_hero.gif",
    "icons/ls_standard.gif",
    "icons/ls_timeexpires.gif",
    "icons/ls_town.gif",
    "icons/m_h3ccmped.png",
    "icons/m_h3maped.png",
    "icons/sz0_s.gif",
    "icons/sz1_m.gif",
    "icons/sz2_l.gif",
    "icons/sz3_xl.gif",
    "icons/sz4_h.gif",
    "icons/sz5_xh.gif",
    "icons/sz6_g.gif",
    "icons/v_ab.gif",
    "icons/v_hota.gif",
    "icons/v_roe.gif",
    "icons/v_sod.gif",
    "icons/v_wog.gif",
    "icons/vc_allmonsters.gif",
    "icons/vc_artifact.gif",
    "icons/vc_buildcity.gif",
    "icons/vc_buildgrail.gif",
    "icons/vc_capturecity.gif",
    "icons/vc_creatures.gif",
    "icons/vc_flagdwellings.gif",
    "icons/vc_flagmines.gif",
    "icons/vc_hero.gif",
    "icons/vc_monster.gif",
    "icons/vc_resources.gif",
    "icons/vc_standard.gif",
    "icons/vc_survivetime.gif",
    "icons/vc_transport.gif",
    "icons/z_backpack.gif",
]

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
    icon_path: str = Image.open("assets/beholder.png")  # Open the image
    icon_path = icon_path.resize((32, 32))  # Resize the image if required
    icon: ImageTk.PhotoImage = ImageTk.PhotoImage(icon_path)  # Convert the image to a PhotoImage
    root.iconphoto(False, icon) # set as software window icon

def load_asset_images(image_paths: List[str]) -> Dict[str, ImageTk.PhotoImage]:
    """
    Load multiple asset images, resize them to (32, 32), and return a dictionary of PhotoImage objects.

    Args:
        image_paths (list): A list of file paths to the images.

    Returns:
        dict: A dictionary containing PhotoImage objects corresponding to the images.
    """
    photo_images = {}
    for path in image_paths:
        filename = os.path.splitext(os.path.basename(path))[0]  # Extract filename without extension
        image = Image.open(path)  # Load the image
        image = image.resize((32, 32))  # Resize the image
        photo_images[filename] = ImageTk.PhotoImage(image)  # Load image and store it in the dictionary
    return photo_images

photo_images = load_asset_images(image_paths)
star_photo = photo_images["star"]
easy_photo = photo_images["dif_easy"]
expert_photo = photo_images["dif_expert"]
hard_photo = photo_images["dif_hard"]
impossible_photo = photo_images["dif_impossible"]
normal_photo = photo_images["dif_normal"]
ls_hero_photo = photo_images["ls_hero"]
ls_standard_photo = photo_images["ls_standard"]
ls_timeexpires_photo = photo_images["ls_timeexpires"]
ls_town_photo = photo_images["ls_town"]
m_h3ccmped_photo = photo_images["m_h3ccmped"]
m_h3maped_photo = photo_images["m_h3maped"]
sz0_s_photo = photo_images["sz0_s"]
sz1_m_photo = photo_images["sz1_m"]
sz2_l_photo = photo_images["sz2_l"]
sz3_xl_photo = photo_images["sz3_xl"]
sz4_h_photo = photo_images["sz4_h"]
sz5_xh_photo = photo_images["sz5_xh"]
sz6_g_photo = photo_images["sz6_g"]
v_ab_photo = photo_images["v_ab"]
v_hota_photo = photo_images["v_hota"]
v_roe_photo = photo_images["v_roe"]
v_sod_photo = photo_images["v_sod"]
v_wog_photo = photo_images["v_wog"]
vc_allmonsters_photo = photo_images["vc_allmonsters"]
vc_artifact_photo = photo_images["vc_artifact"]
vc_buildcity_photo = photo_images["vc_buildcity"]
vc_buildgrail_photo = photo_images["vc_buildgrail"]
vc_capturecity_photo = photo_images["vc_capturecity"]
vc_creatures_photo = photo_images["vc_creatures"]
vc_flagdwellings_photo = photo_images["vc_flagdwellings"]
vc_flagmines_photo = photo_images["vc_flagmines"]
vc_hero_photo = photo_images["vc_hero"]
vc_monster_photo = photo_images["vc_monster"]
vc_resources_photo = photo_images["vc_resources"]
vc_standard_photo = photo_images["vc_standard"]
vc_survivetime_photo = photo_images["vc_survivetime"]
vc_transport_photo = photo_images["vc_transport"]
z_backpack_photo = photo_images["z_backpack"]

def create_directories_if_missing():
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

    # row 0 - Like map button
    like_button = tk.Button(control_frame, text="like", command=like_image)
    like_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # row 1 - Play map button
    play_button = tk.Button(control_frame, text="Play Map", command=play_map)
    play_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # row 2 - Rescan Images button
    load_button = tk.Button(control_frame, text="Rescan Images", command=update_images)
    load_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # row 3 - sort
    sort_label = tk.Label(control_frame, text="Sort", font=("Arial", 16))
    sort_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    liked_frame = tk.Frame(control_frame) # Create frame hold checkbox, text and star image, in same column
    liked_frame.grid(row=3, column=1, padx=5, pady=5, sticky="w")
    liked_checkbox = tk.Checkbutton(liked_frame, text="Liked", command=load_images) # Create the liked checkbox
    liked_checkbox.pack(side=tk.LEFT)
    star_label = tk.Label(liked_frame, image=star_photo) # Create a label for the star image
    star_label.image = star_photo  # Ensure the image is retained
    star_label.pack(side=tk.LEFT)

    name_descending_checkbox = tk.Checkbutton(control_frame, text="Descending", command=load_images)
    name_descending_checkbox.grid(row=3, column=2, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    name_ascending_checkbox = tk.Checkbutton(control_frame, text="Ascending", command=load_images)
    name_ascending_checkbox.grid(row=3, column=3, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    # filter row 4 - expansion
    sort_label = tk.Label(control_frame, text="Expansion", font=("Arial", 16))
    sort_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    restoration_frame = tk.Frame(control_frame)
    restoration_frame.grid(row=4, column=1, padx=5, pady=5, sticky="w")
    restoration_checkbox = tk.Checkbutton(restoration_frame, text="Restoration of Erathia", command=load_images)
    restoration_checkbox.pack(side=tk.LEFT)
    roe_label = tk.Label(restoration_frame, image=v_roe_photo)
    roe_label.image = v_roe_photo
    roe_label.pack(side=tk.LEFT)

    armageddons_checkbox = tk.Checkbutton(control_frame, text="Armageddons Blade", command=load_images)
    armageddons_checkbox.grid(row=4, column=2, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    shadow_checkbox = tk.Checkbutton(control_frame, text="Shadow of Death", command=load_images)
    shadow_checkbox.grid(row=4, column=3, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    hota_checkbox = tk.Checkbutton(control_frame, text="Horn of the Abyss", command=load_images)
    hota_checkbox.grid(row=4, column=4, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    # row 5 - map sizes
    sort_label = tk.Label(control_frame, text="Map size", font=("Arial", 16))
    sort_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    small_maps_checkbox = tk.Checkbutton(control_frame, text="S", command=load_images)
    small_maps_checkbox.grid(row=5, column=1, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    medium_maps_checkbox = tk.Checkbutton(control_frame, text="M", command=load_images)
    medium_maps_checkbox.grid(row=5, column=2, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    large_maps_checkbox = tk.Checkbutton(control_frame, text="L", command=load_images)
    large_maps_checkbox.grid(row=5, column=3, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    extra_large_maps_checkbox = tk.Checkbutton(control_frame, text="XL", command=load_images)
    extra_large_maps_checkbox.grid(row=5, column=4, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    gigantic_maps_checkbox = tk.Checkbutton(control_frame, text="G", command=load_images)
    gigantic_maps_checkbox.grid(row=5, column=5, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    underground_maps_checkbox = tk.Checkbutton(control_frame, text="Underground", command=load_images)
    underground_maps_checkbox.grid(row=5, column=6, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    # row 6 - difficulty
    easy_checkbox = tk.Checkbutton(control_frame, text="Easy", command=load_images)
    easy_checkbox.grid(row=6, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    medium_maps_checkbox = tk.Checkbutton(control_frame, text="Medium", command=load_images)
    medium_maps_checkbox.grid(row=6, column=1, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    hard_maps_checkbox = tk.Checkbutton(control_frame, text="Hard", command=load_images)
    hard_maps_checkbox.grid(row=6, column=2, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    expert_maps_checkbox = tk.Checkbutton(control_frame, text="Expert", command=load_images)
    expert_maps_checkbox.grid(row=6, column=3, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    impossible_maps_checkbox = tk.Checkbutton(control_frame, text="Impossible", command=load_images)
    impossible_maps_checkbox.grid(row=6, column=4, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    # row 7 - win conditions
    acquire_artifact_checkbox = tk.Checkbutton(control_frame, text="Acquire specific Artifact", command=load_images)
    acquire_artifact_checkbox.grid(row=7, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    defeat_monster_checkbox = tk.Checkbutton(control_frame, text="Defeat specific Monster", command=load_images)
    defeat_monster_checkbox.grid(row=7, column=1, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    survive_checkbox = tk.Checkbutton(control_frame, text="Survive certain time", command=load_images)
    survive_checkbox.grid(row=7, column=2, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    standard_checkbox = tk.Checkbutton(control_frame, text="Standard", command=load_images)
    standard_checkbox.grid(row=7, column=3, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    build_grail_checkbox = tk.Checkbutton(control_frame, text="Build Grail structure", command=load_images)
    build_grail_checkbox.grid(row=7, column=4, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    eliminate_monsters_checkbox = tk.Checkbutton(control_frame, text="Eliminiate all Monsters", command=load_images)
    eliminate_monsters_checkbox.grid(row=7, column=5, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    transport_artifact_checkbox = tk.Checkbutton(control_frame, text="Transport specific Artifact", command=load_images)
    transport_artifact_checkbox.grid(row=7, column=6, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    # row 8 - win conditions continued
    accumuulate_creatures_checkbox = tk.Checkbutton(control_frame, text="Accumulate Creatures", command=load_images)
    accumuulate_creatures_checkbox.grid(row=8, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    capture_town_checkbox = tk.Checkbutton(control_frame, text="Capture specific Town", command=load_images)
    capture_town_checkbox.grid(row=8, column=1, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    flag_dwellings_checkbox = tk.Checkbutton(control_frame, text="Flag all creature Dwellings", command=load_images)
    flag_dwellings_checkbox.grid(row=8, column=2, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    upgrade_town_checkbox = tk.Checkbutton(control_frame, text="Upgrade specific Town", command=load_images)
    upgrade_town_checkbox.grid(row=8, column=3, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    accumuulate_resources_checkbox = tk.Checkbutton(control_frame, text="Accumulate resources", command=load_images)
    accumuulate_resources_checkbox.grid(row=8, column=4, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    defeat_hero_checkbox = tk.Checkbutton(control_frame, text="Defeat specific Hero", command=load_images)
    defeat_hero_checkbox.grid(row=8, column=5, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    flag_mines_checkbox = tk.Checkbutton(control_frame, text="Flag all mines", command=load_images)
    flag_mines_checkbox.grid(row=8, column=6, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    # row 9 - lose conditions
    no_conditions_checkbox = tk.Checkbutton(control_frame, text="None", command=load_images)
    no_conditions_checkbox.grid(row=9, column=0, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    lose_hero_checkbox = tk.Checkbutton(control_frame, text="Lose specific Hero", command=load_images)
    lose_hero_checkbox.grid(row=9, column=1, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    lose_town_checkbox = tk.Checkbutton(control_frame, text="Lose specific Town", command=load_images)
    lose_town_checkbox.grid(row=9, column=2, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    time_expire_checkbox = tk.Checkbutton(control_frame, text="Time Expires", command=load_images)
    time_expire_checkbox.grid(row=9, column=3, padx=5, pady=5, sticky="w") # sticky "w" = make the text stick to checkbox

    # row 10 - 11 - Slider for adjusting the number of columns
    cols_slider = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL, label="", command=update_cols, showvalue=False)
    cols_slider.grid(row=10, column=0, padx=5, pady=5, sticky="ew", columnspan=7)
    cols_label = tk.Label(control_frame, text=f"Columns: {COLS}", font=("Arial", 12))
    cols_label.grid(row=11, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # row 12 - 13 - Slider for adjusting the image size
    image_size_slider = tk.Scale(control_frame, from_=100, to=1000, orient=tk.HORIZONTAL, label="", command=update_image_sizes, showvalue=False)
    image_size_slider.grid(row=12, column=0, padx=5, pady=5, sticky="ew", columnspan=7)
    image_size_label = tk.Label(control_frame, text=f"Image size: {IMAGE_WIDTH}x{IMAGE_HEIGHT}", font=("Arial", 12))
    image_size_label.grid(row=13, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # row 14 - Reset settings button
    reset_button = tk.Button(control_frame, text="Reset settings", command=reset_settings)
    reset_button.grid(row=14, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # row 15 - Progress label
    global progress_label
    progress_label = tk.Label(control_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 12))
    progress_label.grid(row=15, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # row 16 - Map name label
    global map_name_label
    map_name_label = tk.Label(control_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 14))
    map_name_label.grid(row=16, column=0, padx=5, pady=5, sticky="ew", columnspan=7)

    # Configure column resizing behavior for the control frame
    # if there are 7 checkboxes across 7 columns in a single row
    # then single widgets (e.g. buttons) in a row without 6 other columns, need to fill them out with columnspan=7
    # the below weighting means each column has the same width
    control_frame.grid_columnconfigure(0, weight=1)
    control_frame.grid_columnconfigure(1, weight=1)
    control_frame.grid_columnconfigure(2, weight=1)
    control_frame.grid_columnconfigure(3, weight=1)
    control_frame.grid_columnconfigure(4, weight=1)
    control_frame.grid_columnconfigure(5, weight=1)
    control_frame.grid_columnconfigure(6, weight=1)
    control_frame.grid_columnconfigure(7, weight=1)

    # Configure column and row resizing behavior for the root window
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)

set_window_icon()
create_directories_if_missing()
display_gui(root, SCREEN_WIDTH, SCREEN_HEIGHT, COLS, IMAGE_WIDTH, IMAGE_HEIGHT, SPACING_X, SPACING_Y, base_dirs)

root.mainloop()
