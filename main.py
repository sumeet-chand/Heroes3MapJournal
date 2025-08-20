# A Heroes of Might and Magic 3 software to download map images, rate them and share notes with others
# Author: Sumeet Chand
# /main.py
# To run the below script first run: pip install pillow requests beautifulsoup4
import tkinter as tk
from PIL import Image, ImageTk
from typing import Dict, Callable, Optional
import os
import platform # for detecting the host OS
import requests # download the images
import urllib.parse # for converting special characters when download e.g. Tovar%27's to Tovar's
import re # for regex
from bs4 import BeautifulSoup # for parsing HTML content

cols: int = 1
image_width: int = 300
image_height: int = 300
spacing_x: int = 20
spacing_y: int = 20
root = tk.Tk()
screen_width: int = root.winfo_screenwidth()
screen_height: int = root.winfo_screenheight()
root.state('zoomed') # maximize window
root.title("Heroes 3 Map Liker")
root.minsize(300, 450)
assets_directory: str = "assets"
map_images_dir: str = os.path.join(assets_directory, "map_images")
progress_label: Optional[tk.Label] = None
background_photo: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open("assets/page.png").resize((screen_width, screen_height)))  # type: ignore
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
# Main canvas frame with scrollbars
canvas_frame: tk.Frame = tk.Frame(root)
canvas_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
canvas_frame.grid_rowconfigure(0, weight=1)
canvas_frame.grid_columnconfigure(0, weight=1)
# Create canvas
canvas: tk.Canvas = tk.Canvas(canvas_frame, bg="white")
canvas.grid(row=0, column=0, sticky="nsew")
# Vertical scrollbar
canvas_vscrollbar: tk.Scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)  # type: ignore
canvas_vscrollbar.grid(row=0, column=1, sticky="ns")
# Horizontal scrollbar
canvas_hscrollbar: tk.Scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=lambda *args: canvas.xview(*args))  # type: ignore
canvas_hscrollbar.grid(row=1, column=0, sticky="ew")
canvas.configure(yscrollcommand=canvas_vscrollbar.set, xscrollcommand=canvas_hscrollbar.set)
# Place the background image at the lowest z-order
canvas.create_image(0, 0, image=background_photo, anchor=tk.NW)  # type: ignore
# Frame inside canvas for images
frame: tk.Frame = tk.Frame(canvas)
frame_id: int = canvas.create_window((0, 0), window=frame, anchor=tk.NW)
map_name_label: tk.Label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 14))
map_name_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
cols_label: tk.Label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 14))
cols_label.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
image_size_label: tk.Label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 14))
image_size_label.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
# Ensure progress_label is always initialized
if progress_label is None:
    progress_label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 12))
    progress_label.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

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
    icon_path: Image.Image = Image.open("assets/view_earth.png")  # Open the image
    icon_path = icon_path.resize((32, 32))  # type: ignore
    icon = ImageTk.PhotoImage(icon_path)  # Convert the image to a PhotoImage
    root.iconphoto(False, icon)  # type: ignore

def load_asset_images(directory: str) -> Dict[str, ImageTk.PhotoImage]:
    """
    Load all asset images from a directory, resize them to (32, 32), and return a dictionary of PhotoImage objects.

    Args:
        directory (str): The directory path containing the images.

    Returns:
        dict: A dictionary containing PhotoImage objects with filenames (without extension) as keys.
    """
    photo_images: Dict[str, ImageTk.PhotoImage] = {}
    for filename in os.listdir(directory):
        if filename.endswith(('.png', '.gif', '.jpg', '.jpeg')):
            path = os.path.join(directory, filename)
            try:
                name = os.path.splitext(filename)[0]  # Extract filename without extension
                image: Image.Image = Image.open(path)  # Load the image
                image = image.resize((32, 32))  # type: ignore
                photo_images[name] = ImageTk.PhotoImage(image)  # Load image and store it in the dictionary
            except Exception as e:
                print(f"Error loading image {path}: {e}")
    return photo_images

def create_directories_if_missing():
    """
    Create directories to hold scrapped map images if they dont exist
    Returns:
        None
    """
    # create image directory if they don't exist
    if not os.path.exists(map_images_dir):
        os.makedirs(map_images_dir)

