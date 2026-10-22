#python -m streamlit run projectile2.py
#  -*- coding: utf-8 -*-
# ແລ່ນດ້ວຍ: python -m streamlit run projectile2.py
import base64
import math
import random

import streamlit as st

G = 10.0  # m/s^2

# ມຸມທີ່ sin/cos ເປັນຕົວເລກສວຍ (ໃຊ້ 3-4-5 ແລະ 30-60)
ANGLES = {
    30: (0.5, math.sqrt(3) / 2),
    37: (0.6, 0.8),
    45: (math.sqrt(2) / 2, math.sqrt(2) / 2),
    53: (0.8, 0.6),
    60: (math.sqrt(3) / 2, 0.5),
}


def f(x, nd=2):
    """ຈັດຮູບແບບຕົວເລກ: ຕັດ 0 ທ້າຍທີ່ບໍ່ຈຳເປັນ"""
    s = f"{x:.{nd}f}".rstrip("0").rstrip(".")
    return s if s else "0"


# ==================================================================
#  ສ່ວນແຕ້ມຮູບ (SVG)
# ==================================================================
FONT = "Leelawadee UI, Noto Sans Lao, Segoe UI, Arial, sans-serif"
INK, BLUE, RED, GREY = "#1f2937", "#2563eb", "#dc2626", "#64748b"
SVG_W, SVG_H = 640, 340


def svg_wrap(body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W} {SVG_H}" '
        f'width="{SVG_W}" height="{SVG_H}" font-family="{FONT}">'
        f'<rect width="{SVG_W}" height="{SVG_H}" rx="10" fill="#f8fafc"/>' + body + "</svg>"
    )


