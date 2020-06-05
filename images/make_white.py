import sys

from PIL import Image

# this script adds a white background to an image
if len(sys.argv) != 3:
    print("usage: " + sys.argv[0] + " [image] [output]")
    sys.exit(1)

img = Image.open(sys.argv[1]).convert('RGBA')
width, height = img.size
bg = Image.new(img.mode, img.size, (255, 255, 255))
i = Image.alpha_composite(bg, img)
i.save(sys.argv[2])