def download_all_images(map_images_dir: str, progress_callback: Optional[Callable[[str], None]] = None):
    """
    Scrap and download all map images, can be targeted to any new repo holding
    Heroes 3 map data/images. So that if any site goes down, this can be tweaked
    to point to the newest online repo to always pull images when re-scan button is clicked

    Args
    
        map_images_dir (str): folder path for map images
        progress_callback - for GUI widget label to callback progress data on how many maps scanned/remaining

    Returns:
        None
    """
    if not os.path.exists(map_images_dir):
        os.makedirs(map_images_dir)

    url = "https://heroes.thelazy.net/index.php/List_of_maps"
    response = requests.get(url, timeout=10)

    soup = BeautifulSoup(response.text, "html.parser")
    map_links: list[str] = []
    for a in soup.find_all("a", href=True):
        href = a.get("href")  # type: ignore
        if href and isinstance(href, str) and href.startswith("/index.php/") and not href.startswith("/index.php/Map_Attributes") and not href.startswith("/index.php/Layer") and not href.startswith("/index.php/Expansions"):
            map_links.append("https://heroes.thelazy.net" + href)

    total_maps = len(map_links)
    current_map = 0

    for map_link in map_links:
        current_map += 1
        progress = f"Downloading new images progress: {current_map}/{total_maps}"
        print(progress)
        if progress_callback:
            progress_callback(progress)
        print(f"Map page URL: {map_link}")
        try:
            map_page = requests.get(map_link, timeout=10)
            map_soup = BeautifulSoup(map_page.text, "html.parser")
            # Find all images with 'map' in src
            img_tags = map_soup.find_all("img", src=True)
            for img in img_tags:
                src = img.get("src")  # type: ignore
                if src and isinstance(src, str) and "map" in src:
                    # Look for the parent <a> tag (download button)
                    parent_a = img.find_parent("a", href=True)
                    parent_href = parent_a.get("href") if parent_a else None  # type: ignore
                    if parent_href and isinstance(parent_href, str) and "map" in parent_href:
                        file_page_url = "https://heroes.thelazy.net" + parent_href
                        print(f"Found file page: {file_page_url}")
                        try:
                            file_page = requests.get(file_page_url, timeout=10)
                            file_soup = BeautifulSoup(file_page.text, "html.parser")
                            # Find the download button or full image
                            full_img = file_soup.find("a", href=True, string="Download")
                            full_img_href = full_img.get("href") if full_img else None  # type: ignore
                            if full_img_href and isinstance(full_img_href, str) and "map" in full_img_href:
                                image_url = "https://heroes.thelazy.net" + full_img_href
                                filename = os.path.basename(urllib.parse.unquote(image_url))
                                download_single_image(image_url, map_images_dir, filename)
                            else:
                                # Fallback: find the largest image with 'map' in href
                                imgs = file_soup.find_all("img", src=True)
                                for img2 in imgs:
                                    img2_src = img2.get("src")  # type: ignore
                                    if img2_src and isinstance(img2_src, str) and "map" in img2_src:
                                        image_url = "https://heroes.thelazy.net" + img2_src
                                        filename = os.path.basename(urllib.parse.unquote(image_url))
                                        download_single_image(image_url, map_images_dir, filename)
                        except Exception as e:
                            print(f"Failed to get file page: {file_page_url}: {e}")
        except requests.exceptions.Timeout:
            print(f"Timeout while downloading: {map_link}")
            if progress_callback:
                progress_callback(f"Timeout for {map_link}. Skipping...")
            continue
        except requests.exceptions.RequestException as e:
            print(f"Request error for {map_link}: {e}")
            if progress_callback:
                progress_callback(f"Error for {map_link}. Skipping...")
            continue

    # Define map_info as an empty dictionary to avoid errors
    map_info: Dict[str, str] = {}

    for map_name, map_link in map_info.items():
        current_map += 1
        progress: str = f"Downloading new images progress: {current_map}/{total_maps}"
        print(progress)
        
        if progress_callback:
            progress_callback(progress)
        
        print(f"Map page URL: {map_link}")  # Print the map page URL
        image_url: str = map_link + "#/media/File:" + map_name.replace(" ", "_") + "_map_auto.png"

        print(f"Processing image URL: {image_url}")
        try:
            image_response = requests.get(image_url, timeout=10)
            img_tags = re.findall(r'<img.+?src="([^"]+)"', image_response.text)
            if img_tags:
                for img_tag in img_tags:
                    match = re.search(r'/images/(.*?)map_auto.png', img_tag)
                    if match:
                        download_link: str = "https://heroes.thelazy.net/images/" + match.group(1) + "map_auto.png"
                        download_link = download_link.replace("/thumb", "")
                        filename: str = os.path.basename(urllib.parse.unquote(download_link))
                        download_single_image(download_link, map_images_dir, filename)
            else:
                print("No download link found.")
        except requests.exceptions.Timeout:
            print(f"Timeout while downloading: {image_url}")
            if progress_callback:
                progress_callback(f"Timeout for {map_name}. Skipping...")
            continue
        except requests.exceptions.RequestException as e:
            print(f"Request error for {image_url}: {e}")
            if progress_callback:
                progress_callback(f"Error for {map_name}. Skipping...")
            continue

    print("Completed processing for all maps.")
    if progress_callback:
        progress_callback("Re-scanning complete!")

