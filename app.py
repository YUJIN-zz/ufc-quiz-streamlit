import streamlit as st
from utils import apply_ufc_theme

st.set_page_config(
    page_title="UFC Main Card Quiz",
    page_icon="🥊",
    layout="centered"
)

apply_ufc_theme()

st.markdown(
    """
    <div class="main-card" style="text-align:center; margin-top: 60px;">
        <h1>WHO'S THE BEST?</h1>
        <h2>학번: 2025404001 </h2>
        <h2>이름: 정유진 </h2>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔥 회원가입", use_container_width=True):
        st.switch_page("pages/1_회원가입.py")

with col2:
    if st.button("🥊 로그인", use_container_width=True):
        st.switch_page("pages/2_로그인.py")

with col3:
    if st.button("🏆 퀴즈 시작", use_container_width=True):
        st.switch_page("pages/3_퀴즈.py")