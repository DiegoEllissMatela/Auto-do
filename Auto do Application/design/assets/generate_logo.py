"""
Logo and Icon Generator for Auto Do Application.
Creates high-resolution brand icon matching the website design ($ in rounded badge).
Works with PIL or built-in Tkinter fallback.
"""

import os
import sys

def generate_brand_logo(output_dir=None):
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)

    png_path = os.path.join(output_dir, "icon.png")
    ico_path = os.path.join(output_dir, "icon.ico")

    # Attempt high-res generation using PIL if available
    try:
        from PIL import Image, ImageDraw, ImageFont  # type: ignore

        size = (256, 256)
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Outer rounded rectangle badge
        bg_color = (25, 26, 38, 255)       # Deep dark indigo surface
        border_color = (99, 102, 241, 220)  # Glowing indigo border
        corner_radius = 52
        
        # Draw shadow
        draw.rounded_rectangle([(12, 16), (244, 248)], radius=corner_radius, fill=(10, 11, 16, 120))
        
        # Main badge
        draw.rounded_rectangle([(10, 10), (246, 246)], radius=corner_radius, fill=bg_color, outline=border_color, width=6)
        
        # Inner subtle glow rectangle
        draw.rounded_rectangle([(24, 24), (232, 232)], radius=corner_radius - 12, outline=(99, 102, 241, 60), width=3)

        # Draw the "$" symbol in the center with modern tech typography
        font = None
        for font_name in ["consola.ttf", "arial.ttf", "segoeui.ttf"]:
            try:
                font = ImageFont.truetype(font_name, 140)
                break
            except Exception:
                continue
        if font is None:
            font = ImageFont.load_default()

        dollar_text = "$"
        try:
            bbox = draw.textbbox((0, 0), dollar_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (size[0] - text_width) // 2 - bbox[0]
            text_y = (size[1] - text_height) // 2 - bbox[1]
        except Exception:
            text_x, text_y = 70, 40

        # Glow under text
        draw.text((text_x, text_y), dollar_text, font=font, fill=(99, 102, 241, 150))
        # Main crisp symbol
        draw.text((text_x, text_y), dollar_text, font=font, fill=(129, 140, 248, 255))

        # Save PNG
        img.save(png_path, "PNG")
        
        # Save ICO
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(ico_path, format="ICO", sizes=icon_sizes)
        print(f"Generated logo assets at: {output_dir}")
        return True

    except ImportError:
        print("PIL is not installed. Using existing assets or standard Tkinter fallback.")
        return False

if __name__ == "__main__":
    generate_brand_logo()
