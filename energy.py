# -*- c
# oding: utf-8 -*-
# ຮັນ: python -m streamlit run energy.py
# (ຕ້ອງ cd /d D:\ph ກ່ອນ ຫຼື ໃຊ້ path ເຕັມ)
#python -m streamlit run energy.py
import math
import random

import pandas as pd
import streamlit as st

# =====================================================
# ສ່ວນທີ 1: ຟັງຊັນຄິດໄລ່ (ແຍກໄດ້ ບໍ່ຕ້ອງມີ streamlit)
# =====================================================

def kinetic(m, v):
    """Ek = 1/2 m v^2"""
    return 0.5 * m * v * v


def grav_pe(m, g, h):
    """Ep = m g h"""
    return m * g * h


def elastic_pe(k, x):
    """Ep(ສະປຣິງ) = 1/2 k x^2"""
    return 0.5 * k * x * x


def work(F, d, theta=0.0):
    """W = F d cos(theta)"""
    return F * d * math.cos(math.radians(theta))


def power_from_work(W, t):
    """P = W / t"""
    return W / t


def power_from_force(F, v, theta=0.0):
    """P = F v cos(theta)"""
    return F * v * math.cos(math.radians(theta))


def efficiency(e_out, e_in):
    """eta = E_out / E_in x 100 %"""
    return 100.0 * e_out / e_in


def speed_conserve(v1, h1, h2, g):
    """ອະນຸລັກພະລັງງານກົນ (ບໍ່ມີແຮງຝືດ): v2 = sqrt(v1^2 + 2 g (h1 - h2))"""
    val = v1 * v1 + 2 * g * (h1 - h2)
    return math.sqrt(val) if val >= 0 else None


def speed_from_net_work(m, v1, W_net):
    """ທິດສະດີງານ-ພະລັງງານ: W_net = Ek2 - Ek1 -> v2 = sqrt(v1^2 + 2 W_net / m)"""
    val = v1 * v1 + 2 * W_net / m
    return math.sqrt(val) if val >= 0 else None


def pendulum_speed_bottom(L, theta0, g):
    """ລູກຕຸ້ມແກວ່ງ ປ່ອຍຈາກມູມ theta0: v = sqrt(2 g L (1 - cos theta0))"""
    return math.sqrt(2 * g * L * (1 - math.cos(math.radians(theta0))))


def spring_launch_speed(k, x, m):
    """1/2 k x^2 = 1/2 m v^2 -> v = x sqrt(k / m)"""
    return x * math.sqrt(k / m)


def incline_slide(m, h0, alpha, mu, g, steps=60):
    """ເລື່ອນລົງພື້ນເອຽງ ມູມ alpha ມີສຳປະສິດຝືດ mu
    ຄືນລາຍການ: ໄລຍະ s, ຄວາມສູງ h, Ep, Ek, ຄວາມຮ້ອນ Q ແລະ ຄວາມໄວ v
    Ek = m g (h0 - h) - mu m g cos(a) s   (ຖ້າ Ek < 0 ວັດຖຸຢຸດກ່ອນ)"""
    a = math.radians(alpha)
    total = h0 / math.sin(a)
    rows = []
    for i in range(steps + 1):
        s = total * i / steps
        h = h0 - s * math.sin(a)
        ep = m * g * h
        q = mu * m * g * math.cos(a) * s
        ek = m * g * (h0 - h) - q
        rows.append((s, h, ep, ek, q))
    return total, rows


# =====================================================
# ສ່ວນທີ 2: ຄັງໂຈດຄຳນວນ (ສຸ່ມຕົວເລກ + ເຉລີຍ)
# =====================================================

