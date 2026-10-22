#python -m streamlit run projectile_all.py 
# -*- coding: utf-8 -*-
# ຮັນ: python -m streamlit run projectile_all.py
# (ຕ້ອງ cd /d D:\ph ກ່ອນ ຫຼື ໃຊ້ path ເຕັມ)
import math

import pandas as pd
import streamlit as st

# =====================================================
# ສ່ວນທີ 1: ຟັງຊັນຄິດໄລ່ (ໃຊ້ແຍກໄດ້ ບໍ່ຕ້ອງມີ streamlit)
# ທຸກຟັງຊັນ: v0 (m/s), theta (ອົງສາ), g (m/s^2), h0 (m)
# =====================================================

def components(v0, theta):
    """ແຍກຄວາມໄວຕົ້ນ: v0x = v0 cos(t), v0y = v0 sin(t)"""
    th = math.radians(theta)
    return v0 * math.cos(th), v0 * math.sin(th)


def position_at(v0, theta, t, g, h0=0.0):
    """ຕຳແໜ່ງ ທີ່ເວລາ t:  x = v0 cos(t) t ,  y = h0 + v0 sin(t) t - g t^2 / 2"""
    v0x, v0y = components(v0, theta)
    return v0x * t, h0 + v0y * t - 0.5 * g * t * t


def velocity_at(v0, theta, t, g):
    """ຄວາມໄວ ທີ່ເວລາ t: vx = v0x, vy = v0y - g t, ຂະໜາດ, ແລະ ມູມທິດທາງ (phi)"""
    v0x, v0y = components(v0, theta)
    vx, vy = v0x, v0y - g * t
    speed = math.hypot(vx, vy)
    phi = math.degrees(math.atan2(vy, vx))  # + ຂຶ້ນ, - ລົງ
    return vx, vy, speed, phi


def time_to_peak(v0, theta, g):
    """ເວລາຂຶ້ນເຖິງຈຸດສູງສຸດ: t = v0 sin(t) / g"""
    return max(components(v0, theta)[1] / g, 0.0)


def max_height(v0, theta, g, h0=0.0):
    """ຄວາມສູງສູງສຸດ: H = h0 + v0^2 sin^2(t) / (2g)"""
    v0y = components(v0, theta)[1]
    if v0y <= 0:
        return h0
    return h0 + v0y ** 2 / (2 * g)


def flight_time(v0, theta, g, h0=0.0):
    """ເວລາລອຍທັງໝົດ (ຈົນ y = 0): T = (v0y + sqrt(v0y^2 + 2 g h0)) / g
    ຖ້າ h0 = 0:  T = 2 v0 sin(t) / g"""
    v0y = components(v0, theta)[1]
    return (v0y + math.sqrt(v0y ** 2 + 2 * g * h0)) / g


def horizontal_range(v0, theta, g, h0=0.0):
    """ໄລຍະຕາມແນວນອນ: R = v0 cos(t) * T
    ຖ້າ h0 = 0:  R = v0^2 sin(2t) / g"""
    return components(v0, theta)[0] * flight_time(v0, theta, g, h0)


def trajectory_y(x, v0, theta, g, h0=0.0):
    """ສົມຜົນວິຖີ: y = h0 + x tan(t) - g x^2 / (2 v0^2 cos^2(t))"""
    th = math.radians(theta)
    return h0 + x * math.tan(th) - g * x * x / (2 * v0 ** 2 * math.cos(th) ** 2)


def impact_state(v0, theta, g, h0=0.0):
    """ຄວາມໄວ ແລະ ມູມ ຕອນຕົກພື້ນ.  vy_impact = -sqrt(v0y^2 + 2 g h0)
    ຂະໜາດ: v = sqrt(v0^2 + 2 g h0)   ມູມຕົກ: tan(phi) = |vy| / vx"""
    v0x, v0y = components(v0, theta)
    vy = -math.sqrt(v0y ** 2 + 2 * g * h0)
    speed = math.hypot(v0x, vy)
    angle = math.degrees(math.atan2(abs(vy), v0x))  # ມູມທຽບແນວນອນ (ຕ່ຳກວ່າແນວນອນ)
    return v0x, vy, speed, angle


