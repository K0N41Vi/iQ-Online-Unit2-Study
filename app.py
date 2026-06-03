import streamlit as st
import random
import time

from data import VOCAB_DATA
from data import MEANING_CHOICES

st.set_page_config(
    page_title="TOEIC Vocabulary Trainer",
    page_icon="📘",
    layout="centered"
)

# --------------------
# UI
# --------------------

st.markdown("""
<style>

.stApp {
    background-color: #fcfaf7;
}

.word-badge {
    background:#ea580c;
    color:white;
    padding:10px 20px;
    border-radius:8px;
    display:inline-block;
    font-weight:bold;
    font-size:1.3rem;
}

.scan-cover{
    background:#ddd;
    border-radius:10px;
    padding:40px;
    text-align:center;
    font-size:1.2rem;
}

</style>
""", unsafe_allow_html=True)

# --------------------
# session state
# --------------------

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "scan_started" not in st.session_state:
    st.session_state.scan_started = False

if "scan_start_time" not in st.session_state:
    st.session_state.scan_start_time = None

# --------------------
# sidebar
# --------------------

st.sidebar.title("Unit 2 Vocabulary")

selected_word = st.sidebar.radio(
    "単語一覧",
    range(len(VOCAB_DATA)),
    format_func=lambda x:
        f"{x+1}. {VOCAB_DATA[x]['word']}"
)

q = VOCAB_DATA[selected_word]

# --------------------
# header
# --------------------

st.markdown(
    f"<div class='word-badge'>{q['word']}</div>",
    unsafe_allow_html=True
)

st.write("")

# ====================
# Q1
# ====================

st.subheader("Q1 意味問題")

choices = [q["meaning"]]

while len(choices) < 4:
    c = random.choice(MEANING_CHOICES)
    if c not in choices:
        choices.append(c)

random.shuffle(choices)

q1 = st.radio(
    "最も適切な意味を選びましょう",
    choices,
    key=f"q1_{selected_word}"
)

# ====================
# Q2
# ====================

st.subheader("Q2 類語問題")

correct_synonyms = q["synonyms"]

st.caption(
    f"正解は {len(correct_synonyms)} 個あります"
)

selected_synonyms = []

all_choices = correct_synonyms.copy()

fake_pool = []

for vocab in VOCAB_DATA:
    fake_pool.extend(vocab["synonyms"])

fake_pool = list(set(fake_pool))

while len(all_choices) < 6:
    f = random.choice(fake_pool)
    if f not in all_choices:
        all_choices.append(f)

random.shuffle(all_choices)

for option in all_choices:

    checked = st.checkbox(
        option,
        key=f"{selected_word}_{option}"
    )

    if checked:
        selected_synonyms.append(option)

# ====================
# scan
# ====================

st.divider()

st.subheader("Q3 スキャニング")

if not st.session_state.scan_started:

    st.markdown(
        """
        <div class='scan-cover'>
        スキャニング問題はまだ開始されていません
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🚀 スキャニング開始！",
        type="primary"
    ):

        st.session_state.scan_started = True
        st.session_state.scan_start_time = time.time()

        st.rerun()

else:

    elapsed = (
        time.time()
        - st.session_state.scan_start_time
    )

    st.info(
        f"経過時間: {elapsed:.1f} 秒"
    )

    st.warning(
        "次にHTMLクリック式へ差し替えます"
    )

# ====================
# save
# ====================

st.divider()

if st.button(
    "この回答でOK",
    type="primary"
):

    q1_correct = (
        q1 == q["meaning"]
    )

    q2_correct = (
        set(selected_synonyms)
        ==
        set(correct_synonyms)
    )

    st.session_state.answers[q["word"]] = {

        "q1": q1_correct,

        "q2": q2_correct,

        "selected":
        selected_synonyms
    }

    st.success("保存しました")
