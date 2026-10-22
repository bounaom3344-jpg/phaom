#python -m streamlit run projectile.py
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Projectile Motion", layout="wide")
st.title("ການເຄື່ອນທີ່ແບບໂຄ້ງ (Projectile Motion)")
st.write(
    "ການເຄື່ອນທີ່ແບບໂຄ້ງແຍກເປັນ **ສອງແກນທີ່ເປັນອິດສະຫຼະຕໍ່ກັນ**: "
    "ແກນນອນເປັນການເຄື່ອນທີ່ຊື່ສະໝໍ່າສະເໝີ (ຄວາມໄວຄົງທີ່) "
    "ແລະ ແກນຕັ້ງເປັນການເຄື່ອນທີ່ດ້ວຍຄວາມເລັ່ງຄົງທີ່ (ຕົກອິດສະຫຼະ)."
)

# ---------------- ຮັບຄ່າຈາກຜູ້ໃຊ້ ----------------
with st.sidebar:
    st.header("ຕັ້ງຄ່າ")
    v0 = st.slider("ຄວາມໄວເລີ່ມຕົ້ນ v₀ (m/s)", 1.0, 100.0, 30.0, 1.0)
    theta_deg = st.slider("ມຸມຍິງ θ (ອົງສາ)", 0, 90, 45)
    h0 = st.slider("ຄວາມສູງເລີ່ມຕົ້ນ h₀ (m)", 0.0, 100.0, 0.0, 1.0)
    g = st.selectbox("ຄວາມເລັ່ງໂນ້ມຖ່ວງ g (m/s²)", [9.8, 10.0])

# ---------------- ຄິດໄລ່ ----------------
th = np.radians(theta_deg)
vx = v0 * np.cos(th)           # ຄວາມໄວແກນນອນ (ຄົງທີ່)
vy0 = v0 * np.sin(th)          # ຄວາມໄວເລີ່ມຕົ້ນແກນຕັ້ງ

T = (vy0 + np.sqrt(vy0**2 + 2 * g * h0)) / g   # ເວລາທັງໝົດໃນອາກາດ
t_up = vy0 / g                                  # ເວລາຂຶ້ນເຖິງຈຸດສູງສຸດ
H = h0 + vy0**2 / (2 * g)                       # ຄວາມສູງສູງສຸດ
R = vx * T                                      # ໄລຍະທາງທາງນອນ

if T < 0.05:
    st.warning("ວັດຖຸຕົກລົງພື້ນທັນທີ. ລອງເພີ່ມມຸມ ຫຼື ຄວາມສູງເລີ່ມຕົ້ນ.")
    st.stop()

# ---------------- ສູດ ----------------
st.header("1) ສູດທີ່ໃຊ້")
c1, c2 = st.columns(2)
with c1:
    st.subheader("ແກນນອນ (x): ຄວາມໄວຄົງທີ່")
    st.latex(r"a_x = 0")
    st.latex(r"v_x = v_0\cos\theta")
    st.latex(r"x = v_0\cos\theta \cdot t")
with c2:
    st.subheader("ແກນຕັ້ງ (y): ຄວາມເລັ່ງ −g")
    st.latex(r"a_y = -g")
    st.latex(r"v_y = v_0\sin\theta - g t")
    st.latex(r"y = h_0 + v_0\sin\theta \cdot t - \tfrac{1}{2} g t^2")

st.subheader("ຄ່າສໍາຄັນຂອງວິຖີ")
c3, c4, c5 = st.columns(3)
with c3:
    st.latex(r"t_{\text{up}} = \dfrac{v_0\sin\theta}{g}")
    st.latex(r"H = h_0 + \dfrac{(v_0\sin\theta)^2}{2g}")
with c4:
    st.latex(r"T = \dfrac{v_0\sin\theta + \sqrt{(v_0\sin\theta)^2 + 2gh_0}}{g}")
with c5:
    st.latex(r"R = v_0\cos\theta \cdot T")
    st.latex(r"v = \sqrt{v_x^2 + v_y^2}")

st.subheader("ຜົນຄິດໄລ່ຕາມຄ່າທີ່ເລືອກ")
m1, m2, m3, m4 = st.columns(4)
m1.metric("ເວລາຂຶ້ນສູງສຸດ t_up", f"{t_up:.2f} s")
m2.metric("ຄວາມສູງສູງສຸດ H", f"{H:.2f} m")
m3.metric("ເວລາທັງໝົດ T", f"{T:.2f} s")
m4.metric("ໄລຍະທາງນອນ R", f"{R:.2f} m")
st.write(f"vₓ = {vx:.2f} m/s (ຄົງທີ່),  v₀y = {vy0:.2f} m/s")

# ---------------- ເວລາ t ປັດຈຸບັນ ----------------
st.header("2) ເບິ່ງການເຄື່ອນທີ່ຕາມເວລາ")
t = st.slider("ເວລາ t (s)", 0.0, float(round(T, 2)), 0.0, 0.01)

x_t = vx * t
y_t = max(h0 + vy0 * t - 0.5 * g * t**2, 0.0)
vy_t = vy0 - g * t
speed = float(np.hypot(vx, vy_t))
angle_now = float(np.degrees(np.arctan2(vy_t, vx)))

