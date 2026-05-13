import json
import hashlib
from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path("data/ufc_main_cards.csv")
USERS_PATH = Path("users.json")


def apply_ufc_theme():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #080808 0%, #1a0000 50%, #000000 100%);
            color: white;
        }

        h1, h2, h3 {
            color: #ff1f1f !important;
            font-weight: 900 !important;
        }

        p, div, span, label {
            color: white;
        }

        .main-card {
            background: rgba(20, 20, 20, 0.92);
            border: 1px solid #ff1f1f;
            border-radius: 18px;
            padding: 28px;
            box-shadow: 0 0 25px rgba(255, 0, 0, 0.35);
            margin-bottom: 20px;
        }

        .fight-card {
            background: rgba(15, 15, 15, 0.95);
            border-left: 6px solid #ff1f1f;
            border-radius: 14px;
            padding: 18px;
            margin: 16px 0;
        }

        .result-card {
            background: rgba(255, 31, 31, 0.12);
            border: 1px solid #ff1f1f;
            border-radius: 14px;
            padding: 18px;
            margin: 14px 0;
        }

        div.stButton > button {
            background-color: #ff1f1f;
            color: white;
            border-radius: 12px;
            border: none;
            font-weight: 800;
            padding: 0.7rem 1.2rem;
        }

        div.stButton > button:hover {
            background-color: #cc0000;
            color: white;
            border: 1px solid white;
        }

        .stRadio label, .stSlider label, .stTextInput label {
            color: white !important;
            font-weight: 700;
        }

        section[data-testid="stSidebar"] {
            display: none;
        }

        div[data-testid="collapsedControl"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner="UFC 경기 데이터를 불러오는 중입니다...")
def load_fight_data():
    """
    캐싱 적용 지점 1:
    UFC 경기 데이터 CSV를 읽어오는 함수입니다.
    Streamlit은 버튼 클릭이나 입력값 변경 때마다 코드가 다시 실행되므로,
    같은 CSV 파일을 반복해서 읽지 않도록 캐싱을 적용했습니다.
    """
    df = pd.read_csv(DATA_PATH)
    return df


@st.cache_data(show_spinner="퀴즈 데이터를 준비하는 중입니다...")
def prepare_quiz_data():
    """
    캐싱 적용 지점 2:
    퀴즈에 사용할 데이터를 전처리하는 함수입니다.
    경기명과 선수명을 합친 match_title 컬럼을 추가하고,
    이 결과를 캐싱하여 반복 계산을 줄입니다.
    """
    df = load_fight_data().copy()
    df["match_title"] = df["event"] + " | " + df["fighter_a"] + " vs " + df["fighter_b"]
    return df


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    if not USERS_PATH.exists():
        USERS_PATH.write_text("{}", encoding="utf-8")

    with open(USERS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


def create_user(name, username, password):
    users = load_users()

    if not name or not username or not password:
        return False, "이름, 아이디, 비밀번호를 모두 입력하세요."

    if username in users:
        return False, "이미 존재하는 아이디입니다."

    users[username] = {
        "name": name,
        "password": hash_password(password)
    }

    save_users(users)

    return True, "회원가입이 완료되었습니다."


def check_login(username, password):
    users = load_users()

    if username not in users:
        return False

    user_info = users[username]

    if isinstance(user_info, str):
        return user_info == hash_password(password)

    return user_info["password"] == hash_password(password)


def get_user_name(username):
    users = load_users()

    if username not in users:
        return username

    user_info = users[username]

    if isinstance(user_info, str):
        return username

    return user_info.get("name", username)


def reset_quiz_state():
    keys = ["quiz_questions", "submitted", "answers", "score"]
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]