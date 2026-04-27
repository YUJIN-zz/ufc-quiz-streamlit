import random

import streamlit as st

from utils import apply_ufc_theme, prepare_quiz_data, reset_quiz_state

st.set_page_config(
    page_title="UFC 퀴즈",
    page_icon="🏆",
    layout="wide"
)

apply_ufc_theme()

st.title("🏆 역대 UFC 메인카드 경기 결과 맞추기")

if not st.session_state.get("logged_in", False):
    st.error("퀴즈를 풀기 위해서는 먼저 로그인해야 합니다.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🥊 로그인하러 가기", use_container_width=True):
            st.switch_page("pages/2_로그인.py")

    with col2:
        if st.button("🏠 홈으로", use_container_width=True):
            st.switch_page("app.py")

    st.stop()

display_name = st.session_state.get("name", st.session_state.get("username", "사용자"))
st.success(f"{display_name}님 로그인 중")

df = prepare_quiz_data()

st.markdown(
    """
    <div class="main-card">
        원하는 문제 수를 선택한 뒤, 실제 UFC 메인카드 경기에서 승리한 선수를 맞혀보세요.
    </div>
    """,
    unsafe_allow_html=True
)

question_count = st.slider(
    "문제 수 선택",
    min_value=3,
    max_value=len(df),
    value=5
)

if st.button("새 퀴즈 시작", use_container_width=True):
    reset_quiz_state()

    quiz_df = df.sample(question_count).reset_index(drop=True)
    questions = []

    for _, row in quiz_df.iterrows():
        correct = row["winner"]

        options = [row["fighter_a"], row["fighter_b"]]
        random.shuffle(options)

        question_text = f"{row['event']} 메인이벤트의 승자는 누구일까요?"

        questions.append(
            {
                "event": row["event"],
                "year": row["year"],
                "fighter_a": row["fighter_a"],
                "fighter_b": row["fighter_b"],
                "question": question_text,
                "options": options,
                "correct": correct,
                "winner": row["winner"],
                "loser": row["loser"],
                "method": row["method_category"],
                "method_detail": row["method_detail"],
                "round": row["round"],
                "summary": row["summary"],
            }
        )

    st.session_state["quiz_questions"] = questions
    st.session_state["submitted"] = False
    st.session_state["answers"] = {}

if "quiz_questions" not in st.session_state:
    st.info("문제 수를 선택한 뒤 '새 퀴즈 시작' 버튼을 누르세요.")

    if st.button("🏠 홈으로 돌아가기", use_container_width=True):
        st.switch_page("app.py")

    st.stop()

questions = st.session_state["quiz_questions"]

with st.form("quiz_form"):
    answers = {}

    for i, q in enumerate(questions, start=1):
        st.markdown(
            f"""
            <div class="fight-card">
                <h3>Q{i}. {q["question"]}</h3>
                <p><b>경기:</b> {q["fighter_a"]} vs {q["fighter_b"]}</p>
                <p><b>연도:</b> {q["year"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        answers[i] = st.radio(
            label=f"Q{i} 정답 선택",
            options=q["options"],
            key=f"question_{i}",
            horizontal=True
        )

    submitted = st.form_submit_button("결과 확인")

if submitted:
    score = 0

    for i, q in enumerate(questions, start=1):
        if answers[i] == q["correct"]:
            score += 1

    st.session_state["submitted"] = True
    st.session_state["answers"] = answers
    st.session_state["score"] = score

if st.session_state.get("submitted", False):
    score = st.session_state["score"]
    total = len(questions)
    accuracy = round(score / total * 100, 1)

    st.markdown("---")
    st.header("🔥 최종 결과")

    st.markdown(
        f"""
        <div class="result-card">
            <h2>{score} / {total}점</h2>
            <h3>정답률: {accuracy}%</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    if accuracy >= 80:
        st.success("UFC 메인카드 고인물입니다. 경기 흐름을 꽤 잘 알고 있습니다.")
    elif accuracy >= 50:
        st.warning("나쁘지 않습니다. 유명 경기 위주로 복습하면 더 좋아질 수 있습니다.")
    else:
        st.error("아직은 UFC 입문자에 가깝습니다. 경기 요약을 보면서 다시 도전해보세요.")

    st.subheader("문제별 해설")

    for i, q in enumerate(questions, start=1):
        user_answer = st.session_state["answers"][i]
        is_correct = user_answer == q["correct"]

        result_icon = "✅ 정답" if is_correct else "❌ 오답"

        st.markdown(
            f"""
            <div class="fight-card">
                <h3>{result_icon} | Q{i}. {q["event"]}</h3>
                <p><b>경기:</b> {q["fighter_a"]} vs {q["fighter_b"]}</p>
                <p><b>내 선택:</b> {user_answer}</p>
                <p><b>정답:</b> {q["correct"]}</p>
                <p><b>경기 결과:</b> {q["winner"]} def. {q["loser"]}</p>
                <p><b>승리 방식:</b> {q["method"]} / {q["method_detail"]} / {q["round"]}라운드</p>
                <p><b>경기 요약:</b> {q["summary"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("다시 풀기", use_container_width=True):
            reset_quiz_state()
            st.rerun()

    with col2:
        if st.button("🏠 홈으로", use_container_width=True):
            st.switch_page("app.py")