def speed_at_height(v0, g, h0, y):
    """ອະນຸລັກພະລັງງານ: v = sqrt(v0^2 - 2 g (y - h0))  (ບໍ່ຂຶ້ນກັບມູມ)"""
    val = v0 ** 2 - 2 * g * (y - h0)
    return math.sqrt(val) if val >= 0 else None


def times_at_height(v0, theta, g, h0, y):
    """ເວລາທີ່ວັດຖຸຢູ່ຄວາມສູງ y: g t^2/2 - v0y t + (y - h0) = 0 -> ສູງສຸດ 2 ຄ່າ"""
    v0y = components(v0, theta)[1]
    disc = v0y ** 2 - 2 * g * (y - h0)
    if disc < 0:
        return []
    r = math.sqrt(disc)
    return sorted({(v0y - r) / g, (v0y + r) / g})


def angles_for_range(v0, R, g):
    """ຫາມູມຈາກໄລຍະ (h0 = 0): sin(2t) = R g / v0^2
    ໄດ້ 2 ມູມ ທີ່ເປັນມູມປະກອບກັນ: t1 ແລະ 90 - t1"""
    s = R * g / v0 ** 2
    if s > 1 or s < 0:
        return None
    t1 = 0.5 * math.degrees(math.asin(s))
    return t1, 90 - t1


def max_range_angle(v0, g, h0=0.0):
    """ມູມທີ່ໄດ້ໄລຍະໄກສຸດ: tan(t) = v0 / sqrt(v0^2 + 2 g h0)   (h0 = 0 -> 45 ອົງສາ)"""
    return math.degrees(math.atan(v0 / math.sqrt(v0 ** 2 + 2 * g * h0)))


def incline_range(v0, theta, alpha, g):
    """ຍິງຂຶ້ນພື້ນເອຽງ ມູມ alpha (theta ວັດຈາກແນວນອນ):
    L = 2 v0^2 cos(t) sin(t - a) / (g cos^2(a))"""
    t, a = math.radians(theta), math.radians(alpha)
    return 2 * v0 ** 2 * math.cos(t) * math.sin(t - a) / (g * math.cos(a) ** 2)


def incline_best(v0, alpha, g):
    """ມູມດີທີ່ສຸດຂຶ້ນພື້ນເອຽງ: t = 45 + a/2 ,  Lmax = v0^2 / (g (1 + sin a))"""
    best = 45 + alpha / 2
    lmax = v0 ** 2 / (g * (1 + math.sin(math.radians(alpha))))
    return best, lmax


# ຄ່າ sin, cos, tan ຂອງມູມພິເສດ (ຕົວເລກຕັດ 3-4-5 ແລະ 30-60-90)
SPECIAL = {
    0: ("0", "1", "0"),
    30: ("1/2", "√3/2", "1/√3 = √3/3"),
    37: ("3/5", "4/5", "3/4"),
    45: ("√2/2", "√2/2", "1"),
    53: ("4/5", "3/5", "4/3"),
    60: ("√3/2", "1/2", "√3"),
    90: ("1", "0", "ບໍ່ມີຄ່າ"),
}


# =====================================================
# ສ່ວນທີ 2: ໜ້າເວັບ Streamlit
# =====================================================
st.set_page_config(page_title="ການເຄື່ອນທີ່ໂຄ້ງ", layout="wide")
st.title("ການເຄື່ອນທີ່ແບບໂຄ້ງ (Projectile Motion)")

with st.sidebar:
    st.header("ຄ່າຄົງທີ່")
    g = st.number_input("g (m/s²)", min_value=0.1, value=10.0, step=0.1)
    st.caption("ໃຊ້ g = 10 ຕາມບົດຮຽນ, ຫຼື 9.8 ຖ້າຕ້ອງການຄ່າລະອຽດ")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["ສູດທັງໝົດ", "ຄິດໄລ່ + ກຣາຟ", "ຫາມູມຈາກໄລຍະ", "ປຽບທຽບມູມ", "ພື້ນເອຽງ"]
)

