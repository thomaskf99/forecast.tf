import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
def get_distribution(pred: float, max_rounds: int) -> tuple:

    dist = {}

    pred = max(0.00000001, min(0.99999999, pred))

    # print(f"The round win % is {pred}")

    score_chance = []
    score_lines = []

    for hypoth_blue_score in range(max_rounds):
        chance_of_ocurrence = math.factorial(max_rounds + hypoth_blue_score - 1)/(math.factorial(max_rounds - 1) * math.factorial(hypoth_blue_score)) * (pred ** (max_rounds)) * ((1-pred) ** hypoth_blue_score)
        score_chance.append(chance_of_ocurrence)
        # score_lines.append(f"{max_rounds}-{hypoth_blue_score}")
        score_lines.append(f"{hypoth_blue_score}-{max_rounds}")
        dist[f"{hypoth_blue_score}-{max_rounds}"] = chance_of_ocurrence

    for hypoth_red_score in reversed(range(max_rounds)):
        chance_of_ocurrence = math.factorial(hypoth_red_score + max_rounds - 1)/(math.factorial(max_rounds - 1) * math.factorial(hypoth_red_score)) * ((1- pred) ** (max_rounds)) * (pred ** hypoth_red_score)
        score_chance.append(chance_of_ocurrence)
        # score_lines.append(f"{hypoth_red_score}-{max_rounds}")
        score_lines.append(f"{max_rounds}-{hypoth_red_score}")
        dist[f"{max_rounds}-{hypoth_red_score}"] = chance_of_ocurrence

    ind = score_chance.index(max(score_chance))
    total = sum(score_chance)
    score_chance = [i / total for i in score_chance]

    predicted_scoreline = score_lines[ind]

    c = 0
    i = 0
    while c < 0.5:
        c+= score_chance[i]
        i+=1
    
    median_index = i - 1
    median_score = score_lines[median_index]

    median = eval(median_score)
    score_lines = [eval(score) for score in score_lines]

    mean = 0
    for i in range(len(score_lines)):
        mean += score_lines[i] * score_chance[i]
    
    # print(f"Mean Score Diff : {mean}")

    var = 0
    for i in range(len(score_lines)):
        var += (score_lines[i]-median)**2 * score_chance[i]
    var /= (len(score_lines) - 1)

    sd = var ** 0.5

    return dist, mean, median, predicted_scoreline, sd

    # score_diff = bluescore - redscore

    # p_val = 0
    # if eval(predicted_scoreline) >= score_diff:
    #     for i in range(len(score_lines)):
    #         if score_lines[i] <= score_diff:
    #             print(score_lines[i], score_chance[i])
    #             p_val += score_chance[i]
    # elif eval(predicted_scoreline) < score_diff:
    #     for i in range(len(score_lines)):
    #         if score_lines[i] >= score_diff:
    #             print(score_lines[i], score_chance[i])
    #             p_val += score_chance[i]

    # ALPHA = 0.20

    # print(f"SD : {sd}")
    # print(f"Chance of Scoreline or more extreme: {p_val}")

def create_bar_chart(data):
    fig, ax = plt.subplots()
    ax.bar(data.keys(), data.values())
    ax.set_xlabel('Scorelines')
    ax.set_ylabel('Likelihood')
    ax.set_title('Score Distribution')
    return fig

if __name__ == "__main__":
    # st.write("""
    # # My first app
    # Hello *world!*
    # """)
    with st.form("Sample Game Submission"):
        st.write("Inside the form")
        pred = st.number_input("Round Probability", min_value = 0.00, max_value = 1.00, value = 0.51, step = 0.01)
        rounds = st.number_input("Number of rounds", min_value=1, max_value=10, value=5, step=1)
        submitted = st.form_submit_button("Submit")
        if submitted:
            dist, mean, median, predicted_scoreline, sd = get_distribution(pred, rounds)
            st.pyplot(create_bar_chart(dist))

    st.write("Outside the form")
    st.title('Dictionary to Bar Graph')
    st.write('This app displays a bar graph based on the provided dictionary data.')
    

    # Display the bar chart in Streamlit




 
# df = pd.read_csv("my_data.csv")
# st.line_chart(df)