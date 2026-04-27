import streamlit as st
from utils import apply_ufc_theme, create_user

st.set_page_config(
    page_title="회원가입",
    page_icon="🔥",
    layout="centered"
)

apply_ufc_theme()

st.title("🔥 회원가입")

st.markdown(
    """
    <div class="main-card">
        회원가입을 하여 당신의 UFC덕후력을 뽐내보세요.
    </div>
    """,
    unsafe_allow_html=True
)

name = st.text_input("이름")
username = st.text_input("아이디")
password = st.text_input("비밀번호", type="password")
password_check = st.text_input("비밀번호 확인", type="password")

if st.button("회원가입", use_container_width=True):
    if password != password_check:
        st.error("비밀번호와 비밀번호 확인이 일치하지 않습니다.")
    else:
        success, message = create_user(name, username, password)

        if success:
            st.success(message)
            st.info("이제 로그인 페이지에서 로그인하세요.")
        else:
            st.error(message)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 홈으로", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("🥊 로그인하러 가기", use_container_width=True):
        st.switch_page("pages/2_로그인.py")