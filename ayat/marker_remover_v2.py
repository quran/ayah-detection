import sys
import cv2
import numpy as np

from find_ayat_v2 import find_ayat


def remove_markers(rgb_filename, gray_filename, output):
    img_rgb = cv2.imread(rgb_filename)
    (ayat, contours) = find_ayat(img_rgb)
    mask = np.ones(img_rgb.shape[:2], dtype="uint8") * 255
    cv2.drawContours(mask, contours, -1, 0, -1)
    cv2.drawContours(mask, contours, -1, 0, 2)
    # cv2.imshow("mask", mask)
    # cv2.waitKey(0)

    img_gray = cv2.imread(gray_filename, flags=cv2.IMREAD_UNCHANGED)
    img_gray = cv2.bitwise_and(img_gray, img_gray, mask=mask)
    # cv2.imshow("image", img_gray)
    # cv2.waitKey(0)

    print(output)
    cv2.imwrite(output, img_gray)


def main():
    rgb_filename = sys.argv[1]
    gray_filename = sys.argv[2]
    output = sys.argv[3]
    remove_markers(rgb_filename, gray_filename, output)


if __name__ == "__main__":
    main()
