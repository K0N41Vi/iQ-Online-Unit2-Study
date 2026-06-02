import streamlit as st
import random

# =========================
# ページ設定
# =========================

st.set_page_config(
    page_title="TOEIC Unit Trainer",
    page_icon="📚",
    layout="wide"
)

# =========================
# UI
# =========================

st.markdown("""
<style>

.stApp {
    background-color: #fcfaf7;
}

.word-card {
    background-color:#f3ede4;
    padding:20px;
    border-radius:10px;
    border:2px solid #d97706;
    margin-bottom:15px;
}

.target-badge {
    background-color:#ea580c;
    color:white;
    padding:10px 18px;
    border-radius:8px;
    display:inline-block;
    font-weight:bold;
    font-size:22px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 問題データ
# =========================

WORDS = [

{
    "word":"benefit",

    "meaning":"利益・恩恵",

    "meaning_choices":[
        "利益・恩恵",
        "経験",
        "契約",
        "需要"
    ],

    "synonyms":[
        "advantage",
        "perk"
    ],

    "synonym_choices":[
        "advantage",
        "perk",
        "labor",
        "wage",
        "supply"
    ],

    "scanning_questions":[

        {
            "target":"advantage",

            "passage":
            """
            Working remotely has several advantages for employees.
            It reduces commuting time and improves work-life balance.
            Many companies now offer flexible schedules.
            """
        },

        {
            "target":"perk",

            "passage":
            """
            One perk of working at this company is the free lunch program.
            Employees can enjoy healthy meals every day.
            This helps improve workplace satisfaction.
            """
        }
    ]
},

{
    "word":"expertise",

    "meaning":"専門知識",

    "meaning_choices":[
        "専門知識",
        "給料",
        "商品",
        "広告"
    ],

    "synonyms":[
        "knowledge",
        "skill",
        "experience"
    ],

    "synonym_choices":[
        "knowledge",
        "skill",
        "experience",
        "demand",
        "labor",
        "wage"
    ],

    "scanning_questions":[

        {
            "target":"knowledge",

            "passage":
            """
            New employees receive extensive training.
            This gives them the knowledge necessary to succeed.
            Managers are available to answer questions.
            """
        },

        {
            "target":"skill",

            "passage":
            """
            Strong communication skills are highly valued.
            They help employees work effectively with clients.
            Teamwork is also important.
            """
        },

        {
            "target":"experience",

            "passage":
            """
            Candidates with previous experience are preferred.
            They can adapt to the role more quickly.
            The company values practical understanding.
            """
        }
    ]
},

{
    "word":"freelancer",

    "meaning":"フリーランス",

    "meaning_choices":[
        "フリーランス",
        "正社員",
        "管理職",
        "顧客"
    ],

    "synonyms":[
        "independent worker",
        "contractor"
    ],

    "synonym_choices":[
        "independent worker",
        "contractor",
        "manager",
        "supplier",
        "client"
    ],

    "scanning_questions":[

        {
            "target":"contractor",

            "passage":
            """
            The company hired a contractor for the project.
            He was not a full-time employee.
            His contract will end after six months.
            """
        },

        {
            "target":"independent",

            "passage":
            """
            She works independently and chooses her own clients.
            This flexibility allows her to travel frequently.
            Many professionals prefer this style of work.
            """
        }
    ]
}

]

# =========================
# session
# =========================

if "current_word" not in st.session_state:
    st.session_state.current_word = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

# =========================
# sidebar
# =========================

with st.sidebar:

    st.title("📚 TOEIC Trainer")

    for i, item in enumerate(WORDS):

        if st.button(
            f"{i+1}. {item['word']}",
            use_container_width=True
        ):
            st.session_state.current_word = i
            st.rerun()

    st.divider()

    if st.button(
        "📊 結果を見る",
        use_container_width=True
    ):
        st.session_state.current_word = "result"
        st.rerun()

# =========================
# 結果ページ
# =========================

if st.session_state.current_word == "result":

    st.title("📊 学習結果")

    total = len(WORDS) * 3
    correct = 0

    for result in st.session_state.answers.values():
        correct += sum(result.values())

    st.metric(
        "正答率",
        f"{(correct/total)*100:.1f}%"
        if total > 0 else "0%"
    )

    st.write("---")

    st.subheader("間違えた問題")

    for word, result in st.session_state.answers.items():

        if not all(result.values()):

            st.write(f"### ❌ {word}")

            if not result["q1"]:
                st.write("- Q1 意味問題")

            if not result["q2"]:
                st.write("- Q2 類語問題")

            if not result["q3"]:
                st.write("- Q3 スキャニング")

    st.stop()

# =========================
# 問題ページ
# =========================

data = WORDS[st.session_state.current_word]

st.progress(
    (st.session_state.current_word+1)/len(WORDS)
)

st.markdown(
    f'<div class="target-badge">{data["word"].upper()}</div>',
    unsafe_allow_html=True
)

st.write("")

# ------------------
# Q1
# ------------------

st.subheader("Q1 意味を選んでください")

q1 = st.radio(
    "",
    data["meaning_choices"]
)

# ------------------
# Q2
# ------------------

st.subheader("Q2 類語をすべて選んでください")

st.caption(
    f"正解は {len(data['synonyms'])} 個あります"
)

selected_synonyms = []

for item in data["synonym_choices"]:

    if st.checkbox(item):

        selected_synonyms.append(item)

# ------------------
# Q3
# ------------------

st.subheader("Q3 同じ意味の単語をクリック")

question = random.choice(
    data["scanning_questions"]
)

st.info(question["passage"])

selected_word = None

words = question["passage"].replace("\n", " ").split()

cols = st.columns(min(len(words), 8))

for i, word in enumerate(words):

    with cols[i % 8]:

        if st.button(
            word,
            key=f"{i}_{word}"
        ):
            selected_word = word.strip(".,").lower()

# ------------------
# 採点
# ------------------

if st.button(
    "採点する",
    type="primary"
):

    q1_correct = (
        q1 == data["meaning"]
    )

    q2_correct = (
        set(selected_synonyms)
        ==
        set(data["synonyms"])
    )

    q3_correct = (
        selected_word ==
        question["target"].lower()
    )

    st.session_state.answers[
        data["word"]
    ] = {

        "q1": q1_correct,
        "q2": q2_correct,
        "q3": q3_correct
    }

    st.write("---")

    st.success(
        f"Q1 {'⭕' if q1_correct else '❌'}"
    )

    st.success(
        f"Q2 {'⭕' if q2_correct else '❌'}"
    )

    st.success(
        f"Q3 {'⭕' if q3_correct else '❌'}"
    )

    score = sum([
        q1_correct,
        q2_correct,
        q3_correct
    ])

    st.subheader(
        f"この単語のスコア: {score}/3"
    )
