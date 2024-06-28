# /display_gui.py

import tkinter as tk
from PIL import Image, ImageTk
from typing import Dict
import os
import urllib.parse
import platform
from download_images import download_images

def display_gui(root, SCREEN_WIDTH: int, SCREEN_HEIGHT: int, COLS: int, IMAGE_WIDTH: int, IMAGE_HEIGHT: int, SPACING_X: int, SPACING_Y: int, map_image_dir: str, photo_images: Dict[str, ImageTk.PhotoImage]):
    """
    start toolkit interface (Tkinter) GUI Window

    Args
        root (Tk): the GUI Window
        SCREEN_WIDTH (int): window width
        SCREEN_HEIGHT(int):  window height
        COLS(int): columns for images
        IMAGE_WIDTH(int): images width
        IMAGE_HEIGHT(int): images height
        SPACING_X(int): x padding between images
        SPACING_Y(int): y padding between images
        base_dirs: list[str]: folders to load/download images to/from

    Returns:
        None
    """

    progress_label = None
    map_name_label = None

    def toggle_control_panel():
        """
        Button to hide or show control panel triggers this function

        Returns:
            None
        
        """
        if control_frame.winfo_viewable():
            control_frame.grid_remove()
            toggle_button.config(text="Show settings", image=photo_images["book_open"], compound="right")
        else:
            control_frame.grid()
            toggle_button.config(text="Hide settings", image=photo_images["book_closed"], compound="right")
    
    def update_images():
        """
        rescan images button progress label

        Returns:
            None
        """
        progress_label.config(text="Rescanning images...")
        root.update()  # Force update of the GUI
        download_images(map_image_dir, update_progress)
        load_images()

    def update_progress(status):
        """
        rescan images button progress label

        Returns:
            None
        """
        progress_label.config(text=status)
        root.update()

    def show_map_name(event, map_name):
        """
        show map name when clicking image on label

        Returns:
            None
        """
        cleaned_name = map_name.replace('_', ' ').replace(' map auto', '')
        cleaned_name = urllib.parse.unquote(cleaned_name)
        map_name_label.config(text=f"Map: {cleaned_name}")

    def load_images():
        """
        load all images again, called usually after every gui change e.g. changing columns, load new state

        Returns:
            None
        """
        for widget in frame.winfo_children():
            widget.destroy()

        # Load images from map_images_dir
        for entry in os.listdir(map_image_dir):
            path = os.path.join(map_image_dir, entry)
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
        """
        bind scroll bar GUI element to canvas

        Returns:
            None
        """
        canvas.configure(scrollregion=canvas.bbox("all"))

    def update_cols(value):
        """
        columns count slider

        Returns:
            None
        """
        nonlocal COLS
        COLS = int(value)
        cols_label.config(text=f"Columns: {COLS}")
        load_images()

    def update_image_sizes(value):
        """
        image size slider

        Returns:
            None
        """
        nonlocal IMAGE_WIDTH, IMAGE_HEIGHT
        size = int(value)
        IMAGE_WIDTH = size
        IMAGE_HEIGHT = size
        image_size_label.config(text=f"Image size: {IMAGE_WIDTH}x{IMAGE_HEIGHT}")
        load_images()

    def like_image():
        """
        like image button to save liked images to be able to filter from.

        Returns:
            None
        """
        print("Liked image: ")
    
    def play_map():
        """
        Button for open Heroes 3 launcher, start game and navigate to chosen map settings

        Returns:
            None
        """
        print("Starting map: ")

    def reset_settings():
        """
        Button to reset all settings/filters back to normal

        Returns:
            None
        """
        COLS = 1
        IMAGE_WIDTH = 300
        IMAGE_HEIGHT = 300

    def on_key_press(event):
        """
        Keyboard input handling. On keyboard key/button click/press perform relevant action below

        Returns:
            None
        """
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

    background_photo = ImageTk.PhotoImage(Image.open("assets/page.png").resize((SCREEN_WIDTH, SCREEN_HEIGHT)))
    # canvas.create_image(0, 0, image=background_photo, anchor=tk.NW) - NOT SETTING BACKGROUND IMAGE NEEDS FIX

    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=2, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    def on_mouse_wheel(event):
        """
        If platform is a MacOS use touchpad scrolling which is two fingers button 4 and 5 for touch
        scrolling. Otherwise use the default mouse wheel for scrolling in any other OS

        Returns:
            None
        """
        if platform.system() == "Darwin":  # Check if the platform is macOS
            canvas.yview_scroll(int(-1 * event.delta), "units")  # Adjust the scrolling for macOS touchpads
        else:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")  # For other platforms, use the original scrolling behavior
    canvas.bind_all("<MouseWheel>", lambda event: on_mouse_wheel(event)) # bind event MouseWheel to function on_mouse_wheel

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW) # by embedding a frame in the canvas window it becomes scrollable

    load_images()

    frame.bind("<Configure>", update_scroll_region)

    # Bind all key presses to the on_key_press function
    canvas.bind_all("<KeyPress>", on_key_press)

    # Create control frame GUI elements are the rows after it
    control_frame = tk.Frame(root)
    control_frame.grid(row=1, column=0, columnspan=5, sticky="ew")

    # root frame - row 0 - control panel visibility button
    toggle_button = tk.Button(root, text="Hide Settings", image=photo_images["book_closed"], compound="right", command=toggle_control_panel)
    toggle_button.grid(row=0, column=0, sticky="ne", padx=2, pady=2)

    # root frame - row 1  - Map name label
    map_name_label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 14))
    map_name_label.grid(row=1, column=0, sticky="ne", padx=2, pady=2)

    # row 1 - Like map button
    like_button = tk.Button(control_frame, text="like", command=like_image)
    like_button.grid(row=1, column=0, padx=2, pady=2, sticky="ew", columnspan=5)

    # row 2 - Play map button
    play_button = tk.Button(control_frame, text="Play map", command=play_map)
    play_button.grid(row=2, column=0, padx=2, pady=2, sticky="ew", columnspan=5)

    # row 3 - Rescan Images button
    load_button = tk.Button(control_frame, text="Rescan Images", command=update_images)
    load_button.grid(row=3, column=0, padx=2, pady=2, sticky="ew", columnspan=5)

    # row 4 - sort
    sort_label = tk.Label(control_frame, text="Filter", font=("Arial", 12))
    sort_label.grid(row=4, column=0, columnspan=3, padx=2, pady=2, sticky="w")

    liked_frame = tk.Frame(control_frame) # Create frame hold checkbox, text and star image, in same column
    liked_frame.grid(row=4, column=1, padx=2, pady=2, sticky="w")
    liked_checkbox = tk.Checkbutton(liked_frame, text="Liked", command=load_images) # Create the liked checkbox
    liked_checkbox.pack(side=tk.LEFT)
    liked_label = tk.Label(liked_frame, image=photo_images["star"]) # Create a label for the star image
    liked_label.pack(side=tk.LEFT)

    name_descending_frame = tk.Frame(control_frame)
    name_descending_frame.grid(row=4, column=2, padx=2, pady=2, sticky="w")
    name_descending_checkbox = tk.Checkbutton(name_descending_frame, text="Name descending", command=load_images)
    name_descending_checkbox.pack(side=tk.LEFT)
    name_descending_label = tk.Label(name_descending_frame, image=photo_images["name_descending"])
    name_descending_label.pack(side=tk.LEFT)

    name_ascending_frame = tk.Frame(control_frame)
    name_ascending_frame.grid(row=4, column=3, padx=2, pady=2, sticky="w")
    name_ascending_checkbox = tk.Checkbutton(name_ascending_frame, text="Name ascending", command=load_images)
    name_ascending_checkbox.pack(side=tk.LEFT)
    name_ascending_label = tk.Label(name_ascending_frame, image=photo_images["name_ascending"])
    name_ascending_label.pack(side=tk.LEFT)

    subterranean_frame = tk.Frame(control_frame)
    subterranean_frame.grid(row=4, column=4, padx=2, pady=2, sticky="w")
    subterranean_checkbox = tk.Checkbutton(subterranean_frame, text="subterranean", command=load_images)
    subterranean_checkbox.pack(side=tk.LEFT)
    subterranean_label = tk.Label(subterranean_frame, image=photo_images["subterranean"])
    subterranean_label.pack(side=tk.LEFT)

    # filter row 5 - expansion
    sort_label = tk.Label(control_frame, text="Expansion", font=("Arial", 12))
    sort_label.grid(row=5, column=0, columnspan=3, padx=2, pady=2, sticky="w")

    roe_frame = tk.Frame(control_frame)
    roe_frame.grid(row=5, column=1, padx=2, pady=2, sticky="w")
    roe_checkbox = tk.Checkbutton(roe_frame, text="Restoration of Erathia", command=load_images)
    roe_checkbox.pack(side=tk.LEFT)
    roe_label = tk.Label(roe_frame, image=photo_images["v_roe"])
    roe_label.pack(side=tk.LEFT)

    ab_frame = tk.Frame(control_frame)
    ab_frame.grid(row=5, column=2, padx=2, pady=2, sticky="w")
    ab_checkbox = tk.Checkbutton(ab_frame, text="Armageddons Blade", command=load_images)
    ab_checkbox.pack(side=tk.LEFT)
    ab_label = tk.Label(ab_frame, image=photo_images["v_ab"])
    ab_label.pack(side=tk.LEFT)

    sod_frame = tk.Frame(control_frame)
    sod_frame.grid(row=5, column=3, padx=2, pady=2, sticky="w")
    sod_checkbox = tk.Checkbutton(sod_frame, text="Shadow of Death", command=load_images)
    sod_checkbox.pack(side=tk.LEFT)
    sod_label = tk.Label(sod_frame, image=photo_images["v_sod"])
    sod_label.pack(side=tk.LEFT)

    hota_frame = tk.Frame(control_frame)
    hota_frame.grid(row=5, column=4, padx=2, pady=2, sticky="w")
    hota_checkbox = tk.Checkbutton(hota_frame, text="Horn of the Abyss", command=load_images)
    hota_checkbox.pack(side=tk.LEFT)
    hota_label = tk.Label(hota_frame, image=photo_images["v_hota"])
    hota_label.pack(side=tk.LEFT)

    # row 6 - map sizes
    sort_label = tk.Label(control_frame, text="Map size", font=("Arial", 12))
    sort_label.grid(row=6, column=0, columnspan=3, padx=2, pady=2, sticky="w")

    small_map_frame = tk.Frame(control_frame)
    small_map_frame.grid(row=6, column=1, padx=2, pady=2, sticky="w")
    small_map_checkbox = tk.Checkbutton(small_map_frame, text="S", command=load_images)
    small_map_checkbox.pack(side=tk.LEFT)
    small_map_label = tk.Label(small_map_frame, image=photo_images["sz0_s"])
    small_map_label.pack(side=tk.LEFT)

    medium_map_frame = tk.Frame(control_frame)
    medium_map_frame.grid(row=6, column=2, padx=2, pady=2, sticky="w")
    medium_map_checkbox = tk.Checkbutton(medium_map_frame, text="M", command=load_images)
    medium_map_checkbox.pack(side=tk.LEFT)
    medium_map_label = tk.Label(medium_map_frame, image=photo_images["sz1_m"])
    medium_map_label.pack(side=tk.LEFT)

    large_map_frame = tk.Frame(control_frame)
    large_map_frame.grid(row=6, column=3, padx=2, pady=2, sticky="w")
    large_map_checkbox = tk.Checkbutton(large_map_frame, text="L", command=load_images)
    large_map_checkbox.pack(side=tk.LEFT)
    large_map_label = tk.Label(large_map_frame, image=photo_images["sz2_l"])
    large_map_label.pack(side=tk.LEFT)

    extra_large_map_frame = tk.Frame(control_frame)
    extra_large_map_frame.grid(row=6, column=4, padx=2, pady=2, sticky="w")
    extra_large_map_checkbox = tk.Checkbutton(extra_large_map_frame, text="XL", command=load_images)
    extra_large_map_checkbox.pack(side=tk.LEFT)
    extra_large_map_label = tk.Label(extra_large_map_frame, image=photo_images["sz3_xl"])
    extra_large_map_label.pack(side=tk.LEFT)

    # row 7 - map size continued
    huge_map_frame = tk.Frame(control_frame)
    huge_map_frame.grid(row=7, column=0, padx=2, pady=2, sticky="w")
    huge_map_checkbox = tk.Checkbutton(huge_map_frame, text="H", command=load_images)
    huge_map_checkbox.pack(side=tk.LEFT)
    huge_map_label = tk.Label(huge_map_frame, image=photo_images["sz4_h"])
    huge_map_label.pack(side=tk.LEFT)

    extra_huge_map_frame = tk.Frame(control_frame)
    extra_huge_map_frame.grid(row=7, column=1, padx=2, pady=2, sticky="w")
    extra_huge_map_checkbox = tk.Checkbutton(extra_huge_map_frame, text="XH", command=load_images)
    extra_huge_map_checkbox.pack(side=tk.LEFT)
    extra_huge_map_label = tk.Label(extra_huge_map_frame, image=photo_images["sz5_xh"])
    extra_huge_map_label.pack(side=tk.LEFT)

    giant_map_frame = tk.Frame(control_frame)
    giant_map_frame.grid(row=7, column=2, padx=2, pady=2, sticky="w")
    giant_map_checkbox = tk.Checkbutton(giant_map_frame, text="G", command=load_images)
    giant_map_checkbox.pack(side=tk.LEFT)
    giant_map_label = tk.Label(giant_map_frame, image=photo_images["sz6_g"])
    giant_map_label.pack(side=tk.LEFT)


    # row 8 - difficulty
    sort_label = tk.Label(control_frame, text="Difficulty", font=("Arial", 12))
    sort_label.grid(row=8, column=0, columnspan=3, padx=2, pady=2, sticky="w")

    easy_map_frame = tk.Frame(control_frame)
    easy_map_frame.grid(row=8, column=1, padx=2, pady=2, sticky="w")
    easy_map_checkbox = tk.Checkbutton(easy_map_frame, text="Easy", command=load_images)
    easy_map_checkbox.pack(side=tk.LEFT)
    easy_map_label = tk.Label(easy_map_frame, image=photo_images["dif_easy"])
    easy_map_label.pack(side=tk.LEFT)

    normal_map_frame = tk.Frame(control_frame)
    normal_map_frame.grid(row=8, column=2, padx=2, pady=2, sticky="w")
    normal_map_checkbox = tk.Checkbutton(normal_map_frame, text="Normal", command=load_images)
    normal_map_checkbox.pack(side=tk.LEFT)
    normal_map_label = tk.Label(normal_map_frame, image=photo_images["dif_normal"])
    normal_map_label.pack(side=tk.LEFT)

    hard_map_frame = tk.Frame(control_frame)
    hard_map_frame.grid(row=8, column=3, padx=2, pady=2, sticky="w")
    hard_map_checkbox = tk.Checkbutton(hard_map_frame, text="Hard", command=load_images)
    hard_map_checkbox.pack(side=tk.LEFT)
    hard_map_label = tk.Label(hard_map_frame, image=photo_images["dif_hard"])
    hard_map_label.pack(side=tk.LEFT)

    expert_map_frame = tk.Frame(control_frame)
    expert_map_frame.grid(row=8, column=4, padx=2, pady=2, sticky="w")
    expert_map_checkbox = tk.Checkbutton(expert_map_frame, text="Expert", command=load_images)
    expert_map_checkbox.pack(side=tk.LEFT)
    expert_map_label = tk.Label(expert_map_frame, image=photo_images["dif_expert"])
    expert_map_label.pack(side=tk.LEFT)

    # row 9 - difficulty continued
    impossible_map_frame = tk.Frame(control_frame)
    impossible_map_frame.grid(row=9, column=0, padx=2, pady=2, sticky="w")
    impossible_map_checkbox = tk.Checkbutton(impossible_map_frame, text="Impossible", command=load_images)
    impossible_map_checkbox.pack(side=tk.LEFT)
    impossible_map_label = tk.Label(impossible_map_frame, image=photo_images["dif_impossible"])
    impossible_map_label.pack(side=tk.LEFT)


    # row 10 - win conditions
    sort_label = tk.Label(control_frame, text="Win conditions", font=("Arial", 12))
    sort_label.grid(row=10, column=0, columnspan=3, padx=2, pady=2, sticky="w")

    acquire_artifact_frame = tk.Frame(control_frame)
    acquire_artifact_frame.grid(row=10, column=1, padx=2, pady=2, sticky="w")
    acquire_artifact_checkbox = tk.Checkbutton(acquire_artifact_frame, text="Acquire specific Artifact", command=load_images)
    acquire_artifact_checkbox.pack(side=tk.LEFT)
    acquire_artifact_label = tk.Label(acquire_artifact_frame, image=photo_images["vc_artifact"])
    acquire_artifact_label.pack(side=tk.LEFT)

    defeat_monster_frame = tk.Frame(control_frame)
    defeat_monster_frame.grid(row=10, column=2, padx=2, pady=2, sticky="w")
    defeat_monster_checkbox = tk.Checkbutton(defeat_monster_frame, text="Defeat specific Monster", command=load_images)
    defeat_monster_checkbox.pack(side=tk.LEFT)
    defeat_monster_label = tk.Label(defeat_monster_frame, image=photo_images["vc_monster"])
    defeat_monster_label.pack(side=tk.LEFT)

    survive_frame = tk.Frame(control_frame)
    survive_frame.grid(row=10, column=3, padx=2, pady=2, sticky="w")
    survive_checkbox = tk.Checkbutton(survive_frame, text="Survive certain time", command=load_images)
    survive_checkbox.pack(side=tk.LEFT)
    survive_label = tk.Label(survive_frame, image=photo_images["vc_survivetime"])
    survive_label.pack(side=tk.LEFT)

    standard_frame = tk.Frame(control_frame)
    standard_frame.grid(row=10, column=4, padx=2, pady=2, sticky="w")
    standard_checkbox = tk.Checkbutton(standard_frame, text="Standard", command=load_images)
    standard_checkbox.pack(side=tk.LEFT)
    standard_label = tk.Label(standard_frame, image=photo_images["vc_standard"])
    standard_label.pack(side=tk.LEFT)


    # row 11 - win conditions
    build_grail_frame = tk.Frame(control_frame)
    build_grail_frame.grid(row=11, column=0, padx=2, pady=2, sticky="w")
    build_grail_checkbox = tk.Checkbutton(build_grail_frame, text="Build Grail structure", command=load_images)
    build_grail_checkbox.pack(side=tk.LEFT)
    build_grail_label = tk.Label(build_grail_frame, image=photo_images["vc_buildgrail"])
    build_grail_label.pack(side=tk.LEFT)

    eliminate_monsters_frame = tk.Frame(control_frame)
    eliminate_monsters_frame.grid(row=11, column=1, padx=2, pady=2, sticky="w")
    eliminate_monsters_checkbox = tk.Checkbutton(eliminate_monsters_frame, text="Eliminiate all Monsters", command=load_images)
    eliminate_monsters_checkbox.pack(side=tk.LEFT)
    eliminate_monsters_label = tk.Label(eliminate_monsters_frame, image=photo_images["vc_allmonsters"])
    eliminate_monsters_label.pack(side=tk.LEFT)

    transport_artifact_frame = tk.Frame(control_frame)
    transport_artifact_frame.grid(row=11, column=2, padx=2, pady=2, sticky="w")
    transport_artifact_checkbox = tk.Checkbutton(transport_artifact_frame, text="Transport specific Artifact", command=load_images)
    transport_artifact_checkbox.pack(side=tk.LEFT)
    transport_artifact_label = tk.Label(transport_artifact_frame, image=photo_images["vc_transport"])
    transport_artifact_label.pack(side=tk.LEFT)
    
    accumuulate_creatures_frame = tk.Frame(control_frame)
    accumuulate_creatures_frame.grid(row=11, column=3, padx=2, pady=2, sticky="w")
    accumuulate_creatures_checkbox = tk.Checkbutton(accumuulate_creatures_frame, text="Accumulate Creatures", command=load_images)
    accumuulate_creatures_checkbox.pack(side=tk.LEFT)
    accumuulate_creatures_label = tk.Label(accumuulate_creatures_frame, image=photo_images["vc_creatures"])
    accumuulate_creatures_label.pack(side=tk.LEFT)

    # row 12 - win conditions continued
    capture_town_frame = tk.Frame(control_frame)
    capture_town_frame.grid(row=12, column=0, padx=2, pady=2, sticky="w")
    capture_town_checkbox = tk.Checkbutton(capture_town_frame, text="Capture specific Town", command=load_images)
    capture_town_checkbox.pack(side=tk.LEFT)
    capture_town_label = tk.Label(capture_town_frame, image=photo_images["vc_capturecity"])
    capture_town_label.pack(side=tk.LEFT)

    flag_dwellings_frame = tk.Frame(control_frame)
    flag_dwellings_frame.grid(row=12, column=1, padx=2, pady=2, sticky="w")
    flag_dwellings_checkbox = tk.Checkbutton(flag_dwellings_frame, text="Flag all creature Dwellings", command=load_images)
    flag_dwellings_checkbox.pack(side=tk.LEFT)
    flag_dwellings_label = tk.Label(flag_dwellings_frame, image=photo_images["vc_flagdwellings"])
    flag_dwellings_label.pack(side=tk.LEFT)

    upgrade_town_frame = tk.Frame(control_frame)
    upgrade_town_frame.grid(row=12, column=2, padx=2, pady=2, sticky="w")
    upgrade_town_checkbox = tk.Checkbutton(upgrade_town_frame, text="Upgrade specific Town", command=load_images)
    upgrade_town_checkbox.pack(side=tk.LEFT)
    upgrade_town_label = tk.Label(upgrade_town_frame, image=photo_images["vc_buildcity"])
    upgrade_town_label.pack(side=tk.LEFT)

    accumuulate_resources_frame = tk.Frame(control_frame)
    accumuulate_resources_frame.grid(row=12, column=3, padx=2, pady=2, sticky="w")
    accumuulate_resources_checkbox = tk.Checkbutton(accumuulate_resources_frame, text="Accumulate resources", command=load_images)
    accumuulate_resources_checkbox.pack(side=tk.LEFT)
    accumuulate_resources_label = tk.Label(accumuulate_resources_frame, image=photo_images["vc_resources"])
    accumuulate_resources_label.pack(side=tk.LEFT)


    # row 13 - win conditions continued
    defeat_hero_frame = tk.Frame(control_frame)
    defeat_hero_frame.grid(row=13, column=0, padx=2, pady=2, sticky="w")
    defeat_hero_checkbox = tk.Checkbutton(defeat_hero_frame, text="Defeat specific Hero", command=load_images)
    defeat_hero_checkbox.pack(side=tk.LEFT)
    defeat_hero_label = tk.Label(defeat_hero_frame, image=photo_images["vc_hero"])
    defeat_hero_label.pack(side=tk.LEFT)

    flag_mines_frame = tk.Frame(control_frame)
    flag_mines_frame.grid(row=13, column=1, padx=2, pady=2, sticky="w")
    flag_mines_checkbox = tk.Checkbutton(flag_mines_frame, text="Flag all mines", command=load_images)
    flag_mines_checkbox.pack(side=tk.LEFT)
    flag_mines_label = tk.Label(flag_mines_frame, image=photo_images["vc_flagmines"])
    flag_mines_label.pack(side=tk.LEFT)


    # row 14 - lose conditions
    sort_label = tk.Label(control_frame, text="Lose conditions", font=("Arial", 12))
    sort_label.grid(row=14, column=0, columnspan=3, padx=2, pady=2, sticky="w")

    no_conditions_frame = tk.Frame(control_frame)
    no_conditions_frame.grid(row=14, column=1, padx=2, pady=2, sticky="w")
    no_conditions_checkbox = tk.Checkbutton(no_conditions_frame, text="None", command=load_images)
    no_conditions_checkbox.pack(side=tk.LEFT)
    no_conditions_label = tk.Label(no_conditions_frame, image=photo_images["ls_standard"])
    no_conditions_label.pack(side=tk.LEFT)

    lose_hero_frame = tk.Frame(control_frame)
    lose_hero_frame.grid(row=14, column=2, padx=2, pady=2, sticky="w")
    lose_hero_checkbox = tk.Checkbutton(lose_hero_frame, text="Lose specific Hero", command=load_images)
    lose_hero_checkbox.pack(side=tk.LEFT)
    lose_hero_label = tk.Label(lose_hero_frame, image=photo_images["ls_hero"])
    lose_hero_label.pack(side=tk.LEFT)

    lose_town_frame = tk.Frame(control_frame)
    lose_town_frame.grid(row=14, column=3, padx=2, pady=2, sticky="w")
    lose_town_checkbox = tk.Checkbutton(lose_town_frame, text="Lose specific Town", command=load_images)
    lose_town_checkbox.pack(side=tk.LEFT)
    lose_town_label = tk.Label(lose_town_frame, image=photo_images["ls_town"])
    lose_town_label.pack(side=tk.LEFT)

    time_expire_frame = tk.Frame(control_frame)
    time_expire_frame.grid(row=14, column=4, padx=2, pady=2, sticky="w")
    time_expire_checkbox = tk.Checkbutton(time_expire_frame, text="Time Expires", command=load_images)
    time_expire_checkbox.pack(side=tk.LEFT)
    time_expire_label = tk.Label(time_expire_frame, image=photo_images["ls_timeexpires"])
    time_expire_label.pack(side=tk.LEFT)

    # row 15 - 16 - Slider for adjusting the number of columns
    cols_slider = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL, label="", command=update_cols, showvalue=False)
    cols_slider.grid(row=15, column=0, padx=2, pady=2, sticky="ew", columnspan=5)
    cols_label = tk.Label(control_frame, text=f"Columns: {COLS}", font=("Arial", 12))
    cols_label.grid(row=16, column=0, padx=2, pady=2, sticky="ew", columnspan=5)

    # row 17 - 18 - Slider for adjusting the image size
    image_size_slider = tk.Scale(control_frame, from_=100, to=1000, orient=tk.HORIZONTAL, label="", command=update_image_sizes, showvalue=False)
    image_size_slider.grid(row=17, column=0, padx=2, pady=2, sticky="ew", columnspan=5)
    image_size_label = tk.Label(control_frame, text=f"Image size: {IMAGE_WIDTH}x{IMAGE_HEIGHT}", font=("Arial", 12))
    image_size_label.grid(row=18, column=0, padx=2, pady=2, sticky="ew", columnspan=5)

    # row 19 - Reset settings button
    reset_button = tk.Button(control_frame, text="Reset settings", command=reset_settings)
    reset_button.grid(row=19, column=0, padx=2, pady=2, sticky="ew", columnspan=5)

    # row 20 - Progress label
    progress_label = tk.Label(control_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 12))
    progress_label.grid(row=20, column=0, padx=2, pady=2, sticky="ew", columnspan=5)

    # Configure column resizing behavior for the control frame
    # if there are 7 checkboxes across 7 columns in a single row
    # then single widgets (e.g. buttons) in a row without 6 other columns, need to fill them out with columnspan=5
    # the below weighting means each column has the same width
    control_frame.grid_columnconfigure(0, weight=1)
    control_frame.grid_columnconfigure(1, weight=1)
    control_frame.grid_columnconfigure(2, weight=1)
    control_frame.grid_columnconfigure(3, weight=1)
    control_frame.grid_columnconfigure(4, weight=1)
    control_frame.grid_columnconfigure(5, weight=1)

    # Configure column and row resizing behavior for the root window
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)
