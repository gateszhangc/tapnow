from pathlib import Path
from math import cos, sin, pi

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "brand"
OUT.mkdir(parents=True, exist_ok=True)

COLORS = {
    "ink": (11, 15, 20),
    "ink2": (17, 24, 32),
    "paper": (246, 241, 232),
    "cyan": (72, 228, 210),
    "coral": (255, 107, 74),
    "lime": (200, 255, 90),
    "blue": (122, 168, 255),
}


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def gradient_background(size):
    width, height = size
    img = Image.new("RGB", size, COLORS["ink"])
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            nx = x / max(width - 1, 1)
            ny = y / max(height - 1, 1)
            glow_a = max(0, 1 - ((nx - 0.78) ** 2 + (ny - 0.25) ** 2) / 0.22)
            glow_b = max(0, 1 - ((nx - 0.2) ** 2 + (ny - 0.76) ** 2) / 0.18)
            r = int(11 + 35 * ny + COLORS["cyan"][0] * glow_a * 0.22 + COLORS["coral"][0] * glow_b * 0.18)
            g = int(15 + 28 * ny + COLORS["cyan"][1] * glow_a * 0.22 + COLORS["coral"][1] * glow_b * 0.12)
            b = int(20 + 30 * ny + COLORS["blue"][2] * glow_a * 0.18 + COLORS["coral"][2] * glow_b * 0.1)
            pixels[x, y] = (min(r, 255), min(g, 255), min(b, 255))
    return img


def draw_grid(draw, width, height, alpha=42):
    for x in range(0, width, 72):
        draw.line((x, 0, x, height), fill=(246, 241, 232, alpha), width=1)
    for y in range(0, height, 72):
        draw.line((0, y, width, y), fill=(246, 241, 232, alpha), width=1)


def draw_signal_mark(draw, center, scale=1.0, with_shadow=False):
    cx, cy = center
    radius = int(96 * scale)
    nodes = []
    for i, angle in enumerate([-0.38, 0.3, 1.18, 2.32, 3.45]):
        distance = radius * (0.72 + 0.16 * (i % 2))
        nodes.append((cx + cos(angle * pi) * distance, cy + sin(angle * pi) * distance))

    if with_shadow:
        draw.ellipse((cx - radius * 1.15, cy - radius * 1.15, cx + radius * 1.15, cy + radius * 1.15), fill=(0, 0, 0, 76))

    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=COLORS["paper"] + (230,), width=max(2, int(5 * scale)))
    draw.arc((cx - radius * 1.18, cy - radius * 1.18, cx + radius * 1.18, cy + radius * 1.18), 205, 345, fill=COLORS["cyan"] + (255,), width=max(3, int(9 * scale)))
    draw.arc((cx - radius * 0.74, cy - radius * 0.74, cx + radius * 0.74, cy + radius * 0.74), 20, 178, fill=COLORS["coral"] + (255,), width=max(3, int(8 * scale)))
    draw.arc((cx - radius * 0.42, cy - radius * 0.42, cx + radius * 0.42, cy + radius * 0.42), 245, 84, fill=COLORS["lime"] + (255,), width=max(3, int(7 * scale)))

    for x, y in nodes:
        draw.line((cx, cy, x, y), fill=(246, 241, 232, 118), width=max(1, int(3 * scale)))
    for idx, (x, y) in enumerate(nodes):
        color = [COLORS["cyan"], COLORS["coral"], COLORS["lime"], COLORS["blue"], COLORS["paper"]][idx]
        node_radius = int(12 * scale)
        draw.ellipse((x - node_radius, y - node_radius, x + node_radius, y + node_radius), fill=color + (255,))
    draw.ellipse((cx - 18 * scale, cy - 18 * scale, cx + 18 * scale, cy + 18 * scale), fill=COLORS["paper"] + (255,))
    draw.ellipse((cx - 7 * scale, cy - 7 * scale, cx + 7 * scale, cy + 7 * scale), fill=COLORS["ink"] + (255,))