def _fmt(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def p_kinetic(r, g):
    m = r.choice([2, 4, 5, 10, 20, 50, 60, 1000])
    v = r.choice([2, 3, 4, 5, 10, 12, 15, 20])
    ans = kinetic(m, v)
    q = (
        f"ວັດຖຸມວນ {m} kg ເຄື່ອນທີ່ດ້ວຍຄວາມໄວ {v} m/s. ຫາພະລັງງານຈົນ "
        f"(Ek)"
    )
    sol = f"Ek = ½mv² = ½ × {m} × {v}² = **{_fmt(ans)} J**"
    return q, ans, "J", sol


def p_gpe(r, g):
    m = r.choice([1, 2, 3, 5, 10, 20, 50])
    h = r.choice([2, 5, 8, 10, 15, 20, 30])
    ans = grav_pe(m, g, h)
    q = (
        f"ຍົກວັດຖຸມວນ {m} kg ຂຶ້ນສູງ {h} m ຈາກພື້ນ (g = "
        f"{_fmt(g)} m/s²). ຫາພະລັງງານສັກ (Ep)"
    )
    sol = f"Ep = mgh = {m} × {_fmt(g)} × {h} = **{_fmt(ans)} J**"
    return q, ans, "J", sol


def p_free_fall(r, g):
    h = r.choice([5, 10, 20, 45, 80, 125])
    ans = math.sqrt(2 * g * h)
    q = (
        f"ປ່ອຍວັດຖຸຈາກຄວາມສູງ {h} m (ຈາກສະພາບນິ່ງ, ບໍ່ມີແຮງຕ້ານອາກາດ, "
        f"g = {_fmt(g)}). ຫາຄວາມໄວຕອນຕົກພື້ນ"
    )
    sol = (
        f"ອະນຸລັກພະລັງງານ: mgh = ½mv²  →  v = √(2gh) = √(2 "
        f"× {_fmt(g)} × {h}) = **{_fmt(ans)} m/s**"
    )
    return q, ans, "m/s", sol


def p_work(r, g):
    F = r.choice([10, 20, 50, 100, 200])
    d = r.choice([2, 5, 10, 20])
    th = r.choice([0, 30, 37, 53, 60])
    ans = work(F, d, th)
    q = (
        f"ອອກແຮງ {F} N ໃນທິດທາງທຳມຸມ {th}° ກັບແນວນອນ ເຮັດໃຫ້ກ່ອງເລື່ອນໄປ "
        f"{d} m ຕາມແນວນອນ. ຫາງານຂອງແຮງນີ້"
    )
    sol = f"W = Fd cosθ = {F} × {d} × cos {th}° = **{_fmt(ans)} J**"
    return q, ans, "J", sol


def p_power(r, g):
    W = r.choice([600, 1200, 3000, 5000, 7200])
    t = r.choice([2, 5, 10, 20, 60])
    ans = W / t
    q = f"ເຄື່ອງຈັກເຮັດງານ {W} J ໃນເວລາ {t} s. ຫາກຳລັງ (P)"
    sol = f"P = W/t = {W} / {t} = **{_fmt(ans)} W**"
    return q, ans, "W", sol


def p_spring(r, g):
    k = r.choice([100, 200, 400, 500, 1000])
    x = r.choice([0.05, 0.1, 0.2, 0.3])
    ans = elastic_pe(k, x)
    q = (
        f"ສະປຣິງມີຄ່າຄົງທີ່ k = {k} N/m ຖືກຍືດອອກ {x} m. "
        f"ຫາພະລັງງານສັກຍືດຫຍຸ່ນ"
    )
    sol = f"Ep = ½kx² = ½ × {k} × {x}² = **{_fmt(ans)} J**"
    return q, ans, "J", sol


def p_work_energy(r, g):
    m = r.choice([2, 4, 5, 10, 20])
    v1 = r.choice([2, 4, 5, 6])
    v2 = r.choice([8, 10, 12, 15])
    ans = kinetic(m, v2) - kinetic(m, v1)
    q = (
        f"ວັດຖຸມວນ {m} kg ຄວາມໄວປ່ຽນຈາກ {v1} m/s ເປັນ {v2} "
        f"m/s. ຫາງານລວມທີ່ເຮັດຕໍ່ວັດຖຸ"
    )
    sol = (
        f"W = ΔEk = ½m(v₂² − v₁²) = ½ × {m} × ({v2}² − {v1}²) "
        f"= **{_fmt(ans)} J**"
    )
    return q, ans, "J", sol


def p_incline(r, g):
    h = r.choice([1.25, 3.2, 5, 7.2, 10, 20])
    ans = math.sqrt(2 * g * h)
    al = r.choice([30, 37, 45, 53])
    q = (
        f"ວັດຖຸລື່ນລົງພື້ນເອຽງລື່ນ (ບໍ່ມີແຮງຝືດ) ມູມ {al}° "
        f"ຈາກຄວາມສູງ {h} m ຈາກສະພາບນິ່ງ "
        f"(g = {_fmt(g)}). ຫາຄວາມໄວທີ່ຕີນພື້ນເອຽງ"
    )
    sol = (
        f"mgh = ½mv²  →  v = √(2gh) = √(2 × {_fmt(g)} × "
        f"{h}) = **{_fmt(ans)} m/s** "
        f"(ບໍ່ຂຶ້ນກັບມູມ {al}° ແລະ ມວນ)"
    )
    return q, ans, "m/s", sol


def p_pendulum(r, g):
    L = r.choice([0.5, 1, 1.6, 2, 2.5])
    th = r.choice([37, 53, 60, 90])
    ans = pendulum_speed_bottom(L, th, g)
    q = (
        f"ລູກຕຸ້ມແຂວນເຊືອກຍາວ {L} m ຖືກດຶງໃຫ້ເຊືອກທຳມຸມ "
        f"{th}° ກັບແນວຕັ້ງ ແລ້ວປ່ອຍ. ຫາຄວາມໄວທີ່ຈຸດຕ່ຳສຸດ "
        f"(g = {_fmt(g)})"
    )
    sol = (
        f"ຄວາມສູງທີ່ຫຼຸດ h = L(1 − cosθ) = {L}(1 − cos {th}°) "
        f"= {_fmt(L * (1 - math.cos(math.radians(th))))} "
        f"m\n\n"
        f"v = √(2gh) = **{_fmt(ans)} m/s**"
    )
    return q, ans, "m/s", sol


def p_efficiency(r, g):
    e_in = r.choice([500, 800, 1000, 2000, 5000])
    eta = r.choice([20, 40, 50, 60, 75, 80])
    e_out = e_in * eta / 100
    q = (
        f"ເຄື່ອງຈັກຮັບພະລັງງານ {e_in} J ແລະ ໃຫ້ພະລັງງານທີ່ໃຊ້ປະໂຫຍດ "
        f"{_fmt(e_out)} J. ຫາປະສິດທິພາບ (%)"
    )
    sol = (
        f"η = E_out / E_in × 100 = {_fmt(e_out)} / {e_in} "
        f"× 100 = **{_fmt(eta)} %**"
    )
    return q, eta, "%", sol


def p_friction_stop(r, g):
    v = r.choice([4, 6, 8, 10, 12])
    mu = r.choice([0.1, 0.2, 0.25, 0.4, 0.5])
    ans = v * v / (2 * mu * g)
    q = (
        f"ກ່ອງເລື່ອນເທິງພື້ນແນວນອນມີ μ = {mu} ດ້ວຍຄວາມໄວຕົ້ນ "
        f"{v} m/s ແລ້ວຢຸດ. "
        f"ມັນເລື່ອນໄປໄກເທົ່າໃດ (g = {_fmt(g)})"
    )
    sol = (
        f"ງານຂອງແຮງຝືດ = ການປ່ຽນ Ek:  −μmg·d = 0 − ½mv²\n\n"
        f"d = v² / (2μg) = {v}² / (2 × {mu} × {_fmt(g)}) "
        f"= **{_fmt(ans)} m**"
    )
    return q, ans, "m", sol


PROBLEMS = {
    "ພະລັງງານຈົນ": p_kinetic,
    "ພະລັງງານສັກໂນ້ມຖ່ວງ": p_gpe,
    "ພະລັງງານສັກຍືດຫຍຸ່ນ": p_spring,
    "ງານ (W = Fd cosθ)": p_work,
    "ກຳລັງ": p_power,
    "ທິດສະດີງານ-ພະລັງງານ": p_work_energy,
    "ຕົກອິດສະຫຼະ": p_free_fall,
    "ພື້ນເອຽງລື່ນ": p_incline,
    "ລູກຕຸ້ມແກວ່ງ": p_pendulum,
    "ແຮງຝືດ": p_friction_stop,
    "ປະສິດທິພາບ": p_efficiency,
}

# ຄຳຖາມເລືອກຕອບ (ແນວຄິດ)
CONCEPT = [
    {
        "q": (
            "ຖ້າຄວາມໄວຂອງວັດຖຸເພີ່ມເປັນ 2 ເທົ່າ (ມວນເທົ່າເກົ່າ) "
            "ພະລັງງານຈົນຈະເປັນແນວໃດ?"
        ),
        "opts": [
            "ເພີ່ມເປັນ 2 ເທົ່າ",
            "ເພີ່ມເປັນ 4 ເທົ່າ",
            "ເພີ່ມເປັນ 8 ເທົ່າ",
            "ບໍ່ປ່ຽນ",
        ],
        "ans": 1,
        "exp": (
            "Ek = ½mv² ແປຜັນຕາມ v². ເມື່ອ v ເປັນ 2 ເທົ່າ, v² "
            "ເປັນ 4 ເທົ່າ ຈຶ່ງໄດ້ Ek ເປັນ 4 ເທົ່າ."
        ),
    },
    {
        "q": (
            "ແຮງຕັ້ງສາກກັບທິດການຍ້າຍ (ເຊັ່ນ ແຮງປົກກະຕິເທິງພື້ນແນວນອນ) "
            "ເຮັດງານເທົ່າໃດ?"
        ),
        "opts": ["ເປັນບວກ", "ເປັນລົບ", "ສູນ", "ຂຶ້ນກັບຂະໜາດຂອງແຮງ"],
        "ans": 2,
        "exp": (
            "W = Fd cosθ, ເມື່ອ θ = 90° ໄດ້ cos 90° = 0 ສະນັ້ນ "
            "W = 0."
        ),
    },
    {
        "q": (
            "ວັດຖຸຕົກອິດສະຫຼະ (ບໍ່ມີແຮງຕ້ານອາກາດ). ພະລັງງານກົນລວມ "
            "(Ek + Ep) ເປັນແນວໃດ?"
        ),
        "opts": ["ເພີ່ມຂຶ້ນ", "ຫຼຸດລົງ", "ຄົງທີ່", "ເປັນສູນ"],
        "ans": 2,
        "exp": (
            "ມີແຕ່ແຮງໂນ້ມຖ່ວງ (ແຮງອະນຸລັກ) ເຮັດງານ ຈຶ່ງອະນຸລັກພະລັງງານກົນ: "
            "Ep ຫຼຸດ, Ek ເພີ່ມ ເທົ່າກັນ."
        ),
    },
    {
        "q": (
            "ວັດຖຸຖືກຍິງໂຄ້ງດ້ວຍມູມ θ (0° < θ < 90°). ທີ່ຈຸດສູງສຸດ "
            "ພະລັງງານຈົນເປັນແນວໃດ?"
        ),
        "opts": [
            "ເປັນສູນ",
            "ບໍ່ເປັນສູນ ເພາະຍັງມີ vₓ",
            "ເທົ່າກັບຕອນເລີ່ມ",
            "ເປັນຄ່າສູງສຸດ",
        ],
        "ans": 1,
        "exp": (
            "ທີ່ຈຸດສູງສຸດ vᵧ = 0 ແຕ່ vₓ = v₀cosθ ຍັງຢູ່ ສະນັ້ນ "
            "Ek = ½m(v₀cosθ)² > 0."
        ),
    },
    {
        "q": (
            "ວັດຖຸເລື່ອນລົງພື້ນເອຽງລື່ນ (ບໍ່ມີແຮງຝືດ) ຈາກຄວາມສູງ "
            "h. ຄວາມໄວທີ່ຕີນພື້ນເອຽງຂຶ້ນກັບຫຍັງ?"
        ),
        "opts": [
            "ມວນ ແລະ ມູມພື້ນເອຽງ",
            "ມູມພື້ນເອຽງຢ່າງດຽວ",
            "ມວນຢ່າງດຽວ",
            "ຄວາມສູງ h ເທົ່ານັ້ນ",
        ],
        "ans": 3,
        "exp": (
            "mgh = ½mv² ມວນຕັດກັນໄດ້ v = √(2gh) ບໍ່ຂຶ້ນກັບມູມ "
            "ຫຼື ມວນ."
        ),
    },
    {
        "q": "ເມື່ອມີແຮງຝືດ ພະລັງງານກົນຂອງລະບົບທີ່ຫຼຸດໄປ ໄປໃສ?",
        "opts": [
            "ຫາຍໄປເລີຍ",
            "ປ່ຽນເປັນຄວາມຮ້ອນ (ພະລັງງານລວມຍັງຄົງ)",
            "ປ່ຽນເປັນມວນ",
            "ປ່ຽນເປັນພະລັງງານສັກ",
        ],
        "ans": 1,
        "exp": (
            "ພະລັງງານບໍ່ສູນຫາຍ ມັນປ່ຽນຮູບເປັນຄວາມຮ້ອນ ແລະ ສຽງ. "
            "ພະລັງງານລວມທຸກຮູບແບບຍັງຄົງທີ່."
        ),
    },
    {
        "q": "ຫົວໜ່ວຍ watt (W) ເທົ່າກັບຫຍັງ?",
        "opts": ["N·m", "J/s", "kg·m/s", "N/s"],
        "ans": 1,
        "exp": "ກຳລັງ P = W/t ສະນັ້ນ 1 W = 1 J/s.",
    },
    {
        "q": "1 kWh ເທົ່າກັບຈັກ joule?",
        "opts": ["1 000 J", "60 000 J", "3.6 × 10⁶ J", "3.6 × 10³ J"],
        "ans": 2,
        "exp": "1 kWh = 1000 W × 3600 s = 3.6 × 10⁶ J.",
    },
    {
        "q": "ເຄື່ອງຈັກຊະນິດໜຶ່ງສາມາດມີປະສິດທິພາບເກີນ 100% ໄດ້ບໍ?",
        "opts": [
            "ໄດ້ ຖ້າອອກແບບດີ",
            "ໄດ້ ຖ້າບໍ່ມີແຮງຝືດ",
            "ບໍ່ໄດ້ ເພາະຈະຂັດກັບການອະນຸລັກພະລັງງານ",
            "ໄດ້ ຖ້າໃຊ້ສະປຣິງ",
        ],
        "ans": 2,
        "exp": (
            "ພະລັງງານທີ່ໄດ້ອອກຕ້ອງບໍ່ເກີນພະລັງງານທີ່ໃສ່ເຂົ້າ "
            "ສະນັ້ນ η ≤ 100%."
        ),
    },
    {
        "q": "ແຮງຝືດຈະເຮັດງານແບບໃດ ເມື່ອວັດຖຸເລື່ອນໄປ?",
        "opts": [
            "ງານເປັນບວກ",
            "ງານເປັນລົບ",
            "ງານເປັນສູນສະເໝີ",
            "ງານບໍ່ມີຄວາມໝາຍ",
        ],
        "ans": 1,
        "exp": (
            "ແຮງຝືດມີທິດກົງກັນຂ້າມກັບການເຄື່ອນທີ່ (θ = 180°) "
            "ສະນັ້ນ W = −fd, ຫຼຸດ Ek ຂອງວັດຖຸ."
        ),
    },
]


# =====================================================
# ສ່ວນທີ 3: ໜ້າເວັບ Streamlit
# =====================================================
st.set_page_config(page_title="ພະລັງງານ", layout="wide")
st.title("ງານ ແລະ ພະລັງງານ (Work and Energy)")

with st.sidebar:
    st.header("ຄ່າຄົງທີ່")
    g = st.number_input("g (m/s²)", min_value=0.1, value=10.0, step=0.1)
    st.caption("ໃຊ້ g = 10 ຕາມບົດຮຽນ, ຫຼື 9.8 ຖ້າຕ້ອງການຄ່າລະອຽດ")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["ຫຼັກການ", "ເຄື່ອງຄິດໄລ່", "ການອະນຸລັກພະລັງງານ", "ໂຈດຝຶກຫັດ", "ຄຳຖາມແນວຄິດ"]
)

