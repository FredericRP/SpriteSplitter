import sys, os
from PIL import Image

def extract_sprites(input_image_path, output_path):
    # Load the spritesheet
    spritesheet = Image.open(input_image_path)

    # Define minimum size for sprites
    min_sprite_size = (4, 4)

    # Function to check if a pixel has non-transparent color
    def is_non_transparent_pixel(image, x, y):
        pixel = image.getpixel((x, y))
        return pixel[3] != 0  # Check alpha channel for transparency

    # Function to explore non-transparent areas and extract sprites
    def explore_area(start_x, start_y):
        area = []
        stack = [(start_x, start_y)]
        visited.add((start_x, start_y))

        while stack:
            x, y = stack.pop()
            area.append((x, y))

            neighbors = [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1)
            ]

            for nx, ny in neighbors:
                if 0 <= nx < spritesheet.width and 0 <= ny < spritesheet.height and is_non_transparent_pixel(spritesheet, nx, ny) and (nx, ny) not in visited:
                    stack.append((nx, ny))
                    visited.add((nx, ny))

        return area

    # Extract individual sprites
    sprites = []
    visited = set()

    for y in range(spritesheet.height):
        for x in range(spritesheet.width):
            if is_non_transparent_pixel(spritesheet, x, y) and (x, y) not in visited:
                area = explore_area(x, y)

                min_x = min(x for x, _ in area)
                max_x = max(x for x, _ in area)
                min_y = min(y for _, y in area)
                max_y = max(y for _, y in area)

                sprite_width = max_x - min_x + 1
                sprite_height = max_y - min_y + 1

                if sprite_width >= min_sprite_size[0] and sprite_height >= min_sprite_size[1]:
                    sprite = spritesheet.crop((min_x, min_y, max_x + 1, max_y + 1))
                    sprites.append(sprite)

    # Save individual sprites
    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    for idx, sprite in enumerate(sprites):
        sprite.save(f"{output_path}/sprite_{idx}.png", "PNG")

# Check if the correct number of arguments is provided
if len(sys.argv) != 3:
    print("Usage: python remove_bg_and_split.py <spritesheet_path> <output_folder>")
    sys.exit(1)

# Get arguments
spritesheet_path = sys.argv[1]
output_folder = sys.argv[2]

# Call the function with provided arguments
extract_sprites(spritesheet_path, output_folder)