def save_mark():
    size = 1024
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((150, 150, 874, 874), fill=COLORS["cyan"] + (42,))
    glow_draw.ellipse((280, 210, 920, 850), fill=COLORS["coral"] + (28,))
    glow = glow.filter(ImageFilter.GaussianBlur(44))
    img.alpha_composite(glow)
    draw = ImageDraw.Draw(img)
    draw_signal_mark(draw, (512, 512), 2.8)
    img.save(OUT / "logo-mark.png")
    img.resize((256, 256), Image.Resampling.LANCZOS).save(OUT / "favicon.png")
    img.resize((180, 180), Image.Resampling.LANCZOS).save(OUT / "apple-touch-icon.png")


def save_wordmark():
    img = Image.new("RGBA", (1500, 480), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_signal_mark(draw, (215, 240), 1.2)
    title_font = font(166, bold=True)
    label_font = font(34, bold=True)
    draw.text((390, 120), "TapNow", fill=COLORS["paper"] + (255,), font=title_font)
    draw.text((398, 305), "AI-NATIVE CREATIVE CANVAS", fill=COLORS["cyan"] + (255,), font=label_font)
    draw.line((396, 365, 1020, 365), fill=COLORS["coral"] + (255,), width=5)
    img.save(OUT / "logo-wordmark.png")


def save_hero_and_social():
    for name, size in [("hero-canvas.png", (1600, 980)), ("social-card.png", (1200, 630))]:
        width, height = size
        base = gradient_background(size).convert("RGBA")
        overlay = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw_grid(draw, width, height, 28)

        for i in range(11):
            x = int(width * (0.56 + 0.04 * (i % 4)))
            y = int(height * (0.16 + 0.071 * i))
            w = int(width * (0.16 + 0.015 * (i % 3)))
            h = int(height * 0.06)
            color = [COLORS["cyan"], COLORS["coral"], COLORS["lime"], COLORS["blue"]][i % 4]
            draw.rounded_rectangle((x, y, x + w, y + h), radius=10, outline=color + (170,), width=2, fill=(11, 15, 20, 126))
            draw.ellipse((x + 18, y + h / 2 - 6, x + 30, y + h / 2 + 6), fill=color + (255,))
            draw.line((x + 46, y + h / 2, x + w - 24, y + h / 2), fill=(246, 241, 232, 95), width=2)
            if i:
                prev_y = int(height * (0.16 + 0.071 * (i - 1))) + h
                draw.line((x + 34, prev_y, x + 34, y), fill=(246, 241, 232, 58), width=2)

        for i in range(26):
            x1 = int(width * (0.08 + (i * 37 % 700) / 1000))
            y1 = int(height * (0.1 + (i * 61 % 760) / 1000))
            x2 = x1 + int(80 + (i % 5) * 34)
            y2 = y1 + int(((i % 7) - 3) * 18)
            color = [COLORS["cyan"], COLORS["coral"], COLORS["lime"], COLORS["blue"]][i % 4]
            draw.line((x1, y1, x2, y2), fill=color + (76,), width=1)
            draw.ellipse((x1 - 3, y1 - 3, x1 + 3, y1 + 3), fill=color + (200,))

        draw_signal_mark(draw, (int(width * 0.74), int(height * 0.46)), 1.45 if width > 1300 else 1.05)

        title_font = font(122 if width > 1300 else 92, bold=True)
        sub_font = font(34 if width > 1300 else 28, bold=True)
        small_font = font(23 if width > 1300 else 20, bold=True)
        draw.text((int(width * 0.07), int(height * 0.24)), "TapNow", fill=COLORS["paper"] + (255,), font=title_font)
        draw.text((int(width * 0.075), int(height * 0.39)), "AI-NATIVE CREATIVE CANVAS", fill=COLORS["cyan"] + (255,), font=sub_font)
        draw.text((int(width * 0.075), int(height * 0.47)), "TEXT  IMAGE  AUDIO  VIDEO", fill=COLORS["lime"] + (255,), font=small_font)
        draw.line((int(width * 0.075), int(height * 0.535), int(width * 0.43), int(height * 0.535)), fill=COLORS["coral"] + (255,), width=5)

        base.alpha_composite(overlay)
        base.save(OUT / name)


if __name__ == "__main__":
    save_mark()
    save_wordmark()
    save_hero_and_social()
