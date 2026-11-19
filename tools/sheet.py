"""Lay a tall capture out as side-by-side columns so it reads in a few images."""
import sys, os
import numpy as np
from PIL import Image
src, out, step, per = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
im = Image.open(src).convert("RGB"); a = np.asarray(im)
rows = np.where((a < 250).any(axis=(1, 2)))[0]; h = int(rows.max()) + 1
print("content height", h)
im = im.crop((0, 0, im.width, h))
cols = [im.crop((0, y, im.width, min(y + step, h))) for y in range(0, h, step)]
base = os.path.splitext(os.path.basename(src))[0]
for i in range(0, len(cols), per):
    grp = cols[i:i + per]
    sheet = Image.new("RGB", (len(grp) * (im.width + 24) - 24, step), (200, 200, 200))
    for j, c in enumerate(grp): sheet.paste(c, (j * (im.width + 24), 0))
    p = os.path.join(out, "%s_sheet_%d.jpg" % (base, i // per)); sheet.save(p, quality=88); print(p, sheet.size)
