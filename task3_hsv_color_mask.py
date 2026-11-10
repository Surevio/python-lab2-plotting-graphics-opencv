# Лабораторная работа 2, задание 3
# Рихельгоф В.И., АА-23-07
# Обработка рисунка из задания 2 (risunok_zadanie2.png):
# серый, BGR -> HSV, диапазон цвета ползунками, маска, наложение маски
# s - сохранить, q или Esc - сохранить и выйти

import os
import cv2
import numpy as np

FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")  # картинки и результаты кладу сюда
os.makedirs(FOLDER, exist_ok=True)
PICTURE_FILE = os.path.join(FOLDER, "risunok_zadanie2.png")

# по умолчанию красный (кузов машинки). в opencv H от 0 до 179, S и V от 0 до 255
DEFAULT_LOW = (0, 120, 100)
DEFAULT_HIGH = (8, 255, 255)

# окна называю латиницей, русские названия opencv показывает кракозябрами
WIN_SLIDERS = "Sliders"
WINDOWS = ["1 Original", "2 Gray", "3 HSV", "4 Mask", "5 Result"]


# cv2.imread не открывает путь с русскими буквами, поэтому так
def read_image(path):
    data = np.fromfile(path, dtype=np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def write_image(path, image):
    ok, buf = cv2.imencode(".png", image)
    if ok:
        buf.tofile(path)


def process(img, low, high):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)          # оттенки серого
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)            # BGR -> HSV
    lower = np.array(low, dtype=np.uint8)                 # нижняя граница цвета
    upper = np.array(high, dtype=np.uint8)                # верхняя граница цвета
    mask = cv2.inRange(hsv, lower, upper)                 # маска: в диапазоне белое, остальное черное
    result = cv2.bitwise_and(img, img, mask=mask)         # вырезаем нужный цвет из оригинала
    return gray, hsv, mask, result


def save_results(gray, hsv, mask, result, low, high):
    write_image(os.path.join(FOLDER, "rez_1_gray.png"), gray)
    write_image(os.path.join(FOLDER, "rez_2_hsv.png"), hsv)
    write_image(os.path.join(FOLDER, "rez_3_mask.png"), mask)
    write_image(os.path.join(FOLDER, "rez_4_result.png"), result)
    white = cv2.countNonZero(mask)
    total = mask.shape[0] * mask.shape[1]
    f = open(os.path.join(FOLDER, "rez_hsv_diapazon.txt"), "w", encoding="utf-8")
    f.write("Лаба 2, задание 3, Рихельгоф В.И., АА-23-07\n")
    f.write("Нижняя граница HSV: H=%d, S=%d, V=%d\n" % low)
    f.write("Верхняя граница HSV: H=%d, S=%d, V=%d\n" % high)
    f.write("Белых пикселей в маске: %d из %d (%.2f%%)\n" % (white, total, 100 * white / total))
    f.close()
    print("Сохранено:", low, high)


def nothing(x):
    pass


if not os.path.exists(PICTURE_FILE):
    print("Нет файла", PICTURE_FILE)
    print("Сначала запустите task2_car_animation.py и нажмите Нарисовать")
    exit()

img = read_image(PICTURE_FILE)
print("Двигайте ползунки в окне Sliders. s - сохранить, q или Esc - выход")

h, w = img.shape[:2]
for k in range(len(WINDOWS)):
    cv2.namedWindow(WINDOWS[k], cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOWS[k], w // 2, h // 2)
    cv2.moveWindow(WINDOWS[k], 10 + (k % 3) * (w // 2 + 10), 10 + (k // 3) * (h // 2 + 40))

cv2.namedWindow(WIN_SLIDERS, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WIN_SLIDERS, w // 2, 300)
cv2.moveWindow(WIN_SLIDERS, 10 + 2 * (w // 2 + 10), 10 + h // 2 + 40)
cv2.createTrackbar("H min", WIN_SLIDERS, DEFAULT_LOW[0], 179, nothing)
cv2.createTrackbar("H max", WIN_SLIDERS, DEFAULT_HIGH[0], 179, nothing)
cv2.createTrackbar("S min", WIN_SLIDERS, DEFAULT_LOW[1], 255, nothing)
cv2.createTrackbar("S max", WIN_SLIDERS, DEFAULT_HIGH[1], 255, nothing)
cv2.createTrackbar("V min", WIN_SLIDERS, DEFAULT_LOW[2], 255, nothing)
cv2.createTrackbar("V max", WIN_SLIDERS, DEFAULT_HIGH[2], 255, nothing)

while True:
    low = (cv2.getTrackbarPos("H min", WIN_SLIDERS),
           cv2.getTrackbarPos("S min", WIN_SLIDERS),
           cv2.getTrackbarPos("V min", WIN_SLIDERS))
    high = (cv2.getTrackbarPos("H max", WIN_SLIDERS),
            cv2.getTrackbarPos("S max", WIN_SLIDERS),
            cv2.getTrackbarPos("V max", WIN_SLIDERS))
    gray, hsv, mask, result = process(img, low, high)

    cv2.imshow(WINDOWS[0], img)
    cv2.imshow(WINDOWS[1], gray)
    cv2.imshow(WINDOWS[2], hsv)
    cv2.imshow(WINDOWS[3], mask)
    cv2.imshow(WINDOWS[4], result)

    key = cv2.waitKey(50) & 0xFF
    if key == ord("s"):
        save_results(gray, hsv, mask, result, low, high)
    # выход по q, Esc или если закрыли окно с ползунками
    if key == ord("q") or key == 27 or cv2.getWindowProperty(WIN_SLIDERS, cv2.WND_PROP_VISIBLE) < 1:
        save_results(gray, hsv, mask, result, low, high)
        break

cv2.destroyAllWindows()