def download_single_image(image_url: str, save_path: str, filename: str):
    """
    Download an image from the given URL and save it to the specified path with the given filename.

    Args
    
        image_url (str): URL of the image to download
        save_path (str): Path where the image should be saved
        filename (str): Name of the file to save as

    Returns:
        None
    """
    if os.path.exists(os.path.join(save_path, filename)):
        print(f"Image already exists: {os.path.join(save_path, filename)}")
    else:
        try:
            response = requests.get(image_url, timeout=10)
            with open(os.path.join(save_path, filename), 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded: {os.path.join(save_path, filename)}")
        except Exception as e:
            print(f"Failed to download image from {image_url}: {str(e)}")

def toggle_control_panel():

    """
    Button to hide or show control panel triggers this function

    Returns:
        None
    """
    global control_frame_container
    if control_frame_container.winfo_viewable():
        control_frame_container.grid_remove()
        toggle_button.config(text="Show settings", image=photo_images["book_open"], compound="right")
    else:
        control_frame_container.grid()
        toggle_button.config(text="Hide settings", image=photo_images["book_closed"], compound="right")
    
def update_images():
        """
        rescan images button progress label

        Returns:
            None
        """
        if progress_label is not None:
            progress_label.config(text="Rescanning images...")
            root.update()  # Force update of the GUI
        download_all_images(map_images_dir, update_progress)
        load_images()
    
def update_progress(status: str) -> None:
        """
        rescan images button progress label

        Returns:
            None
        """
        if progress_label is not None:
            progress_label.config(text=status)
            root.update()
        else:
            print(f"Progress label is not initialized. Status: {status}")

def show_map_name(map_name: str) -> None:
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
        for entry in os.listdir(map_images_dir):
            path = os.path.join(map_images_dir, entry)
            if os.path.isfile(path) and path.endswith('.png'):
                image = Image.open(path)
                image = image.resize((image_width, image_height))  # type: ignore
                photo = ImageTk.PhotoImage(image)
                label = tk.Label(frame, image=photo)
                label.image = photo  # type: ignore
                label.map_name = os.path.splitext(entry)[0]  # type: ignore
                label.bind("<Button-1>", lambda event: show_map_name(event.widget.map_name))  # type: ignore
                row: int = len(frame.grid_slaves()) // int(cols)
                col: int = len(frame.grid_slaves()) % int(cols)
                label.grid(row=row, column=col, padx=spacing_x, pady=spacing_y)

        update_scroll_region(None)  # Update the scroll region after loading images

def update_scroll_region(event: Optional[tk.Event] = None) -> None:
        """
        bind scroll bar GUI element to canvas

        Returns:
            None
        """
        canvas.configure(scrollregion=canvas.bbox("all"))

def update_cols(value: str) -> None:
        """
        Slider to create more columns

        Returns:
            None
        """
        cols: int = int(value)
        cols_label.config(text=f"Columns: {cols}")
        load_images()

def update_image_sizes(value: str) -> None:
        """
        image size slider

        Returns:
            None
        """
        size: int = int(value)
        image_width = size
        image_height = size
        image_size_label.config(text=f"Image size: {image_width}x{image_height}")
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
        global cols, image_width, image_height, screen_width, screen_height
        cols = 1
        image_width = 300
        image_height = 300
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        cols_label.config(text=f"Columns: {cols}")
        image_size_label.config(text=f"Image size: {image_width}x{image_height}")
        load_images()

def on_key_press(event: tk.Event) -> None:
        """
        Keyboard input handling. On keyboard key/button click/press perform relevant action below

        Returns:
            None
        """
        if event.keysym == "Up":
            canvas.yview_scroll(-1, "units")  # type: ignore
        if event.keysym == "Down":
            canvas.yview_scroll(1, "units")  # type: ignore
        if event.keysym == "Left":
            canvas.xview_scroll(-1, "units")
        if event.keysym == "Right":
            canvas.xview_scroll(1, "units")

def on_mouse_wheel(event: tk.Event):
        """
        If platform is a MacOS use touchpad scrolling which is two fingers button 4 and 5 for touch
        scrolling. Otherwise use the default mouse wheel for scrolling in any other OS

        Returns:
            None
        """
        delta = getattr(event, 'delta', 0)
        if platform.system() == "Darwin":  # Check if the platform is macOS
            canvas.yview_scroll(int(-1 * delta), "units")  # Adjust the scrolling for macOS touchpads
        else:
            canvas.yview_scroll(int(-1*(delta/120)), "units")  # For other platforms, use the original scrolling behavior
    
def create_control_frame():
    """
    Create the scrollable settings pane (control_frame) and add all widgets to it.
    Returns the control_frame and progress_label.
    """
    control_frame_container = tk.Frame(root)
    control_frame_container.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)
    control_canvas = tk.Canvas(control_frame_container, height=300, width=600)
    control_scrollbar = tk.Scrollbar(control_frame_container, orient=tk.VERTICAL, command=control_canvas.yview)  # type: ignore
    control_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    control_hscrollbar = tk.Scrollbar(control_frame_container, orient=tk.HORIZONTAL, command=control_canvas.xview)  # type: ignore
    control_hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    control_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    control_canvas.configure(yscrollcommand=control_scrollbar.set, xscrollcommand=control_hscrollbar.set)
    control_frame = tk.Frame(control_canvas)
    control_canvas.create_window((0, 0), window=control_frame, anchor=tk.NW)
    def update_control_scroll_region(event: object = None) -> None:  # type: ignore
        control_canvas.configure(scrollregion=control_canvas.bbox("all"))
    control_frame.bind("<Configure>", update_control_scroll_region)  # type: ignore

    # row 1 - Like map button
    like_button = tk.Button(control_frame, text="like", command=like_image)
    like_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=5)

    # row 2 - Play map button
    play_button = tk.Button(control_frame, text="Play map", command=play_map)
    play_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew", columnspan=5)

    # row 3 - Rescan Images button
    load_button = tk.Button(control_frame, text="Rescan images", command=update_images)
    load_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew", columnspan=5)

    # row 4 - Reset settings button
    reset_settings_button = tk.Button(control_frame, text="Reset settings", command=reset_settings)
    reset_settings_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=5)

    # row 5 - sort
    sort_label = tk.Label(control_frame, text="Filter", font=("Arial", 12))
    sort_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    liked_frame = tk.Frame(control_frame) # Create frame hold checkbox, text and star image, in same column
    liked_frame.grid(row=4, column=1, padx=5, pady=5, sticky="w")
    liked_checkbox = tk.Checkbutton(liked_frame, text="Liked", command=load_images) # Create the liked checkbox
    liked_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    liked_label = tk.Label(liked_frame, image=photo_images["star"]) # Create a label for the star image
    liked_label.pack(side=tk.LEFT, padx=2, pady=2)

    name_descending_frame = tk.Frame(control_frame)
    name_descending_frame.grid(row=4, column=2, padx=5, pady=5, sticky="w")
    name_descending_checkbox = tk.Checkbutton(name_descending_frame, text="Name descending", command=load_images)
    name_descending_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    name_descending_label = tk.Label(name_descending_frame, image=photo_images["name_descending"])
    name_descending_label.pack(side=tk.LEFT, padx=2, pady=2)

    name_ascending_frame = tk.Frame(control_frame)
    name_ascending_frame.grid(row=4, column=3, padx=5, pady=5, sticky="w")
    name_ascending_checkbox = tk.Checkbutton(name_ascending_frame, text="Name ascending", command=load_images)
    name_ascending_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    name_ascending_label = tk.Label(name_ascending_frame, image=photo_images["name_ascending"])
    name_ascending_label.pack(side=tk.LEFT, padx=2, pady=2)

    subterranean_frame = tk.Frame(control_frame)
    subterranean_frame.grid(row=4, column=4, padx=5, pady=5, sticky="w")
    subterranean_checkbox = tk.Checkbutton(subterranean_frame, text="subterranean", command=load_images)
    subterranean_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    subterranean_label = tk.Label(subterranean_frame, image=photo_images["subterranean"])
    subterranean_label.pack(side=tk.LEFT, padx=2, pady=2)

    # filter row 5 - expansion
    sort_label = tk.Label(control_frame, text="Expansion", font=("Arial", 12))
    sort_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    roe_frame = tk.Frame(control_frame)
    roe_frame.grid(row=5, column=1, padx=5, pady=5, sticky="w")
    roe_checkbox = tk.Checkbutton(roe_frame, text="Restoration of Erathia", command=load_images)
    roe_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    roe_label = tk.Label(roe_frame, image=photo_images["v_roe"])
    roe_label.pack(side=tk.LEFT, padx=2, pady=2)

    ab_frame = tk.Frame(control_frame)
    ab_frame.grid(row=5, column=2, padx=5, pady=5, sticky="w")
    ab_checkbox = tk.Checkbutton(ab_frame, text="Armageddons Blade", command=load_images)
    ab_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    ab_label = tk.Label(ab_frame, image=photo_images["v_ab"])
    ab_label.pack(side=tk.LEFT, padx=2, pady=2)

    sod_frame = tk.Frame(control_frame)
    sod_frame.grid(row=5, column=3, padx=5, pady=5, sticky="w")
    sod_checkbox = tk.Checkbutton(sod_frame, text="Shadow of Death", command=load_images)
    sod_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    sod_label = tk.Label(sod_frame, image=photo_images["v_sod"])
    sod_label.pack(side=tk.LEFT, padx=2, pady=2)

    hota_frame = tk.Frame(control_frame)
    hota_frame.grid(row=5, column=4, padx=5, pady=5, sticky="w")
    hota_checkbox = tk.Checkbutton(hota_frame, text="Horn of the Abyss", command=load_images)
    hota_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    hota_label = tk.Label(hota_frame, image=photo_images["v_hota"])
    hota_label.pack(side=tk.LEFT, padx=2, pady=2)

    # row 6 - map sizes
    sort_label = tk.Label(control_frame, text="Map size", font=("Arial", 12))
    sort_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    small_map_frame = tk.Frame(control_frame)
    small_map_frame.grid(row=6, column=1, padx=5, pady=5, sticky="w")
    small_map_checkbox = tk.Checkbutton(small_map_frame, text="S", command=load_images)
    small_map_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    small_map_label = tk.Label(small_map_frame, image=photo_images["sz0_s"])
    small_map_label.pack(side=tk.LEFT, padx=2, pady=2)

    medium_map_frame = tk.Frame(control_frame)
    medium_map_frame.grid(row=6, column=2, padx=5, pady=5, sticky="w")
    medium_map_checkbox = tk.Checkbutton(medium_map_frame, text="M", command=load_images)
    medium_map_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    medium_map_label = tk.Label(medium_map_frame, image=photo_images["sz1_m"])
    medium_map_label.pack(side=tk.LEFT, padx=2, pady=2)

    large_map_frame = tk.Frame(control_frame)
    large_map_frame.grid(row=6, column=3, padx=5, pady=5, sticky="w")
    large_map_checkbox = tk.Checkbutton(large_map_frame, text="L", command=load_images)
    large_map_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    large_map_label = tk.Label(large_map_frame, image=photo_images["sz2_l"])
    large_map_label.pack(side=tk.LEFT, padx=2, pady=2)

    extra_large_map_frame = tk.Frame(control_frame)
    extra_large_map_frame.grid(row=6, column=4, padx=5, pady=5, sticky="w")
    extra_large_map_checkbox = tk.Checkbutton(extra_large_map_frame, text="XL", command=load_images)
    extra_large_map_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    extra_large_map_label = tk.Label(extra_large_map_frame, image=photo_images["sz3_xl"])
    extra_large_map_label.pack(side=tk.LEFT, padx=2, pady=2)

    # row 7 - map size continued
    huge_map_frame = tk.Frame(control_frame)
    huge_map_frame.grid(row=7, column=0, padx=5, pady=5, sticky="w")
    huge_map_checkbox = tk.Checkbutton(huge_map_frame, text="H", command=load_images)
    huge_map_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    huge_map_label = tk.Label(huge_map_frame, image=photo_images["sz4_h"])
    huge_map_label.pack(side=tk.LEFT, padx=2, pady=2)

    extra_huge_map_frame = tk.Frame(control_frame)
    extra_huge_map_frame.grid(row=7, column=1, padx=5, pady=5, sticky="w")
    extra_huge_map_checkbox = tk.Checkbutton(extra_huge_map_frame, text="XH", command=load_images)
    extra_huge_map_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    extra_huge_map_label = tk.Label(extra_huge_map_frame, image=photo_images["sz5_xh"])
    extra_huge_map_label.pack(side=tk.LEFT, padx=2, pady=2)

    giant_map_frame = tk.Frame(control_frame)
    giant_map_frame.grid(row=7, column=2, padx=5, pady=5, sticky="w")
    giant_map_checkbox = tk.Checkbutton(giant_map_frame, text="G", command=load_images)
    giant_map_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    giant_map_label = tk.Label(giant_map_frame, image=photo_images["sz6_g"])
    giant_map_label.pack(side=tk.LEFT, padx=2, pady=2)


    # row 8 - difficulty
    sort_label = tk.Label(control_frame, text="Difficulty", font=("Arial", 12))
    sort_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    easy_map_frame = tk.Frame(control_frame)
    easy_map_frame.grid(row=8, column=1, padx=5, pady=5, sticky="w")
    easy_map_checkbox = tk.Checkbutton(easy_map_frame, text="Easy", command=load_images)
    easy_map_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    easy_map_label = tk.Label(easy_map_frame, image=photo_images["dif_easy"])
    easy_map_label.pack(side=tk.LEFT, padx=2, pady=2)

    normal_map_frame = tk.Frame(control_frame)
    normal_map_frame.grid(row=8, column=2, padx=5, pady=5, sticky="w")
    normal_map_checkbox = tk.Checkbutton(normal_map_frame, text="Normal", command=load_images)
    normal_map_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    normal_map_label = tk.Label(normal_map_frame, image=photo_images["dif_normal"])
    normal_map_label.pack(side=tk.LEFT, padx=2, pady=2)

    hard_map_frame = tk.Frame(control_frame)
    hard_map_frame.grid(row=8, column=3, padx=5, pady=5, sticky="w")
    hard_map_checkbox = tk.Checkbutton(hard_map_frame, text="Hard", command=load_images)
    hard_map_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    hard_map_label = tk.Label(hard_map_frame, image=photo_images["dif_hard"])
    hard_map_label.pack(side=tk.LEFT, padx=2, pady=2)

    expert_map_frame = tk.Frame(control_frame)
    expert_map_frame.grid(row=8, column=4, padx=5, pady=5, sticky="w")
    expert_map_checkbox = tk.Checkbutton(expert_map_frame, text="Expert", command=load_images)
    expert_map_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    expert_map_label = tk.Label(expert_map_frame, image=photo_images["dif_expert"])
    expert_map_label.pack(side=tk.LEFT, padx=2, pady=2)

    # row 9 - difficulty continued
    impossible_map_frame = tk.Frame(control_frame)
    impossible_map_frame.grid(row=9, column=0, padx=5, pady=5, sticky="w")
    impossible_map_checkbox = tk.Checkbutton(impossible_map_frame, text="Impossible", command=load_images)
    impossible_map_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    impossible_map_label = tk.Label(impossible_map_frame, image=photo_images["dif_impossible"])
    impossible_map_label.pack(side=tk.LEFT, padx=2, pady=2)


    # row 10 - win conditions
    sort_label = tk.Label(control_frame, text="Win conditions", font=("Arial", 12))
    sort_label.grid(row=10, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    acquire_artifact_frame = tk.Frame(control_frame)
    acquire_artifact_frame.grid(row=10, column=1, padx=5, pady=5, sticky="w")
    acquire_artifact_checkbox = tk.Checkbutton(acquire_artifact_frame, text="Acquire specific Artifact", command=load_images)
    acquire_artifact_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    acquire_artifact_label = tk.Label(acquire_artifact_frame, image=photo_images["vc_artifact"])
    acquire_artifact_label.pack(side=tk.LEFT, padx=2, pady=2)

    defeat_monster_frame = tk.Frame(control_frame)
    defeat_monster_frame.grid(row=10, column=2, padx=5, pady=5, sticky="w")
    defeat_monster_checkbox = tk.Checkbutton(defeat_monster_frame, text="Defeat specific Monster", command=load_images)
    defeat_monster_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    defeat_monster_label = tk.Label(defeat_monster_frame, image=photo_images["vc_monster"])
    defeat_monster_label.pack(side=tk.LEFT, padx=2, pady=2)

    survive_frame = tk.Frame(control_frame)
    survive_frame.grid(row=10, column=3, padx=5, pady=5, sticky="w")
    survive_checkbox = tk.Checkbutton(survive_frame, text="Survive certain time", command=load_images)
    survive_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    survive_label = tk.Label(survive_frame, image=photo_images["vc_survivetime"])
    survive_label.pack(side=tk.LEFT, padx=2, pady=2)

    standard_frame = tk.Frame(control_frame)
    standard_frame.grid(row=10, column=4, padx=5, pady=5, sticky="w")
    standard_checkbox = tk.Checkbutton(standard_frame, text="Standard", command=load_images)
    standard_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    standard_label = tk.Label(standard_frame, image=photo_images["vc_standard"])
    standard_label.pack(side=tk.LEFT, padx=2, pady=2)


    # row 11 - win conditions
    build_grail_frame = tk.Frame(control_frame)
    build_grail_frame.grid(row=11, column=0, padx=5, pady=5, sticky="w")
    build_grail_checkbox = tk.Checkbutton(build_grail_frame, text="Build Grail structure", command=load_images)
    build_grail_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    build_grail_label = tk.Label(build_grail_frame, image=photo_images["vc_buildgrail"])
    build_grail_label.pack(side=tk.LEFT, padx=2, pady=2)

    eliminate_monsters_frame = tk.Frame(control_frame)
    eliminate_monsters_frame.grid(row=11, column=1, padx=5, pady=5, sticky="w")
    eliminate_monsters_checkbox = tk.Checkbutton(eliminate_monsters_frame, text="Eliminiate all Monsters", command=load_images)
    eliminate_monsters_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    eliminate_monsters_label = tk.Label(eliminate_monsters_frame, image=photo_images["vc_allmonsters"])
    eliminate_monsters_label.pack(side=tk.LEFT, padx=2, pady=2)

    transport_artifact_frame = tk.Frame(control_frame)
    transport_artifact_frame.grid(row=11, column=2, padx=5, pady=5, sticky="w")
    transport_artifact_checkbox = tk.Checkbutton(transport_artifact_frame, text="Transport specific Artifact", command=load_images)
    transport_artifact_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    transport_artifact_label = tk.Label(transport_artifact_frame, image=photo_images["vc_transport"])
    transport_artifact_label.pack(side=tk.LEFT, padx=2, pady=2)
    
    accumuulate_creatures_frame = tk.Frame(control_frame)
    accumuulate_creatures_frame.grid(row=11, column=3, padx=5, pady=5, sticky="w")
    accumuulate_creatures_checkbox = tk.Checkbutton(accumuulate_creatures_frame, text="Accumulate Creatures", command=load_images)
    accumuulate_creatures_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    accumuulate_creatures_label = tk.Label(accumuulate_creatures_frame, image=photo_images["vc_creatures"])
    accumuulate_creatures_label.pack(side=tk.LEFT, padx=2, pady=2)

    # row 12 - win conditions continued
    capture_town_frame = tk.Frame(control_frame)
    capture_town_frame.grid(row=12, column=0, padx=5, pady=5, sticky="w")
    capture_town_checkbox = tk.Checkbutton(capture_town_frame, text="Capture specific Town", command=load_images)
    capture_town_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    capture_town_label = tk.Label(capture_town_frame, image=photo_images["vc_capturecity"])
    capture_town_label.pack(side=tk.LEFT, padx=2, pady=2)

    flag_dwellings_frame = tk.Frame(control_frame)
    flag_dwellings_frame.grid(row=12, column=1, padx=5, pady=5, sticky="w")
    flag_dwellings_checkbox = tk.Checkbutton(flag_dwellings_frame, text="Flag all creature Dwellings", command=load_images)
    flag_dwellings_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    flag_dwellings_label = tk.Label(flag_dwellings_frame, image=photo_images["vc_flagdwellings"])
    flag_dwellings_label.pack(side=tk.LEFT, padx=2, pady=2)

    upgrade_town_frame = tk.Frame(control_frame)
    upgrade_town_frame.grid(row=12, column=2, padx=5, pady=5, sticky="w")
    upgrade_town_checkbox = tk.Checkbutton(upgrade_town_frame, text="Upgrade specific Town", command=load_images)
    upgrade_town_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    upgrade_town_label = tk.Label(upgrade_town_frame, image=photo_images["vc_buildcity"])
    upgrade_town_label.pack(side=tk.LEFT, padx=2, pady=2)

    accumuulate_resources_frame = tk.Frame(control_frame)
    accumuulate_resources_frame.grid(row=12, column=3, padx=5, pady=5, sticky="w")
    accumuulate_resources_checkbox = tk.Checkbutton(accumuulate_resources_frame, text="Accumulate resources", command=load_images)
    accumuulate_resources_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    accumuulate_resources_label = tk.Label(accumuulate_resources_frame, image=photo_images["vc_resources"])
    accumuulate_resources_label.pack(side=tk.LEFT, padx=2, pady=2)


    # row 13 - win conditions continued
    defeat_hero_frame = tk.Frame(control_frame)
    defeat_hero_frame.grid(row=13, column=0, padx=5, pady=5, sticky="w")
    defeat_hero_checkbox = tk.Checkbutton(defeat_hero_frame, text="Defeat specific Hero", command=load_images)
    defeat_hero_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    defeat_hero_label = tk.Label(defeat_hero_frame, image=photo_images["vc_hero"])
    defeat_hero_label.pack(side=tk.LEFT, padx=2, pady=2)

    flag_mines_frame = tk.Frame(control_frame)
    flag_mines_frame.grid(row=13, column=1, padx=5, pady=5, sticky="w")
    flag_mines_checkbox = tk.Checkbutton(flag_mines_frame, text="Flag all mines", command=load_images)
    flag_mines_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    flag_mines_label = tk.Label(flag_mines_frame, image=photo_images["vc_flagmines"])
    flag_mines_label.pack(side=tk.LEFT, padx=2, pady=2)


    # row 14 - lose conditions
    sort_label = tk.Label(control_frame, text="Lose conditions", font=("Arial", 12))
    sort_label.grid(row=14, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    no_conditions_frame = tk.Frame(control_frame)
    no_conditions_frame.grid(row=14, column=1, padx=5, pady=5, sticky="w")
    no_conditions_checkbox = tk.Checkbutton(no_conditions_frame, text="None", command=load_images)
    no_conditions_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    no_conditions_label = tk.Label(no_conditions_frame, image=photo_images["ls_standard"])
    no_conditions_label.pack(side=tk.LEFT, padx=2, pady=2)

    lose_hero_frame = tk.Frame(control_frame)
    lose_hero_frame.grid(row=14, column=2, padx=5, pady=5, sticky="w")
    lose_hero_checkbox = tk.Checkbutton(lose_hero_frame, text="Lose specific Hero", command=load_images)
    lose_hero_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    lose_hero_label = tk.Label(lose_hero_frame, image=photo_images["ls_hero"])
    lose_hero_label.pack(side=tk.LEFT, padx=2, pady=2)

    lose_town_frame = tk.Frame(control_frame)
    lose_town_frame.grid(row=14, column=3, padx=5, pady=5, sticky="w")
    lose_town_checkbox = tk.Checkbutton(lose_town_frame, text="Lose specific Town", command=load_images)
    lose_town_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    lose_town_label = tk.Label(lose_town_frame, image=photo_images["ls_town"])
    lose_town_label.pack(side=tk.LEFT, padx=2, pady=2)

    time_expire_frame = tk.Frame(control_frame)
    time_expire_frame.grid(row=14, column=4, padx=5, pady=5, sticky="w")
    time_expire_checkbox = tk.Checkbutton(time_expire_frame, text="Time Expires", command=load_images)
    time_expire_checkbox.pack(side=tk.LEFT, padx=2, pady=2)
    time_expire_label = tk.Label(time_expire_frame, image=photo_images["ls_timeexpires"])
    time_expire_label.pack(side=tk.LEFT, padx=2, pady=2)

    # row 15 - 16 - Slider for adjusting the number of columns
    cols_slider = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL, label="", command=update_cols, showvalue=False)
    cols_slider.grid(row=15, column=0, padx=5, pady=5, sticky="ew", columnspan=5)
    cols_label = tk.Label(control_frame, text=f"Columns: {cols}", font=("Arial", 12))
    cols_label.grid(row=16, column=0, padx=5, pady=5, sticky="ew", columnspan=5)

    # row 17 - 18 - Slider for adjusting the image size
    image_size_slider = tk.Scale(control_frame, from_=100, to=1000, orient=tk.HORIZONTAL, label="", command=update_image_sizes, showvalue=False)
    image_size_slider.grid(row=17, column=0, padx=5, pady=5, sticky="ew", columnspan=5)
    image_size_label = tk.Label(control_frame, text=f"Image size: {image_width}x{image_height}", font=("Arial", 12))
    image_size_label.grid(row=18, column=0, padx=5, pady=5, sticky="ew", columnspan=5)

    # row 19 - Reset settings button
    reset_button = tk.Button(control_frame, text="Reset settings", command=reset_settings)
    reset_button.grid(row=19, column=0, padx=5, pady=5, sticky="ew", columnspan=5)

    return control_frame_container, control_frame, progress_label

set_window_icon()

photo_images: Dict[str, ImageTk.PhotoImage] = load_asset_images(assets_directory)

create_directories_if_missing()

load_images()

frame.bind("<Configure>", update_scroll_region)

# Bind all key presses to the on_key_press function
canvas.bind_all("<KeyPress>", on_key_press)

# Make control_frame_container and control_frame global so toggle_control_panel can access them
global control_frame_container, control_frame
control_frame_container, control_frame, progress_label = create_control_frame()
# Show control panel by default (row 0)
toggle_button = tk.Button(root, text="Hide settings", image=photo_images["book_closed"], compound="right", command=toggle_control_panel)
toggle_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

root.mainloop()
