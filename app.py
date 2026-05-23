import streamlit as st
import random
import base64
import time

st.set_page_config(page_title="History Date Memorizer", page_icon="😵", layout="centered")




def play_local_sound(path):
    try:
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(
            f'<audio autoplay style="display:none;">'
            f'<source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>',
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        pass


#  question bank 

TRIVIA_CATEGORIES = {
    "Mao's China and Japan": {
        "When did the Qing Dynasty end?": "1911",
        "When was the CCP formed?": "1921",
        "When did the first United Front form?": "1923",
        "When did the first United Front end?": "1927",
        "When was the Jiangxi Soviet established?": "1931",
        "When did the Long March start?": "1934",
        "When did the Long March end?": "1935",
        "Where did Mao Zedong maintain his power after the Long March?": "Yan An",
        "When did the Chinese Civil War end?": "1949",
        "When was the Sino-Soviet Treaty signed?": "1950",
        "When did the Three and Five anti campaings happen? (dates for each of them using /)": "1951/1952",
        "When did the First Five Year plan start?": "1953",
        "When did the First Five Year plan end?": "1957",
        "When did the Hundred Flowers campaign happen?": "1956",
        "When did the Sino-Soviet breakup occur?": "1958",
        "When did the Great Leap forward start?": "1958",
        "When did the Great Leap forward end?": "1962",
        "When did the Great Proletarian Cultural revolution start?": "1966",
        "When did the Great Proletarian Cultural revolution end?": "1976",
        "What is the timeframe for Mao Zedong's rise to power?": "1927-1949",
        "What is timeframe for Mao Zedong's maintanence of power?": "1949-1976"
    },
    "Hitler and the Weimar republic": {
        "This part is WIP": "check later",
        "This part is WIP": "check later",
        "This part is WIP": "check later"
    },
    "The Cold War": {
        "This part is WIP": "check later",
        "This part is WIP": "check later",
        "This part is WIP": "check later"
    },
    "Musolini": {
        "This part is WIP": "check later",
        "This part is WIP": "check later",
        "This part is WIP": "check later"
    },
    "Historiography": {
        "This part is WIP": "check later",
        "This part is WIP": "check later",
        "This part is WIP": "check later"
    }
}




#  styles 

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #ffffff !important;
}

h1, h2, h3, p, span, label, div {
    color: #000000 !important;
    font-family: 'Helvetica', sans-serif !important;
}

[data-testid="stVerticalBlock"] {
    text-align: center !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0.5rem !important;
}

.centered-title {
    text-align: center !important;
    width: 100% !important;
    display: block !important;
}