def _t(x, y, s, size=13, anchor="middle", color=INK, weight="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{color}" font-weight="{weight}">{s}</text>')


def _ln(x1, y1, x2, y2, color=INK, w=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{w}"{d}/>')


def _arrow(x1, y1, x2, y2, color=BLUE, w=2.4, head=10):
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
    px, py = -math.sin(ang) * head * 0.45, math.cos(ang) * head * 0.45
    return (_ln(x1, y1, bx, by, color, w) +
            f'<polygon points="{x2:.1f},{y2:.1f} {bx+px:.1f},{by+py:.1f} {bx-px:.1f},{by-py:.1f}" '
            f'fill="{color}"/>')


def _dim(x1, y1, x2, y2, color=INK):
    return _arrow(x1, y1, x2, y2, color, 1.4, 7) + _arrow(x2, y2, x1, y1, color, 1.4, 7)


def _path(pts, color=RED, w=2.5, dash=None):
    d = " ".join(("M" if i == 0 else "L") + f"{x:.1f},{y:.1f}" for i, (x, y) in enumerate(pts))
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}"{ds}/>'


def _dot(x, y, color=RED, r=5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}"/>'


def _ground(yg):
    return (f'<rect x="0" y="{yg}" width="{SVG_W}" height="{SVG_H-yg}" fill="#dcebd2"/>' +
            _ln(0, yg, SVG_W, yg, "#4d7c0f", 2))


def _car(cx, yg, ghost=False):
    col = "#94a3b8" if ghost else BLUE
    op = 0.55 if ghost else 1
    dash = ' stroke="#64748b" stroke-dasharray="3 3"' if ghost else ""
    return (
        f'<g opacity="{op}">'
        f'<rect x="{cx-24:.1f}" y="{yg-20}" width="48" height="12" rx="3" fill="{col}"{dash}/>'
        f'<rect x="{cx-12:.1f}" y="{yg-30}" width="24" height="10" rx="3" fill="{col}"{dash}/>'
        f'<circle cx="{cx-14:.1f}" cy="{yg-6}" r="6" fill="#111827"/>'
        f'<circle cx="{cx+14:.1f}" cy="{yg-6}" r="6" fill="#111827"/></g>'
    )


def _plane(cx, cy):
    return (
        f'<ellipse cx="{cx}" cy="{cy}" rx="28" ry="7" fill="#64748b"/>'
        f'<polygon points="{cx-24},{cy-3} {cx-34},{cy-17} {cx-26},{cy-17} {cx-14},{cy-3}" fill="#475569"/>'
        f'<polygon points="{cx-6},{cy+2} {cx+8},{cy+2} {cx-8},{cy+16} {cx-16},{cy+16}" fill="#475569"/>'
        f'<circle cx="{cx+16}" cy="{cy-2}" r="2.5" fill="white"/>'
    )


def _cannon(px, yg, th):
    py = yg - 12
    return (
        f'<g transform="rotate({-th} {px} {py})">'
        f'<rect x="{px-4}" y="{py-5}" width="42" height="10" rx="3" fill="#475569"/></g>'
        f'<rect x="{px-18}" y="{yg-12}" width="30" height="12" rx="3" fill="#1f2937"/>'
        f'<circle cx="{px-3}" cy="{yg-6}" r="7" fill="#111827"/>'
    )


def _angle_marker(px, py, th, r=42):
    a = math.radians(th)
    p1 = (px + r, py)
    p2 = (px + r * math.cos(a), py - r * math.sin(a))
    lx = px + (r + 8) * math.cos(a / 2)
    ly = py - (r + 8) * math.sin(a / 2)
    return (
        _ln(px, py, px + r + 25, py, GREY, 1.2, "4 4") +
        f'<path d="M{p1[0]:.1f},{p1[1]:.1f} A{r},{r} 0 0 0 {p2[0]:.1f},{p2[1]:.1f}" '
        f'fill="none" stroke="{INK}" stroke-width="1.5"/>' +
        _t(lx, ly + 4, f"θ = {th}°", 12, "start")
    )


def _legend(lines):
    return "".join(_t(14, 24 + 18 * i, s, 13, "start", INK, "bold") for i, s in enumerate(lines))


def _traj(x0, y0, vx, vy, T, k, n=60):
    out = []
    for i in range(n + 1):
        t = T * i / n
        out.append((x0 + vx * t * k, y0 - (vy * t - 0.5 * G * t * t) * k))
    return out


def _two_cars(gx, cx, YG, car_dir, ghost_lbl, car_lbl):
    """วาดรถ 2 คัน: ตอนเริ่ม (เส้นประ) และตอนวัตถุตก (ทึบ) + ลูกศรความเร็วรถ"""
    b = _car(gx, YG, ghost=True) + _car(cx, YG)
    right_is_ghost = gx > cx
    b += _t(gx + (-14 if right_is_ghost else 14), YG - 38, ghost_lbl, 11,
            "start" if right_is_ghost else "end", GREY)
    b += _t(cx + (14 if right_is_ghost else -14), YG - 38, car_lbl, 11,
            "end" if right_is_ghost else "start", INK)
    b += _arrow(cx, YG - 58, cx + car_dir * 45, YG - 58, BLUE, 2.2, 8)
    b += _t(cx + car_dir * 22, YG - 64, "vc", 12, color=BLUE)
    return b


# ==================================================================
#  ຊະນິດ 1: ຖິ້ມຕາມແນວນອນ
# ==================================================================
def p_horizontal():
    t = random.randint(1, 5)
    h = 0.5 * G * t * t
    v0 = random.choice(range(5, 41, 5))
    text = (
        f"ຖິ້ມກ້ອນຫີນຕາມແນວນອນດ້ວຍຄວາມໄວ {v0} m/s ຈາກຍອດຫຼັກຜາສູງ {f(h)} m "
        f"ເໜືອພື້ນດິນ (ຄວາມໄວເລີ່ມຕົ້ນແນວຕັ້ງ = 0). ຈົ່ງຫາ:\n"
        f"   ກ) ເວລາທີ່ກ້ອນຫີນຢູ່ໃນອາກາດ\n"
        f"   ຂ) ໄລຍະທາງແນວນອນທີ່ກ້ອນຫີນຕົກຫ່າງຈາກຖານຜາ\n"
        f"   ຄ) ຄວາມໄວຂອງກ້ອນຫີນກ່ອນຕົກຮອດພື້ນ"
    )
    x = v0 * t
    vy = G * t
    v = math.hypot(v0, vy)
    ang = math.degrees(math.atan2(vy, v0))
    sol = (
        f"   ກ) h = ½gt²  →  t = √(2h/g) = √(2×{f(h)}/{f(G)}) = {f(t)} s\n"
        f"   ຂ) x = v₀t = {v0}×{f(t)} = {f(x)} m\n"
        f"   ຄ) vₓ = {v0} m/s,  v_y = gt = {f(G)}×{f(t)} = {f(vy)} m/s\n"
        f"      v = √(vₓ² + v_y²) = {f(v)} m/s  (ມຸມກັບແນວນອນ ≈ {f(ang,1)}°)"
    )
    # ---- ຮູບ (ແຕ້ມແບບແຜນຜັງ ບໍ່ຕາມມາດຕາສ່ວນ) ----
    X0, YG, TOP = 130, 285, 95
    ex = SVG_W - X0 - 70
    pts = [(X0 + ex * u, TOP + (YG - TOP) * u * u) for u in [i / 50 for i in range(51)]]
    b = _ground(YG)
    b += f'<rect x="{X0-70}" y="{TOP}" width="70" height="{YG-TOP}" fill="#94a3b8"/>'
    b += _t(X0 - 35, (TOP + YG) / 2, f"h = {f(h)} m", 13, color="white", weight="bold")
    b += _path(pts, RED, 2.5, "6 4")
    b += _dot(X0, TOP) + _dot(X0 + ex, YG)
    b += _arrow(X0, TOP, X0 + 80, TOP, BLUE)
    b += _t(X0 + 40, TOP - 12, f"v0 = {v0} m/s", 13, color=BLUE)
    b += _dim(X0, YG + 24, X0 + ex, YG + 24)
    b += _t(X0 + ex / 2, YG + 41, "x = ?", 13)
    return text, sol, svg_wrap(b)


# ==================================================================
#  ຊະນິດ 2: ຍິງຈາກພື້ນດ້ວຍມຸມ
# ==================================================================
def p_angle_ground():
    th = random.choice(list(ANGLES))
    sn, cs = ANGLES[th]
    v0 = random.choice(range(10, 61, 5))
    text = (
        f"ເຕະບານຈາກພື້ນສະໜາມດ້ວຍຄວາມໄວ {v0} m/s ໂດຍເຮັດມຸມ {th}° ກັບແນວນອນ. "
        f"ຈົ່ງຫາ:\n"
        f"   ກ) ເວລາທີ່ບານຂຶ້ນເຖິງຈຸດສູງສຸດ\n"
        f"   ຂ) ຄວາມສູງສູງສຸດ\n"
        f"   ຄ) ເວລາທັງໝົດທີ່ບານຢູ່ໃນອາກາດ\n"
        f"   ງ) ໄລຍະທາງແນວນອນທີ່ບານຕົກ (ພິກັດໄກສຸດ)"
    )
    vx, vy = v0 * cs, v0 * sn
    t_up = vy / G
    hmax = vy ** 2 / (2 * G)
    T = 2 * t_up
    R = vx * T
    sol = (
        f"   ແຍກຄວາມໄວ: v₀ₓ = v₀cos{th}° = {f(vx)} m/s,  v₀y = v₀sin{th}° = {f(vy)} m/s\n"
        f"   ກ) ທີ່ຈຸດສູງສຸດ v_y = 0  →  t = v₀y/g = {f(vy)}/{f(G)} = {f(t_up)} s\n"
        f"   ຂ) H = v₀y²/(2g) = {f(vy)}²/(2×{f(G)}) = {f(hmax)} m\n"
        f"   ຄ) T = 2v₀y/g = {f(T)} s\n"
        f"   ງ) R = v₀ₓ·T = {f(vx)}×{f(T)} = {f(R)} m"
    )
    # ---- ຮູບ (ຕາມມາດຕາສ່ວນ) ----
    X0, YG = 60, 280
    k = min((SVG_W - X0 - 50) / R, (YG - 70) / hmax)
    b = _ground(YG)
    b += _path(_traj(X0, YG, vx, vy, T, k), RED, 2.5, "6 4")
    ax, ay = X0 + vx * t_up * k, YG - hmax * k
    b += _ln(ax, ay, ax, YG, GREY, 1.2, "4 4") + _dot(ax, ay, "#f59e0b")
    b += _t(ax + 8, (ay + YG) / 2, "H = ?", 13, "start")
    b += _dot(X0, YG) + _dot(X0 + R * k, YG)
    b += _angle_marker(X0, YG, th)
    b += _arrow(X0, YG, X0 + 70 * cs, YG - 70 * sn, BLUE)
    b += _t(X0 + 70 * cs + 8, YG - 70 * sn - 4, f"v0 = {v0} m/s", 13, "start", BLUE)
    b += _dim(X0, YG + 24, X0 + R * k, YG + 24)
    b += _t(X0 + R * k / 2, YG + 41, "R = ?", 13)
    return text, sol, svg_wrap(b)


# ==================================================================
#  ຊະນິດ 3: ຍິງດ້ວຍມຸມຈາກທີ່ສູງ
# ==================================================================
def p_angle_height():
    th = random.choice([30, 37, 45, 53])
    sn, cs = ANGLES[th]
    v0 = random.choice(range(10, 41, 5))
    h = random.choice(range(10, 81, 10))
    text = (
        f"ໂຍນລູກບານຈາກຕຶກສູງ {h} m ດ້ວຍຄວາມໄວ {v0} m/s ໂດຍເງີຍຂຶ້ນເຮັດມຸມ {th}° "
        f"ກັບແນວນອນ. ຈົ່ງຫາ:\n"
        f"   ກ) ຄວາມສູງສູງສຸດເມື່ອທຽບກັບພື້ນດິນ\n"
        f"   ຂ) ເວລາທີ່ລູກບານຕົກເຖິງພື້ນ\n"
        f"   ຄ) ໄລຍະທາງແນວນອນທີ່ລູກບານຕົກຫ່າງຈາກຖານຕຶກ"
    )
    vx, vy = v0 * cs, v0 * sn
    hmax = h + vy ** 2 / (2 * G)
    a, bq, cc = 0.5 * G, -vy, -h
    t = (-bq + math.sqrt(bq * bq - 4 * a * cc)) / (2 * a)
    x = vx * t
    sol = (
        f"   v₀ₓ = {f(vx)} m/s,  v₀y = {f(vy)} m/s\n"
        f"   ກ) H = h + v₀y²/(2g) = {h} + {f(vy)}²/(2×{f(G)}) = {f(hmax)} m\n"
        f"   ຂ) ຕົກເຖິງພື້ນ y = 0:  0 = {h} + {f(vy)}t − ½({f(G)})t²\n"
        f"      → {f(a)}t² − {f(vy)}t − {h} = 0  →  t ≈ {f(t)} s (ເອົາຄ່າບວກ)\n"
        f"   ຄ) x = v₀ₓ·t = {f(vx)}×{f(t)} ≈ {f(x)} m"
    )
    # ---- ຮູບ (ຕາມມາດຕາສ່ວນ) ----
    X0, YG = 130, 280
    k = min((SVG_W - X0 - 50) / x, (YG - 65) / hmax)
    y0 = YG - h * k
    b = _ground(YG)
    b += f'<rect x="{X0-70}" y="{y0:.1f}" width="70" height="{h*k:.1f}" fill="#94a3b8"/>'
    b += _t(X0 - 35, (y0 + YG) / 2 + 4, f"h = {h} m", 13, color="white", weight="bold")
    b += _path(_traj(X0, y0, vx, vy, t, k), RED, 2.5, "6 4")
    ax, ay = X0 + vx * (vy / G) * k, YG - hmax * k
    b += _ln(ax, ay, ax, YG, GREY, 1.2, "4 4") + _dot(ax, ay, "#f59e0b")
    b += _t(ax + 8, (ay + YG) / 2, "H = ?", 13, "start")
    b += _dot(X0, y0) + _dot(X0 + x * k, YG)
    b += _angle_marker(X0, y0, th)
    b += _arrow(X0, y0, X0 + 70 * cs, y0 - 70 * sn, BLUE)
    b += _t(X0 + 70 * cs + 8, y0 - 70 * sn - 4, f"v0 = {v0} m/s", 13, "start", BLUE)
    b += _dim(X0, YG + 24, X0 + x * k, YG + 24)
    b += _t(X0 + x * k / 2, YG + 41, "x = ?", 13)
    return text, sol, svg_wrap(b)


# ==================================================================
#  ສະຖານະການ "ຍົນ + ລົດ" (ໃຊ້ຮ່ວມກັນໃນຊະນິດ 4 ແລະ 5)
# ==================================================================
def _scene_plane_car(H, xland, d, car_dir, legend, ghost_lbl, car_lbl, obj_color=RED):
    X0, YG, YP = 130, 275, 100
    k = (SVG_W - X0 - 70) / max(xland, d)
    gx, cx = X0 + d * k, X0 + xland * k
    pts = [(X0 + xland * k * u, YP + (YG - YP) * u * u) for u in [i / 60 for i in range(61)]]
    b = _ground(YG)
    b += _ln(X0, YP, X0, YG, GREY, 1.2, "4 4")
    b += _path(pts, obj_color, 2.5, "6 4") + _dot(cx, YG, obj_color, 4)
    b += _plane(X0, YP)
    b += _arrow(X0 + 32, YP, X0 + 90, YP, BLUE, 2.2, 8) + _t(X0 + 62, YP - 10, "vp", 12, color=BLUE)
    b += _two_cars(gx, cx, YG, car_dir, ghost_lbl, car_lbl)
    b += _dim(X0 - 48, YG, X0 - 48, YP)
    b += _t(X0 - 54, (YG + YP) / 2 + 4, f"H = {f(H)} m", 13, "end")
    b += _dim(X0, YG + 24, gx, YG + 24) + _t((X0 + gx) / 2, YG + 41, "d = ?", 13)
    b += _legend(legend)
    return svg_wrap(b)


# ==================================================================
#  ຊະນິດ 4: ສອງວັດຖຸ - ຍົນປ່ອຍວັດຖຸໃສ່ລົດ
# ==================================================================
def p_plane_drop():
    t = random.randint(3, 8)
    H = 0.5 * G * t * t
    vp = random.choice(range(40, 101, 10))
    same = random.choice([True, False])
    vc = random.choice(range(10, 31, 5))
    direction = "ໄປທາງດຽວກັນກັບຍົນ (ຢູ່ທາງໜ້າຍົນ)" if same else "ແລ່ນສວນທາງກັບຍົນ (ຢູ່ທາງໜ້າຍົນ)"
    text = (
        f"ຍົນລຳໜຶ່ງບິນໃນແນວນອນດ້ວຍຄວາມໄວ {vp} m/s ທີ່ຄວາມສູງ {f(H)} m. "
        f"ນັກບິນຕ້ອງການປ່ອຍຖົງຊ່ວຍເຫຼືອໃສ່ລົດຄັນໜຶ່ງທີ່ແລ່ນດ້ວຍຄວາມໄວຄົງທີ່ "
        f"{vc} m/s ເທິງຖະໜົນຊື່ {direction}. ຈົ່ງຫາ:\n"
        f"   ກ) ເວລາທີ່ຖົງຕົກເຖິງພື້ນ\n"
        f"   ຂ) ຕ້ອງປ່ອຍຖົງເມື່ອລົດຢູ່ຫ່າງຈາກຈຸດທີ່ຢູ່ກົງລຸ່ມຍົນເທົ່າໃດ ຖົງຈຶ່ງຕົກໃສ່ລົດພໍດີ?"
    )
    rel = (vp - vc) if same else (vp + vc)
    d = rel * t
    rel_expr = f"({vp} − {vc})" if same else f"({vp} + {vc})"
    sol = (
        f"   ກ) t = √(2H/g) = √(2×{f(H)}/{f(G)}) = {f(t)} s\n"
        f"      (ຖົງມີຄວາມໄວແນວຕັ້ງເລີ່ມຕົ້ນ = 0, ຄວາມໄວແນວນອນ = {vp} m/s ເທົ່າຍົນ)\n"
        f"   ຂ) ຕຳແໜ່ງແນວນອນຕອນຕົກ: ຖົງໄປໄດ້ x_ຖົງ = {vp}×{f(t)} = {f(vp*t)} m\n"
        f"      ລົດໄປໄດ້ x_ລົດ = {vc}×{f(t)} = {f(vc*t)} m\n"
        f"      ໄລຍະເລີ່ມຕົ້ນ d = x_ຖົງ {'−' if same else '+'} x_ລົດ = {rel_expr}×{f(t)} = {f(d)} m"
    )
    svg = _scene_plane_car(
        H, vp * t, d, +1 if same else -1,
        [f"vp = {vp} m/s", f"vc = {vc} m/s"],
        "ຕອນປ່ອຍ", "ຕອນຖົງຕົກ")
    return text, sol, svg


# ==================================================================
#  ຊະນິດ 5: ສອງວັດຖຸ - ຍົນຍິງກະສຸນຕາມແນວນອນໃສ່ລົດ
# ==================================================================
def p_plane_fire():
    t = random.randint(3, 6)
    H = 0.5 * G * t * t
    vp = random.choice(range(50, 101, 10))
    u = random.choice(range(100, 301, 50))
    vc = random.choice(range(10, 31, 5))
    text = (
        f"ຍົນຮົບບິນໃນແນວນອນດ້ວຍຄວາມໄວ {vp} m/s ທີ່ຄວາມສູງ {f(H)} m ແລ້ວຍິງກະສຸນ"
        f"ຕາມແນວນອນໄປທາງໜ້າດ້ວຍຄວາມໄວ {u} m/s ທຽບກັບຍົນ ໃສ່ລົດຖັງທີ່ແລ່ນໜີດ້ວຍຄວາມໄວ "
        f"{vc} m/s ໄປທາງດຽວກັນກັບຍົນ. ຈົ່ງຫາ:\n"
        f"   ກ) ຄວາມໄວຂອງກະສຸນທຽບກັບພື້ນດິນຕອນອອກຈາກຍົນ\n"
        f"   ຂ) ເວລາທີ່ກະສຸນໃຊ້ຈົນຕົກເຖິງລະດັບພື້ນ\n"
        f"   ຄ) ຕ້ອງຍິງຕອນລົດຢູ່ຫ່າງຈາກຈຸດກົງລຸ່ມຍົນເທົ່າໃດ ຈຶ່ງຖືກລົດພໍດີ?"
    )
    vb = vp + u
    d = (vb - vc) * t
    sol = (
        f"   ກ) v_ກະສຸນ(ພື້ນ) = v_ຍົນ + u = {vp} + {u} = {vb} m/s (ແນວນອນ)\n"
        f"   ຂ) t = √(2H/g) = {f(t)} s\n"
        f"   ຄ) x_ກະສຸນ = {vb}×{f(t)} = {f(vb*t)} m,  x_ລົດ = {vc}×{f(t)} = {f(vc*t)} m\n"
        f"      d = x_ກະສຸນ − x_ລົດ = ({vb} − {vc})×{f(t)} = {f(d)} m"
    )
    svg = _scene_plane_car(
        H, vb * t, d, +1,
        [f"vp = {vp} m/s", f"u = {u} m/s (ທຽບກັບຍົນ)", f"vc = {vc} m/s"],
        "ຕອນຍິງ", "ຕອນກະສຸນຕົກ")
    return text, sol, svg


# ==================================================================
#  ຊະນິດ 6: ສອງວັດຖຸ - ປືນໃຫຍ່ຢູ່ພື້ນຍິງດ້ວຍມຸມໃສ່ລົດທີ່ແລ່ນໜີ
# ==================================================================
def p_cannon_vs_car():
    while True:
        th = random.choice([30, 37, 45, 53, 60])
        sn, cs = ANGLES[th]
        v0 = random.choice(range(30, 101, 10))
        vc = random.choice(range(5, 31, 5))
        T = 2 * v0 * sn / G
        R = v0 * cs * T
        d0 = R - vc * T
        if d0 > 20:
            break
    text = (
        f"ປືນໃຫຍ່ຢູ່ເທິງພື້ນລາບ ຍິງລູກກະສຸນດ້ວຍຄວາມໄວ {v0} m/s ເຮັດມຸມ {th}° ກັບ"
        f"ແນວນອນ ໃສ່ລົດຄັນໜຶ່ງທີ່ກຳລັງແລ່ນໜີຈາກປືນເປັນເສັ້ນຊື່ດ້ວຍຄວາມໄວຄົງທີ່ {vc} m/s. "
        f"ລູກກະສຸນຕົກຖືກລົດພໍດີ. ຈົ່ງຫາ:\n"
        f"   ກ) ເວລາທີ່ລູກກະສຸນຢູ່ໃນອາກາດ\n"
        f"   ຂ) ໄລຍະທາງແນວນອນທີ່ລູກກະສຸນເດີນທາງ\n"
        f"   ຄ) ຕອນຍິງ ລົດຢູ່ຫ່າງຈາກປືນເທົ່າໃດ?"
    )
    vx, vy = v0 * cs, v0 * sn
    sol = (
        f"   v₀ₓ = {f(vx)} m/s,  v₀y = {f(vy)} m/s\n"
        f"   ກ) T = 2v₀y/g = 2×{f(vy)}/{f(G)} = {f(T)} s\n"
        f"   ຂ) R = v₀ₓ·T = {f(vx)}×{f(T)} = {f(R)} m\n"
        f"   ຄ) ລົດໄປໄດ້ໃນເວລາ T: {vc}×{f(T)} = {f(vc*T)} m\n"
        f"      d₀ + {f(vc*T)} = R  →  d₀ = {f(R)} − {f(vc*T)} = {f(d0)} m"
    )
    # ---- ຮູບ (ຕາມມາດຕາສ່ວນ) ----
    X0, YG = 60, 262
    hmax = vy ** 2 / (2 * G)
    k = min((SVG_W - X0 - 70) / R, (YG - 75) / hmax)
    gx, cx = X0 + d0 * k, X0 + R * k
    b = _ground(YG)
    b += _path(_traj(X0, YG - 12, vx, vy, T, k), RED, 2.5, "6 4") + _dot(cx, YG, RED, 4)
    b += _cannon(X0, YG, th)
    b += _angle_marker(X0, YG - 12, th, 50)
    b += _two_cars(gx, cx, YG, +1, "ຕອນຍິງ", "ຕອນກະສຸນຕົກ")
    b += _dim(X0, YG + 20, gx, YG + 20) + _t((X0 + gx) / 2, YG + 35, "d0 = ?", 13)
    b += _dim(X0, YG + 46, cx, YG + 46) + _t((X0 + cx) / 2, YG + 61, "R = ?", 13)
    b += _legend([f"v0 = {v0} m/s", f"θ = {th}°", f"vc = {vc} m/s"])
    return text, sol, svg_wrap(b)


GENERATORS = {
    1: ("ຖິ້ມຕາມແນວນອນ (v₀y = 0)", p_horizontal),
    2: ("ຍິງຈາກພື້ນດ້ວຍມຸມ (v₀ ≠ 0)", p_angle_ground),
    3: ("ຍິງດ້ວຍມຸມຈາກທີ່ສູງ (v₀ ≠ 0)", p_angle_height),
    4: ("ສອງວັດຖຸ: ຍົນປ່ອຍຂອງໃສ່ລົດ", p_plane_drop),
    5: ("ສອງວັດຖຸ: ຍົນຍິງກະສຸນໃສ່ລົດ", p_plane_fire),
    6: ("ສອງວັດຖຸ: ປືນໃຫຍ່ຍິງໃສ່ລົດທີ່ແລ່ນໜີ", p_cannon_vs_car),
}


# ==================================================================
#  ໜ້າເວັບ Streamlit
# ==================================================================
def to_html(s):
    """ແປງຂໍ້ຄວາມໃຫ້ສະແດງໃນ Streamlit: ຮັກສາການຍໍ້ໜ້າ ແລະ _ ບໍ່ໃຫ້ກາຍເປັນຕົວອຽງ"""
    out = []
    for line in s.split("\n"):
        n = len(line) - len(line.lstrip(" "))
        out.append("&nbsp;" * n + line.lstrip(" ").replace("_", "&#95;"))
    return "<br>".join(out)


def svg_to_img(svg):
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return (f'<img src="data:image/svg+xml;base64,{b64}" '
            f'style="width:100%;max-width:640px;border-radius:10px;">')


if __name__ == "__main__" or True:
    st.set_page_config(page_title="ໂຈດຟີຊິກ: ການເຄື່ອນທີ່ໂຄ້ງ", page_icon="🎯")
    st.title("🎯 ໂຕສ້າງໂຈດຟີຊິກ: ການເຄື່ອນທີ່ໂຄ້ງ")
    st.caption("ໃຊ້ g = 10 m/s²")

    with st.sidebar:
        st.header("ຕັ້ງຄ່າ")
        chosen = st.multiselect(
            "ຊະນິດໂຈດ",
            options=list(GENERATORS),
            default=list(GENERATORS),
            format_func=lambda k: f"{k}. {GENERATORS[k][0]}",
        )
        n = st.number_input("ຈຳນວນຂໍ້", min_value=1, max_value=50, value=6, step=1)
        fixed = st.checkbox("ກຳນົດ seed (ໄດ້ຜົນເດີມທຸກຄັ້ງ)")
        seed = st.number_input("seed", value=42, step=1) if fixed else None
        show_img = st.checkbox("ສະແດງຮູບປະກອບ", value=True)
        show_sol = st.checkbox("ສະແດງວິທີແກ້", value=True)
        go = st.button("ສ້າງໂຈດ", type="primary", use_container_width=True)

    if go or "problems" not in st.session_state:
        if not chosen:
            st.warning("ກະລຸນາເລືອກຢ່າງໜ້ອຍ 1 ຊະນິດ")
            st.stop()
        if seed is not None:
            random.seed(int(seed))
        items = []
        for i in range(int(n)):
            if len(chosen) == 1:
                k = chosen[0]
            elif n <= len(chosen):
                k = chosen[i]
            else:
                k = random.choice(chosen)
            name, gen = GENERATORS[k]
            text, sol, svg = gen()
            items.append((name, text, sol, svg))
        st.session_state["problems"] = items

    for i, (name, text, sol, svg) in enumerate(st.session_state["problems"], 1):
        st.subheader(f"ຂໍ້ {i}.")
        st.caption(name)
        st.markdown(to_html(text), unsafe_allow_html=True)
        if show_img:
            st.markdown(svg_to_img(svg), unsafe_allow_html=True)
        if show_sol:
            with st.expander("ເບິ່ງວິທີແກ້"):
                st.markdown(to_html(sol), unsafe_allow_html=True)
        st.divider()