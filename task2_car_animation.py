# Лабораторная работа 2, задание 2
# Рихельгоф Владимир Иванович, АА-23-07
# Машинка едет по волнистой дороге туда-обратно.
# Кнопки: Нарисовать, Движение/Стоп, Сохранить рисунок (картинка нужна для задания 3)

import math
import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont

AUTHOR = "Рихельгоф Владимир Иванович, группа АА-23-07"
FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")  # картинки и результаты кладу сюда
os.makedirs(FOLDER, exist_ok=True)
PICTURE_FILE = os.path.join(FOLDER, "risunok_zadanie2.png")

W, H = 700, 420         # размер холста
CAR_W, CAR_H = 150, 82  # размер машинки
MARGIN = 10             # отступ от края
SMOKE = 40              # дым торчит левее машинки


# высота дороги в точке x (синусоида)
def road_y(x):
    return 300 + 25 * math.sin(x / 60)


# машинка: тип фигуры, координаты (от левого верхнего угла машинки), заливка, контур
CAR = [
    ("polygon", [25, 32, 45, 8, 100, 8, 120, 32], "#E53E3E", "black"),   # кабина
    ("rect",    [0, 30, 145, 62],                  "#E53E3E", "black"),   # кузов
    ("polygon", [35, 30, 50, 13, 70, 13, 70, 30],  "#BEE3F8", "black"),   # окно 1
    ("polygon", [76, 30, 76, 13, 96, 13, 110, 30], "#BEE3F8", "black"),   # окно 2
    ("oval",    [130, 36, 144, 46],                "#FAF089", "black"),   # фара
    ("oval",    [15, 50, 47, 82],                  "#2D3748", "black"),   # колесо 1
    ("oval",    [98, 50, 130, 82],                 "#2D3748", "black"),   # колесо 2
    ("oval",    [25, 60, 37, 72],                  "#A0AEC0", "black"),   # диск 1
    ("oval",    [108, 60, 120, 72],                "#A0AEC0", "black"),   # диск 2
    ("line",    [0, 56, 145, 56],                  "#2D3748", None),      # бампер
]


# дым из трубы - волнистая линия
def smoke_points():
    points = []
    for k in range(20):
        points += [-k * 2, 50 - 6 * math.sin(k / 2)]
    return points


# фон: небо, трава, солнце, дорога, подпись
def draw_scene(canvas):
    canvas.create_rectangle(0, 0, W, H, fill="#BEE3F8", outline="")
    canvas.create_rectangle(0, 330, W, H, fill="#68D391", outline="")
    for k in range(8):
        a = k * math.pi / 4
        canvas.create_line(620 + 35 * math.cos(a), 70 + 35 * math.sin(a),
                           620 + 50 * math.cos(a), 70 + 50 * math.sin(a), fill="#ED8936", width=3)
    canvas.create_oval(595, 45, 645, 95, fill="#FBD38D", outline="#ED8936", width=2)
    road = []
    for x in range(0, W + 1, 5):
        road += [x, road_y(x)]
    canvas.create_line(road, fill="#4A5568", width=6, smooth=True)
    canvas.create_text(12, H - 18, text=AUTHOR, anchor="w", fill="#1A202C", font=("Arial", 12, "bold"))


# рисует машинку, (x, y) - левый верхний угол. у всех частей тег "car"
def draw_car(canvas, x, y):
    for kind, coords, fill, outline in CAR:
        pts = [c + (x if i % 2 == 0 else y) for i, c in enumerate(coords)]
        if kind == "rect":
            canvas.create_rectangle(pts, fill=fill, outline=outline, width=2, tags="car")
        elif kind == "oval":
            canvas.create_oval(pts, fill=fill, outline=outline, width=2, tags="car")
        elif kind == "polygon":
            canvas.create_polygon(pts, fill=fill, outline=outline, width=2, tags="car")
        elif kind == "line":
            canvas.create_line(pts, fill=fill, width=3, tags="car")
    smoke = [c + (x if i % 2 == 0 else y) for i, c in enumerate(smoke_points())]
    canvas.create_line(smoke, fill="#718096", width=3, smooth=True, tags="car")


