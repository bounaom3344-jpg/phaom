# python -m streamlit run optic.py
# ຮັນດ້ວຍຄຳສັ່ງນີ້ໃນ Terminal (ບໍ່ແມ່ນພິມໃນໂປຣແກຣມ):
#     python -m streamlit run optic.py
# ຕິດຕັ້ງຄັ້ງທຳອິດ:  pip install streamlit matplotlib
"""ແສງເລຂາຄະນິດ: ກະຈົກ ແລະ ເລນບາງ (ສູດ, ເຄື່ອງຄິດໄລ່, ບົດເລກ, ຮູບລັງສີ)
ກົດເຄື່ອງໝາຍ: ພາບຈິງເປັນບວກ. f > 0: ກະຈົກເວ້າ/ເລນນູນ, f < 0: ກະຈົກນູນ/ເລນເວ້າ"""
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import streamlit as st

# ຟອນລາວສຳລັບຮູບ matplotlib (Leelawadee UI ມີໃນ Windows)
_have = {f.name for f in font_manager.fontManager.ttflist}
for _f in ("Noto Sans Lao", "Leelawadee UI", "Phetsarath OT", "Saysettha OT", "Tahoma"):
    if _f in _have:
        plt.rcParams["font.family"] = _f
        break
plt.rcParams["axes.unicode_minus"] = False

# ຊື່, ເຄື່ອງໝາຍ f, ເປັນກະຈົກ?, ເປັນກະຈົກພຽງ?
TYPES = {
    "ກະຈົກເວ້າ": (+1, True, False),
    "ກະຈົກນູນ": (-1, True, False),
    "ກະຈົກພຽງ": (0, True, True),
    "ເລນນູນ (ລວມແສງ)": (+1, False, False),
    "ເລນເວ້າ (ກະຈາຍແສງ)": (-1, False, False),
}


def f2(x):
    v = round(x, 2)
    return f"{0.0 if v == 0 else v:g}"


def solve(name, F, s, h):
    sign, is_mirror, plane = TYPES[name]
    r = dict(name=name, s=s, h=h, steps=[], inf=False)
    st_ = r["steps"]
    if plane:
        r.update(f=float("inf"), sp=-s, m=1.0, hp=h)
        st_ += ["ກະຈົກພຽງ: f → ∞ ດັ່ງນັ້ນ 1/s′ = −1/s",
                f"s′ = −s = −{f2(s)} cm (ລົບ = ພາບເສມືອນຢູ່ຫຼັງກະຈົກ)",
                f"m = −s′/s = +1,  h′ = h = {f2(h)} cm"]
    else:
        f = sign * F
        r["f"] = f
        st_.append(f"f = {'+' if f > 0 else '−'}{f2(F)} cm  ({name}: f {'> 0' if f > 0 else '< 0'})")
        if abs(s - f) < 1e-9:
            r["inf"] = True
            st_.append("s = f ⇒ 1/s′ = 0 ⇒ s′ → ∞: ລັງສີອອກຂະໜານກັນ, ບໍ່ເກີດພາບ")
            return r
        st_.append(f"1/s′ = 1/f − 1/s = 1/({f2(f)}) − 1/{f2(s)} = {f2(1/f - 1/s)} cm⁻¹")
        sp = f * s / (s - f)
        m = -sp / s
        r.update(sp=sp, m=m, hp=m * h)
        st_ += [f"s′ = {f2(sp)} cm",
                f"m = −s′/s = −({f2(sp)})/{f2(s)} = {f2(m)}",
                f"h′ = m·h = {f2(m)} × {f2(h)} = {f2(m * h)} cm"]
    r["real"] = r["sp"] > 0
    a = abs(r["m"])
    size = "ຂະຫຍາຍ" if a > 1.0001 else "ຫຍໍ້" if a < 0.9999 else "ເທົ່າເດີມ"
    r["nature"] = f"ພາບ{'ຈິງ' if r['real'] else 'ເສມືອນ'}, {'ຕັ້ງ' if r['m'] > 0 else 'ກັບຫົວ'}, {size}"
    st_.append("ສະຫຼຸບ: " + r["nature"])
    return r


