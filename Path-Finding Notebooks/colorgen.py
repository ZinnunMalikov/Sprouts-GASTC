import colorsys

def generate_colors(num_colors):
    colors = []
    for i in range(num_colors):
        # Generate HSV values with varying hue and saturation
        hue = (i * (360 / num_colors)) % 360
        saturation = 50  # Vary saturation for visibility
        value = 85 + (i % 4) * 5  # Vary value (lightness) for visibility

        # Convert HSV to RGB
        rgb = colorsys.hsv_to_rgb(hue / 360, saturation / 100, value / 100)

        # Convert RGB to integer values in the range [0, 255]
        rgb_int = tuple(int(channel * 255) for channel in rgb)

        # Avoid (240, 240, 240) and (0, 0, 0)
        if rgb_int != (240, 240, 240) and rgb_int != (0, 0, 0):
            colors.append(rgb_int)

    return colors

# Generate 40 colors
num_colors = 40
generated_colors = generate_colors(num_colors)

print(generated_colors)

