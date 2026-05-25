import streamlit as st
import random
import base64
import time

st.set_page_config(page_title="History Date Memorizer", page_icon="😵", layout="centered")


# ── helpers ───────────────────────────────────────────────────────────────────

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


# ── question bank ─────────────────────────────────────────────────────────────

TRIVIA_CATEGORIES = {
    "Mao's China and Japan": {
        "When did the Qing Dynasty end?": "1911",
        "When was the CCP formed?": "1921",
        "When did the first United Front form?": "1923",
        "When did the first United Front end?": "1927",
        "When were the warlords defeated in China?": "1928",
        "When was the Jiangxi Soviet established?": "1931",
        "When did the Long March start?": "1934",
        "When did the Long March end?": "1935",
        "Where did Mao Zedong maintain his power after the Long March?": "Yan An",
        "When did the Second United front form?": "1937",
        "When did the Second United front end?": "1945",
        "When did the Chinese Civil War end?": "1949",
        "When was the Sino-Soviet Treaty signed?": "1950",
        "When did the Three and Five anti campaigns happen? (dates for each using /)": "1951/1952",
        "When did the First Five Year Plan start?": "1953",
        "When did the First Five Year Plan end?": "1957",
        "When did the Hundred Flowers campaign happen?": "1956",
        "When did the Sino-Soviet split occur?": "1958",
        "When did the Great Leap Forward start?": "1958",
        "When did the Great Leap Forward end?": "1962",
        "When did the Cultural Revolution start?": "1966",
        "When did the Cultural Revolution end?": "1976",
        "What is the timeframe for Mao's rise to power?": "1927-1949",
        "What is the timeframe for Mao's maintenance of power?": "1949-1976",
        # Japan
        "What is the timeframe for Japan's move to global war?": "1931-1941",
        "When did the bomb explode on the Southern Manchurian railway? (Month and Year)": "September 1931",
        "When was Manchuria self-proclaimed Manchukuo by the Japanese? (Month and Year)": "March 1931",
        "When did China appeal to the LON forming the Lytton Report? (Month and Year)": "December 1931",
        "When was the Lytton Report published?": "1932",
        "When did the Marco Polo Bridge incident happen?": "1937",
        "When did Japan take over Nanjing? (Month and Year)": "December 1937",
        "When was the Tripartite Pact signed?": "1940",
        "When was the Soviet-Japanese Neutrality Pact signed?": "1941",
        "When did Japan attack Pearl Harbor?": "1941",
    },
    "Hitler and the Weimar Republic": {
        # Weimar / Rise to Power
        "When was the Treaty of Versailles signed?": "1918",
        "When did the Spartacist Revolution happen? (Month and Year)": "January 1919",
        "When was the Nazi party founded?": "1920",
        "What was the Nazi paramilitary group during Hitler's rise to power called?": "SA",
        "When did the French occupation of the Ruhr happen?": "1923",
        "When did the Munich Putsch happen?": "1923",
        "Was the Munich Putsch successful?": "No",
        "What book did Hitler write in jail?": "Mein Kampf",
        "When was the Rentemark introduced? (Month and Year)": "November 1923",
        "When was the Rentemark turned into the Reichsmark?": "1924",
        "When did Germany sign the Locarno Treaties?": "1925",
        "When was Germany admitted into the League of Nations?": "1926",
        "When did the Wall Street Crash happen?": "1929",
        "Was there inflation with the Great Depression in Germany?": "No",
        "When was Hitler appointed Chancellor of Germany? (Month and Year)": "January 1933",
        "When did the Reichstag fire occur? (Month and Year)": "February 1933",
        "When was the Enabling Act passed? (Month and Year)": "March 1933",
        "What is the timeframe for Hitler's rise to power?": "1923-1933",
        # Maintenance of Power
        "When did the Night of the Long Knives happen? (Month and Year)": "January 1934",
        "When were the Nuremberg Laws passed?": "1935",
        "When did the Berlin Olympic Games take place?": "1936",
        "When did Kristallnacht occur? (Month and Year)": "November 1938",
        "What is the timeframe for Hitler's maintenance of power?": "1934-1945",
        "When was the New Plan controlling wages and prices enacted?": "1934",
        "When was the Four Year Plan emphasising autarky introduced?": "1936",
        "When was the Hitler Youth created?": "1933",
        "When was the Hitler Youth made compulsory?": "1936",
        "When was the Lebensborn project introduced?": "1935",
        "When was the Mother's Cross established?": "1939",
        # Move to Global War
        "What is the timeframe for Germany's move to global war?": "1933-1939",
        "When did Germany withdraw from the League of Nations?": "1933",
        "When did Hitler announce conscription and remilitarization?": "1935",
        "When did German troops remilitarize the Rhineland? (Month and Year)": "March 1936",
        "When did Germany annex Austria (Anschluss)? (Month and Year)": "1938",
        "When was the Munich Agreement signed?": "1938",
        "When did Germany invade the rest of Czechoslovakia?": "1939",
        "When was the Nazi-Soviet Non-Aggression Pact signed? (Month and Year)": "August 1939",
        "When did Germany invade Poland? (Month and Year)": "September 1939",
    },
    "The Cold War": {},
    "Mussolini": {},
    "Historiography": None,   # None = special sub-category screen
}