def make_fig(r):
    sign, is_mirror, plane = TYPES[r["name"]]
    s, h = r["s"], r["h"]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axhline(0, color="gray", lw=1)
    A = abs(r["f"])
    reach = max(s, 2 * A if A != float("inf") else s)
    if not r["inf"]:
        reach = max(reach, min(abs(r["sp"]), 3 * reach))
    reach *= 1.15
    ym = max(h, 0 if r["inf"] else abs(r["hp"])) * 1.6
    H = ym * 0.95

    if is_mirror and not plane:
        bow = 0.04 * reach * (1 if sign > 0 else -1)
        ys = [H * (2 * i / 60 - 1) for i in range(61)]
        ax.plot([bow * (1 - (y / H) ** 2) for y in ys], ys, color="tab:blue", lw=3)
    else:
        ax.plot([0, 0], [-H, H], color="tab:blue", lw=3)
        if not is_mirror:
            up, dn = ("^", "v") if sign > 0 else ("v", "^")
            ax.plot([0], [H], marker=up, color="tab:blue", ms=10)
            ax.plot([0], [-H], marker=dn, color="tab:blue", ms=10)
    if not plane:
        if is_mirror:
            g = -1 if sign > 0 else 1
            marks = [(g * A, "F"), (g * 2 * A, "C")]
        else:
            marks = [(-A, "F"), (A, "F′"), (-2 * A, "2F"), (2 * A, "2F′")]
        for x, lb in marks:
            ax.plot(x, 0, "k|", ms=10)
            ax.text(x, -ym * 0.12, lb, ha="center", va="top")

    ax.annotate("", xy=(-s, h), xytext=(-s, 0), arrowprops=dict(arrowstyle="-|>", color="black", lw=2.5))
    ax.text(-s, h + ym * 0.05, "ວັດຖຸ", ha="center")
    if r["inf"]:
        ax.set_title(f"{r['name']}: s = f (ບໍ່ເກີດພາບ)")
    else:
        Xi = -r["sp"] if is_mirror else r["sp"]
        I, T = (Xi, r["hp"]), (-s, h)
        for P in ((0, h), (0, 0)):
            ax.plot([T[0], P[0]], [T[1], P[1]], color="tab:red", lw=1.6)
            dx, dy = I[0] - P[0], I[1] - P[1]
            if r["real"]:
                ax.plot([P[0], I[0] + .3 * dx], [P[1], I[1] + .3 * dy], color="tab:red", lw=1.6)
            else:
                ax.plot([P[0], P[0] - dx], [P[1], P[1] - dy], color="tab:red", lw=1.6)
                ax.plot([P[0], I[0]], [P[1], I[1]], color="tab:red", lw=1.2, ls="--")
        ax.annotate("", xy=I, xytext=(I[0], 0),
                    arrowprops=dict(arrowstyle="-|>", color="teal", lw=2.5, ls="-" if r["real"] else "--"))
        ax.text(I[0], I[1] + (1 if I[1] >= 0 else -1.6) * ym * 0.06, "ພາບ", ha="center", color="teal")
        ax.set_title(f"{r['name']}:  s′ = {f2(r['sp'])} cm,  m = {f2(r['m'])},  {r['nature']}")
    ax.set_xlim(-reach, reach)
    ax.set_ylim(-ym, ym)
    ax.set_xlabel("ໄລຍະຕາມແກນ (cm)")
    ax.set_ylabel("ຄວາມສູງ (cm)")
    ax.grid(alpha=.25)
    fig.tight_layout()
    return fig


