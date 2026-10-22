#!/usr/bin/env python3
"""
ໂປຣແກຣມສ້າງໂຈດຟີຊິກ (ພ້ອມຮູບປະກອບ ແລະ ເເນວທາງແກ້)
  1) ການເຄື່ອນທີ່ຊື່ສະໝໍ່າສະເໝີ         (Uniform motion)
  2) ການເຄື່ອນທີ່ຊື່ປ່ຽນແປງສະໝໍ່າສະເໝີ  (Uniformly accelerated motion)
  3) ການຕົກຕາມລໍາພັງ                     (Free fall)

ວິທີໃຊ້:
    pip install matplotlib numpy
    python physics_generator.py                 # ຢ່າງລະ 3 ຂໍ້
    python physics_generator.py -n 5 --seed 1   # ຢ່າງລະ 5 ຂໍ້, ໃຊ້ seed ເພື່ອໃຫ້ໄດ້ຊຸດເດີມ

ຜົນລັບ: ໂຟນເດີ output/ ມີ problems.html ແລະ ຮູບ PNG ທັງໝົດ
ໝາຍເຫດ: ຄ່າ g = 10 m/s²  (ປ່ຽນໄດ້ທີ່ຕົວແປ G)
"""
import argparse
import html
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

G = 10  # ຄວາມເລັ່ງຍ້ອນແຮງໂນ້ມຖ່ວງ (m/s²)
OUT = "output"

# ຕົວອັກສອນໃນຮູບໃຊ້ສັນຍາລັກເທົ່ານັ້ນ (v, a, t, s) ເພື່ອບໍ່ໃຫ້ຕິດບັນຫາຟອນລາວ
plt.rcParams.update({"font.size": 11, "axes.grid": True, "grid.alpha": 0.3})


def fmt(x):
    """ຈັດຮູບແບບຕົວເລກ: ຕັດ .0 ອອກ"""
    return f"{x:.2f}".rstrip("0").rstrip(".")


def arrow(ax, p1, p2, color="k", style="-|>", lw=1.6, ls="-"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=14,
                                 color=color, lw=lw, linestyle=ls))


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    return name


# ----------------------------------------------------------------------
# 1) ການເຄື່ອນທີ່ຊື່ສະໝໍ່າສະເໝີ
# ----------------------------------------------------------------------
def uniform_motion(idx):
    v = random.choice(range(5, 31, 5))      # m/s
    t = random.choice(range(4, 21, 2))      # s
    s = v * t
    kind = random.choice(["s", "t"])

    if kind == "s":
        q = (f"ລົດຄັນໜຶ່ງແລ່ນດ້ວຍຄວາມໄວຄົງທີ່ {v} m/s ເປັນເວລາ {t} s. "
             f"ຈົງຄິດໄລ່ໄລຍະທາງທີ່ລົດແລ່ນໄດ້ ແລະ ແຕ້ມກຣາຟ s–t.")
        sol = [f"ໃຊ້ສູດ s = v·t",
               f"s = {v} × {t} = {s} m"]
        ans = f"s = {s} m"
        label_s, label_t = f"s = ?", f"t = {t} s"
    else:
        q = (f"ລົດຄັນໜຶ່ງແລ່ນດ້ວຍຄວາມໄວຄົງທີ່ {v} m/s ແລ່ນໄດ້ໄລຍະທາງ {s} m. "
             f"ຈົ່ງຄິດໄລ່ເວລາທີ່ໃຊ້ ແລະ ແຕ້ມກຣາຟ s–t.")
        sol = [f"ໃຊ້ສູດ s = v·t  ⇒  t = s / v",
               f"t = {s} / {v} = {t} s"]
        ans = f"t = {t} s"
        label_s, label_t = f"s = {s} m", "t = ?"

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.4),
                                 gridspec_kw={"width_ratios": [1.3, 1]})
    # ຮູບທີ 1: ລົດເທິງຖະໜົນ
    a1.set_xlim(0, 10); a1.set_ylim(0, 3.2); a1.axis("off")
    a1.add_patch(Rectangle((0, 0.9), 10, 0.15, color="gray"))
    a1.add_patch(Rectangle((6.2, 1.05), 1.8, 0.5, color="tab:blue"))
    a1.add_patch(Rectangle((6.6, 1.55), 1.0, 0.35, color="tab:blue"))
    for cx in (6.7, 7.5):
        a1.add_patch(Circle((cx, 1.05), 0.18, color="black"))
    a1.add_patch(Rectangle((0.8, 1.05), 1.8, 0.5, color="lightblue", alpha=0.6))
    a1.add_patch(Rectangle((1.2, 1.55), 1.0, 0.35, color="lightblue", alpha=0.6))
    arrow(a1, (8.2, 1.35), (9.6, 1.35), "tab:red")
    a1.text(8.9, 1.55, f"v = {v} m/s", ha="center", color="tab:red")
    arrow(a1, (1.7, 0.55), (7.1, 0.55), "k", "<|-|>")
    a1.text(4.4, 0.15, label_s, ha="center", fontsize=12)
    a1.text(4.4, 2.5, label_t, ha="center", fontsize=12)
    a1.set_title("ໂຈດຂໍ້ " + str(idx), fontsize=1, color="white")

    # ຮູບທີ 2: ກຣາຟ s–t
    tt = np.linspace(0, t * 1.2, 50)
    a2.plot(tt, v * tt, color="tab:blue", lw=2)
    a2.plot([t], [s], "ro")
    a2.plot([t, t], [0, s], "r--", lw=1); a2.plot([0, t], [s, s], "r--", lw=1)
    a2.set_xlabel("t (s)"); a2.set_ylabel("s (m)")
    a2.set_title("s–t graph (straight line, slope = v)")
    return dict(q=q, sol=sol, ans=ans, img=save(fig, f"uniform_{idx}.png"))