# canvas нельзя сохранить в png, поэтому рисую то же самое через PIL
def save_picture(x, y):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, H], fill="#BEE3F8")
    d.rectangle([0, 330, W, H], fill="#68D391")
    for k in range(8):
        a = k * math.pi / 4
        d.line([620 + 35 * math.cos(a), 70 + 35 * math.sin(a),
                620 + 50 * math.cos(a), 70 + 50 * math.sin(a)], fill="#ED8936", width=3)
    d.ellipse([595, 45, 645, 95], fill="#FBD38D", outline="#ED8936", width=2)
    d.line([(px, road_y(px)) for px in range(0, W + 1, 5)], fill="#4A5568", width=6, joint="curve")
    try:
        font = ImageFont.truetype("arialbd.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
    d.text((12, H - 28), AUTHOR, fill="#1A202C", font=font)
    for kind, coords, fill, outline in CAR:
        pts = [c + (x if i % 2 == 0 else y) for i, c in enumerate(coords)]
        if kind == "rect":
            d.rectangle(pts, fill=fill, outline=outline, width=2)
        elif kind == "oval":
            d.ellipse(pts, fill=fill, outline=outline, width=2)
        elif kind == "polygon":
            d.polygon(pts, fill=fill, outline=outline)
        elif kind == "line":
            d.line(pts, fill=fill, width=3)
    smoke = [c + (x if i % 2 == 0 else y) for i, c in enumerate(smoke_points())]
    d.line(smoke, fill="#718096", width=3)
    img.save(PICTURE_FILE)


class App:
    def __init__(self, root):
        self.root = root
        self.x = MARGIN + 40     # где машинка стоит в начале
        self.y = 0
        self.dx = 3              # шаг, минус - едет влево
        self.drawn = False
        self.moving = False

        root.title("Лаба 2, задание 2 - " + AUTHOR)
        root.configure(bg="#E8F1FB")
        root.resizable(False, False)

        tk.Label(root, text=AUTHOR, font=("Arial", 13, "bold"), bg="#2B5C9E", fg="white", pady=6).pack(fill="x")
        self.canvas = tk.Canvas(root, width=W, height=H, highlightthickness=3, highlightbackground="#2B5C9E")
        self.canvas.pack(padx=10, pady=10)
        draw_scene(self.canvas)

        frame = tk.Frame(root, bg="#E8F1FB")
        frame.pack(pady=(0, 10))
        tk.Button(frame, text="Нарисовать", width=14, font=("Arial", 11, "bold"),
                  bg="#2F855A", fg="white", command=self.draw).pack(side="left", padx=5)
        self.move_button = tk.Button(frame, text="Движение", width=14, font=("Arial", 11, "bold"),
                                     bg="#2B5C9E", fg="white", command=self.toggle, state="disabled")
        self.move_button.pack(side="left", padx=5)
        tk.Button(frame, text="Сохранить рисунок", width=16, font=("Arial", 11, "bold"),
                  bg="#B7791F", fg="white", command=self.save).pack(side="left", padx=5)

    # машинка стоит колесами на дороге (берем высоту дороги под серединой машинки)
    def car_y(self, x):
        return road_y(x + CAR_W / 2) - CAR_H

    def draw(self):
        self.moving = False
        self.canvas.delete("car")    # чтобы не было двух машинок
        self.y = self.car_y(self.x)
        draw_car(self.canvas, self.x, self.y)
        self.drawn = True
        self.move_button.config(state="normal", text="Движение")
        save_picture(self.x, self.y)

    def toggle(self):
        self.moving = not self.moving
        self.move_button.config(text="Стоп" if self.moving else "Движение")
        if self.moving:
            self.step()

    def step(self):
        if not self.moving:
            return
        new_x = self.x + self.dx
        # дошли до края - разворот
        if new_x < MARGIN + SMOKE or new_x > W - CAR_W - MARGIN:
            self.dx = -self.dx
            new_x = self.x + self.dx
        new_y = self.car_y(new_x)
        self.canvas.move("car", new_x - self.x, new_y - self.y)
        self.x, self.y = new_x, new_y
        self.root.after(20, self.step)

    def save(self):
        if self.drawn:
            save_picture(self.x, self.y)


window = tk.Tk()
App(window)
window.mainloop()