# ---------------- TAB 1: ສູດ ----------------
with tab1:
    st.subheader("ຕາຕະລາງ sin, cos, tan ຂອງມູມພິເສດ")
    rows = []
    for ang, (s, c, t) in SPECIAL.items():
        r = math.radians(ang)
        rows.append(
            {
                "ມູມ": f"{ang}°",
                "sin": s,
                "cos": c,
                "tan": t,
                "sin ເປັນທົດສະນິຍົມ": round(math.sin(r), 4),
                "cos ເປັນທົດສະນິຍົມ": round(math.cos(r), 4),
                "sin 2θ": round(math.sin(2 * r), 4),
            }
        )
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("1) ແຍກຄວາມໄວຕົ້ນ")
        st.latex(r"v_{0x} = v_0\cos\theta \qquad v_{0y} = v_0\sin\theta")
        st.latex(r"v_0=\sqrt{v_{0x}^2+v_{0y}^2}\qquad \tan\theta=\frac{v_{0y}}{v_{0x}}")

        st.subheader("2) ຄວາມໄວທີ່ເວລາ t")
        st.latex(r"v_x = v_0\cos\theta \quad(\text{ຄົງທີ່})")
        st.latex(r"v_y = v_0\sin\theta - gt")
        st.latex(r"v=\sqrt{v_x^2+v_y^2}\qquad \tan\varphi=\frac{v_y}{v_x}")

        st.subheader("3) ຕຳແໜ່ງທີ່ເວລາ t")
        st.latex(r"x = v_0\cos\theta\, t")
        st.latex(r"y = h_0 + v_0\sin\theta\, t - \tfrac12 g t^2")

        st.subheader("4) ສົມຜົນວິຖີ (ຕັດ t ອອກ)")
        st.latex(r"y = h_0 + x\tan\theta - \frac{g x^2}{2v_0^2\cos^2\theta}")

    with c2:
        st.subheader("5) ຈຸດສູງສຸດ")
        st.latex(r"t_{\uparrow} = \frac{v_0\sin\theta}{g}")
        st.latex(r"H_{max} = h_0 + \frac{v_0^2\sin^2\theta}{2g}")

        st.subheader("6) ເວລາລອຍ ແລະ ໄລຍະ")
        st.latex(r"T=\frac{v_0\sin\theta+\sqrt{v_0^2\sin^2\theta+2gh_0}}{g}")
        st.latex(r"R = v_0\cos\theta \cdot T")
        st.markdown("**ກໍລະນີ h₀ = 0 (ຍິງຈາກພື້ນ):**")
        st.latex(r"T=\frac{2v_0\sin\theta}{g}\qquad R=\frac{v_0^2\sin 2\theta}{g}")
        st.latex(r"\sin 2\theta = 2\sin\theta\cos\theta")

        st.subheader("7) ມູມພິເສດ")
        st.latex(r"R_{max}=\frac{v_0^2}{g}\ \ (\theta=45^\circ,\ h_0=0)")
        st.latex(r"R(\theta)=R(90^\circ-\theta)\ \ (\text{ມູມປະກອບໄດ້ໄລຍະເທົ່າກັນ})")
        st.latex(r"\tan\theta_{best}=\frac{v_0}{\sqrt{v_0^2+2gh_0}}\ \ (h_0>0)")
        st.latex(r"H_{max}=\frac{R}{4}\tan\theta\ \ (h_0=0)")

        st.subheader("8) ຕົກພື້ນ")
        st.latex(r"v_{y,end}=-\sqrt{v_0^2\sin^2\theta+2gh_0}")
        st.latex(r"v_{end}=\sqrt{v_0^2+2gh_0}\qquad \tan\varphi_{end}=\frac{|v_{y,end}|}{v_0\cos\theta}")

        st.subheader("9) ຍິງແນວນອນ (θ = 0°)")
        st.latex(r"x=v_0 t\quad y=h_0-\tfrac12gt^2\quad T=\sqrt{\tfrac{2h_0}{g}}\quad R=v_0\sqrt{\tfrac{2h_0}{g}}")

        st.subheader("10) ຄວາມໄວທີ່ຄວາມສູງ y")
        st.latex(r"v=\sqrt{v_0^2-2g(y-h_0)}")

