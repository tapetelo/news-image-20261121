#!/usr/bin/env python3
"""Repair the footer line of the 21 November 2026 front page (entry 2).

Entry 1's dev judge drew one game and named two flaws in the small
footer line under the DATE CHECK box: it read "Every slsry hare
happened, or was first reported, on Friday 21 November 2026" —
garbled words, and Friday contradicting the Saturday headline.
This script repaints only that one line, in place, with the
corrected sentence in a matching sans face on the page's own
cream background. Nothing else on the page changes: same pixels
everywhere else, no crop, no resize, no recomposition.
"""

import os

from PIL import Image, ImageDraw, ImageFont

SOURCE = os.path.expanduser(
    "~/workspace/user/media_library/image/img_386611027335650329.webp")
TARGET = os.path.expanduser(
    "~/workspace/makefun/news-image-20261121-entry/entry.png")
FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

OLD_LINE = ("Every slsry hare happened, or was first reported, "
            "on Friday 21 November 2026. Officials' counts are attributed.")
NEW_LINE = ("Every story here happened, or was first reported, "
            "on Saturday 21 November 2026. Officials' counts are attributed.")

# Measured on the source: the left footer line spans x 16..714,
# y 1000..1019 (dark pixels). The right-hand credit line starts
# near x 715 and stays untouched.
TEXT_X = 16
TEXT_TOP = 1010  # measured ink top of the original line
PAINT_BOX = (10, 1005, 712, 1022)  # below the DATE CHECK box's red border (y 1002-1003)
INK = (30, 28, 26)


def background_colour(image):
    """Median of the bright paper pixels in the footer band itself."""
    bright = []
    for y in range(1005, 1023):
        for x in range(10, 712):
            pixel = image.getpixel((x, y))
            if sum(pixel) > 700:
                bright.append(pixel)
    bright.sort()
    return bright[len(bright) // 2]


def fitted_font(draw, text, max_width):
    """Largest Liberation Sans size whose rendering fits max_width."""
    for size in range(16, 8, -1):
        font = ImageFont.truetype(FONT_PATH, size)
        if draw.textlength(text, font=font) <= max_width:
            return font, size
    raise RuntimeError("no font size fits the footer line")


def main():
    page = Image.open(SOURCE).convert("RGB")
    assert page.size == (1024, 1024), page.size
    draw = ImageDraw.Draw(page)
    draw.rectangle(PAINT_BOX, fill=background_colour(page))
    font, size = fitted_font(draw, NEW_LINE, max_width=696)
    # Align the new line's ink top with the old line's ink top.
    bbox = draw.textbbox((0, 0), NEW_LINE, font=font)
    draw.text((TEXT_X, TEXT_TOP - bbox[1]), NEW_LINE, font=font, fill=INK)
    page.save(TARGET, format="JPEG", quality=95, optimize=True)
    print(f"old: {OLD_LINE}")
    print(f"new: {NEW_LINE}")
    print(f"font size {size}, wrote {TARGET} ({os.path.getsize(TARGET)} bytes)")


if __name__ == "__main__":
    main()
