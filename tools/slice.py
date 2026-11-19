import sys, os
from PIL import Image
src, out, step = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = Image.open(src).convert("RGB"); print(im.size)
base = os.path.splitext(os.path.basename(src))[0]
for i, y in enumerate(range(0, im.height, step)):
    part = im.crop((0, y, im.width, min(y + step, im.height)))
    p = os.path.join(out, "%s_%02d.jpg" % (base, i)); part.save(p, quality=88); print(p, part.size)
