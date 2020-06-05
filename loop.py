import sys
import cv2
from PIL import Image

from ayat.find_ayat_v2 import find_ayat, draw
from lines.lines import find_lines


def verify_lines(image_dir, filename):
    image = Image.open(image_dir + filename).convert('RGBA')
    lines = find_lines(image, 110, 35, 0)
    if len(lines) is not 15:
        print('failure: found %d lines on %s' % (len(lines), filename))


def count_ayat(image_dir, filename):
    img_rgb = cv2.imread(image_dir + filename)
    (ayat, contours) = find_ayat(img_rgb)
    print('found: %d in %s' % (len(ayat), filename))
    draw(img_rgb, contours, 'out/' + filename)
    return ayat


def main():
    total = 0
    image_dir = sys.argv[1] + '/'
    prefix = 'page'

    for i in range(1, 605):
        filename = prefix + str(i).zfill(3) + '.jpg'
        print('processing %s' % filename)
        verify_lines(image_dir, filename)

        ayat = count_ayat(image_dir, filename)
        total = total + len(ayat)
    print('found a total of %d ayat.' % total)


if __name__ == "__main__":
    main()
