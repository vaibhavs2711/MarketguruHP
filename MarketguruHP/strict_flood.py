from PIL import Image

def strict_flood_fill(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    visited = set()
    # Start from all pixels along the 4 borders
    queue = []
    for x in range(width):
        queue.append((x, 0))
        queue.append((x, height - 1))
    for y in range(height):
        queue.append((0, y))
        queue.append((width - 1, y))
        
    for start_x, start_y in queue:
        if (start_x, start_y) in visited:
            continue
            
        r, g, b, a = pixels[start_x, start_y]
        if r < 240 or g < 240 or b < 240:
            continue
            
        q = [(start_x, start_y)]
        visited.add((start_x, start_y))
        
        while q:
            x, y = q.pop(0)
            pixels[x, y] = (255, 255, 255, 0)
            
            for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if 0 <= nx < width and 0 <= ny < height:
                    if (nx, ny) not in visited:
                        nr, ng, nb, na = pixels[nx, ny]
                        if nr >= 240 and ng >= 240 and nb >= 240:
                            visited.add((nx, ny))
                            q.append((nx, ny))

    img.save(output_path, "PNG")

strict_flood_fill("logo_orig.png", "logo.png")
print("Strict flood fill done!")