def show_result(r):
    if not r["inf"]:
        c1, c2, c3 = st.columns(3)
        c1.metric("ໄລຍະພາບ s′", f"{f2(r['sp'])} cm")
        c2.metric("ກຳລັງຂະຫຍາຍ m", f2(r["m"]))
        c3.metric("ຄວາມສູງພາບ h′", f"{f2(r['hp'])} cm")
        st.info(r["nature"])
    st.markdown("**ວິທີຄິດໄລ່**")
    for i, line in enumerate(r["steps"], 1):
        st.write(f"{i}. {line}")
    fig = make_fig(r)
    st.pyplot(fig)
    plt.close(fig)


ASK = {"sp": "ໄລຍະພາບ s′ (cm)", "m": "ກຳລັງຂະຫຍາຍ m", "hp": "ຄວາມສູງພາບ h′ (cm)"}


def make_problem(only=None):
    name = only or random.choice(["ກະຈົກເວ້າ", "ກະຈົກນູນ", "ເລນນູນ (ລວມແສງ)", "ເລນເວ້າ (ກະຈາຍແສງ)"])
    F = random.choice([8, 10, 12, 15, 18, 20, 24, 25, 30])
    if TYPES[name][0] > 0:
        s = F
        while s == F:
            s = round(F * random.choice([.5, .75, 1.5, 2, 2.5, 3]) * 2) / 2
    else:
        s = random.choice([10, 15, 20, 30, 40])
    h = random.choice([2, 3, 4, 5, 6])
    ask = random.choice(list(ASK))
    el = "ກະຈົກ" if TYPES[name][1] else "ເລນ"
    text = (f"ວັດຖຸສູງ {h} cm ວາງຫ່າງຈາກ{name.split(' ')[0]} {s:g} cm. "
            f"{el}ມີຄວາມຍາວໂຟກັສ {F} cm. ຈົ່ງຄິດໄລ່ {ASK[ask]}.")
    return dict(text=text, ask=ask, r=solve(name, F, s, h))


def tab_formulas():
    st.subheader("ສູດຫຼັກ")
    st.latex(r"\frac{1}{f}=\frac{1}{s}+\frac{1}{s'}")
    st.latex(r"m=\frac{h'}{h}=-\frac{s'}{s}")
    st.latex(r"f=\frac{R}{2}\quad(\text{ກະຈົກໂຄ້ງ})")
    st.latex(r"\frac{1}{f}=(n-1)\left(\frac{1}{R_1}-\frac{1}{R_2}\right)\quad(\text{ສົມຜົນຜູ້ຜະລິດເລນ})")
    st.latex(r"P=\frac{1}{f}\ (\text{ດິອອບເຕີ, } f \text{ ເປັນແມັດ})")
    st.markdown("""
**ກົດເຄື່ອງໝາຍ (ພາບຈິງເປັນບວກ)**
- s > 0 ວັດຖຸຢູ່ດ້ານໜ້າຂອງກະຈົກ/ເລນ
- s′ > 0 ພາບຈິງ, s′ < 0 ພາບເສມືອນ
- f > 0 ກະຈົກເວ້າ / ເລນນູນ; f < 0 ກະຈົກນູນ / ເລນເວ້າ
- m > 0 ພາບຕັ້ງ, m < 0 ພາບກັບຫົວ, |m| > 1 ພາບຂະຫຍາຍ

**ລັງສີຫຼັກ**
- ກະຈົກເວ້າ: ຂະໜານແກນ → ສະທ້ອນຜ່ານ F; ຕົກທີ່ຈຸດຍອດ → ສະທ້ອນມຸມເທົ່າກັນ
- ເລນນູນ: ຂະໜານແກນ → ຫັກເຫຜ່ານ F′; ຜ່ານຈຸດສູນກາງເລນ → ຜ່ານຊື່
- ກະຈົກນູນ / ເລນເວ້າ: ພາບເສມືອນ ຕັ້ງ ແລະ ນ້ອຍກວ່າ ສະເໝີ
""")
    st.table({"ຕຳແໜ່ງວັດຖຸ": ["s > 2f", "s = 2f", "f < s < 2f", "s = f", "s < f"],
              "ພາບ (ກະຈົກເວ້າ / ເລນນູນ)": ["ຈິງ, ກັບຫົວ, ນ້ອຍກວ່າ", "ຈິງ, ກັບຫົວ, ເທົ່າເດີມ",
                                          "ຈິງ, ກັບຫົວ, ໃຫຍ່ກວ່າ", "ບໍ່ເກີດພາບ", "ເສມືອນ, ຕັ້ງ, ໃຫຍ່ກວ່າ"]})