# ----------------------------------------------------------------------
# 2) ການເຄື່ອນທີ່ຊື່ປ່ຽນແປງສະໝໍ່າສະເໝີ
# ----------------------------------------------------------------------
def accelerated_motion(idx):
    u = random.choice(range(0, 21, 5))      # m/s
    a = random.choice([2, 3, 4, 5])         # m/s²
    t = random.choice(range(3, 11))         # s
    v = u + a * t
    s = u * t + a * t * t / 2

    q = (f"ລົດເລີ່ມຕົ້ນດ້ວຍຄວາມໄວ {u} m/s ແລ້ວເລັ່ງຄົງທີ່ {a} m/s² ເປັນເວລາ {t} s. "
         f"ຈົ່ງຄິດໄລ່ (ກ) ຄວາມໄວສຸດທ້າຍ  (ຂ) ໄລຍະທາງທີ່ແລ່ນໄດ້  "
         f"ແລະ ແຕ້ມກຣາຟ v–t.")
    sol = ["(ກ) ໃຊ້ສູດ v = u + a·t",
           f"v = {u} + {a}×{t} = {v} m/s",
           "(ຂ) ໃຊ້ສູດ s = u·t + ½·a·t²",
           f"s = {u}×{t} + ½×{a}×{t}² = {fmt(s)} m",
           "ກວດຄືນ: s = (u+v)/2 · t = "
           f"({u}+{v})/2 × {t} = {fmt((u + v) / 2 * t)} m"]
    ans = f"v = {v} m/s,  s = {fmt(s)} m"

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.4),
                                 gridspec_kw={"width_ratios": [1.3, 1]})
    # ຮູບທີ 1: ຈຸດ 3 ຕໍາແໜ່ງ ຄວາມໄວເພີ່ມຂຶ້ນ
    a1.set_xlim(0, 11); a1.set_ylim(0, 3); a1.axis("off")
    a1.add_patch(Rectangle((0, 1.0), 11, 0.12, color="gray"))
    ts = [0, t / 2, t]
    xs = [0.8, 0.8 + 8.4 * (u * t / 2 + a * (t / 2) ** 2 / 2) / s if s else 0.8, 9.0]
    for k, (ti, x) in enumerate(zip(ts, xs)):
        vi = u + a * ti
        a1.add_patch(Rectangle((x - 0.45, 1.12), 0.9, 0.4, color="tab:blue", alpha=0.35 + 0.3 * k))
        for dx in (-0.25, 0.25):
            a1.add_patch(Circle((x + dx, 1.12), 0.12, color="black"))
        L = 0.3 + 0.9 * (vi / max(v, 1))
        arrow(a1, (x, 1.8), (x + L, 1.8), "tab:red")
        a1.text(x, 2.1, f"t={fmt(ti)} s", ha="center", fontsize=9)
        a1.text(x + L / 2, 1.88, f"{fmt(vi)}", ha="center", fontsize=9, color="tab:red")
    a1.text(5, 0.45, f"a = {a} m/s² (constant)", ha="center", fontsize=12)

    # ຮູບທີ 2: ກຣາຟ v–t ພ້ອມພື້ນທີ່ = ໄລຍະທາງ
    tt = np.linspace(0, t, 50)
    a2.plot(tt, u + a * tt, color="tab:blue", lw=2)
    a2.fill_between(tt, 0, u + a * tt, alpha=0.2, color="tab:blue")
    a2.text(t / 2, (u + v) / 4, f"area = s = {fmt(s)} m", ha="center")
    a2.set_xlabel("t (s)"); a2.set_ylabel("v (m/s)")
    a2.set_title("v–t graph (slope = a)")
    a2.set_xlim(0, t * 1.05); a2.set_ylim(0, v * 1.15)
    return dict(q=q, sol=sol, ans=ans, img=save(fig, f"accel_{idx}.png"))


