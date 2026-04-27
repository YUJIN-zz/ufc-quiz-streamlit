import streamlit as st
from utils import apply_ufc_theme, check_login, get_user_name

st.set_page_config(
    page_title="로그인",
    page_icon="🥊",
    layout="centered"
)

apply_ufc_theme()

st.title("🥊 로그인")

st.markdown(
    """
    <div class="main-card">
        로그인에 성공하면 당신의 덕후력을 뽐낼 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True
)

username = st.text_input("아이디")
password = st.text_input("비밀번호", type="password")

if st.button("로그인", use_container_width=True):
    if check_login(username, password):
        name = get_user_name(username)

        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.session_state["name"] = name

        st.success(f"{name}님, 로그인에 성공했습니다.")
        st.info("퀴즈 시작 버튼을 눌러 이동하세요.")
    else:
        st.session_state["logged_in"] = False
        st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

if st.button("로그아웃", use_container_width=True):
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["name"] = ""
    st.success("로그아웃되었습니다.")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 홈으로", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("🔥 회원가입", use_container_width=True):
        st.switch_page("pages/1_회원가입.py")

with col3:
    if st.button("🏆 퀴즈 시작", use_container_width=True):
        st.switch_page("pages/3_퀴즈.py")