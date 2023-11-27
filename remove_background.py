import sys
import os
from PIL import Image
import requests

def extract_filename(full_filename):
    # Extract the base filename without extension
    filename = os.path.basename(full_filename)
    filename_without_extension = os.path.splitext(filename)[0]
    return filename_without_extension

def remove_background(spritesheet_path, output_folder):
    # Request background removal from remove.bg API
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(spritesheet_path, 'rb')},
        data={'size': 'preview'},
        headers={'X-Api-Key': api_key},
    )

    if response.status_code == requests.codes.ok:
        filename_without_extension = extract_filename(spritesheet_path)
        # Save the image with the background removed
        with open(f"{output_folder}/{filename_without_extension}.png", 'wb') as out:
            out.write(response.content)

# Check if the correct number of arguments is provided
if len(sys.argv) != 4:
    print("Usage: python remove_background.py <spritesheet_path> <output_folder> <api_key>")
    sys.exit(1)

# Get arguments
spritesheet_path = sys.argv[1]
output_folder = sys.argv[2]
api_key = sys.argv[3]

# Call the function with provided arguments
remove_background(spritesheet_path, output_folder, api_key)
