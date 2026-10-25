import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
BLUE_TOP, BLUE_BOTTOM = (58, 125, 196), (34, 88, 160)
YELLOW, YELLOW_SHADOW = (247, 226, 74), (214, 186, 40)
RED, OUTLINE, WHITE = (232, 62, 52), (40, 22, 26), (255, 255, 255)

def render(size, content=1.0):
    S = size * 4  # supersample for smooth edges
    img = Image.new("RGB", (S, S))
    d = ImageDraw.Draw(img)
    for y in range(S):  # vertical blue gradient
        t = y / (S - 1)
        d.line([(0, y), (S, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(BLUE_TOP, BLUE_BOTTOM)))

    c = S / 2
    k = S * content  # content box edge length
    # Triangle with a white rim, as in the box art.
    top, base_y, half = c - 0.41 * k, c + 0.37 * k, 0.49 * k
    rim = 0.035 * k
    d.polygon([(c, top - rim * 1.9), (c - half - rim * 1.7, base_y + rim), (c + half + rim * 1.7, base_y + rim)], fill=WHITE)
    d.polygon([(c, top), (c - half, base_y), (c + half, base_y)], fill=YELLOW)

    def word(text, cy, width):
        size_px = 10
        font = ImageFont.truetype(FONT, size_px)
        size_px = int(size_px * width / d.textlength(text, font=font))
        font = ImageFont.truetype(FONT, size_px)
        sw_white, sw_dark = int(size_px * 0.13), int(size_px * 0.045)
        # Yellow drop shadow, white backing, dark outline, red face.
        off = int(size_px * 0.05)
        d.text((c + off, cy + off), text, font=font, fill=YELLOW_SHADOW, anchor="mm", stroke_width=sw_white, stroke_fill=YELLOW_SHADOW)
        d.text((c, cy), text, font=font, fill=WHITE, anchor="mm", stroke_width=sw_white, stroke_fill=WHITE)
        d.text((c, cy), text, font=font, fill=RED, anchor="mm", stroke_width=sw_dark, stroke_fill=OUTLINE)

    word("FIRE", c - 0.05 * k, 0.70 * k)
    word("TEAM", c + 0.23 * k, 0.84 * k)
    return img.resize((size, size), Image.LANCZOS)

# Usage: python3 tools/make_icon.py www/static
out = sys.argv[1]
render(512).save(f"{out}/icon-512.png", optimize=True)
render(192).save(f"{out}/icon-192.png", optimize=True)
render(180).save(f"{out}/apple-touch-icon.png", optimize=True)
render(512, content=0.78).save(f"{out}/icon-maskable-512.png", optimize=True)  # keep inside the maskable safe zone
render(1024).save(f"{out}/../../tools/icon-1024.png", optimize=True)  # App Store / Xcode size, not served
