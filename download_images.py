import os
import requests
import re

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
        progress = f"Progress: {current_map}/{total_maps}"
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
