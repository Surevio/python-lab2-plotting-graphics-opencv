# Лабораторная работа 2, задание 1
# Рихельгоф В.И., АА-23-07, вариант 17
# P = min(x,a)*ln(v) / корень 5 степени из |v-4|, a = 1.35
# v зависит от x (три случая), x от -2 до 4, шаг 0.5

import math
import os
import matplotlib.pyplot as plt

A = 1.35
X_START = -2.0
X_END = 4.0
H = 0.5
EPS = 1e-12

AUTHOR = "Рихельгоф В.И., группа АА-23-07, вариант 17"
FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")  # картинки и результаты кладу сюда
os.makedirs(FOLDER, exist_ok=True)


# кубический корень, чтобы работал и для отрицательных чисел
def cbrt(t):
    return math.copysign(abs(t) ** (1 / 3), t)


def v_of_x(x):
    if x <= 0.1:
        return cbrt(x + 2) + math.sin(x) ** 2
    elif x < 2:
        return A * x / (x ** 2 + 0.32)
    else:
        return math.atan(A * x / 2) ** 2


# считает v и P, если ОДЗ нарушено - ошибка
def p_of_x(x):
    v = v_of_x(x)
    if v <= 0:
        raise ValueError("ln(v) не определен, v = %.3f" % v)
    if abs(v - 4) < EPS:
        raise ValueError("деление на ноль, v = 4")
    p = min(x, A) * math.log(v) / abs(v - 4) ** (1 / 5)
    return v, p


def make_table():
    rows = []
    n = int((X_END - X_START) / H + 1e-9) + 1   # количество точек
    for k in range(n):
        x = X_START + k * H
        try:
            v, p = p_of_x(x)
            rows.append([x, v, p, None])
        except ValueError as e:
            rows.append([x, None, None, str(e)])
    return rows


def print_table(rows):
    print(AUTHOR)
    print("+------+---------+-----------+-----------+")
    print("|  N   |    x    |     v     |     P     |")
    print("+------+---------+-----------+-----------+")
    for i in range(len(rows)):
        x, v, p, err = rows[i]
        if err is None:
            print("| %4d | %7.2f | %9.4f | %9.4f |" % (i + 1, x, v, p))
        else:
            print("| %4d | %7.2f |  не определено (%s)" % (i + 1, x, err))
    print("+------+---------+-----------+-----------+")


# точки для плавной линии, каждую ветку считаем отдельно
def dense_curve():
    parts = [(X_START, 0.1), (0.1, 2.0), (2.0, X_END)]
    curves = []
    for left, right in parts:
        xs = []
        ys = []
        for k in range(301):
            x = left + (right - left) * k / 300
            if left == 0.1 and k == 0:
                x = x + 1e-6          # точка 0.1 относится к первой ветке
            if right == 2.0 and k == 300:
                x = x - 1e-6          # точка 2 относится к третьей ветке
            try:
                ys.append(p_of_x(x)[1])
            except ValueError:
                ys.append(float("nan"))
            xs.append(x)
        curves.append((xs, ys))
    return curves


def draw(rows):
    fig = plt.figure(figsize=(13, 6.8), facecolor="#EEF3FA")
    fig.suptitle("Табулирование функции P(x) - " + AUTHOR, fontsize=14, fontweight="bold", color="#1F3B66")

    ax = fig.add_axes([0.06, 0.10, 0.58, 0.78])
    ax.set_facecolor("#FFFDF5")

    colors = ["#2B6CB0", "#2F855A", "#B7791F"]
    names = ["x <= 0.1", "0.1 < x < 2", "x >= 2"]
    curves = dense_curve()
    for i in range(3):
        ax.plot(curves[i][0], curves[i][1], color=colors[i], linewidth=2.4, label="ветка " + names[i])

    # точки из таблицы и подписи значений
    xs = [r[0] for r in rows if r[3] is None]
    ps = [r[2] for r in rows if r[3] is None]
    ax.scatter(xs, ps, s=55, color="#C53030", edgecolor="white", zorder=5, label="точки таблицы")
    for i in range(len(xs)):
        if i % 2 == 0:
            dy = 14
        else:
            dy = -18
        ax.annotate("%.3f" % ps[i], (xs[i], ps[i]), textcoords="offset points", xytext=(0, dy),
                    ha="center", fontsize=8.5, color="#742A2A",
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#E2A3A3"))

    ax.axvline(0.1, color="gray", linestyle="--")
    ax.axvline(2.0, color="gray", linestyle="--")
    ax.axhline(0, color="#4A5568", linewidth=1)
    ax.set_title("График P(x) на отрезке [-2; 4]", fontsize=12, color="#1F3B66")
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("P(x)", fontsize=12)
    ax.grid(True, linestyle=":")
    ax.legend(loc="lower right", fontsize=9)

    # таблица справа от графика
    tax = fig.add_axes([0.68, 0.10, 0.30, 0.78])
    tax.axis("off")
    tax.set_title("Таблица значений", fontsize=12, color="#1F3B66")
    cells = []
    for i in range(len(rows)):
        x, v, p, err = rows[i]
        if err is None:
            cells.append([i + 1, "%.2f" % x, "%.4f" % v, "%.4f" % p])
        else:
            cells.append([i + 1, "%.2f" % x, "-", "не опр."])
    table = tax.table(cellText=cells, colLabels=["N", "x", "v", "P"], loc="upper center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.45)
    for (r, c), cell in table.get_celld().items():
        if r == 0:
            cell.set_facecolor("#2B5C9E")
            cell.set_text_props(color="white", fontweight="bold")
        elif r % 2 == 0:
            cell.set_facecolor("#EDF2F7")

    fig.savefig(os.path.join(FOLDER, "grafik_P_x.png"), dpi=120, facecolor=fig.get_facecolor())
    plt.show()


rows = make_table()
print_table(rows)
draw(rows)
