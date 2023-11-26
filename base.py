# import pandas as pd
import streamlit as st
from birds.database import (load_csv, get_birds_by_group, get_birds_by_taxonomic_name,
                            get_birds_by_order, get_birds_by_family)
from birds.audio import get_audio
from birds.image import get_image
from birds.utils import clean_bird_name


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
    if 'multi_species' not in st.session_state:
        st.session_state.multi_species = []
    if 'answered_correctly' not in st.session_state:
        st.session_state.answered_correctly = False


def calculate_score(guess, answer):
    if guess == answer:
        st.session_state.answered_correctly = True
        st.session_state.player_score += 1
    else:
        st.session_state.answered_correctly = False
    st.session_state.question_counter += 1


def clear_select():
    calculate_score(st.session_state.player_choice, st.session_state.correct_answer)
    st.session_state.player_choice = None


def reset_session_state():
    st.session_state.question_number = 0
    bird_data.clear()
    get_audio.clear()
    get_image.clear()
    st.rerun()


@st.cache_data
def bird_data(bird_filter):
    random_birds = bird_filter.sample(frac=1)
    return random_birds


def filter_selections(bird_csv, user_input):
    test_err = ('''Quiz will automatically load when minimum requirements are met.\n
                 Please make sure that more than one species is included in the filter.''')

    lookup_dict = {'group': get_birds_by_group, 'order': get_birds_by_order,
                   'family': get_birds_by_family, 'species': get_birds_by_taxonomic_name}
    key_dict = {'multi_group': st.session_state.multi_group, 'multi_order': st.session_state.multi_order,
                'multi_family': st.session_state.multi_family, 'multi_species': st.session_state.multi_species}

    user_input_lower = user_input.lower()
    key_var = "multi_" + user_input_lower

    selections = bird_csv[user_input_lower].unique()
    selections = [names.lower() for names in selections]
    selections = sorted(selections)

    get_birds_func_call = lookup_dict[user_input_lower]

    selected = []
    removed = []
    [selected.append(x) if len(get_birds_func_call(bird_csv, [x])) > 0
        else removed.append(x) for x in key_dict[key_var]]
    delimiter = ', '
    if len(removed) == 1:
        st.toast(f"{delimiter.join(removed)} was removed because it has not been reported in "
                 f"{st.session_state.filter_state}.")
    elif len(removed) > 1:
        st.toast(f"{delimiter.join(removed)} were removed because they have not been reported in "
                 f"{st.session_state.filter_state}.")

    st.sidebar.multiselect(user_input, list(selections), selected,  key=key_var, label_visibility="collapsed")

    bird_filter = get_birds_func_call(bird_csv, key_dict[key_var])
    df_birds = bird_filter['name'].unique()

    if len(key_dict[key_var]) >= 1:
        if len(bird_filter) > 1:
            return bird_filter
        else:
            st.sidebar.dataframe(df_birds, hide_index=True, use_container_width=True)
            st.divider()
            return st.error(test_err), st.stop()
    else:
        st.sidebar.dataframe(df_birds, hide_index=True, use_container_width=True)
        st.divider()
        return st.error(test_err), st.stop()


def data_filter(bird_csv):
    if st.session_state.filter_select == "All":
        return bird_csv
    else:
        return filter_selections(bird_csv, st.session_state.filter_select)


def state_filter(state):
    bird_csv = load_csv('state_info.csv')
    if state != 'All':
        bird_csv = bird_csv[bird_csv[state.lower()] == 1]
    return bird_csv


def state_dropdown_options():
    state_options = load_csv('state_codes.csv')
    state_options.loc[-1] = ['All']
    state_options.index = state_options.index + 1  # shifting index
    state_options.sort_index(inplace=True)
    return state_options


def main():
    st.title("USA Bird Quiz")
    initialize_session_state()

    st.sidebar.radio("Quiz", ["Audio Only", "Image & Audio"], horizontal=True, key="quiz_radio")
    st.sidebar.divider()
    st.sidebar.selectbox("Filter by State:", state_dropdown_options(), key="filter_state")
    st.sidebar.divider()
    st.sidebar.radio("Filter by: ", ["All", "Group", "Order", "Family", "Species"], horizontal=True,
                     key="filter_select")

    birds = bird_data(data_filter(state_filter(st.session_state.filter_state)))
    options = birds['name'].sort_values()
    st.sidebar.divider()
    st.sidebar.text(f"{len(options)} species")
    st.sidebar.dataframe(options, hide_index=True, use_container_width=True)

    ind = st.session_state.question_number
    if ind < len(options):
        st.session_state.correct_answer = birds.iloc[ind, 0]
    else:
        ind = (ind + 1) % len(birds)
        st.session_state.correct_answer = birds.iloc[ind, 0]
    answer_dropdown = birds.loc[birds['quiz_answer_groups'] == birds.iloc[ind, 5]]

    image_url, caption_url = get_image(birds, st.session_state.correct_answer)
    if st.session_state.quiz_radio == "Image & Audio":
        adj1, adj2, adj3 = st.columns([1, 4, 1])
        adj2.image(image_url, caption_url, use_column_width="always")

    st.audio(get_audio(birds, st.session_state.correct_answer))

    with st.form(key="user_guess"):
        if len(answer_dropdown) < 10:
            answer_options = options
        else:
            answer_options = answer_dropdown['name']

        col1, empty, col2, col3 = st.columns([2, 0.75, 0.75, 0.75])
        col1.selectbox("Answer:", answer_options.sort_values(), key="player_choice",
                       index=None, label_visibility="collapsed")

        with col2:
            if st.form_submit_button("Submit", on_click=clear_select):

                if st.session_state.question_number == (len(birds) - 1):
                    st.session_state.previous_answer = st.session_state.correct_answer
                    reset_session_state()

                elif st.session_state.question_number < len(birds):
                    idx = st.session_state.question_number
                    idx = (idx + 1) % len(birds)
                    st.session_state.question_number = idx
                    st.session_state.previous_answer = st.session_state.correct_answer
                    st.rerun()

        with col3:
            if st.form_submit_button("Reset", type="primary", on_click=clear_select):
                st.session_state.player_score = 0
                st.session_state.question_counter = 0
                st.session_state.previous_answer = ""
                reset_session_state()

    print_col1, print_col2 = st.columns([1.25, 0.9])
    with print_col1:
        if st.session_state.question_counter > 0:
            formatted_name = clean_bird_name(st.session_state.previous_answer)
            if st.session_state.answered_correctly:
                st.write(f"[{st.session_state.previous_answer}](https://www.allaboutbirds.org/guide/{formatted_name})"
                         f":green[ is correct! Great Job!] 🎉")
            else:
                st.write(f":red[Incorrect. The correct answer is [{st.session_state.previous_answer}]"
                         f"(https://www.allaboutbirds.org/guide/{formatted_name}).]")
    with print_col2:
        if st.session_state.question_counter > 0:
            st.write(f"Score: {st.session_state.player_score} correct out of {st.session_state.question_counter}.")

    st.divider()
    st.caption(f"All media sourced from [The Cornell Lab of Ornithology: Macaulay Library]"
               f"(https://www.macaulaylibrary.org)")


# st.session_state


# Run main
if __name__ == "__main__":
    st.markdown("""<style>body {text-align: center}
                p {text-align: center} 
                button {float: center} </style>""", unsafe_allow_html=True)
    main()
