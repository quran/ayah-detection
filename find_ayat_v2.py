import cv2
import sys

# new madani
WIDTH_MIN = 60
WIDTH_MAX = 75
HEIGHT_MIN = 90
HEIGHT_MAX = 100

# warsh 1440
# WIDTH_MIN = 51
# WIDTH_MAX = 65
# HEIGHT_MIN = 79
# HEIGHT_MAX = 95


def find_ayat(img_rgb):
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    binarized = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(binarized.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    results = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if WIDTH_MIN < w < WIDTH_MAX and HEIGHT_MIN < h < HEIGHT_MAX:
            results.append((x, y, w, h))
    return results


def draw(img_rgb, ayat, output):
    for point in ayat:
        (x, y, w, h) = point
        cv2.rectangle(img_rgb, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)
    cv2.imwrite(output, img_rgb)


def main():
    if len(sys.argv) < 2:
        print("usage: " + sys.argv[0] + " image")
        sys.exit(1)

    filename = sys.argv[1]
    # filename = "new_madani/page003.png"
    img_rgb = cv2.imread(filename)
    ayat = find_ayat(img_rgb)
    draw(img_rgb, ayat, 'res.png')


if __name__ == "__main__":
    main()