def tab_calc():
    name = st.selectbox("ປະເພດ", list(TYPES))
    plane = TYPES[name][2]
    c1, c2, c3 = st.columns(3)
    F = c1.number_input("ຄວາມຍາວໂຟກັສ |f| (cm)", min_value=0.1, value=15.0, step=1.0, disabled=plane)
    s = c2.number_input("ໄລຍະວັດຖຸ s (cm)", min_value=0.1, value=40.0, step=1.0)
    h = c3.number_input("ຄວາມສູງວັດຖຸ h (cm)", min_value=0.1, value=4.0, step=0.5)
    show_result(solve(name, F, s, h))


def tab_problems():
    if "score" not in st.session_state:
        st.session_state.score = [0, 0]
        st.session_state.p = make_problem()
        st.session_state.done = False
    opt = st.selectbox("ປະເພດບົດເລກ", ["ສຸ່ມທັງໝົດ"] + [k for k in TYPES if k != "ກະຈົກພຽງ"])
    if st.button("ບົດໃໝ່"):
        st.session_state.p = make_problem(None if opt == "ສຸ່ມທັງໝົດ" else opt)
        st.session_state.done = False
        st.session_state.pop("ans", None)
    p = st.session_state.p
    st.markdown(f"#### {p['text']}")
    st.caption("ໃສ່ເຄື່ອງໝາຍຕາມກົດ (s′ > 0 = ພາບຈິງ, m > 0 = ພາບຕັ້ງ)")
    a = st.number_input("ຄຳຕອບ", value=0.0, step=0.1, format="%.2f", key="ans")
    c1, c2 = st.columns(2)
    check, reveal = c1.button("ກວດຄຳຕອບ"), c2.button("ເບິ່ງວິທີແກ້")
    c = p["r"][p["ask"]]
    if check:
        ok = abs(a - c) <= max(0.02 * abs(c), 0.05)
        if not st.session_state.done:
            st.session_state.score[1] += 1
            st.session_state.score[0] += ok
            st.session_state.done = ok
        if ok:
            st.success(f"ຖືກຕ້ອງ! ຄຳຕອບ = {f2(c)}")
            show_result(p["r"])
        else:
            st.error("ຍັງບໍ່ຖືກ, ກວດເຄື່ອງໝາຍ ແລະ ໜ່ວຍ ແລ້ວລອງໃໝ່")
    if reveal:
        if not st.session_state.done:
            st.session_state.score[1] += 1
            st.session_state.done = True
        st.warning(f"ຄຳຕອບ = {f2(c)}")
        show_result(p["r"])
    st.caption(f"ຄະແນນ: ຖືກ {st.session_state.score[0]} / {st.session_state.score[1]} ບົດ")


def main():
    st.set_page_config(page_title="ແສງເລຂາຄະນິດ", layout="centered")
    st.title("ແສງເລຂາຄະນິດ")
    st.caption("ກະຈົກ ແລະ ເລນບາງ: ສູດ, ວິທີຄິດໄລ່, ບົດເລກ ແລະ ແຜນພາບລັງສີ")
    t1, t2, t3 = st.tabs(["ສູດ ແລະ ກົດ", "ເຄື່ອງຄິດໄລ່", "ບົດເລກ"])
    with t1:
        tab_formulas()
    with t2:
        tab_calc()
    with t3:
        tab_problems()


main()