[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background-color: transparent !important;
    width: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

input {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 2px solid #000000 !important;
    border-radius: 4px !important;
    text-align: center !important;
    font-size: 13pt !important;
}

div.stButton > button,
div.stFormSubmitButton > button {
    background-color: #000000 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 0px !important;
    font-family: 'Helvetica', sans-serif !important;
    font-size: 12pt !important;
    font-weight: bold !important;
    padding-top: 6px !important;
    padding-bottom: 6px !important;
    width: 280px !important;
    margin: 0 auto !important;
    display: block !important;
    cursor: pointer !important;
}
div.stButton > button *, div.stFormSubmitButton > button * { color: #ffffff !important; }
div.stButton > button:hover, div.stFormSubmitButton > button:hover { background-color: #ff0000 !important; }

div.stButton > button[data-testid="baseButton-primary"] { background-color: #ff0000 !important; }
div.stButton > button[data-testid="baseButton-primary"]:hover { background-color: #ffffff !important; }

/* little info button pinned bottom-left */
div.block-container > div[data-testid="stVerticalBlock"] > div.element-container:last-child {
    position: fixed !important;
    bottom: 20px !important;
    left: 20px !important;
    width: 40px !important;
    height: 40px !important;
    z-index: 999999 !important;
    margin: 0 !important;
    padding: 0 !important;
}
div.block-container > div[data-testid="stVerticalBlock"] > div.element-container:last-child div.stButton > button {
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
    padding: 0 !important;
    margin: 0 !important;
    font-size: 14pt !important;
    border-radius: 0px !important;
}
div.block-container > div[data-testid="stVerticalBlock"] > div.element-container:last-child div.stButton > button:hover {
    background-color: #ff0000 !important;
}

div[role="dialog"], div[data-testid="stModal"] > div {
    background-color: #ffffff !important;
}
div[role="dialog"] * { color: #000000 !important; }
</style>
""", unsafe_allow_html=True)


#  session state defaults 

defaults = {
    "play_sound": None,
    "screen": "menu",
    "shuffle_mode_active": False,
    "timer_mode_active": False,
    "start_time": None,
    "total_quiz_time": 0,
    "questions": [],
    "answers": [],
    "current_index": 0,
    "score": 0,
    "feedback_text": "",
    "feedback_color": "#ffffff",
    "input_disabled": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def start_quiz(pool):
    """Kick off a quiz from a list of (question, answer) tuples."""
    if st.session_state.shuffle_mode_active:
        random.shuffle(pool)
    st.session_state.questions = [q for q, _ in pool]
    st.session_state.answers = [a for _, a in pool]
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.feedback_text = ""
    st.session_state.input_disabled = False
    st.session_state.start_time = None
    st.session_state.total_quiz_time = 0
    st.session_state.screen = "quiz"
    st.rerun()


#  popup 

@st.dialog("Hello!")
def show_popup_window():
    st.write("This is an open source trivia game focused on helping memorize key historical events. Simply, choose challenges if you wish and select a category to start. Good luck! ")

#  menu screen 

if st.session_state.screen == "menu":
    st.markdown("<div class='centered-title' style='margin-top:25px;'><b style='font-size:18pt;'>Welcome to HDM!</b></div>", unsafe_allow_html=True)
    st.markdown("<div class='centered-title' style='margin-bottom:5px;'><i style='font-size:11pt;'>Choose your category:</i></div>", unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        for name, questions in TRIVIA_CATEGORIES.items():
            # grey out empty categories
            label = name if questions else f"{name} (soon)"
            if st.button(label, key=f"cat_{name}", disabled=not questions):
                start_quiz(list(questions.items()))

        st.markdown("<div class='centered-title' style='margin-top:15px; padding-bottom:10px;'><b style='font-size:14pt;'>Challenges</b></div>", unsafe_allow_html=True)

        if st.button("MIX OF EVERYTHING", key="mix_btn"):
            everything = [(q, a) for cat in TRIVIA_CATEGORIES.values() for q, a in cat.items()]
            random.shuffle(everything)
            start_quiz(everything)

        # shuffle toggle
        if st.session_state.shuffle_mode_active:
            if st.button("🔥 Shuffling Questions! 🔥", type="primary", key="shuf_on"):
                st.session_state.shuffle_mode_active = False
                st.rerun()
        else:
            if st.button("Shuffle Questions?", key="shuf_off"):
                st.session_state.shuffle_mode_active = True
                st.rerun()

        # timer toggle
        if st.session_state.timer_mode_active:
            if st.button("⏱️ Timer Mode Active! ⏱️", type="primary", key="timer_on"):
                st.session_state.timer_mode_active = False
                st.rerun()
        else:
            if st.button("Activate Timer?", key="timer_off"):
                st.session_state.timer_mode_active = True
                st.rerun()


#  quiz screen

elif st.session_state.screen == "quiz":
    idx = st.session_state.current_index
    total = len(st.session_state.questions)

    if idx < total:
        if st.session_state.timer_mode_active and st.session_state.start_time is None:
            st.session_state.start_time = time.time()

        st.markdown(f"<div class='centered-title' style='margin-top:15px;'><i style='font-size:11pt;'>Question {idx + 1} of {total}</i></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='centered-title' style='margin-top:5px;'><b style='font-size:12pt;'>Score: {st.session_state.score}</b></div>", unsafe_allow_html=True)

        if st.session_state.timer_mode_active and st.session_state.start_time is not None:
            start_ms = int(st.session_state.start_time * 1000)
            st.components.v1.html(f"""
            <style>
                body {{ margin:0; padding:0; background:transparent; }}
                .t {{ text-align:center; font-family:Helvetica,sans-serif; font-size:11pt; font-weight:bold; color:#000; }}
            </style>
            <div class="t">Time Elapsed: <span id="t">00:00.000</span></div>
            <script>
                const start = {start_ms};
                setInterval(() => {{
                    const d = Date.now() - start;
                    const m = Math.floor(d / 60000);
                    const s = Math.floor((d % 60000) / 1000);
                    const ms = d % 1000;
                    document.getElementById("t").innerText =
                        String(m).padStart(2,"0") + ":" +
                        String(s).padStart(2,"0") + "." +
                        String(ms).padStart(3,"0");
                }}, 33);
            </script>
            """, height=25)

        st.markdown(f"<div class='centered-title' style='margin-top:20px; margin-bottom:20px; padding:0 20px;'><b style='font-size:14pt;'>{st.session_state.questions[idx]}</b></div>", unsafe_allow_html=True)

        col = st.columns([1, 2, 1])[1]
        with col:
            with st.form(key="hdm_form", clear_on_submit=True):
                user_input = st.text_input("", key="ans_box", disabled=st.session_state.input_disabled, label_visibility="collapsed")
                submitted = st.form_submit_button("Check Answer")

                if submitted and not st.session_state.input_disabled:
                    correct = st.session_state.answers[idx].strip().lower()
                    if user_input.strip().lower() == correct:
                        st.session_state.score += 1
                        st.session_state.feedback_text = "✓ CORRECT! ✓"
                        st.session_state.feedback_color = "#00cc44"
                        st.session_state.play_sound = "correctsound.mp3"
                    else:
                        st.session_state.feedback_text = f"✗ INCORRECT — answer was {st.session_state.answers[idx].upper()} ✗"
                        st.session_state.feedback_color = "#cc0000"
                        st.session_state.play_sound = "incorrectsound.mp3"
                    st.session_state.input_disabled = True
                    st.rerun()

            if st.session_state.play_sound:
                play_local_sound(st.session_state.play_sound)
                st.session_state.play_sound = None

            if st.session_state.feedback_text:
                st.markdown(
                    f"<div class='centered-title' style='margin-top:10px; font-weight:bold; font-size:13pt; "
                    f"color:{st.session_state.feedback_color} !important;'>{st.session_state.feedback_text}</div>",
                    unsafe_allow_html=True,
                )
                st.write("")
                if st.button("Next Question"):
                    st.session_state.current_index += 1
                    st.session_state.feedback_text = ""
                    st.session_state.input_disabled = False
                    st.rerun()
    else:
        if st.session_state.timer_mode_active and st.session_state.start_time is not None:
            st.session_state.total_quiz_time = time.time() - st.session_state.start_time
        st.session_state.screen = "end"
        st.rerun()


#  end screen 

elif st.session_state.screen == "end":
    total = len(st.session_state.questions)
    pct = (st.session_state.score / total) * 100

    st.markdown("<div class='centered-title' style='margin-top:60px;'><b style='font-size:18pt;'>Clear</b></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='centered-title' style='margin-top:20px; margin-bottom:20px;'>"
        f"<b style='font-size:14pt;'>You scored {st.session_state.score} out of {total}!<br>({pct:.0f}% correct)</b>"
        f"</div>",
        unsafe_allow_html=True,
    )

    if st.session_state.timer_mode_active and st.session_state.total_quiz_time > 0:
        ms_total = int(st.session_state.total_quiz_time * 1000)
        mins, rem = divmod(ms_total, 60000)
        secs, ms = divmod(rem, 1000)
        st.markdown(
            f"<div class='centered-title' style='margin-top:-10px; margin-bottom:25px;'>"
            f"<b style='font-size:13pt; color:#ff0000 !important;'>⏱️ Total Time: {mins:02d}:{secs:02d}.{ms:03d}</b>"
            f"</div>",
            unsafe_allow_html=True,
        )

    col = st.columns([1, 2, 1])[1]
    with col:
        if st.button("Back to main menu", key="menu_return_btn"):
            st.session_state.screen = "menu"
            st.rerun()


#  info button

if st.button("ℹ️", key="true_anchored_bottom_left_btn"):
    show_popup_window()
