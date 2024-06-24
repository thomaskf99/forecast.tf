from re import search
from itertools import combinations
from DataHandlerMethods import make_api_request
import pandas as pd



# Searches for the logs of each team since Wed, May 8, 2024
# Stores the output as a JSON in TeamGames.json

if __name__ == "__main__":

    with open("invite-games.csv", "r", encoding="utf8") as previous_games:
        logsCompiled = pd.read_csv(previous_games, index_col = 0)
    
    with open("invite-player-list.csv", "r", encoding="utf8") as f:

        team_ids = pd.read_csv(f)

        for team in team_ids["TeamName"].unique():

            minimum_team_identifying_playercount = 6 #if team == "The Hardworking Hornets" else 7

            players = team_ids.loc[team_ids["TeamName"] == team]["Steam64ID"].values.tolist()
            

            # Constructs combinations of players in case of ringers or subs playing

            for playerset in combinations(players, minimum_team_identifying_playercount):
                
                requestString = ""

                for player in playerset:
                    requestString += str(player) + ','
                requestString = requestString[:-1]
        
                matches = make_api_request(f"http://logs.tf/api/v1/log?player={requestString}&limit=1000")

                for log in matches['logs']:

                    # Checks if the log is unique and sufficiently recent

                    if log['id'] not in logsCompiled.loc[logsCompiled["TeamName"] == team]["LogID"].unique() and log['date'] > 1715140800:
                        # print(log['id'])
                        # print(logsCompiled.loc[logsCompiled["TeamName"] == team]["LogID"].unique())

                        log_info = make_api_request(f"http://logs.tf/api/v1/log/{log['id']}")

    
                        # If the map of the log has a plus (indicative of two logs being combined), it is not included

                        if "+" in log_info["info"]["map"]:
                            print("Failed naming convention")

                            continue
                        
                        # Likewise if the log does not have a map name in typical map format (ie pl_vigil_rc9) then it is thrown out
                        
                        try:
                            map_type = (search("^[^_]+(?=_)",log_info["info"]["map"])).group().upper()
                        except:
                            print("Failed naming convention")
                            continue

                        # If all of the members that make up this version of each team are not present
                        # on the same team color, then the log is thrown out as well

                        count = 0

                        for player in playerset:
                            # print(log['id'])
                            if log_info["players"][team_ids.loc[team_ids["Steam64ID"] == player]["SteamID3"].values[:1][0]]["team"] == "Red":
                                count += 1
                            else:
                                count -= 1
                        
                        if count == minimum_team_identifying_playercount:
                            color = "Red"
                        elif count == -1 * minimum_team_identifying_playercount:
                            color = "Blue"
                        else:
                            continue
                        
                        logsCompiled = pd.concat([logsCompiled, pd.DataFrame({"TeamName" : team, "LogID" : log['id'], "TeamColor" : color, "GameMode" : map_type, "Map" : log_info["info"]["map"]}, index = [0])], ignore_index=True)
                        print(logsCompiled.tail(1))                        

    # The logs are then saved to TeamGames.json
    

    with open("invite-games.csv", "w", encoding="utf8") as outfile:
        logsCompiled.to_csv('invite-games.csv')