# Render the 17 November 2026 front page to a 1024x1024 PNG.
#
# Build-time tool only: it runs here on this machine, where Pillow and
# the DejaVu fonts are installed. The entry itself (main.py) never runs
# this file; it ships the finished entry.png and copies it to /output.
# Run:  python3 tools/render.py [outpath]   (default: entry.png at repo root)
#
# The picture is drawn, not photographed: every pictogram is a few
# geometric shapes, so the file stays small, the text stays crisp, and
# the render is byte-for-byte repeatable.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import news  # noqa: E402

WIDTH, HEIGHT = 1024, 1024
MARGIN = 28

PAPER = (246, 241, 231)
CARD = (255, 253, 248)
INK = (25, 25, 25)
MUTED = (91, 91, 91)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
PALE = (199, 206, 222)
BORDER = (216, 210, 194)
FLAME = (217, 119, 6)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
    os.path.expanduser("~/.fonts"),
]


def locate_font(filename):
    for folder in FONT_DIRS:
        candidate = os.path.join(folder, filename)
        if os.path.isfile(candidate):
            return candidate
    raise FileNotFoundError("font not found: " + filename)


def serif_bold(size):
    return ImageFont.truetype(locate_font("DejaVuSerif-Bold.ttf"), size)


def sans(size):
    return ImageFont.truetype(locate_font("DejaVuSans.ttf"), size)


def sans_bold(size):
    return ImageFont.truetype(locate_font("DejaVuSans-Bold.ttf"), size)


def wrap_text(draw, text, font, width, max_lines=None, first_width=None):
    """Greedy word wrap; returns a list of lines that fit `width`.

    When `first_width` is given, the first line is limited to it (room
    for a pictogram in the top-right corner); later lines use `width`.
    """
    words = text.split()
    lines = []
    current = ""
    limit = first_width if first_width is not None else width
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= limit:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
            limit = width
    if current:
        lines.append(current)
    if max_lines is not None:
        lines = lines[:max_lines]
    return lines


