import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
import re
from DataHandlerMethods import *
import joblib
import xgboost as xgb
import numpy as np
import warnings

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
        dist[f"{max_rounds}-{hypoth_blue_score}"] = chance_of_ocurrence

    for hypoth_red_score in reversed(range(max_rounds)):
        chance_of_ocurrence = math.factorial(hypoth_red_score + max_rounds - 1) / (
                math.factorial(max_rounds - 1) * math.factorial(hypoth_red_score)) * ((1 - pred) ** (max_rounds)) * (
                                      pred ** hypoth_red_score)
        score_chance.append(chance_of_ocurrence)
        score_lines.append(f"{max_rounds}-{hypoth_red_score}")
        dist[f"{hypoth_red_score}-{max_rounds}"] = chance_of_ocurrence


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
def create_bar_chart(data, team1, team2):
    fig, ax = plt.subplots()
    ax.bar(data.keys(), data.values())
    ax.set_xlabel(f'Scorelines - {team1} vs. {team2}')
    ax.set_ylabel('Likelihood')
    ax.set_title('Score Distribution')
    return fig

def get_scaler(dir: str):
    loaded_scaler = joblib.load(dir)
    return loaded_scaler

def get_model(dir: str):
    loaded_model = xgb.Booster()
    loaded_model.load_model(dir)
    return loaded_model

SCALER_DIR = "min_max_scaler.joblib"
MODEL_DIR = "hl_tf2_koth_xgb_a1.model"

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

warnings.filterwarnings("ignore", category=UserWarning, message="X does not have valid feature names, but MinMaxScaler was fitted with feature names")

if __name__ == "__main__":
    st.title("forecast.tf")
    st.write('This website uses an xgboost model and invite player performance to predict their KOTH matches.')

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

    rounds = st.number_input("Number of rounds", min_value=1, max_value=8, value=4, step=1)

    # Now create the form for submission
    with st.form("Submit your selection"):
        submit_button = st.form_submit_button(label="Submit")


    # with st.form("Sample Game Submission"):
      

    if submit_button:
        # st.write(f"Selected Team 1: {selectbox_value}")
        # st.write(f"Selected Games: {multiselect_values}")

        if len(multiselect_values) > 0 and len(multiselect2_values) > 0:
            pattern = r'\d+'

            filtered_matches1 = games[((games['Red'] == st.session_state.selectbox_value) | (games['Blue'] == st.session_state.selectbox_value)) & (games["GameMode"] == "KOTH")].reset_index()
            indicises1 = [int(re.search(pattern, x).group()) - 1 for x in multiselect_values]
            games1 = filtered_matches1.loc[indicises1]

            # st.write(games1)

            team_1_log_info = []
            for index, row in games1.iterrows():
                if row["Blue"] == st.session_state.selectbox_value:
                    try:
                        team_1_log_info.append(select_blue_stats(cleanse_data(make_api_request(f"https://logs.tf/json/{row['LogID']}"))))
                    except Exception as e:
                        raise e
                elif row["Red"] == st.session_state.selectbox_value:
                    try:
                        team_1_log_info.append(select_red_stats(cleanse_data(make_api_request(f"https://logs.tf/json/{row['LogID']}"))))
                    except Exception as e:
                        raise e
            red_average = average_stats(team_1_log_info)
            st.write(f"Calculated average stats for \'{st.session_state.selectbox_value}\'")
            st.write(red_average)
            # st.write(f"Selected Team 2: {selectbox2_value}")
            # st.write(f"Selected Games: {multiselect2_values}")

            filtered_matches2 = games[((games['Red'] == st.session_state.selectbox2_value) | (games['Blue'] == st.session_state.selectbox2_value)) & (games["GameMode"] == "KOTH")].reset_index()
            indicises2 = [int(re.search(pattern, x).group()) - 1 for x in multiselect2_values]
            games2 = filtered_matches2.loc[indicises2]

            # st.write(games2)
            team_2_log_info = []
            for index, row in games2.iterrows():
                if row["Blue"] == st.session_state.selectbox2_value:
                    try:
                        team_2_log_info.append(select_blue_stats(cleanse_data(make_api_request(f"https://logs.tf/json/{row['LogID']}"))))
                    except Exception as e:
                        raise e
                elif row["Red"] == st.session_state.selectbox2_value:
                    try:
                        team_2_log_info.append(select_red_stats(cleanse_data(make_api_request(f"https://logs.tf/json/{row['LogID']}"))))
                    except Exception as e:
                        raise e
            blue_average = average_stats(team_2_log_info)
            # st.write(blue_average)
            st.write(f"Calculated average stats for \'{st.session_state.selectbox2_value}\'")
            st.write(blue_average)
            stats = combine_blue_and_red_aggregates(blue_average, red_average)
            data = np.array([list(stats.values())])

            scaler = get_scaler(SCALER_DIR)

            scaled_data = scaler.transform(data)

            dpred = xgb.DMatrix(scaled_data) 

            model = get_model(MODEL_DIR)

            prediction = model.predict(dpred)
            pred = prediction[0]
            st.write(pred)
            pred = max(0.00000001, min(0.99999999, pred))
            # pred = 1 - pred

            dist, mean, median, predicted_scoreline, sd = get_distribution(pred, rounds)
            st.pyplot(create_bar_chart(dist, selectbox_value, selectbox2_value))
            # print(mean, median, predicted_scoreline)
            # print(dist)
        else:
            st.write("Please select at least one sample log for each team.")