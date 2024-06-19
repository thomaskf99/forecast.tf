import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt

# Load data
with open("invite-player-list.csv", encoding="utf8") as f:
    players = pd.read_csv(f)
    teams = players["TeamName"].drop_duplicates().values.tolist()

with open("invite-games-paired.csv", encoding="utf8") as paired:
    games = pd.read_csv(paired, index_col=0)

# Define the function to get distribution (unchanged)
def get_distribution(pred: float, max_rounds: int) -> tuple:
    dist = {}
    pred = max(0.00000001, min(0.99999999, pred))
    score_chance = []
    score_lines = []

    for hypoth_blue_score in range(max_rounds):
        chance_of_ocurrence = math.factorial(max_rounds + hypoth_blue_score - 1) / (
                math.factorial(max_rounds - 1) * math.factorial(hypoth_blue_score)) * (pred ** (max_rounds)) * (
                                      (1 - pred) ** hypoth_blue_score)
        score_chance.append(chance_of_ocurrence)
        score_lines.append(f"{hypoth_blue_score}-{max_rounds}")
        dist[f"{hypoth_blue_score}-{max_rounds}"] = chance_of_ocurrence

    for hypoth_red_score in reversed(range(max_rounds)):
        chance_of_ocurrence = math.factorial(hypoth_red_score + max_rounds - 1) / (
                math.factorial(max_rounds - 1) * math.factorial(hypoth_red_score)) * ((1 - pred) ** (max_rounds)) * (
                                      pred ** hypoth_red_score)
        score_chance.append(chance_of_ocurrence)
        score_lines.append(f"{max_rounds}-{hypoth_red_score}")
        dist[f"{max_rounds}-{hypoth_red_score}"] = chance_of_ocurrence

    ind = score_chance.index(max(score_chance))
    total = sum(score_chance)
    score_chance = [i / total for i in score_chance]

    predicted_scoreline = score_lines[ind]

    c = 0
    i = 0
    while c < 0.5:
        c += score_chance[i]
        i += 1

    median_index = i - 1
    median_score = score_lines[median_index]

    median = eval(median_score)
    score_lines = [eval(score) for score in score_lines]

    mean = 0
    for i in range(len(score_lines)):
        mean += score_lines[i] * score_chance[i]

    var = 0
    for i in range(len(score_lines)):
        var += (score_lines[i] - median) ** 2 * score_chance[i]
    var /= (len(score_lines) - 1)

    sd = var ** 0.5

    return dist, mean, median, predicted_scoreline, sd

# Define the function to get multiselect options (unchanged)
def get_multiselect_options(matches, team_name, KOTH):
    filtered_matches = matches[((matches['Red'] == team_name) | (matches['Blue'] == team_name)) & (matches["GameMode"] == KOTH)].reset_index()
    options = [f'{index + 1} - {row["Blue"]} vs. {row["Red"]} - {row["Map"]} - {row["LogID"]}' for index, row in filtered_matches.iterrows()]
    return options

# Define the function to create a bar chart (unchanged)
def create_bar_chart(data):
    fig, ax = plt.subplots()
    ax.bar(data.keys(), data.values())
    ax.set_xlabel('Scorelines')
    ax.set_ylabel('Likelihood')
    ax.set_title('Score Distribution')
    return fig

# Initialize session state
if 'selectbox_value' not in st.session_state:
    st.session_state.selectbox_value = teams[0]
if 'multiselect_options' not in st.session_state:
    st.session_state.multiselect_options = get_multiselect_options(games, teams[0], "KOTH")

if 'selectbox2_value' not in st.session_state:
    st.session_state.selectbox2_value = teams[1]
if 'multiselect2_options' not in st.session_state:
    st.session_state.multiselect2_options = get_multiselect_options(games, teams[1], "KOTH")    

# Function to update multiselect options
def update_multiselect_options():
    st.session_state.multiselect_options = get_multiselect_options(games, st.session_state.selectbox_value, "KOTH")

def update_multiselect2_options():
    st.session_state.multiselect2_options = get_multiselect_options(games, st.session_state.selectbox2_value, "KOTH")


if __name__ == "__main__":
    st.title("forecast.tf - developed by the freak")
    st.write('This website uses an xgboost model and invite player performance to predict their matches.')

    selectbox_value = st.selectbox(
        'Select a team for Team 1:',
        teams,
        key="selectbox_value",
        on_change=update_multiselect_options
    )
    multiselect_values = st.multiselect(
        'Select the sample games',
        key = "multiselect_values",
        options=st.session_state.multiselect_options
    )

    selectbox2_value = st.selectbox(
        'Select a team for Team 2:',
        teams,
        key = 'selectbox2_value',
        on_change=update_multiselect2_options 
    )

    multiselect2_values = st.multiselect(
        'Select the sample games',
        key = 'multiselect2_values',
        options=st.session_state.multiselect2_options
    )

    rounds = st.number_input("Number of rounds", min_value=1, max_value=10, value=5, step=1)

    # Now create the form for submission
    with st.form("Submit your selection"):
        submit_button = st.form_submit_button(label="Submit")


    with st.form("Sample Game Submission"):
        st.write("Example Distribution")
        pred = st.number_input("Round Probability", min_value = 0.00, max_value = 1.00, value = 0.51, step = 0.01)
        rounds = st.number_input("Number of rounds", min_value=1, max_value=10, value=5, step=1)
        submitted = st.form_submit_button("Submit")
        if submitted:
            dist, mean, median, predicted_scoreline, sd = get_distribution(pred, rounds)
            st.pyplot(create_bar_chart(dist))

    if submit_button:
        st.write(f"Selected Team 1: {selectbox_value}")
        st.write(f"Selected Games: {multiselect_values}")
        st.write(f"Selected Team 2: {selectbox2_value}")
        st.write(f"Selected Games: {multiselect2_values}")