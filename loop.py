import sys
import cv2
from PIL import Image
from ayat import find_ayat, draw

total = 0
image_dir = sys.argv[1]

# warsh: 1, 560 (last page: 559)
# shamerly: 2, 523 (last page: 522)
for i in range(1, 560):
   filename = str(i).zfill(3) + '.png'
   img_rgb = cv2.imread(image_dir + '/' + filename)
   img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
   template = cv2.imread(sys.argv[2], 0)
   ayat = find_ayat(img_gray, template)
   print 'found: %d in page %d' % (len(ayat), i)
   total = total + len(ayat)
   draw(img_rgb, template, ayat, 'out/' + filename)
print 'found a total of %d ayat.' % total
