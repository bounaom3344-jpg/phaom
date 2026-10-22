#python -m streamlit run motion2.py 
"""
ໜ້າເວັບ Streamlit ສໍາລັບສະແດງໂຈດຟີຊິກ
ຕ້ອງເກັບໄຟລ໌ນີ້ໄວ້ໃນໂຟນເດີດຽວກັບ physics_generator.py

Run:
    python -m streamlit run app_streamlit.py
"""
import os
import random

import streamlit as st

import physics_generator as pg

st.set_page_config(page_title="ໂຈດຟີຊິກ", layout="wide")
st.title("ແບບຝຶກຫັດຟີຊິກ: ການເຄື່ອນທີ່")

n = st.sidebar.slider("ຈໍານວນຂໍ້ຕໍ່ບົດ", 1, 10, 3)
seed = st.sidebar.number_input("Seed (ໃຫ້ໄດ້ຊຸດເດີມ)", value=0, step=1)
st.sidebar.button("ສຸ່ມໂຈດໃໝ່")  # ກົດແລ້ວໜ້າຈະ run ໃໝ່

os.makedirs(pg.OUT, exist_ok=True)
if seed != 0:
    random.seed(int(seed))

for title, fn in pg.SECTIONS:
    st.header(title)
    for i in range(1, n + 1):
        p = fn(i)
        st.markdown(f"**ຂໍ້ {i}.** {p['q']}")
        st.image(os.path.join(pg.OUT, p["img"]))
        with st.expander("ເບິ່ງວິທີແກ້ ແລະ ຄໍາຕອບ"):
            for line in p["sol"]:
                st.write(line)
            st.success("ຄໍາຕອບ: " + p["ans"])
        st.divider()