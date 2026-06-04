import streamlit as st
import random
import time
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript

from data import VOCAB_DATA
from data import MEANING_CHOICES

st.set_page_config(
    page_title="TOEIC Vocabulary Trainer",
    page_icon="📘",
    layout="centered"
)

# --------------------
# CSS
# --------------------

st.markdown("""
<style>

.stApp{
    background-color:#fcfaf7;
}

.word-badge{
    background:#ea580c;
    color:white;
    padding:10px 20px;
    border-radius:8px;
    display:inline-block;
    font-weight:bold;
    font-size:1.3rem;
}

.scan-cover{
    background:#dddddd;
    border-radius:10px;
    padding:40px;
    text-align:center;
    font-size:1.2rem;
}

.scan-box{
    background:white;
    border:1px solid #dddddd;
    border-radius:12px;
    padding:24px;
    line-height:2.2;
    font-size:22px;
}

</style>
""", unsafe_allow_html=True)

# --------------------
# session state
# --------------------

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "scan_started_word" not in st.session_state:
    st.session_state.scan_started_word = None

if "scan_start_time" not in st.session_state:
    st.session_state.scan_start_time = None

if "scan_times" not in st.session_state:
    st.session_state.scan_times = {}

if "scan_finished" not in st.session_state:
    st.session_state.scan_finished = {}

if "scan_click_time" not in st.session_state:
    st.session_state.scan_click_time = None

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

    candidate = random.choice(MEANING_CHOICES)

    if candidate not in choices:
        choices.append(candidate)

random.shuffle(choices)

q1_answer = st.radio(
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
    f"{len(correct_synonyms)}個選択"
)

selected_synonyms = []

all_choices = correct_synonyms.copy()

fake_pool = []

for vocab in VOCAB_DATA:
    fake_pool.extend(vocab["synonyms"])

fake_pool = list(set(fake_pool))

while len(all_choices) < 6:

    candidate = random.choice(fake_pool)

    if candidate not in all_choices:
        all_choices.append(candidate)

random.shuffle(all_choices)

for option in all_choices:

    checked = st.checkbox(
        option,
        key=f"{selected_word}_{option}"
    )

    if checked:
        selected_synonyms.append(option)

st.divider()

# ====================
# Q3
# ====================

st.subheader("Q3 スキャニング")

current_word = q["word"]

scan_running = (
    st.session_state.scan_started_word
    == current_word
)

if not scan_running:

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
        type="primary",
        key=f"start_{current_word}"
    ):

        st.session_state.scan_started_word = (
            current_word
        )

        st.session_state.scan_start_time = (
            time.time()
        )

        st.rerun()

else:

    target = None

    for synonym in q["synonyms"]:
        if synonym in q["scan_text"]:
            target = synonym
            break

    if target is None:
        st.error("scan_text内に類語が見つかりません")
        st.stop()

    scan_html = q["scan_text"].replace(
        target,
        f'<span id="target" onclick="found()" style="cursor:pointer;">{target}</span>'
    )

    html = f"""
    <!DOCTYPE html>
    <html>
    <body>

    <div style="
        background:white;
        border:1px solid #dddddd;
        border-radius:12px;
        padding:24px;
        font-size:22px;
        line-height:2.2;
        white-space:pre-line;
        font-family:sans-serif;
    ">

    {scan_html}

    </div>

    <div id="timer"
         style="
         margin-top:18px;
         font-size:20px;
         font-weight:bold;
         ">
         ⏱️ 0.0 sec
    </div>

    <script>

    const startTime = Date.now();

    let finished = false;

    const timer = setInterval(() => {{

        if(finished) return;

        const elapsed =
            ((Date.now()-startTime)/1000)
            .toFixed(1);

        document.getElementById("timer")
            .innerHTML =
            "⏱️ " + elapsed + " sec";

    }},100);

    function found() {{

        if(finished) return;

        finished = true;

        clearInterval(timer);

        const elapsed =
            ((Date.now()-startTime)/1000)
            .toFixed(2);

        localStorage.setItem(
            "scan_time",
            elapsed
        );

        document.getElementById("timer")
            .innerHTML =
            "✅ Found! " + elapsed + " sec";

        document.getElementById("target")
            .style.background =
            "#fde68a";

        document.getElementById("target")
            .style.fontWeight =
            "bold";

        document.getElementById("target")
            .style.borderRadius =
            "4px";

        document.getElementById("target")
            .style.padding =
            "2px 4px";
    }}

    </script>

    </body>
    </html>
    """

    components.html(
        html,
        height=650,
        scrolling=False
    )

    clicked_time = st_javascript(
        "localStorage.getItem('scan_time')"
    )


    if clicked_time:

        try:

            st.session_state.scan_click_time = (
                float(clicked_time)
            )

        except:
            pass

    st.metric(
        "発見時間",
        f"{st.session_state.scan_click_time:.2f} 秒"
    )

    st.caption(
        "文章中からQ2で学習した類語を探してください"
    )