def draw_tracked(draw, centre_x, y, text, font, fill, tracking=4):
    """Draw centred text with extra space between letters."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = centre_x - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking


def draw_bridge(draw, box, accent):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    water_y = y0 + int(h * 0.78)
    deck_y = y0 + int(h * 0.30)
    # Water: three wavy strokes.
    for i, wy in enumerate((water_y, water_y + 14, water_y + 28)):
        draw.arc([x0 + 6, wy - 8, x0 + w - 6, wy + 8], 0, 180, fill=(29, 78, 216), width=3)
    # Pylons.
    for px in (x0 + int(w * 0.22), x0 + int(w * 0.78)):
        draw.line([px, deck_y - 52, px, deck_y + 4], fill=INK, width=5)
        draw.line([px - 14, deck_y - 52, px + 14, deck_y - 52], fill=INK, width=5)
    # Deck: left span level, right span dropped into the water.
    mid = x0 + w // 2
    draw.line([x0 + 4, deck_y, mid - 26, deck_y], fill=INK, width=7)
    draw.line([mid + 30, deck_y + 26, x1 - 4, deck_y + 44], fill=INK, width=7)
    # Fallen span: a short tilted segment sinking at the gap.
    draw.line([mid - 22, deck_y + 6, mid + 26, deck_y + 30], fill=accent, width=6)
    # Burst where the span gave way.
    bx, by = mid + 2, deck_y - 6
    for dx, dy in ((-16, -12), (0, -20), (16, -12), (-18, 4), (18, 4)):
        draw.line([bx, by, bx + dx, by + dy], fill=accent, width=4)
    draw.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=accent)


def draw_tanker(draw, box, accent):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    hull_y = y0 + int(h * 0.52)
    # Hull.
    draw.polygon(
        [(x0 + 6, hull_y), (x1 - 6, hull_y), (x1 - 22, hull_y + 26), (x0 + 22, hull_y + 26)],
        fill=(30, 58, 95),
    )
    # Containers and funnel.
    draw.rectangle([x0 + 26, hull_y - 22, x0 + 52, hull_y - 2], fill=accent)
    draw.rectangle([x0 + 56, hull_y - 22, x0 + 82, hull_y - 2], fill=(217, 119, 6))
    draw.rectangle([x1 - 44, hull_y - 30, x1 - 24, hull_y - 2], fill=INK)
    # Flame above the cargo.
    fx = x0 + int(w * 0.45)
    draw.polygon(
        [(fx - 12, hull_y - 20), (fx, hull_y - 44), (fx + 12, hull_y - 20)],
        fill=FLAME,
    )
    # A spiked mine drifting clear of the hull, lower left.
    mx, my = x0 + 14, hull_y + 46
    draw.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=INK)
    for dx, dy in ((-12, 0), (12, 0), (0, -12), (0, 12), (-9, -9), (9, -9), (-9, 9), (9, 9)):
        draw.line([mx, my, mx + dx, my + dy], fill=INK, width=2)


def draw_globe(draw, box, accent):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 4
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=accent, width=4)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=accent, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=accent, width=3)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 180, fill=accent, width=3)
    draw.arc([cx - r, cy + r // 2, cx + r, cy + int(r * 1.5)], 180, 360, fill=accent, width=3)


def draw_pin(draw, box, accent):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    top = y0 + 6
    draw.ellipse([cx - 26, top, cx + 26, top + 52], fill=accent)
    draw.polygon([(cx - 22, top + 40), (cx + 22, top + 40), (cx, y1 - 8)], fill=accent)
    draw.ellipse([cx - 10, top + 16, cx + 10, top + 36], fill=CARD)
    # Motion ticks to the right of the pin.
    for i, ty in enumerate((top + 12, top + 30, top + 48)):
        draw.line([x1 - 14, ty, x1 - 2, ty], fill=MUTED, width=3)


def draw_chip(draw, box, accent):
    x0, y0, x1, y1 = box
    w = x1 - x0
    draw.rounded_rectangle([x0 + 14, y0 + 10, x1 - 14, y1 - 10], radius=8, outline=INK, width=4)
    draw.rectangle([x0 + 30, y0 + 26, x1 - 30, y1 - 26], outline=accent, width=3)
    for i in range(3):
        px = x0 + 26 + i * 16
        draw.line([px, y0 + 2, px, y0 + 10], fill=INK, width=3)
        draw.line([px, y1 - 10, px, y1 - 2], fill=INK, width=3)
        py = y0 + 22 + i * 16
        draw.line([x0 + 6, py, x0 + 14, py], fill=INK, width=3)
        draw.line([x1 - 14, py, x1 - 6, py], fill=INK, width=3)
    # Rising arrow across the chip.
    ax0, ay0 = x0 + 30, y1 - 34
    draw.line([ax0, ay0, ax0 + 16, ay0 - 14, ax0 + 30, ay0 - 22], fill=accent, width=4)
    draw.line([ax0 + 30, ay0 - 22, ax0 + 22, ay0 - 22], fill=accent, width=4)
    draw.line([ax0 + 30, ay0 - 22, ax0 + 30, ay0 - 14], fill=accent, width=4)


ICONS = {
    "bridge": draw_bridge,
    "tanker": draw_tanker,
    "globe": draw_globe,
    "pin": draw_pin,
    "chip": draw_chip,
}


def render():
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------
    draw.rectangle([0, 0, WIDTH, 168], fill=NAVY)
    draw_tracked(draw, WIDTH // 2, 24, news.PAGE_KICKER, sans_bold(25), GOLD, tracking=6)
    date_size = 58
    while draw.textlength(news.PAGE_DATE, font=serif_bold(date_size)) > 960 and date_size > 30:
        date_size -= 2
    draw.text(
        (WIDTH // 2, 56), news.PAGE_DATE, font=serif_bold(date_size),
        fill=(255, 255, 255), anchor="ma",
    )
    draw.text(
        (WIDTH // 2, 126), news.PAGE_SUB, font=sans(25), fill=PALE, anchor="ma"
    )
    draw.rectangle([0, 168, WIDTH, 172], fill=GOLD)

    # ---- Lead story ----------------------------------------------
    lx0, ly0, lx1, ly1 = MARGIN, 188, WIDTH - MARGIN, 452
    draw.rounded_rectangle([lx0, ly0, lx1, ly1], radius=10, fill=CARD, outline=BORDER, width=2)
    draw.rectangle([lx0, ly0 + 10, lx0 + 8, ly1 - 10], fill=news.LEAD["accent"])
    text_x = lx0 + 26
    draw.text((text_x, ly0 + 16), news.LEAD["tag"], font=sans_bold(23), fill=news.LEAD["accent"])
    headline = wrap_text(draw, news.LEAD["headline"], serif_bold(40), 640, max_lines=2)
    hy = ly0 + 52
    for line in headline:
        draw.text((text_x, hy), line, font=serif_bold(40), fill=INK)
        hy += 50
    deck = wrap_text(draw, news.LEAD["deck"], sans(26), 640, max_lines=2)
    dy = hy + 10
    for line in deck:
        draw.text((text_x, dy), line, font=sans(26), fill=MUTED)
        dy += 33
    ICONS[news.LEAD["icon"]](draw, (700, 216, 968, 432), news.LEAD["accent"])

    # ---- Story grid ------------------------------------------------
    grid = [
        (MARGIN, 468, 504, 660),
        (520, 468, WIDTH - MARGIN, 660),
        (MARGIN, 676, 504, 868),
        (520, 676, WIDTH - MARGIN, 868),
    ]
    for story, (x0, y0, x1, y1) in zip(news.STORIES, grid):
        draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD, outline=BORDER, width=2)
        draw.rectangle([x0, y0, x1, y0 + 6], fill=story["accent"])
        draw.text((x0 + 18, y0 + 16), story["tag"], font=sans_bold(20), fill=story["accent"])
        ICONS[story["icon"]](draw, (x1 - 86, y0 + 10, x1 - 14, y0 + 82), story["accent"])
        headline = wrap_text(
            draw, story["headline"], serif_bold(28), x1 - x0 - 36,
            max_lines=2, first_width=x1 - x0 - 36 - 74,
        )
        hy = y0 + 46
        for line in headline:
            draw.text((x0 + 18, hy), line, font=serif_bold(28), fill=INK)
            hy += 35
        deck = wrap_text(draw, story["deck"], sans(22), x1 - x0 - 36, max_lines=2)
        dy = hy + 8
        for line in deck:
            draw.text((x0 + 18, dy), line, font=sans(22), fill=MUTED)
            dy += 28

    # ---- Brief strip ------------------------------------------------
    by = 884
    draw.text((MARGIN, by), news.BRIEFS_HEADER, font=sans_bold(21), fill=NAVY)
    draw.line([MARGIN + 250, by + 13, WIDTH - MARGIN, by + 13], fill=BORDER, width=2)
    col_w = 312
    for i, (tag, text) in enumerate(news.BRIEFS):
        cx = MARGIN + i * (col_w + 16)
        lines = wrap_text(draw, tag + " \u2014 " + text, sans(20), col_w, max_lines=2)
        ly = by + 34
        for line in lines:
            draw.text((cx, ly), line, font=sans(20), fill=INK)
            ly += 26

    # ---- Footer ------------------------------------------------------
    draw.text(
        (WIDTH // 2, 992), news.PAGE_FOOTER, font=sans(19), fill=MUTED, anchor="ma"
    )
    return img


def main(argv):
    out = argv[1] if len(argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "entry.png"
    )
    img = render()
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main(sys.argv)