# ----------------------------------------------------------------------
# 3) ການຕົກຕາມລໍາພັງ
# ----------------------------------------------------------------------
def free_fall(idx):
    kind = random.choice(["drop", "up"])
    if kind == "drop":
        t = random.choice([1, 2, 3, 4, 5])
        h = G * t * t / 2
        v = G * t
        q = (f"ປ່ອຍກ້ອນຫີນຕົກຈາກຕຶກສູງ {fmt(h)} m ໂດຍບໍ່ມີຄວາມໄວຕົ້ນ (g = {G} m/s², ບໍ່ຄິດຄວາມຕ້ານທານອາກາດ). "
             f"ຈົ່ງຄິດໄລ່ (ກ) ເວລາທີ່ກ້ອນຫີນຕົກເຖິງພື້ນ  (ຂ) ຄວາມໄວກ່ອນກະທົບພື້ນ.")
        sol = ["(ກ) ໃຊ້ສູດ h = ½·g·t²  ⇒  t = √(2h/g)",
               f"t = √(2×{fmt(h)}/{G}) = {t} s",
               "(ຂ) ໃຊ້ສູດ v = g·t",
               f"v = {G}×{t} = {v} m/s"]
        ans = f"t = {t} s,  v = {v} m/s"

        fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4.4),
                                     gridspec_kw={"width_ratios": [1, 1.2]})
        a1.set_xlim(0, 6); a1.set_ylim(-0.6, 6); a1.axis("off")
        a1.add_patch(Rectangle((0.3, 0), 2.0, 5.0, color="lightgray"))
        a1.add_patch(Rectangle((0, -0.3), 6, 0.3, color="saddlebrown"))
        a1.add_patch(Circle((2.8, 5.2), 0.2, color="dimgray"))
        arrow(a1, (4.0, 5.1), (4.0, 0.2), "k", "<|-|>")
        a1.text(4.2, 2.6, f"h = {fmt(h)} m", fontsize=12, va="center")
        arrow(a1, (2.8, 4.8), (2.8, 3.6), "tab:red")
        a1.text(3.0, 4.2, "g", color="tab:red", fontsize=13)
        a1.text(1.6, 5.35, "v₀ = 0", ha="center")
        tt = np.linspace(0, t, 50)
        a2.plot(tt, G * tt, color="tab:blue", lw=2)
        a2.fill_between(tt, 0, G * tt, alpha=0.2)
        a2.text(t * 0.6, G * t * 0.25, f"area = h = {fmt(h)} m", ha="center")
        a2.set_xlabel("t (s)"); a2.set_ylabel("v (m/s)")
        a2.set_title("v–t graph (free fall)")
    else:
        v0 = random.choice([10, 20, 30, 40])
        t_up = v0 / G
        H = v0 ** 2 / (2 * G)
        T = 2 * t_up
        q = (f"ໂຍນລູກບານຂຶ້ນເທິງຕາມແນວຕັ້ງດ້ວຍຄວາມໄວຕົ້ນ {v0} m/s (g = {G} m/s², ບໍ່ຄິດຄວາມຕ້ານທານອາກາດ). "
             f"ຈົ່ງຄິດໄລ່ (ກ) ເວລາທີ່ລູກບານຂຶ້ນເຖິງຈຸດສູງສຸດ  (ຂ) ຄວາມສູງສູງສຸດ  "
             f"(ຄ) ເວລາທັງໝົດຈົນກັບມາຈຸດເດີມ.")
        sol = ["(ກ) ທີ່ຈຸດສູງສຸດ v = 0, ໃຊ້ v = v₀ − g·t",
               f"t = v₀/g = {v0}/{G} = {fmt(t_up)} s",
               "(ຂ) ໃຊ້ສູດ v² = v₀² − 2·g·H",
               f"H = v₀²/(2g) = {v0}²/(2×{G}) = {fmt(H)} m",
               "(ຄ) ເວລາຂຶ້ນ = ເວລາລົງ",
               f"T = 2×{fmt(t_up)} = {fmt(T)} s"]
        ans = f"t = {fmt(t_up)} s,  H = {fmt(H)} m,  T = {fmt(T)} s"

        fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4.4),
                                     gridspec_kw={"width_ratios": [1, 1.2]})
        a1.set_xlim(0, 6); a1.set_ylim(-0.6, 6); a1.axis("off")
        a1.add_patch(Rectangle((0, -0.3), 6, 0.3, color="saddlebrown"))
        a1.add_patch(Circle((2.0, 0.2), 0.2, color="tab:orange"))
        arrow(a1, (2.0, 0.6), (2.0, 2.0), "tab:red")
        a1.text(2.2, 1.3, f"v₀ = {v0} m/s", color="tab:red")
        a1.plot([2.0, 2.0], [2.2, 5.0], "k:", lw=1)
        a1.add_patch(Circle((2.0, 5.2), 0.2, color="tab:orange", alpha=0.5))
        a1.text(2.4, 5.2, "v = 0", va="center")
        arrow(a1, (4.2, 0.2), (4.2, 5.2), "k", "<|-|>")
        a1.text(4.4, 2.7, "H = ?", fontsize=12)
        arrow(a1, (0.8, 4.6), (0.8, 3.6), "tab:red")
        a1.text(0.4, 4.1, "g", color="tab:red", fontsize=13)
        tt = np.linspace(0, T, 100)
        a2.plot(tt, v0 - G * tt, color="tab:blue", lw=2)
        a2.axhline(0, color="k", lw=0.8)
        a2.fill_between(tt, 0, v0 - G * tt, where=(v0 - G * tt) >= 0, alpha=0.2, color="tab:green")
        a2.fill_between(tt, 0, v0 - G * tt, where=(v0 - G * tt) <= 0, alpha=0.2, color="tab:red")
        a2.plot([t_up], [0], "ko")
        a2.set_xlabel("t (s)"); a2.set_ylabel("v (m/s)")
        a2.set_title("v–t graph (up = +)")
    return dict(q=q, sol=sol, ans=ans, img=save(fig, f"freefall_{idx}.png"))