# ---------------- TAB 2: ຄິດໄລ່ ----------------
with tab2:
    a, b, c = st.columns(3)
    v0 = a.number_input("v₀ (m/s)", min_value=0.1, value=20.0, step=1.0, key="v0_a")
    theta = b.number_input("ມູມ θ (ອົງສາ, 0–90)", min_value=0.0, max_value=90.0, value=37.0, step=1.0, key="th_a")
    h0 = c.number_input("ຄວາມສູງເລີ່ມຕົ້ນ h₀ (m)", min_value=0.0, value=0.0, step=1.0, key="h0_a")

    v0x, v0y = components(v0, theta)
    T = flight_time(v0, theta, g, h0)
    tp = time_to_peak(v0, theta, g)
    H = max_height(v0, theta, g, h0)
    R = horizontal_range(v0, theta, g, h0)
    ivx, ivy, ispeed, iang = impact_state(v0, theta, g, h0)

    st.markdown("### ຜົນຄິດໄລ່")
    m = st.columns(5)
    m[0].metric("v₀ₓ (m/s)", f"{v0x:.2f}")
    m[1].metric("v₀ᵧ (m/s)", f"{v0y:.2f}")
    m[2].metric("ເວລາຂຶ້ນສູງສຸດ (s)", f"{tp:.2f}")
    m[3].metric("ຄວາມສູງສູງສຸດ (m)", f"{H:.2f}")
    m[4].metric("ເວລາລອຍ T (s)", f"{T:.2f}")
    m = st.columns(4)
    m[0].metric("ໄລຍະ R (m)", f"{R:.2f}")
    m[1].metric("ຄວາມໄວຕອນຕົກ (m/s)", f"{ispeed:.2f}")
    m[2].metric("ມູມຕົກ (ຕ່ຳກວ່າແນວນອນ)", f"{iang:.1f}°")
    m[3].metric("ມູມໄດ້ໄລຍະໄກສຸດ", f"{max_range_angle(v0, g, h0):.1f}°")

    with st.expander("ເບິ່ງຂັ້ນຕອນການແທນຄ່າ"):
        st.write(f"v₀ₓ = v₀ cosθ = {v0} × cos {theta}° = **{v0x:.3f}** m/s")
        st.write(f"v₀ᵧ = v₀ sinθ = {v0} × sin {theta}° = **{v0y:.3f}** m/s")
        st.write(f"t(ຂຶ້ນ) = v₀ᵧ / g = {v0y:.3f} / {g} = **{tp:.3f}** s")
        st.write(f"H = h₀ + v₀ᵧ² / 2g = {h0} + {v0y:.3f}² / (2×{g}) = **{H:.3f}** m")
        st.write(f"T = (v₀ᵧ + √(v₀ᵧ² + 2gh₀)) / g = **{T:.3f}** s")
        st.write(f"R = v₀ₓ × T = {v0x:.3f} × {T:.3f} = **{R:.3f}** m")
        if h0 == 0:
            st.write(f"ກວດດ້ວຍສູດ R = v₀² sin2θ / g = **{v0 ** 2 * math.sin(math.radians(2 * theta)) / g:.3f}** m")

    if T <= 0:
        st.warning("ເວລາລອຍເປັນ 0 (ມູມ 0° ແລະ h₀ = 0) ຈຶ່ງບໍ່ມີກຣາຟ. ລອງໃສ່ມູມ ຫຼື ຄວາມສູງ.")
    else:
        st.markdown("### ຈຸດໃດໜຶ່ງໃນວິຖີ")
        t = st.slider("ເວລາ t (s)", 0.0, float(round(T, 3)), 0.0, step=0.01)
        x_t, y_t = position_at(v0, theta, t, g, h0)
        vx_t, vy_t, sp_t, ph_t = velocity_at(v0, theta, t, g)
        m = st.columns(6)
        m[0].metric("x (m)", f"{x_t:.2f}")
        m[1].metric("y (m)", f"{max(y_t, 0):.2f}")
        m[2].metric("vₓ (m/s)", f"{vx_t:.2f}")
        m[3].metric("vᵧ (m/s)", f"{vy_t:.2f}")
        m[4].metric("ຄວາມໄວ v (m/s)", f"{sp_t:.2f}")
        m[5].metric("ມູມທິດທາງ φ", f"{ph_t:.1f}°")
        st.caption("φ ເປັນ + ແມ່ນກຳລັງຂຶ້ນ, ເປັນ − ແມ່ນກຳລັງລົງ (ວັດທຽບແນວນອນ)")

        n = 100
        pts = []
        for i in range(n + 1):
            ti = T * i / n
            xi, yi = position_at(v0, theta, ti, g, h0)
            pts.append({"x (m)": xi, "y (m)": max(yi, 0.0)})
        st.line_chart(pd.DataFrame(pts), x="x (m)", y="y (m)")

        st.markdown("### ຫາເວລາ ແລະ ຄວາມໄວທີ່ຄວາມສູງ y ທີ່ກຳນົດ")
        yq = st.number_input("ຄວາມສູງ y (m)", min_value=0.0, value=float(round(H / 2, 1)), step=1.0)
        ts = times_at_height(v0, theta, g, h0, yq)
        if not ts:
            st.info("ວັດຖຸບໍ່ສູງເຖິງລະດັບນີ້")
        else:
            sp = speed_at_height(v0, g, h0, yq)
            st.write("ເວລາທີ່ຜ່ານລະດັບນີ້: " + ", ".join(f"**{x:.3f} s**" for x in ts))
            st.write(f"ຄວາມໄວທີ່ລະດັບນີ້ (ຂະໜາດ): **{sp:.3f} m/s**")

