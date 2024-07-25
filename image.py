from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_quote_image(quote, author, image_path, font_path="arial.ttf", width=800, height=400):
    # Blank image with white background
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(font_path, 24)
    except IOError:
        font = ImageFont.load_default()

    # Wrap the quote text
    wrapped_text = textwrap.fill(quote, width=60)

    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 3

    # Calculate author text size and position
    author_text = f"- {author}"
    author_bbox = draw.textbbox((0, 0), author_text, font=font)
    author_width = author_bbox[2] - author_bbox[0]
    author_height = author_bbox[3] - author_bbox[1]
    author_x = (width - author_width) / 2
    author_y = text_y + text_height + 20

    # Draw the text on the image
    draw.text((text_x, text_y), wrapped_text, font=font, fill="black")
    draw.text((author_x, author_y), author_text, font=font, fill="black")

    # Save the image
    img.save(image_path)
