#python -m streamlit run motion.py
import random
import streamlit as st

def make_question(kind=None):
    kind = kind or random.choice(["s", "v", "t", "meet"])
    names = ["ກົບ", "ລົດຈັກ", "ລົດຖີບ", "ລົດເມ", "ນັກແລ່ນ"]
    who = random.choice(names)

    if kind == "s":
        v = random.randint(5, 30)
        t = random.randint(2, 20)
        q = f"{who}ເຄື່ອນທີ່ດ້ວຍຄວາມໄວຄົງທີ່ {v} m/s ເປັນເວລາ {t} s. ຄິດໄລ່ໄລຍະທາງ."
        ans = f"{v * t} m"

    elif kind == "v":
        t = random.randint(2, 20)
        v = random.randint(5, 30)
        s = v * t
        q = f"{who}ເຄື່ອນທີ່ໄດ້ໄລຍະທາງ {s} m ໃນເວລາ {t} s. ຄິດໄລ່ຄວາມໄວ."
        ans = f"{v} m/s"

    elif kind == "t":
        v = random.randint(5, 30)
        t = random.randint(2, 20)
        s = v * t
        q = f"{who}ເຄື່ອນທີ່ດ້ວຍຄວາມໄວ {v} m/s ໄດ້ໄລຍະທາງ {s} m. ໃຊ້ເວລາເທົ່າໃດ?"
        ans = f"{t} s"

    else:
        v1, v2 = random.randint(5, 15), random.randint(5, 15)
        t = random.randint(2, 15)
        d = (v1 + v2) * t
        q = (f"ລົດສອງຄັນຢູ່ຫ່າງກັນ {d} m ແລ່ນເຂົ້າຫາກັນດ້ວຍຄວາມໄວ "
             f"{v1} m/s ແລະ {v2} m/s. ຈະພົບກັນຫຼັງຈາກຜ່ານໄປເທົ່າໃດ?")
        ans = f"{t} s"

    return q, ans


# ---------- ສ່ວນສະແດງຜົນ Streamlit ----------
st.title("ແບບຝຶກຫັດການເຄື່ອນທີ່ຊື່ສະໝໍ່າສະເໝີ")

if "q" not in st.session_state:
    st.session_state.q, st.session_state.a = make_question()

if st.button("ສ້າງຂໍ້ໃໝ່"):
    st.session_state.q, st.session_state.a = make_question()

st.write(st.session_state.q)

if st.checkbox("ສະແດງຄໍາຕອບ"):
    st.success(st.session_state.a)