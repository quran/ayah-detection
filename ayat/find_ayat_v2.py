import cv2
import sys

# new madani
WIDTH_MIN = 60
WIDTH_MAX = 75
HEIGHT_MIN = 88
HEIGHT_MAX = 96


def find_ayat(img_rgb):
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    binarized = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(binarized.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    results = []
    selected_contours = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if WIDTH_MIN < w < WIDTH_MAX and HEIGHT_MIN < h < HEIGHT_MAX:
            is_marker = False
            for row in range(y, y + h):
                if is_marker:
                    break
                for col in range(x, x + int(h / 2)):
                    if row >= img_rgb.shape[0] or col >= img_rgb.shape[1]:
                        continue
                    (b, g, r) = img_rgb[row, col]
                    if b > 200 and g > 150 and g < 200 and r < 50:
                        is_marker = True
                        break
            if is_marker:
                results.append((x, y, w, h))
                selected_contours.append(contour)
    # cv2.imshow("image", img_rgb)
    # cv2.waitKey(0)
    return [results, selected_contours]


def draw(img_rgb, contours, output):
    for contour in contours:
        cv2.drawContours(img_rgb, [contour], -1, (240, 0, 159), 3)
    cv2.imwrite(output, img_rgb)


def main():
    if len(sys.argv) < 2:
        print("usage: " + sys.argv[0] + " image")
        sys.exit(1)

    filename = sys.argv[1]
    # filename = "new_madani/page003.png"
    img_rgb = cv2.imread(filename)
    (ayat, contours) = find_ayat(img_rgb)
    draw(img_rgb, contours, 'res.png')
    for ayah in ayat:
        (x, y, w, h) = ayah
        print("marker found at: (%d, %d) - %dx%d" % (x, y, w, h))


if __name__ == "__main__":
    main()