# ---------------- TAB 1: ຫຼັກການ ----------------
with tab1:
    st.markdown(
        """
**ພະລັງງານ (Energy)** ຄືຄວາມສາມາດໃນການເຮັດງານ ມີຫົວໜ່ວຍເປັນ **joule (J)**.
**ງານ (Work)** ຄືພະລັງງານທີ່ຖືກຖ່າຍທອດ ໂດຍແຮງທີ່ເຮັດໃຫ້ວັດຖຸເຄື່ອນທີ່.
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("1) ງານ")
        st.latex(r"W = F\,d\cos\theta")
        st.markdown(
            "- θ = 0°: ແຮງໄປທິດດຽວກັບການຍ້າຍ → W = Fd (ບວກ)\n"
            "- θ = 90°: ແຮງຕັ້ງສາກກັບການຍ້າຍ → W = 0\n"
            "- θ = 180°: ແຮງສວນທິດ (ເຊັ່ນ ແຮງຝືດ) → W = −Fd (ລົບ)"
        )

        st.subheader("2) ພະລັງງານຈົນ (Kinetic Energy)")
        st.latex(r"E_k = \tfrac12 m v^2")

        st.subheader("3) ພະລັງງານສັກ (Potential Energy)")
        st.latex(r"E_p = mgh\quad(\text{ໂນ້ມຖ່ວງ})")
        st.latex(r"E_p = \tfrac12 k x^2\quad(\text{ສະປຣິງ})")

        st.subheader("4) ກຳລັງ (Power)")
        st.latex(r"P = \frac{W}{t} = F\,v\cos\theta")
        st.markdown("1 W = 1 J/s,  1 kW = 1000 W,  1 kWh = 3.6 × 10⁶ J")

    with c2:
        st.subheader("5) ທິດສະດີງານ-ພະລັງງານ")
        st.latex((
            r"W_{net} = \Delta E_k = \tfrac12 m v_2^2-\tfrac12 "
            r"m v_1^2"
        ))
        st.markdown("ງານລວມຂອງທຸກແຮງ ເທົ່າກັບການປ່ຽນແປງພະລັງງານຈົນ.")

        st.subheader("6) ການອະນຸລັກພະລັງງານກົນ")
        st.latex(r"E_{k1}+E_{p1}=E_{k2}+E_{p2}")
        st.latex((
            r"\tfrac12 m v_1^2 + mgh_1 = \tfrac12 m v_2^2 + "
            r"mgh_2"
        ))
        st.markdown((
            "ໃຊ້ໄດ້ເມື່ອມີແຕ່ **ແຮງອະນຸລັກ** (ໂນ້ມຖ່ວງ, ແຮງສະປຣິງ) "
            "ເຮັດງານ."
        ))

        st.subheader("7) ເມື່ອມີແຮງຝືດ")
        st.latex(r"E_{k1}+E_{p1} = E_{k2}+E_{p2} + Q")
        st.latex((
            r"Q = f\,d = \mu N d\quad\Rightarrow\quad Q=\mu "
            r"mg\cos\alpha\cdot s\ \ (\text{ພື້ນເອຽງ})"
        ))

        st.subheader("8) ປະສິດທິພາບ")
        st.latex((
            r"\eta = \frac{E_{out}}{E_{in}}\times 100\%\ \ (\le "
            r"100\%)"
        ))

        st.subheader("9) ສູດທີ່ໃຊ້ໃຫ້ໄວ")
        st.latex(r"v=\sqrt{2gh}\ \ (\text{ຕົກ ຫຼື ລື່ນລົງ ບໍ່ມີຝືດ})")
        st.latex(r"v=\sqrt{2gL(1-\cos\theta)}\ \ (\text{ລູກຕຸ້ມແກວ່ງ})")
        st.latex(r"v=x\sqrt{k/m}\ \ (\text{ສະປຣິງຍິງວັດຖຸ})")

    st.info(
        "ເຄັດລັບການເລືອກວິທີ: ຖ້າບໍ່ມີແຮງຝືດ ແລະ ບໍ່ຖາມເວລາ "
        "→ ໃຊ້ອະນຸລັກພະລັງງານ (ງ່າຍກວ່າໃຊ້ກົດຂອງນິວຕັນ)."
    )

# ---------------- TAB 2: ເຄື່ອງຄິດໄລ່ ----------------
with tab2:
    calc = st.selectbox(
        "ເລືອກຫົວຂໍ້",
        [
            "ພະລັງງານຈົນ Ek",
            "ພະລັງງານສັກໂນ້ມຖ່ວງ Ep",
            "ພະລັງງານສັກຍືດຫຍຸ່ນ",
            "ງານ W = Fd cosθ",
            "ກຳລັງ P",
            "ປະສິດທິພາບ η",
            "ຄວາມໄວຈາກການອະນຸລັກພະລັງງານ",
            "ທິດສະດີງານ-ພະລັງງານ (ຫາ v₂)",
            "ລູກຕຸ້ມແກວ່ງ",
            "ສະປຣິງຍິງວັດຖຸ",
        ],
    )

    def num(label, value, key, lo=0.0, step=1.0):
        return st.number_input(label, min_value=lo, value=float(value), step=step, key=f"{calc}_{key}")

    if calc.startswith("ພະລັງງານຈົນ"):
        m = num("ມວນ m (kg)", 2.0, "m", 0.001)
        v = num("ຄວາມໄວ v (m/s)", 10.0, "v")
        st.success((
            f"Ek = ½mv² = ½ × {m} × {v}² = **{kinetic(m, v):.3f} "
            f"J**"
        ))

    elif calc.startswith("ພະລັງງານສັກໂນ້ມຖ່ວງ"):
        m = num("ມວນ m (kg)", 2.0, "m", 0.001)
        h = num("ຄວາມສູງ h (m)", 5.0, "h")
        st.success((
            f"Ep = mgh = {m} × {g} × {h} = **{grav_pe(m, g, h):.3f} "
            f"J**"
        ))

    elif calc.startswith("ພະລັງງານສັກຍືດຫຍຸ່ນ"):
        k = num("ຄ່າຄົງທີ່ສະປຣິງ k (N/m)", 200.0, "k", 0.001)
        x = num("ການຍືດ/ອັດ x (m)", 0.1, "x", 0.0, 0.01)
        st.success((
            f"Ep = ½kx² = ½ × {k} × {x}² = **{elastic_pe(k, x):.4f} "
            f"J**"
        ))

    elif calc.startswith("ງານ"):
        F = num("ແຮງ F (N)", 50.0, "F")
        d = num("ໄລຍະຍ້າຍ d (m)", 10.0, "d")
        th = st.slider("ມູມ θ ລະຫວ່າງແຮງ ແລະ ການຍ້າຍ (°)", 0, 180, 37, key="W_th")
        st.success((
            f"W = Fd cosθ = {F} × {d} × cos {th}° = **{work(F, d, th):.3f} "
            f"J**"
        ))
        if th > 90:
            st.caption("θ > 90° ງານເປັນລົບ (ແຮງຕ້ານການເຄື່ອນທີ່)")

    elif calc.startswith("ກຳລັງ"):
        mode = st.radio("ໃຊ້ສູດ", ["P = W / t", "P = F v cosθ"], horizontal=True)
        if mode == "P = W / t":
            W = num("ງານ W (J)", 3000.0, "W")
            t = num("ເວລາ t (s)", 10.0, "t", 0.001)
            P = power_from_work(W, t)
        else:
            F = num("ແຮງ F (N)", 500.0, "F2")
            v = num("ຄວາມໄວ v (m/s)", 4.0, "v2")
            th = st.slider("ມູມ θ (°)", 0, 90, 0, key="P_th")
            P = power_from_force(F, v, th)
        st.success(f"P = **{P:.3f} W**  (= {P / 1000:.4f} kW)")

    elif calc.startswith("ປະສິດທິພາບ"):
        ein = num("ພະລັງງານເຂົ້າ (J)", 1000.0, "ein", 0.001)
        eout = num("ພະລັງງານທີ່ໃຊ້ປະໂຫຍດ (J)", 600.0, "eout")
        if eout > ein:
            st.error("ພະລັງງານອອກຕ້ອງບໍ່ເກີນພະລັງງານເຂົ້າ")
        else:
            st.success((
                f"η = {eout}/{ein} × 100 = **{efficiency(eout, ein):.2f} "
                f"%**"
            ))
            st.write((
                f"ພະລັງງານທີ່ສູນເສຍ (ເປັນຄວາມຮ້ອນ ແລະ ອື່ນໆ) = **{ein - eout:.2f} "
                f"J**"
            ))

    elif calc.startswith("ຄວາມໄວຈາກ"):
        v1 = num("ຄວາມໄວຕົ້ນ v₁ (m/s)", 0.0, "v1")
        h1 = num("ຄວາມສູງຕົ້ນ h₁ (m)", 20.0, "h1")
        h2 = num("ຄວາມສູງປາຍ h₂ (m)", 0.0, "h2")
        v2 = speed_conserve(v1, h1, h2, g)
        if v2 is None:
            st.error("ວັດຖຸຂຶ້ນໄປບໍ່ເຖິງລະດັບ h₂")
        else:
            st.success(f"v₂ = √(v₁² + 2g(h₁ − h₂)) = **{v2:.3f} m/s**")

    elif calc.startswith("ທິດສະດີງານ"):
        m = num("ມວນ m (kg)", 5.0, "m", 0.001)
        v1 = num("ຄວາມໄວຕົ້ນ v₁ (m/s)", 2.0, "v1")
        Wn = st.number_input("ງານລວມ W_net (J) (ລົບໄດ້)", value=100.0, step=10.0, key="W_net")
        v2 = speed_from_net_work(m, v1, Wn)
        if v2 is None:
            st.error("ງານລົບໃຫຍ່ເກີນ ວັດຖຸຈະຢຸດກ່ອນ")
        else:
            st.success(f"v₂ = √(v₁² + 2W/m) = **{v2:.3f} m/s**")

    elif calc.startswith("ລູກຕຸ້ມ"):
        L = num("ຄວາມຍາວເຊືອກ L (m)", 2.0, "L", 0.01)
        th = st.slider("ມູມປ່ອຍຈາກແນວຕັ້ງ θ (°)", 0, 90, 60, key="pen_th")
        h = L * (1 - math.cos(math.radians(th)))
        v = pendulum_speed_bottom(L, th, g)
        st.success((
            f"h = L(1 − cosθ) = {h:.3f} m   →   v ຈຸດຕ່ຳສຸດ "
            f"= √(2gh) = **{v:.3f} m/s**"
        ))

    else:
        k = num("k (N/m)", 400.0, "k", 0.001)
        x = num("ການອັດ x (m)", 0.1, "x", 0.0, 0.01)
        m = num("ມວນວັດຖຸ m (kg)", 0.5, "m", 0.001)
        v = spring_launch_speed(k, x, m)
        st.success(f"½kx² = ½mv²  →  v = x√(k/m) = **{v:.3f} m/s**")

# ---------------- TAB 3: ອະນຸລັກພະລັງງານ ----------------
with tab3:
    st.markdown("ວັດຖຸເລື່ອນລົງພື້ນເອຽງ ເບິ່ງວ່າພະລັງງານປ່ຽນຮູບແນວໃດ")
    a, b, c, d = st.columns(4)
    m3 = a.number_input("ມວນ m (kg)", min_value=0.1, value=2.0, step=0.5, key="m3")
    h3 = b.number_input("ຄວາມສູງ h₀ (m)", min_value=0.1, value=5.0, step=0.5, key="h3")
    al3 = c.number_input("ມູມພື້ນເອຽງ α (°)", min_value=5.0, max_value=85.0, value=37.0, step=1.0, key="al3")
    mu3 = d.number_input("ສຳປະສິດຝືດ μ", min_value=0.0, max_value=1.5, value=0.0, step=0.05, key="mu3")

    total, rows = incline_slide(m3, h3, al3, mu3, g)
    # ຕັດຕອນທີ່ Ek < 0 (ຢຸດ)
    valid = [r for r in rows if r[3] >= -1e-9]
    if mu3 >= math.tan(math.radians(al3)):
        st.warning("μ ≥ tanα ວັດຖຸຈະບໍ່ເລື່ອນເອງ (ແຮງຝືດສະຖິດຕ້ານໄວ້)")
    else:
        frac = st.slider("ຕຳແໜ່ງຕາມພື້ນເອຽງ (0 = ເທິງສຸດ, 1 = ຕີນພື້ນເອຽງ)", 0.0, 1.0, 0.5, 0.01)
        s = total * frac
        h = h3 - s * math.sin(math.radians(al3))
        q = mu3 * m3 * g * math.cos(math.radians(al3)) * s
        ek = m3 * g * (h3 - h) - q
        ep = m3 * g * h
        v = math.sqrt(2 * ek / m3) if ek > 0 else 0.0

        mm = st.columns(5)
        mm[0].metric("ໄລຍະຕາມພື້ນເອຽງ s (m)", f"{s:.2f}")
        mm[1].metric("ຄວາມສູງ h (m)", f"{h:.2f}")
        mm[2].metric("ຄວາມໄວ v (m/s)", f"{v:.2f}")
        mm[3].metric("Ek (J)", f"{ek:.2f}")
        mm[4].metric("Ep (J)", f"{ep:.2f}")
        st.bar_chart(
            pd.DataFrame(
                {
                    "ພະລັງງານ (J)": [ep, ek, q, ep + ek + q],
                },
                index=["Ep (ສັກ)", "Ek (ຈົນ)", "Q (ຄວາມຮ້ອນ)", "ລວມ"],
            )
        )
        st.caption(
            f"ພະລັງງານລວມ = Ep + Ek + Q = {ep + ek + q:.2f} "
            f"J ຄົງທີ່ສະເໝີ "
            f"(= mgh₀ = {m3 * g * h3:.2f} J). "
            + ("ບໍ່ມີຝືດ: Ep + Ek ຄົງທີ່." if mu3 == 0 else "ມີຝືດ: Ep + Ek ຫຼຸດລົງ ເພາະກາຍເປັນ Q.")
        )

        df = pd.DataFrame(
            {
                "s (m)": [r[0] for r in rows],
                "Ep": [r[2] for r in rows],
                "Ek": [r[3] for r in rows],
                "Q": [r[4] for r in rows],
            }
        )
        st.line_chart(df, x="s (m)", y=["Ep", "Ek", "Q"])
        if len(valid) == len(rows):
            st.write(
                f"ຄວາມໄວທີ່ຕີນພື້ນເອຽງ = **{math.sqrt(2 * rows[-1][3] / m3):.3f} "
                f"m/s**"
                + (f"  (ຖ້າບໍ່ມີຝືດ: {math.sqrt(2 * g * h3):.3f} m/s)" if mu3 > 0 else "")
            )

# ---------------- TAB 4: ໂຈດຝຶກຫັດ ----------------
with tab4:
    st.session_state.setdefault("seed", 1)
    st.session_state.setdefault("score", [0, 0])  # [ຖືກ, ທັງໝົດ]

    topic = st.selectbox("ເລືອກຫົວຂໍ້", ["ສຸ່ມທຸກຫົວຂໍ້"] + list(PROBLEMS.keys()))
    seed = st.session_state["seed"]
    rng = random.Random(seed)
    if topic == "ສຸ່ມທຸກຫົວຂໍ້":
        fn = rng.choice(list(PROBLEMS.values()))
    else:
        fn = PROBLEMS[topic]
    q, ans, unit, sol = fn(rng, g)
    kid = f"{topic}_{seed}"

    st.markdown(f"#### ໂຈດ #{seed}")
    st.write(q)
    user = st.number_input(f"ຄຳຕອບ ({unit})", value=0.0, format="%.3f", key=f"u_{kid}")
    c1, c2, c3 = st.columns([1, 1, 3])
    if c1.button("ກວດຄຳຕອບ", key=f"chk_{kid}"):
        if f"ok_{kid}" not in st.session_state:
            ok = abs(user - ans) <= 0.02 * abs(ans) + 1e-9
            st.session_state[f"ok_{kid}"] = ok
            st.session_state["score"][1] += 1
            if ok:
                st.session_state["score"][0] += 1
    if c2.button("ໂຈດຕໍ່ໄປ", key=f"nxt_{kid}"):
        st.session_state["seed"] += 1
        st.rerun()

    if f"ok_{kid}" in st.session_state:
        if st.session_state[f"ok_{kid}"]:
            st.success("ຖືກຕ້ອງ!")
        else:
            st.error("ຍັງບໍ່ຖືກ ລອງຄິດໃໝ່ ຫຼື ເບິ່ງວິທີເຮັດ")
    with st.expander("ເບິ່ງວິທີເຮັດ ແລະ ຄຳຕອບ"):
        st.markdown(sol)
    right, total_q = st.session_state["score"]
    st.caption((
        f"ຄະແນນ: {right} / {total_q} (ຍອມຮັບຄວາມຄາດເຄື່ອນ "
        f"±2%)"
    ))

# ---------------- TAB 5: ຄຳຖາມແນວຄິດ ----------------
with tab5:
    st.session_state.setdefault("cidx", 0)
    st.session_state.setdefault("cscore", [0, 0])
    idx = st.session_state["cidx"] % len(CONCEPT)
    item = CONCEPT[idx]

    st.markdown(f"#### ຂໍ້ {idx + 1} / {len(CONCEPT)}")
    st.write(item["q"])
    choice = st.radio("ເລືອກຄຳຕອບ", item["opts"], index=None, key=f"c_{idx}")
    c1, c2 = st.columns([1, 1])
    if c1.button("ກວດຄຳຕອບ", key=f"cchk_{idx}"):
        if choice is None:
            st.warning("ກະລຸນາເລືອກຄຳຕອບກ່ອນ")
        else:
            ok = item["opts"].index(choice) == item["ans"]
            if f"cok_{idx}" not in st.session_state:
                st.session_state[f"cok_{idx}"] = ok
                st.session_state["cscore"][1] += 1
                st.session_state["cscore"][0] += int(ok)
    if c2.button("ຂໍ້ຕໍ່ໄປ", key=f"cnxt_{idx}"):
        st.session_state["cidx"] += 1
        st.rerun()

    if f"cok_{idx}" in st.session_state:
        if st.session_state[f"cok_{idx}"]:
            st.success("ຖືກຕ້ອງ!")
        else:
            st.error(f"ບໍ່ຖືກ. ຄຳຕອບທີ່ຖືກ: **{item['opts'][item['ans']]}**")
        st.info(item["exp"])
    st.caption(f"ຄະແນນ: {st.session_state['cscore'][0]} / {st.session_state['cscore'][1]}")