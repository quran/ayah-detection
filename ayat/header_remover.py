import os
import sys

import cv2
from PIL import Image

from ayat import find_ayat

HEIGHT = 142
WIDTH = 392
TOP_BOTTOM_PIECE_HEIGHT = 12
DEBUG = False


def remove_markers(img, left, right, output):
    pixels = img.load()
    count = len(left)
    for i in range(0, count):
        header = left[i]
        right_header = right[i]

        x = int(header[0])
        y = int(header[1])

        rx = int(right_header[0])
        ry = int(right_header[1])

        for row in range(y, y + HEIGHT):
            for col in range(x, x + WIDTH):
                pixels[col, row] = (0, 0, 0, 0)
        for row in range(ry, ry + HEIGHT):
            for col in range(rx, rx + WIDTH):
                pixels[col, row] = (0, 0, 0, 0)
        for row in range(y, y + TOP_BOTTOM_PIECE_HEIGHT):
            for col in range(x, rx):
                pixels[col, row] = (0, 0, 0, 0)
        for row in range(y + HEIGHT - TOP_BOTTOM_PIECE_HEIGHT, y + HEIGHT):
            for col in range(x, rx):
                pixels[col, row] = (0, 0, 0, 0)

    if DEBUG:
        img.show()

    img.save(output)


def main():
    rgb_image_filename = sys.argv[1]
    left_template_filename = sys.argv[2]
    right_template_filename = sys.argv[3]
    image_path = sys.argv[4]

    # page = "520"
    # rgb_image_filename = "/Users/ahmedre/Desktop/warsh/page%s.jpg" % page
    # left_template_filename = "/Users/ahmedre/Desktop/left.jpg"
    # right_template_filename = "/Users/ahmedre/Desktop/right.jpg"
    # image_path = 'no_markers/page%s.png' % page

    img_rgb = cv2.imread(rgb_image_filename)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(left_template_filename, 0)
    left = find_ayat(img_gray, template, 0.75)
    template = cv2.imread(right_template_filename, 0)
    right = find_ayat(img_gray, template, 0.75)

    image = Image.open(image_path).convert('RGBA')

    output_directory = "no_markers"
    if len(sys.argv) > 5:
        output_directory = sys.argv[5]
    os.makedirs(output_directory, exist_ok=True)

    # for debugging, can just hardcode image_path above and coordinates here
    # instead of doing the actual ayah detection.
    # ayat = [(203.5, 443.5)]
    if len(left) > 0 or len(right) > 0:
        print("processing %s" % image_path)
        remove_markers(image, left, right, os.path.join(output_directory, os.path.basename(image_path)))


if __name__ == "__main__":
    main()
