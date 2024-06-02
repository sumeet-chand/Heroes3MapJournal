import urllib.parse
import os
import requests
import re
import platform

def download_images(base_dir: str, subterranean_dir: str, progress_callback=None):
    """
    Scrap and download all map images, can be targeted to any new repo holding
    Heroes 3 map data/images. So that if any site goes down, this can be tweaked
    to point to the newest online repo to always pull images when rescan button is clicked

    Args
    
        base_dir (str): folder path for overworld images
        subterranean_dir (str): folder path for overworld images
        progress_callback - for GUI widget label to callback progress data on how many maps scanned/remaining

    Returns:
        None
    """
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    if not os.path.exists(subterranean_dir):
        os.makedirs(subterranean_dir)

    url: str = "https://heroes.thelazy.net/index.php/List_of_maps"
    response = requests.get(url)

    map_info: dict = {}
    map_name_tags: list[str] = response.text.split('<td style="text-align:center;">')[1:]

    total_maps: int = len(map_name_tags) // 2
    current_map: int = 0

    for i in range(0, len(map_name_tags), 2):
        map_name_tag: str = map_name_tags[i + 1]
        map_name_match = re.search(r'title="(.*?)"', map_name_tag)
        map_link_match = re.search(r'href="(.*?)"', map_name_tag)
        if map_name_match and map_link_match:
            map_name: str = map_name_match.group(1)
            map_link: str = "https://heroes.thelazy.net" + map_link_match.group(1)
            map_info[map_name] = map_link

    for map_name, map_link in map_info.items():
        current_map += 1
        progress: str = f"Downloading new images progress: {current_map}/{total_maps}"
        print(progress)
        
        if progress_callback:
            progress_callback(progress)
        
        print(f"Map page URL: {map_link}")  # Print the map page URL
        image_url: str = map_link + "#/media/File:" + map_name.replace(" ", "_") + "_map_auto.png"
        print(f"Processing image URL: {image_url}")

        image_response = requests.get(image_url)
        img_tags = re.findall(r'<img.+?src="([^"]+)"', image_response.text)
        if img_tags:
            for img_tag in img_tags:
                if "subterranean" not in img_tag:
                    match = re.search(r'/images/(.*?)map_auto.png', img_tag)
                    if match:
                        download_link: str = "https://heroes.thelazy.net/images/" + match.group(1) + "map_auto.png"
                        download_link = download_link.replace("/thumb", "")
                        filename: str = os.path.join(base_dir, os.path.basename(download_link))
                        download_image(download_link, filename)
                else:
                    match = re.search(r'/images/(.*?)map_auto.png', img_tag)
                    if match:
                        download_link = "https://heroes.thelazy.net/images/" + match.group(1) + "map_auto.png"
                        download_link = download_link.replace("/thumb", "")
                        filename = os.path.join(subterranean_dir, os.path.basename(download_link))
                        download_image(download_link, filename)
        else:
            print("No download link found.")

    print("Completed processing for all maps.")
    if progress_callback:
        progress_callback("Rescanning complete!")

def download_image(image_url: str, save_path: str):
    """
    Scrap and download all map images, can be targetted to any new repo holding
    Heroes 3 map data/images. So that if any site goes down, this can be tweaked
    to point to the newest online repo to always pull images when rescan button is clicked

    Args
    
        image_url (str): folder path for overworld images
        save_path (str): folder path for overworld images

    Returns:
        None
    """
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
