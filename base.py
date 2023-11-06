import streamlit as st
import random
from birds.database import load_csv, get_birds_by_family
from birds.audio import find_bird_urls


def initialize_session_state():
    if 'question_number' not in st.session_state:
        st.session_state.question_number = 0
    if 'player_score' not in st.session_state:
        st.session_state.player_score = 0
    if 'question_counter' not in st.session_state:
        st.session_state.question_counter = 0
    if 'previous_answer' not in st.session_state:
        st.session_state.previous_answer = ""
        

def clear_select():
    st.session_state.my_select = None


def reset_session_state():
    st.session_state.question_number = 0
    bird_data.clear()
    st.experimental_rerun()


@st.cache_data
def bird_data(bird_filter):
    birds = bird_filter.sample(frac=1)
    # st.data_editor(birds)
    return birds


def get_audio(question_number, birds, answer):
    audio_file = find_bird_urls(birds['name'])
    url = random.choice(audio_file[answer])
    return url


def data_filter():
    if st.session_state.txt_filter == "Test":
        bird_filter = get_birds_by_family('sulidae')
        return bird_filter
    elif st.session_state.txt_filter == "All":
        bird_filter = load_csv()
        return bird_filter
    elif st.session_state.txt_filter == "Waterfowl":
        bird_filter = get_birds_by_family('anatidae')
        return bird_filter


def calculate_score(player_choice, correct_answer):
    if player_choice == correct_answer:
        st.session_state.player_score += 1
    st.session_state.question_counter += 1


st.title("North American Bird Quiz")
initialize_session_state()

tab1, tab2 = st.tabs(["Bird List", "Audio"])
with tab1:
    st.radio("Filter by", ["Test", "All", "Waterfowl"], horizontal=True, key="txt_filter")
    st.dataframe(data_filter(), hide_index=True)

with tab2:
    birds = bird_data(data_filter())
    ind = st.session_state.question_number
    options = birds['name'].sort_values()
    answer = birds.iloc[ind, 0]
    st.audio(get_audio(ind, birds, answer))
    # st.write(ind, answer)

    guess = st.selectbox("Answer:", options, key="my_select", index=None)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit", key="submit", on_click=clear_select):
            calculate_score(guess, answer)

            if st.session_state.question_number == (len(birds)-1):
                st.session_state.previous_answer = answer
                reset_session_state()

            elif st.session_state.question_number < len(birds):
                idx = st.session_state.question_number
                idx = (idx + 1) % len(birds)
                st.session_state.question_number = idx
                st.session_state.previous_answer = answer
                st.experimental_rerun()


    if col2.button("Reset", key="reset", type="primary", on_click=clear_select):
        st.session_state.player_score = 0
        st.session_state.question_counter = 0
        st.session_state.previous_answer = ""
        reset_session_state()

    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.question_counter > 0:
            st.write(f"The correct answer is {st.session_state.previous_answer}.")
    with col2:
        if st.session_state.question_counter > 0:
            st.write(f"Score: {st.session_state.player_score} correct out of {st.session_state.question_counter}.")

st.sidebar.st.session_state