n1, n2, n3, n4 = st.columns(4)
n1.metric("x", f"{x_t:.2f} m")
n2.metric("y", f"{y_t:.2f} m")
n3.metric("v_y", f"{vy_t:.2f} m/s")
n4.metric("ຄວາມໄວລວມ v", f"{speed:.2f} m/s")

# ---------------- ຮູບວິຖີ ----------------
ts = np.linspace(0, T, 300)
xs = vx * ts
ys = np.maximum(h0 + vy0 * ts - 0.5 * g * ts**2, 0)

# ຈຸດທຸກໆຊ່ວງເວລາເທົ່າກັນ (stroboscopic)
ts_s = np.linspace(0, T, 11)
xs_s = vx * ts_s
ys_s = np.maximum(h0 + vy0 * ts_s - 0.5 * g * ts_s**2, 0)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(xs, ys, color="tab:blue", lw=2, label="Trajectory")
ax.plot(xs_s, ys_s, "o", color="tab:blue", ms=5, alpha=0.6,
        label="Position every T/10")
# ເງົາ (projection) ເທິງແກນນອນ ແລະ ແກນຕັ້ງ
ax.plot(xs_s, np.zeros_like(xs_s), "s", color="tab:red", ms=5,
        label="Horizontal shadow (equal spacing)")
ax.plot(np.zeros_like(ys_s), ys_s, "s", color="tab:green", ms=5,
        label="Vertical shadow (changing spacing)")
ax.axhline(0, color="k", lw=1)

# ເສັ້ນປະ ຈາກວັດຖຸໄປຫາແກນ
ax.plot([x_t, x_t], [0, y_t], "--", color="gray", lw=1)
ax.plot([0, x_t], [y_t, y_t], "--", color="gray", lw=1)

# ວັດຖຸ + ລູກສອນຄວາມໄວ
ax.plot(x_t, y_t, "o", color="black", ms=11, zorder=5)
k = 0.18 * max(R, H, 1) / max(v0, 1)       # ສເກລລູກສອນ
ax.quiver(x_t, y_t, k * vx, 0, angles="xy", scale_units="xy", scale=1,
          color="tab:red", width=0.006, label="vx")
ax.quiver(x_t, y_t, 0, k * vy_t, angles="xy", scale_units="xy", scale=1,
          color="tab:green", width=0.006, label="vy")
ax.quiver(x_t, y_t, k * vx, k * vy_t, angles="xy", scale_units="xy", scale=1,
          color="tab:purple", width=0.006, label="v (resultant)")

# ຈຸດສູງສຸດ
ax.plot(vx * t_up, H, "*", color="gold", ms=16, mec="k", label="Max height")

ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_title("Projectile trajectory with velocity components")
ax.set_xlim(-0.08 * R - 1, R * 1.1 + 1)
ax.set_ylim(-0.08 * H - 1, H * 1.25 + 1)
ax.set_aspect("equal", adjustable="box")
ax.grid(alpha=0.3)
ax.legend(loc="upper right", fontsize=8)
st.pyplot(fig)

st.info(
    "ສັງເກດ: ຈຸດສີແດງ (ເງົາເທິງແກນນອນ) ຫ່າງກັນເທົ່າໆກັນ → ເຄື່ອນທີ່ດ້ວຍຄວາມໄວຄົງທີ່. "
    "ຈຸດສີຂຽວ (ເງົາເທິງແກນຕັ້ງ) ຫ່າງກັນບໍ່ເທົ່າກັນ → ມີຄວາມເລັ່ງ −g."
)

# ---------------- ກຣາຟແຍກແກນ ----------------
st.header("3) ກຣາຟຂອງແຕ່ລະແກນ")
fig2, axs = plt.subplots(2, 2, figsize=(10, 6), sharex=True)

axs[0, 0].plot(ts, xs, color="tab:red")
axs[0, 0].set_title("Horizontal: x - t (straight line)")
axs[0, 0].set_ylabel("x (m)")

axs[0, 1].plot(ts, ys, color="tab:green")
axs[0, 1].set_title("Vertical: y - t (parabola)")
axs[0, 1].set_ylabel("y (m)")

axs[1, 0].plot(ts, np.full_like(ts, vx), color="tab:red")
axs[1, 0].set_title("Horizontal: vx - t (constant)")
axs[1, 0].set_ylabel("vx (m/s)")
axs[1, 0].set_xlabel("t (s)")

axs[1, 1].plot(ts, vy0 - g * ts, color="tab:green")
axs[1, 1].axhline(0, color="k", lw=0.8)
axs[1, 1].set_title("Vertical: vy - t (slope = -g)")
axs[1, 1].set_ylabel("vy (m/s)")
axs[1, 1].set_xlabel("t (s)")

# ໝາຍເວລາປັດຈຸບັນ
cur = [(axs[0, 0], x_t), (axs[0, 1], y_t), (axs[1, 0], vx), (axs[1, 1], vy_t)]
for a, val in cur:
    a.axvline(t, color="gray", ls="--", lw=1)
    a.plot(t, val, "o", color="black")
    a.grid(alpha=0.3)

fig2.tight_layout()
st.pyplot(fig2)