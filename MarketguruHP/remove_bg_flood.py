from PIL import Image, ImageDraw

def remove_bg_floodfill(input_path, output_path):
    # Open the image and ensure it has an alpha channel
    img = Image.open(input_path).convert("RGBA")
    
    # We will flood fill from the top-left corner (0,0)
    # To do this safely, we create a mask or we can use ImageDraw.floodfill
    # ImageDraw.floodfill fills a contiguous region with a specific color.
    # We will fill the background with a unique magic color, then convert that color to transparent.
    
    magic_color = (255, 0, 255, 255) # Magenta
    
    # Threshold for what is considered background (white or near-white)
    # ImageDraw.floodfill doesn't have tolerance, so we might need to manually do a BFS
    # or if the background is perfectly white, floodfill works.
    
    # Let's write a custom BFS floodfill with tolerance
    width, height = img.size
    pixels = img.load()
    
    visited = set()
    queue = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
    
    for start_x, start_y in queue:
        if (start_x, start_y) in visited:
            continue
            
        q = [(start_x, start_y)]
        visited.add((start_x, start_y))
        
        while q:
            x, y = q.pop(0)
            r, g, b, a = pixels[x, y]
            
            # If it's near white
            if r > 230 and g > 230 and b > 230:
                pixels[x, y] = (255, 255, 255, 0) # Make transparent
                
                # Check neighbors
                for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                    if 0 <= nx < width and 0 <= ny < height:
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            q.append((nx, ny))

    img.save(output_path, "PNG")

# Re-copy the original uploaded image to get the white bg back
import shutil
shutil.copy("C:\\Users\\HP\\.gemini\\antigravity\\brain\\01d4073b-4c66-4841-8b02-1f3e61eccaa7\\media__1781554657305.png", "logo_orig.png")

remove_bg_floodfill("logo_orig.png", "logo.png")
print("Floodfill background removal done!")
