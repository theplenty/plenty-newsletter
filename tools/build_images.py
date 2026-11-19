"""Build newsletter images from the PPT's raw photos. Run: python -I tools/build_images.py <media_dir> <out_dir>"""
import sys, os
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
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

# 1) emblem: white line art on green -> ivory with alpha
src = Image.open(os.path.join(SRC, "image13.png")).convert("RGB").crop((226, 142, 340, 244))
L = np.asarray(src.convert("L")).astype(np.float32)
alpha = ((L - 78) / (205 - 78)).clip(0, 1) ** 0.85
rgba = np.zeros((src.height, src.width, 4), np.uint8)
rgba[..., :3] = IVORY
rgba[..., 3] = (alpha * 255).astype(np.uint8)
em = Image.fromarray(rgba, "RGBA")
bbox = em.getbbox(); em = em.crop(bbox)
em.save(os.path.join(OUT, "emblem.png")); print("emblem.png", em.size)

# 2) hero: the hall set for a conference, fading into the key green below
hero = Image.open(os.path.join(SRC, "image3.jpeg")).convert("RGB")
hero = cover(hero, 1280, 780, cy=0.44)
hero = grade(hero, 1.08, 0.90, 0.96)
hero = fade_to(hero, GREEN, top=0.22, top_max=1.0, bottom=0.42, bottom_max=1.0)
save_jpg(hero, "hero.jpg", 88)

# 3) space photos
for src_name, out_name, cy in (("image5.jpeg", "space-banquet.jpg", 0.5), ("image2.jpeg", "space-lobby.jpg", 0.5)):
    im = cover(Image.open(os.path.join(SRC, src_name)).convert("RGB"), 544, 408, cy=cy)
    save_jpg(grade(im), out_name)

# 4) event story photos
for src_name, out_name in (("image7.jpeg", "story-kams.jpg"), ("image9.jpeg", "story-dhp.jpg")):
    im = cover(Image.open(os.path.join(SRC, src_name)).convert("RGB"), 544, 408)
    save_jpg(grade(im), out_name)

# 5) video thumbnail: crop away the player chrome, add a quiet play mark
v = Image.open(os.path.join(SRC, "image10.png")).convert("RGB").crop((67, 8, 1269, 684))
v = v.resize((1120, 630), Image.LANCZOS)
v = grade(v, 1.04, 0.95, 0.90)
S = 4  # supersample the overlay for clean edges
ov = Image.new("RGBA", (v.width * S, v.height * S), (0, 0, 0, 0))
d = ImageDraw.Draw(ov)
cx, cy, r = 96 * S, (v.height - 96) * S, 46 * S
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GREEN + (215,), outline=IVORY + (255,), width=2 * S)
t = 17 * S
d.polygon([(cx - t * 0.55, cy - t), (cx - t * 0.55, cy + t), (cx + t * 1.05, cy)], fill=IVORY + (255,))
ov = ov.resize(v.size, Image.LANCZOS)
v = Image.alpha_composite(v.convert("RGBA"), ov)
save_jpg(v, "video-wyd.jpg", 86)