# ---------------- TAB 3: ຫາມູມ ----------------
with tab3:
    st.markdown("ຍິງຈາກພື້ນ (h₀ = 0) ແລະ ຮູ້ໄລຍະ R ທີ່ຕ້ອງການ: **sin 2θ = R g / v₀²**")
    a, b = st.columns(2)
    v0b = a.number_input("v₀ (m/s)", min_value=0.1, value=20.0, step=1.0, key="v0_b")
    Rb = b.number_input("ໄລຍະ R (m)", min_value=0.0, value=30.0, step=1.0, key="R_b")
    st.write(f"ໄລຍະໄກສຸດທີ່ເປັນໄປໄດ້: R_max = v₀²/g = **{v0b ** 2 / g:.2f} m**")
    res = angles_for_range(v0b, Rb, g)
    if res is None:
        st.error("ໄລຍະນີ້ໄກເກີນ ບໍ່ສາມາດເຖິງໄດ້ດ້ວຍຄວາມໄວນີ້")
    else:
        t1, t2 = res
        st.success(f"ມູມຕ່ຳ θ₁ = {t1:.2f}°   ແລະ   ມູມສູງ θ₂ = 90° − θ₁ = {t2:.2f}°")
        rows = []
        for name, ang in (("θ₁ (ມູມຕ່ຳ)", t1), ("θ₂ (ມູມສູງ)", t2)):
            rows.append(
                {
                    "ມູມ": name,
                    "θ (°)": round(ang, 2),
                    "R (m)": round(horizontal_range(v0b, ang, g), 2),
                    "H (m)": round(max_height(v0b, ang, g), 2),
                    "T (s)": round(flight_time(v0b, ang, g), 2),
                }
            )
        st.dataframe(pd.DataFrame(rows), hide_index=True)
        st.caption("ມູມຕ່ຳ: ໄປໄວ ແລະ ຕ່ຳ.  ມູມສູງ: ລອຍນານ ແລະ ສູງກວ່າ.")

