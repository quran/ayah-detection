import cv2
import sys
import numpy as np


# heavily based on the "template matching" tutorial for opencv python

def is_x_in_range(x_range, pt):
    if x_range[0] <= pt[0] <= x_range[1]:
        return True, False
    elif pt[0] >= x_range[0] and pt[0] - x_range[1] < 10:
        return True, True
    elif pt[0] <= x_range[1] and x_range[0] - pt[0] < 10:
        return True, True
    return False, False


def is_y_in_range(y_range, pt):
    if y_range[0] <= pt[1] <= y_range[1]:
        return True, False
    elif pt[1] >= y_range[0] and pt[1] - y_range[1] < 10:
        return True, True
    elif pt[1] <= y_range[1] and y_range[1] - pt[1] < 10:
        return True, True
    return False, False


def process(ayat):
    result = []
    cur_y = ayat[0][1]
    same_line = []
    for ayah in ayat:
        if abs(ayah[1] - cur_y) < 20:
            same_line.append(ayah)
        else:
            same_line.sort(key=lambda tup: tup[0])
            for s in same_line[::-1]:
                result.append(s)
            cur_y = ayah[1]
            same_line = [ayah]

    same_line.sort(key=lambda tup: tup[0])
    for s in same_line[::-1]:
        result.append(s)
    return result


def find_ayat(img_gray, template, threshold=0.5):
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    points = list(zip(*loc[::-1]))
    ayat = []
    if len(points) == 0:
        return ayat

    extras = []
    x_range = (points[0][0], points[0][0])
    y_range = (points[0][1], points[0][1])
    actual_y_range = y_range

    for pt in points:
        x_in_range, should_expand_x = is_x_in_range(x_range, pt)
        y_in_range, should_expand_y = is_y_in_range(y_range, pt)

        if x_in_range and y_in_range:
            if should_expand_x:
                x_range = (min(pt[0], x_range[0]), max(pt[0], x_range[1]))
            if should_expand_y:
                y_range = (min(pt[1], y_range[0]), max(pt[1], y_range[1]))
                actual_y_range = y_range
        elif y_in_range:
            # more than one ayah lives on this line
            added = False
            for i in range(0, len(extras)):
                e = extras[i]
                in_range, expand_x = is_x_in_range(e, pt)
                if in_range:
                    if expand_x:
                        extras[i] = (min(e[0], pt[0]), max(pt[0], e[1]), e[2], e[3])
                    in_y_range, expand_y = is_y_in_range(e, pt)
                    if expand_y:
                        extras[i] = (e[0], e[1], min(e[2], pt[1]), max(e[3], pt[1]))
                    added = True
                    break
            if not added:
                extras.append((pt[0], pt[0], pt[1], pt[1]))
            if should_expand_y:
                y_range = (min(pt[1], y_range[0]), max(pt[1], y_range[1]))
        else:
            x_avg = (x_range[0] + x_range[1]) / 2
            y_avg = (actual_y_range[0] + actual_y_range[1]) / 2
            ayat.append((x_avg, y_avg))
            x_range = (pt[0], pt[0])
            y_range = (pt[1], pt[1])
            actual_y_range = y_range
            for e in extras:
                e_x_avg = (e[0] + e[1]) / 2
                e_y_avg = (e[2] + e[3]) / 2
                ayat.append((e_x_avg, e_y_avg))
            extras = []

    y_avg = (actual_y_range[0] + actual_y_range[1]) / 2
    ayat.append(((x_range[1] + x_range[0]) / 2, y_avg))
    for e in extras:
        e_x_avg = (e[0] + e[1]) / 2
        e_y_avg = (e[2] + e[3]) / 2
        ayat.append((e_x_avg, e_y_avg))
    return process(ayat)


def draw(img_rgb, template, ayat, output):
    w, h = template.shape[::-1]
    for point in ayat:
        pt = (int(point[0]), int(point[1]))
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), thickness=2)
    cv2.imwrite(output, img_rgb)


def main():
    if len(sys.argv) < 3:
        print("usage: " + sys.argv[0] + " image template")
        sys.exit(1)

    img_rgb = cv2.imread(sys.argv[1])
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(sys.argv[2], 0)
    ayat = find_ayat(img_gray, template)
    for ayah in ayat:
        print(ayah)
    draw(img_rgb, template, ayat, 'res.png')


if __name__ == "__main__":
    main()
