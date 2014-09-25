import sys
import cv2
from PIL import Image
from lines import find_lines, draw
from ayat import find_ayat

# warsh: 1, 560 (last page: 559)
# shamerly: 2, 523 (last page: 522)
# qaloon: 1, 605 (last page: 604)
for i in range(2, 523):
   filename = str(i).zfill(3) + '.png'

   # find lines
   image = Image.open(sys.argv[1] + '/' + filename).convert('RGBA')

   # note: these values will change depending on image type and size
   # warsh: 100/35/False, shamerly: 110/87/False, 175/75/True for qaloon
   lines = find_lines(image, 110, 87, False)
   print 'found: %d lines on page %d' % (len(lines), i)
   draw(image, lines, 'out/' + filename)
