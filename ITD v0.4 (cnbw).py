import requests
from PIL import Image
from io import BytesIO

def get_image(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

def apply_bw_dither(img):
    """Standard Floyd-Steinberg B&W Dithering"""
    return img.convert('L').convert('1')

def apply_color_bayer(img, contrast=1.5, brightness=0.45, max_ceiling=185):
    """Tactical Color Bayer Dithering (Standard Library + Pillow)"""
    img = img.convert('RGB')
    width, height = img.size
    pixels = img.load()

    # 8x8 Bayer Matrix
    bayer8 = [
        [ 0, 32,  8, 40,  2, 34, 10, 42],
        [48, 16, 56, 24, 50, 18, 58, 26],
        [12, 44,  4, 36, 14, 46,  6, 38],
        [60, 28, 68, 20, 62, 30, 70, 22],
        [ 3, 35, 11, 43,  1, 33,  9, 41],
        [51, 19, 59, 27, 49, 17, 57, 25],
        [15, 47,  7, 39, 13, 45,  5, 37],
        [63, 31, 71, 23, 61, 29, 69, 21]
    ]
    factor = 256 / 64

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            channels = []
            for col in (r, g, b):
                # Apply Gamma (1.6) and adjustments
                val = 255 * (col / 255) ** 1.6
                val = val * brightness * contrast
                val = min(max_ceiling, max(0, val))
                
                threshold = bayer8[y % 8][x % 8] * factor
                channels.append(255 if val > threshold else 0)
            
            pixels[x, y] = tuple(channels)
    return img

def main():
    print("--- Tactical Image Ditherer ---")
    url = input("Image URL: ").strip()
    mode = input("Black and White or Color? (bw/c): ").strip().lower()
    save_name = input("Save as (filename): ").strip()

    # Ensure valid filename
    if not save_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        save_name += ".png"

    try:
        print("Processing...")
        original = get_image(url)
        
        if mode == 'bw':
            result = apply_bw_dither(original)
        elif mode == 'c':
            result = apply_color_bayer(original)
        else:
            print("Invalid mode. Pick 'bw' or 'c'.")
            return

        result.save(save_name)
        result.show()
        print(f"Done! Image saved as: {save_name}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
