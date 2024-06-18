import json
from itertools import combinations
import pandas as pd

if __name__ == "__main__":

    with open("invite-games.csv", encoding="utf8") as invite_games:
        invite_games = pd.read_csv(invite_games, index_col = [0])

    with open("invite-games-paired.csv", encoding="utf8") as invite_game_pairings:
        invite_game_pairings = pd.read_csv(invite_game_pairings, index_col = [0])

        for team_pair in combinations(invite_games.values.tolist(), 2):
            team_A = team_pair[0]
            team_B = team_pair[1]
            
    # If the two LogID's are equivalent, they are the same game

            if team_A[1] == team_B[1] and team_A[1] not in invite_game_pairings['LogID'].tolist():
                if team_A[2] == "Blue":
                    invite_game_pairings = pd.concat([invite_game_pairings, pd.DataFrame({"Blue" : team_A[0], "Red": team_B[0],"LogID" : team_A[1], "GameMode" : team_A[3]}, index = [0])], ignore_index=True)
                else:
                    invite_game_pairings = pd.concat([invite_game_pairings, pd.DataFrame({"Blue" : team_B[0], "Red": team_A[0],"LogID" : team_A[1], "GameMode" : team_A[3]}, index = [0])], ignore_index=True)

                print(invite_game_pairings.tail(1))

        invite_game_pairings.to_csv('invite-games-paired.csv')


    with open("invite-games-paired.csv", encoding="utf8") as invite_game_pairings:
        invite_game_pairings = pd.read_csv(invite_game_pairings, index_col = [0])

        for index, row in invite_games.iterrows():
            if row["LogID"] not in invite_game_pairings["LogID"].values.tolist():
                if row["TeamColor"] == "Blue":
                    invite_game_pairings = pd.concat([invite_game_pairings, pd.DataFrame({"Blue" : row["TeamName"], "Red": "Unknown","LogID" : team_A[1], "GameMode" : team_A[3]}, index = [0])], ignore_index=True)
                else:
                    invite_game_pairings = pd.concat([invite_game_pairings, pd.DataFrame({"Blue" : "Unknown", "Red": row["TeamName"],"LogID" : team_A[1], "GameMode" : team_A[3]}, index = [0])], ignore_index=True)


        for team_pair in combinations(invite_games.values.tolist(), 2):
            team_A = team_pair[0]
            team_B = team_pair[1]
            
    # If the two LogID's are equivalent, they are the same game

            if team_A[1] == team_B[1] and team_A[1] not in invite_game_pairings['LogID'].tolist():
                if team_A[2] == "Blue":
                    invite_game_pairings = pd.concat([invite_game_pairings, pd.DataFrame({"Blue" : team_A[0], "Red": team_B[0],"LogID" : team_A[1], "GameMode" : team_A[3]}, index = [0])], ignore_index=True)
                else:
                    invite_game_pairings = pd.concat([invite_game_pairings, pd.DataFrame({"Blue" : team_B[0], "Red": team_A[0],"LogID" : team_A[1], "GameMode" : team_A[3]}, index = [0])], ignore_index=True)

                print(invite_game_pairings.tail(1))
        
        invite_game_pairings = invite_game_pairings.sort_values(by='LogID', ascending=False).reset_index(drop=True)

        invite_game_pairings.to_csv('invite-games-paired.csv')