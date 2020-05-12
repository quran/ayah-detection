from PIL import Image
import numpy as np
import sys

# this script is from http://stackoverflow.com/questions/5365589
# it converts a white background to be transparent
if len(sys.argv) != 3:
    print("usage: " + sys.argv[0] + " [image] [output]")
    sys.exit(1)

# split the number into r, g, b
# threshold is how high each of r/g/b must be considered to
# remove it (keeping in mind that white is 255).
threshold = 200

# in theory, lowering dist ensures more gray colors
# are eliminated - but in practice, i found that ignoring
# the dist parameter returned better results.
dist = 5
use_dist = False

img = Image.open(sys.argv[1]).convert('RGBA')
# np.asarray(img) is read only. Wrap it in np.array to make it modifiable.
arr = np.array(np.asarray(img))
r, g, b, a = np.rollaxis(arr, axis=-1)
mask = ((r > threshold)
        & (g > threshold)
        & (b > threshold))
if use_dist:
    mask = (mask
            & (np.abs(r - g) < dist)
            & (np.abs(r - b) < dist)
            & (np.abs(g - b) < dist))
arr[mask, 3] = 0
img = Image.fromarray(arr, mode='RGBA')
img.save(sys.argv[2])
