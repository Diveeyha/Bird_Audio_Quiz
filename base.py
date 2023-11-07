import streamlit as st
from birds.database import load_csv, get_birds_by_family, get_birds_by_group
from birds.audio import get_audio
from birds.image import get_image


def initialize_session_state():
    if 'question_number' not in st.session_state:
        st.session_state.question_number = 0
    if 'player_score' not in st.session_state:
        st.session_state.player_score = 0
    if 'question_counter' not in st.session_state:
        st.session_state.question_counter = 0
    if 'previous_answer' not in st.session_state:
        st.session_state.previous_answer = ""
    if 'correct_answer' not in st.session_state:
        st.session_state.correct_answer = ""


def calculate_score(guess, answer):
    if guess == answer:
        st.session_state.player_score += 1
    st.session_state.question_counter += 1


def clear_select():
    calculate_score(st.session_state.player_choice, st.session_state.correct_answer)
    st.session_state.player_choice = None


def reset_session_state():
    st.session_state.question_number = 0
    bird_data.clear()
    get_image.clear()
    st.experimental_rerun()


@st.cache_data
def bird_data(bird_filter):
    birds = bird_filter.sample(frac=1)
    # st.data_editor(birds)
    return birds


def data_filter():
    if st.session_state.filter_select == "Test":
        #bird_filter = get_birds_by_family('sulidae')
        bird_filter = get_birds_by_group('storks')
        return bird_filter
    elif st.session_state.filter_select == "All":
        bird_filter = load_csv()
        return bird_filter
    elif st.session_state.filter_select == "Waterfowl":
        bird_filter = get_birds_by_family('anatidae')
        return bird_filter


st.title("North American Bird Quiz")
initialize_session_state()

with st.sidebar:
    st.radio("Quiz", ["Audio Only", "Image & Audio"], horizontal=True, key="quiz_radio")
    st.selectbox("Filter by", ("Test", "All", "Waterfowl"), key="filter_select")
    st.dataframe(data_filter()['name'], hide_index=True)


st.text("This quiz tests your identification skills.")
birds = bird_data(data_filter())
ind = st.session_state.question_number
options = birds['name'].sort_values()
st.session_state.correct_answer = birds.iloc[ind, 0]

image_url, caption_url = get_image(birds, st.session_state.correct_answer)
# st.text(get_image_urls())
if (st.session_state.quiz_radio == "Image & Audio"):
    st.image(image_url, caption_url, width=470)

st.audio(get_audio(birds, st.session_state.correct_answer))
# st.write(ind, st.session_state.correct_answer)

with st.form(key="user_guess"):
    st.selectbox("Answer:", options, key="player_choice", index=None)

    col1, col2 = st.columns([8, 1])
    with col1:
        if st.form_submit_button("Submit", on_click=clear_select):

            if st.session_state.question_number == (len(birds) - 1):
                st.session_state.previous_answer = st.session_state.correct_answer
                reset_session_state()

            elif st.session_state.question_number < len(birds):
                idx = st.session_state.question_number
                idx = (idx + 1) % len(birds)
                st.session_state.question_number = idx
                st.session_state.previous_answer = st.session_state.correct_answer
                st.experimental_rerun()

    with col2:
        if st.form_submit_button("Reset", type="primary", on_click=clear_select):
            st.session_state.player_score = 0
            st.session_state.question_counter = 0
            st.session_state.previous_answer = ""
            reset_session_state()

col1, col2 = st.columns(2)
with col1:
    if st.session_state.question_counter > 0:
        st.write(f"Correct answer is {st.session_state.previous_answer}.")
with col2:
    if st.session_state.question_counter > 0:
        st.write(f"Score: {st.session_state.player_score} correct out of {st.session_state.question_counter}.")

st.session_state
