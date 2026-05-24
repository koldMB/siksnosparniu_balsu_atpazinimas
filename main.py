import cv2
import numpy as np
import os


def nothing(x):
    pass


def get_input_with_default(text, default):
    value = input(f"{text} [{default}]: ").strip()
    if value == "":
        return default
    return int(value)


class ImageViewer:
    def __init__(self, name, img):
        self.name = name
        self.img = img

        cv2.namedWindow(name, cv2.WINDOW_NORMAL)

        cv2.createTrackbar("X", name, 0, img.shape[1], nothing)
        cv2.createTrackbar("Y", name, 0, img.shape[0], nothing)
        cv2.createTrackbar("Zoom", name, 10, 50, nothing)

    def show(self):
        while True:
            x = cv2.getTrackbarPos("X", self.name)
            y = cv2.getTrackbarPos("Y", self.name)
            z = cv2.getTrackbarPos("Zoom", self.name)

            z = max(1, z) / 10.0

            h, w = self.img.shape[:2]

            vw = max(10, int(w / z))
            vh = max(10, int(h / z))

            x = min(x, max(0, w - vw))
            y = min(y, max(0, h - vh))

            view = cv2.resize(self.img[y:y + vh, x:x + vw], (1200, 700))

            cv2.imshow(self.name, view)

            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):
                break

        cv2.destroyWindow(self.name)


def select_hsv(hsv):
    cv2.namedWindow("HSV SELECTOR")

    cv2.createTrackbar("L H", "HSV SELECTOR", 0, 180, nothing)
    cv2.createTrackbar("L S", "HSV SELECTOR", 0, 255, nothing)
    cv2.createTrackbar("L V", "HSV SELECTOR", 0, 255, nothing)

    cv2.createTrackbar("U H", "HSV SELECTOR", 180, 180, nothing)
    cv2.createTrackbar("U S", "HSV SELECTOR", 255, 255, nothing)
    cv2.createTrackbar("U V", "HSV SELECTOR", 255, 255, nothing)

    while True:
        lh = cv2.getTrackbarPos("L H", "HSV SELECTOR")
        ls = cv2.getTrackbarPos("L S", "HSV SELECTOR")
        lv = cv2.getTrackbarPos("L V", "HSV SELECTOR")

        uh = cv2.getTrackbarPos("U H", "HSV SELECTOR")
        us = cv2.getTrackbarPos("U S", "HSV SELECTOR")
        uv = cv2.getTrackbarPos("U V", "HSV SELECTOR")

        lower = np.array([lh, ls, lv])
        upper = np.array([uh, us, uv])

        mask = cv2.inRange(hsv, lower, upper)
        cv2.imshow("HSV SELECTOR", mask)

        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            return lower, upper


print("INPUT VALUES")

min_region_size = get_input_with_default("Min region size", 2)

img = cv2.imread(os.path.join(os.path.dirname(__file__), "PIPPIP.png"))

if img is None:
    print("Image not found")
    exit()

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

use_custom = input("Use HSV selector? (taip/ne): ").strip().lower()

if use_custom == "taip":
    lower, upper = select_hsv(hsv)
else:
    lower = np.array([17, 0, 248])
    upper = np.array([180, 184, 255])

mask = cv2.inRange(hsv, lower, upper)

mask = cv2.medianBlur(mask, 3)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
    mask, connectivity=8
)

h, w = mask.shape

regions = []

for i in range(1, num_labels):
    x, y, ww, hh, area = stats[i]

    if area < min_region_size:
        continue

    if ww > 0.9 * w and hh > 0.9 * h:
        continue

    regions.append((x, y, ww, hh))

print(f"Regions: {len(regions)}")

for i, (x, y, ww, hh) in enumerate(regions):
    print(f"{i+1}: x={x}, y={y}, w={ww}, h={hh}")

cv2.imwrite("BW.png", mask)

ImageViewer("BW", mask).show()