# ====================
# 保存
# ====================

st.divider()

if st.button(
    "この回答でOK",
    type="primary",
    key=f"save_{current_word}"
):

    q1_correct = (
        q1_answer
        == q["meaning"]
    )

    q2_correct = (
        set(selected_synonyms)
        ==
        set(correct_synonyms)
    )

    if (
        st.session_state.scan_click_time
        is not None
    ):

        st.session_state.scan_times[
            current_word
        ] = (
            st.session_state.scan_click_time
        )

    st.session_state.answers[
        current_word
    ] = {

        "q1": q1_correct,

        "q2": q2_correct,

        "selected": selected_synonyms
    }

    st.session_state.scan_started_word = None

    st.session_state.scan_start_time = None

    st.session_state.scan_click_time = None

    st.success(
        f"{current_word} を保存しました"
    )

# ====================
# 回答状況
# ====================

st.sidebar.divider()

saved_count = len(
    st.session_state.answers
)

st.sidebar.write(
    f"保存済み: {saved_count}/24"
)

# ====================
# 結果表示
# ====================

if saved_count > 0:

    st.sidebar.divider()

    if st.sidebar.button("結果を見る"):

        st.subheader("学習結果")

        total_q1 = 0
        total_q2 = 0

        for word, result in (
            st.session_state.answers.items()
        ):

            if result["q1"]:
                total_q1 += 1

            if result["q2"]:
                total_q2 += 1

        st.write(
            f"Q1正解数: {total_q1}/{saved_count}"
        )

        st.write(
            f"Q2正解数: {total_q2}/{saved_count}"
        )

        accuracy = (
            (total_q1 + total_q2)
            /
            (saved_count * 2)
        ) * 100

        st.write(
            f"総合正答率: {accuracy:.1f}%"
        )

        st.divider()

        st.subheader("スキャニング結果")

        total_scan_time = 0

        for word, t in (
            st.session_state.scan_times.items()
        ):

            total_scan_time += t

            st.write(
                f"{word} : {t:.2f} 秒"
            )

        st.divider()

        st.subheader(
            f"合計スキャン時間: {total_scan_time:.2f} 秒"
        )

        
        average_time = (
        total_scan_time
        / len(st.session_state.scan_times)
        )

        st.write(
        f"平均スキャン時間: {average_time:.2f} 秒"
        )

        if average_time < 3 and accuracy >= 90:
            title = "👑 TOEIC level 990"

        elif average_time < 4 and accuracy >= 80:
            title = "⚡ TOEIC level 900"

        elif average_time < 6:
            title = "🔥 TOEIC level 800"

        elif average_time < 7:
            title = "📚 TOEIC level 700"

        else:
            title = "🌱 まだまだです"

        st.success(
            f"称号：{title}"
        )

        st.divider()

        for word, result in (
            st.session_state.answers.items()
        ):

            q1_mark = (
            "⭕"
            if result["q1"]
            else "❌"
            )

            q2_mark = (
            "⭕"
            if result["q2"]
            else "❌"
            )

            st.write(
                 f"{word}　Q1:{q1_mark}　Q2:{q2_mark}"
            )   