# ---------------- TAB 4: ປຽບທຽບ ----------------
with tab4:
    a, b = st.columns(2)
    v0c = a.number_input("v₀ (m/s)", min_value=0.1, value=20.0, step=1.0, key="v0_c")
    h0c = b.number_input("h₀ (m)", min_value=0.0, value=0.0, step=1.0, key="h0_c")
    angs = st.multiselect(
        "ເລືອກມູມທີ່ຕ້ອງການປຽບທຽບ",
        [15, 30, 37, 45, 53, 60, 75],
        default=[30, 45, 60],
    )
    if angs:
        table = []
        Rmax_all = max(horizontal_range(v0c, ang, g, h0c) for ang in angs)
        xs = [Rmax_all * i / 150 for i in range(151)]
        data = {"x (m)": xs}
        for ang in angs:
            Ra = horizontal_range(v0c, ang, g, h0c)
            table.append(
                {
                    "θ (°)": ang,
                    "R (m)": round(Ra, 2),
                    "H (m)": round(max_height(v0c, ang, g, h0c), 2),
                    "T (s)": round(flight_time(v0c, ang, g, h0c), 2),
                    "ຄວາມໄວຕອນຕົກ (m/s)": round(impact_state(v0c, ang, g, h0c)[2], 2),
                }
            )
            col = []
            for x in xs:
                y = trajectory_y(x, v0c, ang, g, h0c) if ang < 90 else float("nan")
                col.append(y if (x <= Ra and y >= 0) else float("nan"))
            data[f"{ang}°"] = col
        st.dataframe(pd.DataFrame(table), hide_index=True, use_container_width=True)
        st.line_chart(pd.DataFrame(data), x="x (m)")
        st.caption(
            f"ມູມໄດ້ໄລຍະໄກສຸດ (ຈາກສູດ) = {max_range_angle(v0c, g, h0c):.1f}°. "
            "ເມື່ອ h₀ = 0, ມູມປະກອບກັນ (ເຊັ່ນ 30° ກັບ 60°) ໄດ້ໄລຍະເທົ່າກັນ."
        )
    else:
        st.info("ເລືອກຢ່າງໜ້ອຍ 1 ມູມ")

# ---------------- TAB 5: ພື້ນເອຽງ ----------------
with tab5:
    st.markdown("ຍິງຂຶ້ນພື້ນເອຽງມູມ α (θ ວັດຈາກແນວນອນ, ຕ້ອງ θ > α)")
    a, b, c = st.columns(3)
    v0d = a.number_input("v₀ (m/s)", min_value=0.1, value=20.0, step=1.0, key="v0_d")
    alpha = b.number_input("ມູມພື້ນເອຽງ α (°)", min_value=0.0, max_value=80.0, value=30.0, step=1.0)
    thd = c.number_input("ມູມຍິງ θ (°)", min_value=0.0, max_value=90.0, value=60.0, step=1.0, key="th_d")
    st.latex(r"L=\frac{2v_0^2\cos\theta\,\sin(\theta-\alpha)}{g\cos^2\alpha}")
    st.latex(r"\theta_{best}=45^\circ+\frac{\alpha}{2}\qquad L_{max}=\frac{v_0^2}{g(1+\sin\alpha)}")
    if thd <= alpha:
        st.warning("ມູມຍິງຕ້ອງໃຫຍ່ກວ່າມູມພື້ນເອຽງ")
    else:
        L = incline_range(v0d, thd, alpha, g)
        best, lmax = incline_best(v0d, alpha, g)
        m = st.columns(3)
        m[0].metric("ໄລຍະຕາມພື້ນເອຽງ L (m)", f"{L:.2f}")
        m[1].metric("ມູມດີທີ່ສຸດ θ", f"{best:.1f}°")
        m[2].metric("L ສູງສຸດ (m)", f"{lmax:.2f}")