# ----------------------------------------------------------------------
# ສ້າງໄຟລ໌ HTML
# ----------------------------------------------------------------------
SECTIONS = [
    ("ບົດທີ 1: ການເຄື່ອນທີ່ຊື່ສະໝໍ່າສະເໝີ", uniform_motion),
    ("ບົດທີ 2: ການເຄື່ອນທີ່ຊື່ປ່ຽນແປງສະໝໍ່າສະເໝີ", accelerated_motion),
    ("ບົດທີ 3: ການຕົກຕາມລໍາພັງ", free_fall),
]

CSS = """
body{font-family:'Noto Sans Lao','Phetsarath OT','Saysettha OT',sans-serif;
     max-width:900px;margin:30px auto;padding:0 16px;line-height:1.7;color:#222}
h1{text-align:center} h2{border-bottom:2px solid #3b6fb6;padding-bottom:4px;color:#3b6fb6}
.card{border:1px solid #ddd;border-radius:10px;padding:14px 18px;margin:18px 0;background:#fafafa}
.card img{max-width:100%;display:block;margin:10px auto}
details{margin-top:8px} summary{cursor:pointer;color:#c0392b;font-weight:bold}
.ans{background:#e8f5e9;padding:6px 10px;border-radius:6px;margin-top:6px}
@media print{details{display:block} details>*{display:block}}
"""


def build(n):
    os.makedirs(OUT, exist_ok=True)
    parts = [f"<!doctype html><html lang='lo'><head><meta charset='utf-8'>"
             f"<title>ໂຈດຟີຊິກ</title><style>{CSS}</style></head><body>"
             f"<h1>ແບບຝຶກຫັດຟີຊິກ: ກົນສາດ (ການເຄື່ອນທີ່)</h1>"]
    for title, fn in SECTIONS:
        parts.append(f"<h2>{title}</h2>")
        for i in range(1, n + 1):
            p = fn(i)
            sol = "<br>".join(html.escape(s) for s in p["sol"])
            parts.append(
                f"<div class='card'><b>ຂໍ້ {i}.</b> {html.escape(p['q'])}"
                f"<img src='{p['img']}' alt='ຮູບປະກອບ'>"
                f"<details><summary>ເບິ່ງວິທີແກ້ ແລະ ຄໍາຕອບ</summary>"
                f"<p>{sol}</p><div class='ans'>ຄໍາຕອບ: {html.escape(p['ans'])}</div>"
                f"</details></div>")
    parts.append("</body></html>")
    path = os.path.join(OUT, "problems.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"ສໍາເລັດ! ເປີດໄຟລ໌: {path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=3, help="ຈໍານວນຂໍ້ຕໍ່ບົດ")
    ap.add_argument("--seed", type=int, default=None, help="ກໍານົດ seed ເພື່ອໄດ້ຊຸດໂຈດເດີມ")
    args = ap.parse_args()
    if args.seed is not None:
        random.seed(args.seed)
    build(args.n)
