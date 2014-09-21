import sys
import cv2
from PIL import Image
from lines import find_lines
from ayat import find_ayat

if False:
# find lines
   image = Image.open(sys.argv[1]).convert('RGBA')

# note: these values will change depending on image type and size
# warsh: 100/20/False, shamerly: 110/50/False, 175/75/True for qaloon
   lines = find_lines(image, 100, 20, False)
   for line in lines:
         print line

# find ayat
img_rgb = cv2.imread(sys.argv[1])
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread(sys.argv[2], 0)
ayat = find_ayat(img_gray, template)
print 'found: %d' % len(ayat)
