from PIL import Image

def extract_colored_parts(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            # If the pixel is greyscale (white, grey, black), the RGB values are very close
            if max(r, g, b) - min(r, g, b) < 15:
                # It's a grey/white pixel, make it transparent
                pixels[x, y] = (255, 255, 255, 0)
            else:
                # It's colored (yellow/green arch), keep it
                pass

    img.save(output_path, "PNG")

extract_colored_parts("logo_orig.png", "logo.png")
print("Colored parts extracted!")
