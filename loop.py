import sys
import cv2
from PIL import Image
from ayat import find_ayat, draw
from lines import find_lines


def verify_lines(image_dir, filename):
    image = Image.open(image_dir + filename).convert('RGBA')
    # warsh: 100/35/0, shamerly: 110/87/0, 175/75/1 for qaloon
    lines = find_lines(image, 175, 75, 1)
    if len(lines) is not 15:
        print('failure: found %d lines on %s' % (len(lines), filename))


def count_ayat(image_dir, filename, template_file):
    img_rgb = cv2.imread(image_dir + filename)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_file, 0)
    ayat = find_ayat(img_gray, template)
    print('found: %d in %s' % (len(ayat), filename))
    draw(img_rgb, template, ayat, 'out/' + filename)
    return ayat


def main():
    # total = 0
    image_dir = sys.argv[1] + '/'

    # warsh: 1, 560 (last page: 559)
    # shamerly: 2, 523 (last page: 522)
    # qaloon: 1, 605 (last page: 604)
    for i in range(1, 605):
        filename = str(i).zfill(3) + '.png'
        # print 'processing %s' % filename
        verify_lines(image_dir, filename)

        # ayat = count_ayat(image_dir, filename, sys.argv[2])
        # total = total + len(ayat)
    # print 'found a total of %d ayat.' % total


if __name__ == "__main__":
    main()
