import os
import sys

import cv2
from PIL import Image

from ayat import find_ayat

DEBUG = False
MARKER_EMPTY_TOP = 4
MARKER_EMPTY_BOTTOM = 3


def marker_lengths(marker_img):
    pixels = marker_img.load()
    result = {}
    for row in range(MARKER_EMPTY_TOP, marker_img.size[1] - MARKER_EMPTY_BOTTOM):
        least = -1
        for col in range(marker_img.size[0]):
            (red, green, blue, alpha) = pixels[col, row]
            if red == 0 and green == 0 and blue == 0:
                least = col
                break

        most = -1
        for col in range(marker_img.size[0] - 1, 0, -1):
            (red, green, blue, alpha) = pixels[col, row]
            if red == 0 and green == 0 and blue == 0:
                most = col
                break

        result[row] = (least, most)

    for row in range(0, MARKER_EMPTY_TOP):
        result[row] = result[MARKER_EMPTY_TOP]
    for row in range(marker_img.size[1] - MARKER_EMPTY_BOTTOM, marker_img.size[1]):
        result[row] = result[MARKER_EMPTY_BOTTOM]
    return result


def remove_markers(template_marker_lengths, img, ayat, output):
    pixels = img.load()
    for ayah in ayat:
        x = int(ayah[0])
        y = int(ayah[1])

        min_y = y
        max_y = min_y + len(template_marker_lengths)
        actual_height = max_y - min_y
        template_height = len(template_marker_lengths)
        start_offset = template_height - actual_height

        for row in range(min_y, max_y):
            if start_offset < 0:
                (min_x, max_x) = template_marker_lengths[0]
            else:
                (min_x, max_x) = template_marker_lengths[start_offset]
                if start_offset > 0:
                    (last_min_x, last_max_x) = template_marker_lengths[start_offset - 1]
                    (min_x, max_x) = min(last_min_x, min_x), max(last_max_x, max_x)
                    if start_offset > 1:
                        (last_min_x, last_max_x) = template_marker_lengths[start_offset - 2]
                        (min_x, max_x) = min(last_min_x, min_x), max(last_max_x, max_x)

            for col in range(x + min_x - 1, x + max_x + 2):
                pixels[col, row] = (0, 0, 0, 0)
            start_offset = start_offset + 1

    if DEBUG:
        img.show()

    img.save(output)


def main():
    rgb_image_filename = sys.argv[1]
    template_filename = sys.argv[2]
    bw_template_path = sys.argv[3]
    image_path = sys.argv[4]
    # rgb_image_filename = "/Users/ahmedre/Desktop/warsh/page264.jpg"
    # template_filename = "images/templates/warsh/1440_template.png"
    # bw_template_path = "bw_warsh_template.jpg"
    # image_path = 'images/warsh/page264.png'

    img_rgb = cv2.imread(rgb_image_filename)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_filename, 0)
    ayat = find_ayat(img_gray, template)
    if len(ayat) == 0:
        print("no matches for %s" % rgb_image_filename)
        return

    bw_template = Image.open(bw_template_path).convert('RGBA')
    template_marker_lengths = marker_lengths(bw_template)

    image = Image.open(image_path).convert('RGBA')

    output_directory = "no_markers"
    if len(sys.argv) > 5:
        output_directory = sys.argv[5]
    os.makedirs(output_directory, exist_ok=True)

    # for debugging, can just hardcode image_path above and coordinates here
    # instead of doing the actual ayah detection.
    # ayat = [(203.5, 443.5), (894.5, 971.5), (1009.0, 1235.0), (172.0, 1224.5), (497.0, 1500.5), (41.0, 1896.5)]
    remove_markers(template_marker_lengths, image, ayat, os.path.join(output_directory, os.path.basename(image_path)))


if __name__ == "__main__":
    main()
