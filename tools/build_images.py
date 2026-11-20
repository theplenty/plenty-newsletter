"""Build the newsletter images.

Run from the project root:  python -I tools/build_images.py 2026-11
Sources live in assets/ (not published); results go to <issue>/images/.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ISSUE = sys.argv[1] if len(sys.argv) > 1 else "2026-11"
OUT = os.path.join(ISSUE, "images")
MEDIA = os.path.join("assets", "media")
BRAND = os.path.join("assets", "brand")
FOOD = os.path.join("assets", "food")
WORK = os.path.join("preview", "work")

GREEN = (14, 59, 44)      # #0e3b2c  key colour
IVORY = (244, 238, 224)   # #f4eee0


def grade(im, contrast=1.06, color=0.92, bright=0.98):
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Color(im).enhance(color)
    return ImageEnhance.Brightness(im).enhance(bright)


def cover(im, w, h, cx=0.5, cy=0.5):
    """Crop to the target aspect around a focal point, then resize."""
    sw, sh = im.size
    ar = w / h
    if sw / sh > ar:
        cw, ch = int(sh * ar), sh
    else:
        cw, ch = sw, int(sw / ar)
    x0 = int(min(max(sw * cx - cw / 2, 0), sw - cw))
    y0 = int(min(max(sh * cy - ch / 2, 0), sh - ch))
    return im.crop((x0, y0, x0 + cw, y0 + ch)).resize((w, h), Image.LANCZOS)


def save_jpg(im, name, q=86):
    p = os.path.join(OUT, name)
    im.convert("RGB").save(p, "JPEG", quality=q, optimize=True, progressive=True, subsampling=0)
    print(name, im.size, os.path.getsize(p) // 1024, "KB")


def fade_to(im, color, top=0.0, bottom=0.0, top_max=0.0, bottom_max=1.0):
    """Blend towards a solid colour at the top/bottom edges with an eased ramp."""
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    h = a.shape[0]
    alpha = np.zeros(h, np.float32)
    if top > 0:
        n = int(h * top); u = np.linspace(0, 1, n)
        alpha[:n] = np.maximum(alpha[:n], (1 - u * u * (3 - 2 * u)) * top_max)
    if bottom > 0:
        n = int(h * bottom); t = np.linspace(0, 1, n)
        ease = t * t * (3 - 2 * t)
        alpha[h - n:] = np.maximum(alpha[h - n:], ease * bottom_max)
    al = alpha[:, None, None]
    out = a * (1 - al) + np.array(color, np.float32)[None, None, :] * al
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))


def load_logo(name):
    """Official logo lockup, cropped to its ink."""
    im = Image.open(os.path.join(BRAND, name)).convert("RGBA")
    alpha = np.asarray(im)[..., 3]
    ys, xs = np.where(alpha > 12)
    return im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))


# ── 1) masthead logo (official white lockup) ──────────────────────────────
def build_logo():
    logo = load_logo("logo-white.webp")
    w = 480
    h = round(logo.height * w / logo.width)
    logo = logo.resize((w, h), Image.LANCZOS)
    logo.save(os.path.join(OUT, "logo-white.png"), optimize=True)
    print("logo-white.png", logo.size)


# ── 2) hero: levelled, media wall showing the PLENTY logo ─────────────────
ROTATE = -1.475                      # measured tilt of the wall's top edge
WALL = (1223, 898, 2113, 1210)       # media wall incl. bezel glow, after rotation
PODIUM_BOX = (1283, 1128, 1352, 1210)
PODIUM_SIGN = (1287, 1131, 1347, 1146)
FLAG_BOX = (2022, 1102, 2066, 1210)


def wall_art(w, h):
    """What the LED wall shows: a quiet dark-green field with the white logo."""
    s = 3
    W, H = w * s, h * s
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W * 0.50)) ** 2 + ((yy - H / 2) / (H * 0.72)) ** 2).clip(0, 1)
    edge = np.array([4, 12, 9], np.float32)
    core = np.array([15, 44, 34], np.float32)
    field = edge + (core - edge) * ((1 - d) ** 1.6)[..., None]
    art = Image.fromarray(field.clip(0, 255).astype(np.uint8)).convert("RGBA")

    logo = load_logo("logo-white.webp")
    lh = int(H * 0.60)
    lw = round(logo.width * lh / logo.height)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    pos = ((W - lw) // 2, (H - lh) // 2)

    # soft bloom around the lit logo, as an LED wall has in a photo
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow.paste(logo, pos, logo)
    bloom = glow.filter(ImageFilter.GaussianBlur(s * 5))
    bloom.putalpha(bloom.getchannel("A").point(lambda v: int(v * 0.45)))
    art = Image.alpha_composite(art, bloom)
    art = Image.alpha_composite(art, glow)
    art = art.convert("RGB").resize((w, h), Image.LANCZOS)
    art = art.filter(ImageFilter.GaussianBlur(0.9))    # match the photo's softness
    grain = np.random.default_rng(7).normal(0, 2.2, (h, w, 1))
    return Image.fromarray((np.asarray(art).astype(np.float32) + grain).clip(0, 255).astype(np.uint8))


def build_hero():
    src = Image.open(os.path.join(MEDIA, "image3.jpeg")).convert("RGB")
    rot = src.rotate(ROTATE, resample=Image.BICUBIC, expand=False)
    a = np.asarray(rot).astype(np.float32)
    x0, y0, x1, y1 = WALL

    # screen pixels = the wall rectangle minus what stands in front of it
    mask = np.zeros(a.shape[:2], np.float32)
    mask[y0:y1, x0:x1] = 1.0
    lit = (a[..., 2] > 165) & (a[..., 1] > 150)       # the bright LED panels
    for bx0, by0, bx1, by1 in (PODIUM_BOX, FLAG_BOX):
        keep = ~lit[by0:by1, bx0:bx1]
        mask[by0:by1, bx0:bx1][keep] = 0.0
    sx0, sy0, sx1, sy1 = PODIUM_SIGN
    mask[sy0:sy1, sx0:sx1] = 0.0
    mask = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.3))).astype(np.float32) / 255

    art = np.zeros_like(a)
    art[y0:y1, x0:x1] = np.asarray(wall_art(x1 - x0, y1 - y0)).astype(np.float32)
    out = a * (1 - mask[..., None]) + art * mask[..., None]

    # the lit strip under the wall was a reflection of the bright panels: calm it down
    band = np.zeros(a.shape[:2], np.float32)
    band[y1:y1 + 13, x0:x1] = 1.0
    band = np.asarray(Image.fromarray((band * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.0))).astype(np.float32) / 255
    out = out * (1 - 0.55 * band[..., None])
    out[sy0:sy1, sx0:sx1] *= 0.5                       # podium sign was lit by the old screen

    im = Image.fromarray(out.clip(0, 255).astype(np.uint8))
    os.makedirs(WORK, exist_ok=True)
    im.crop((1100, 820, 2240, 1330)).save(os.path.join(WORK, "wall_after.jpg"), quality=92)

    im = im.crop((70, 90, 3230, 2385))                 # drop the corners rotation left empty
    hero = cover(im, 1280, 780, cy=0.46)
    hero = grade(hero, 1.08, 0.90, 0.96)
    hero = fade_to(hero, GREEN, top=0.22, top_max=1.0, bottom=0.42, bottom_max=1.0)
    save_jpg(hero, "hero.jpg", 88)


# ── 3) space, story, dining photos ────────────────────────────────────────
def build_photos():
    for src_name, out_name in (("image5.jpeg", "space-banquet.jpg"), ("image2.jpeg", "space-lobby.jpg"),
                               ("image7.jpeg", "story-kams.jpg"), ("image9.jpeg", "story-dhp.jpg")):
        im = cover(Image.open(os.path.join(MEDIA, src_name)).convert("RGB"), 576, 432)
        save_jpg(grade(im), out_name)
    # course meal: a plain photograph, framed on the plates
    im = Image.open(os.path.join(FOOD, "course-western.jpg")).convert("RGB")
    im = im.crop((296, 74, 1800, 1202))                # tighter on the plates, same 4:3
    save_jpg(grade(cover(im, 576, 432), 1.04, 1.0, 1.0), "dining-course.jpg", 88)
    # lunch box: drop the menu card on the left of the source sheet
    im = Image.open(os.path.join(FOOD, "lunchbox-korean.jpg")).convert("RGB")
    im = im.crop((632, 0, im.width, im.height))
    save_jpg(grade(cover(im, 576, 432, cx=0.47), 1.04, 1.0, 1.0), "dining-korean.jpg", 88)


# ── 4) video thumbnail: crop away the player chrome, add a quiet play mark ─
def build_video():
    v = Image.open(os.path.join(MEDIA, "image10.png")).convert("RGB").crop((67, 8, 1269, 684))
    v = v.resize((1120, 630), Image.LANCZOS)
    v = grade(v, 1.04, 0.95, 0.90)
    s = 4
    ov = Image.new("RGBA", (v.width * s, v.height * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    cx, cy, r = 96 * s, (v.height - 96) * s, 46 * s
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GREEN + (215,), outline=IVORY + (255,), width=2 * s)
    t = 17 * s
    d.polygon([(cx - t * 0.55, cy - t), (cx - t * 0.55, cy + t), (cx + t * 1.05, cy)], fill=IVORY + (255,))
    ov = ov.resize(v.size, Image.LANCZOS)
    v = Image.alpha_composite(v.convert("RGBA"), ov)
    save_jpg(v, "video-wyd.jpg", 86)


os.makedirs(OUT, exist_ok=True)
build_logo()
build_hero()
build_photos()
build_video()