# Historiography sub-categories — fill these in as you go
HISTORIOGRAPHY_CATEGORIES = {
    "Mao Historiography": {},
    "Hitler Historiography": {},
    "Cold War Historiography": {},
    "Mussolini Historiography": {},
}


# ── styles ────────────────────────────────────────────────────────────────────

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

/* pinned info button bottom-left */
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
div[role="dialog"], div[data-testid="stModal"] > div { background-color: #ffffff !important; }
div[role="dialog"] * { color: #000000 !important; }
</style>
""", unsafe_allow_html=True)


# ── session state defaults ────────────────────────────────────────────────────

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
    "wrong_questions": [],   # list of (question, correct_answer) for results screen
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def start_quiz(pool):
    """Start a quiz from a list of (question, answer) tuples."""
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
    st.session_state.wrong_questions = []
    st.session_state.screen = "quiz"
    st.rerun()

def go_to_menu():
    st.session_state.screen = "menu"
    st.rerun()


# ── popup ─────────────────────────────────────────────────────────────────────

@st.dialog("Hello!")
def show_popup_window():
    st.write(
        "This is an open source trivia game focused on helping memorize key historical events. "
        "Choose challenges if you wish and select a category to start. Good luck!"
    )


# ── menu screen ───────────────────────────────────────────────────────────────

if st.session_state.screen == "menu":
    st.markdown("<div class='centered-title' style='margin-top:25px;'><b style='font-size:18pt;'>Welcome to HDM!</b></div>", unsafe_allow_html=True)
    st.markdown("<div class='centered-title' style='margin-bottom:5px;'><i style='font-size:11pt;'>Choose your category:</i></div>", unsafe_allow_html=True)

    # CSS for eye icon + hover answer panel
    st.markdown("""
    <style>
    .eye-wrap {
        position: relative;
        display: inline-block;
        vertical-align: middle;
        margin-bottom: 4px;
    }
    .eye-btn {
        width: 36px;
        height: 36px;
        background: #000;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        cursor: default;
        font-size: 16px;
        line-height: 1;
        user-select: none;
    }
    .eye-panel {
        display: none;
        position: absolute;
        left: 44px;
        top: 50%;
        transform: translateY(-50%);
        background: #fff;
        border: 2px solid #000;
        padding: 10px 14px;
        z-index: 9999;
        min-width: 260px;
        max-width: 360px;
        text-align: left;
        font-family: Helvetica, sans-serif;
        font-size: 10.5pt;
        box-shadow: 4px 4px 0px #000;
    }
    .eye-wrap:hover .eye-panel { display: block; }
    .qa-row { margin-bottom: 7px; }
    .qa-q { font-weight: bold; color: #000 !important; }
    .qa-a { color: #cc0000 !important; }
    </style>
    """, unsafe_allow_html=True)

    def make_eye_html(questions_dict):
        rows = ""
        for q, a in questions_dict.items():
            rows += (
                f'<div class="qa-row">'
                f'<div class="qa-q">{q}</div>'
                f'<div class="qa-a">&#8594; {a.upper()}</div>'
                f'</div>'
            )
        return (
            f'<div class="eye-wrap">'
            f'  <div class="eye-btn">&#128065;</div>'
            f'  <div class="eye-panel">'
            f'    <div style="font-weight:bold;margin-bottom:8px;border-bottom:1px solid #000;padding-bottom:4px;">Answers</div>'
            f'    {rows}'
            f'  </div>'
            f'</div>'
        )

    col = st.columns([1, 2, 1])[1]
    with col:
        for name, questions in TRIVIA_CATEGORIES.items():
            has_q = bool(questions)  # False for None and empty dict

            # eye icon row — only for categories that actually have questions
            if has_q:
                st.markdown(make_eye_html(questions), unsafe_allow_html=True)

            if questions is None:
                if st.button(name, key=f"cat_{name}"):
                    st.session_state.screen = "historiography_menu"
                    st.rerun()
            elif questions:
                if st.button(name, key=f"cat_{name}"):
                    start_quiz(list(questions.items()))
            else:
                st.button(f"{name} (soon)", key=f"cat_{name}", disabled=True)

        st.markdown("<div class='centered-title' style='margin-top:15px; padding-bottom:10px;'><b style='font-size:14pt;'>Challenges</b></div>", unsafe_allow_html=True)

        if st.button("MIX OF EVERYTHING", key="mix_btn"):
            everything = [
                (q, a)
                for cat in TRIVIA_CATEGORIES.values()
                if cat  # skip None and empty
                for q, a in cat.items()
            ]
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


# ── historiography sub-menu ───────────────────────────────────────────────────

elif st.session_state.screen == "historiography_menu":
    st.markdown("<div class='centered-title' style='margin-top:25px;'><b style='font-size:18pt;'>Historiography</b></div>", unsafe_allow_html=True)
    st.markdown("<div class='centered-title' style='margin-bottom:10px;'><i style='font-size:11pt;'>Choose a topic:</i></div>", unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        for name, questions in HISTORIOGRAPHY_CATEGORIES.items():
            if questions:
                if st.button(name, key=f"histo_{name}"):
                    start_quiz(list(questions.items()))
            else:
                st.button(f"{name} (soon)", key=f"histo_{name}", disabled=True)

        st.write("")
        if st.button("← Back to Menu", key="histo_back"):
            go_to_menu()


# ── quiz screen ───────────────────────────────────────────────────────────────

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

                # swap the button label depending on state — same position, different action
                if st.session_state.input_disabled:
                    next_clicked = st.form_submit_button("Next Question")
                    check_clicked = False
                else:
                    check_clicked = st.form_submit_button("Check Answer")
                    next_clicked = False

                if check_clicked:
                    correct = st.session_state.answers[idx].strip().lower()
                    if user_input.strip().lower() == correct:
                        st.session_state.score += 1
                        st.session_state.feedback_text = "✓ CORRECT! ✓"
                        st.session_state.feedback_color = "#00cc44"
                        st.session_state.play_sound = "correctsound.mp3"
                    else:
                        st.session_state.wrong_questions.append(
                            (st.session_state.questions[idx], st.session_state.answers[idx])
                        )
                        st.session_state.feedback_text = f"✗ INCORRECT — answer was {st.session_state.answers[idx].upper()} ✗"
                        st.session_state.feedback_color = "#cc0000"
                        st.session_state.play_sound = "incorrectsound.mp3"
                    st.session_state.input_disabled = True
                    st.rerun()

                if next_clicked:
                    st.session_state.current_index += 1
                    st.session_state.feedback_text = ""
                    st.session_state.input_disabled = False
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

            # give up button — always visible during quiz
            st.write("")
            if st.button("Give Up", key="give_up_btn"):
                go_to_menu()

    else:
        if st.session_state.timer_mode_active and st.session_state.start_time is not None:
            st.session_state.total_quiz_time = time.time() - st.session_state.start_time
        st.session_state.screen = "end"
        st.rerun()


# ── end screen ────────────────────────────────────────────────────────────────

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
        if st.button("See Results", key="see_results_btn"):
            st.session_state.screen = "results"
            st.rerun()

        st.write("")
        if st.button("Back to main menu", key="menu_return_btn"):
            go_to_menu()


# ── results screen ────────────────────────────────────────────────────────────

elif st.session_state.screen == "results":
    wrong = st.session_state.wrong_questions

    if not wrong:
        st.markdown("<div class='centered-title' style='margin-top:60px;'><b style='font-size:22pt;'>🎉 Good job!</b></div>", unsafe_allow_html=True)
        st.markdown("<div class='centered-title' style='margin-top:10px;'><i style='font-size:12pt;'>You got everything right.</i></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='centered-title' style='margin-top:40px; margin-bottom:5px;'><b style='font-size:18pt;'>Questions you missed</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='centered-title' style='margin-bottom:20px;'><i style='font-size:11pt;'>{len(wrong)} wrong out of {len(st.session_state.questions)}</i></div>", unsafe_allow_html=True)

        for q, a in wrong:
            st.markdown(
                f"<div style='text-align:left; margin: 8px auto; max-width:480px; border-left: 3px solid #000; padding-left:12px;'>"
                f"<b style='font-size:11pt;'>{q}</b><br>"
                f"<span style='font-size:11pt; color:#cc0000 !important;'>→ {a.upper()}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.write("")
    col = st.columns([1, 2, 1])[1]
    with col:
        if st.button("Back to main menu", key="results_menu_btn"):
            go_to_menu()


# ── info button (must stay last for CSS pin to work) ─────────────────────────

if st.button("ℹ️", key="true_anchored_bottom_left_btn"):
    show_popup_window()
