from PIL import Image, ImageDraw, ImageFont
import os
import string

ASSETS_DIR = './assets'

if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

def create_placeholders():
    print("Generating placeholder images for A-Z using Pillow...")
    for char in string.ascii_uppercase:
        filename = os.path.join(ASSETS_DIR, f'{char}.jpg')
        if not os.path.exists(filename):
            # Create a black image
            img = Image.new('RGB', (500, 500), color = (0, 0, 0))
            d = ImageDraw.Draw(img)
            
            # Draw text
            # Default font
            try:
                # Try to load a nice font, or default
                font = ImageFont.truetype("arial.ttf", 250)
                font_small = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                font = ImageFont.load_default()
                font_small = ImageFont.load_default()

            # Center text (approximate for default font, better for truetype)
            # For simplicity, just placing it
            d.text((150, 100), char, font=font, fill=(255, 255, 255))
            d.text((150, 400), "(Placeholder)", font=font_small, fill=(200, 200, 200))
            
            # Save
            img.save(filename)
            print(f"Created {filename}")
        else:
            print(f"Skipping {filename}, already exists.")

    print("Done! You can replace these images in the 'assets' folder with real sign language images later.")

if __name__ == "__main__":
    create_placeholders()
