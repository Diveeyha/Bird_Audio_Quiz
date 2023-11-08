import streamlit as st
from birds.database import (load_csv, get_birds_by_group,
                            get_birds_by_order, get_birds_by_family)
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
    if 'multi_group' not in st.session_state:
        st.session_state.multi_group = []
    if 'multi_order' not in st.session_state:
        st.session_state.multi_order = []
    if 'multi_family' not in st.session_state:
        st.session_state.multi_family = []


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
    get_audio.clear()
    get_image.clear()
    st.experimental_rerun()


@st.cache_data
def bird_data(bird_filter):
    random_birds = bird_filter.sample(frac=1)
    # st.data_editor(birds)
    return random_birds


def data_filter():
    bird_csv = load_csv()
    if st.session_state.filter_select == "All":
        bird_filter = bird_csv
        return bird_filter
    elif st.session_state.filter_select == "Group":
        selections = bird_csv['group'].unique()
        st.multiselect('Groups', list(selections), key="multi_group")
        bird_filter = get_birds_by_group(st.session_state.multi_group)
        if len(st.session_state.multi_group) >= 1:
            return bird_filter
        else:
            st.stop()
    elif st.session_state.filter_select == "Order":
        selections = bird_csv['order'].unique()
        st.multiselect('Orders', list(selections), key="multi_order")
        bird_filter = get_birds_by_order(st.session_state.multi_order)
        if len(st.session_state.multi_order) >= 1:
            return bird_filter
        else:
            st.stop()
    elif st.session_state.filter_select == "Family":
        selections = bird_csv['family'].unique()
        st.multiselect('Families', list(selections), key="multi_family")
        bird_filter = get_birds_by_family(st.session_state.multi_family)
        if len(st.session_state.multi_family) >= 1:
            return bird_filter
        else:
            st.stop()


st.title("North American Bird Quiz")
st.text("This quiz tests your identification skills.")
initialize_session_state()

with st.sidebar:
    st.radio("Quiz", ["Audio Only", "Image & Audio"], horizontal=True, key="quiz_radio")
    st.selectbox("Select", ("All", "Group", "Order", "Family"), key="filter_select")
    birds = bird_data(data_filter())
    options = birds['name'].sort_values()
    st.dataframe(options, hide_index=True, use_container_width=True)

ind = st.session_state.question_number
st.session_state.correct_answer = birds.iloc[ind, 0]

image_url, caption_url = get_image(birds, st.session_state.correct_answer)
if st.session_state.quiz_radio == "Image & Audio":
    st.image(image_url, caption_url, width=470)

st.audio(get_audio(birds, st.session_state.correct_answer))

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

st.caption("All media sourced from [The Cornell Lab of Ornithology: Macaulay Library](https://www.macaulaylibrary.org)")
# st.session_state
