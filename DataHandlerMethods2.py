import math
from re import search, sub
import json
import pprint
import pandas as pd
import os

INVPHI = (math.sqrt(5) - 1) / 2  # 1 / phi


def gss(f, b0, r0, center, neighborhood = .1, tolerance=1e-10):

    a = center - neighborhood
    b = center + neighborhood

    """
    Golden-section search
    to find the minimum of f on [a,b]

    * f: a strictly unimodal function on [a,b]

    """
    while abs(b - a) > tolerance:
        c = b - (b - a) * INVPHI
        d = a + (b - a) * INVPHI
        if f(b0, r0, c) > f(b0, r0, d):
            b = d
        else:  # f(c) > f(d) to find the maximum
            a = c

    return (b + a) / 2

def p(b, r, v):
    return (math.factorial(b+r) * math.pow((1 - v),b) * math.pow(v, r)) / (math.factorial(b) * math.factorial(r))

def p_adjusted_for_win(b, r, v, m = 4):
    t = 0
    for n in range(m):
        t += (p(n,m,v) + p(m,n,v))

    return (p(b,r,v) / t)


def find_optival_v_val(b,r):
    if r == b:
        return .5
    center = r / (b + r)
    if center == 0 or center == 1:
        return center
    return gss(p_adjusted_for_win, b, r, center)


def cleanse_data2(log_id: int, data: dict) -> dict:
    
    # Takes the dictionary and returns the cleaned data for analysis
    
    player_stats = data["players"]

    stats = {
        "Date" : float('nan'),
        "LogID" : float('nan'),
        "RedScoutKillsMin" : float('nan'),
        "RedScoutAssistsMin" : float('nan'),
        "RedScoutDeathsMin" : float('nan'),
        "RedScoutDPM" : float('nan'),
        "RedScoutDTM" : float('nan'),
        "RedScoutHPM" : float('nan'),
        "RedSoldierKillsMin" : float('nan'),
        "RedSoldierAssistsMin" : float('nan'),
        "RedSoldierDeathsMin" : float('nan'),
        "RedSoldierDPM" : float('nan'),
        "RedSoldierDTM" : float('nan'),
        "RedSoldierHPM" : float('nan'),
        "RedPyroKillsMin" : float('nan'),
        "RedPyroAssistsMin" : float('nan'),
        "RedPyroDeathsMin" : float('nan'),
        "RedPyroDPM" : float('nan'),
        "RedPyroDTM" : float('nan'),
        "RedPyroHPM" : float('nan'),
        "RedDemomanKillsMin" : float('nan'),
        "RedDemomanAssistsMin" : float('nan'),
        "RedDemomanDeathsMin" : float('nan'),
        "RedDemomanDPM" : float('nan'),
        "RedDemomanDTM" : float('nan'),
        "RedDemomanHPM" : float('nan'),
        "RedHeavyweaponsKillsMin" : float('nan'),
        "RedHeavyweaponsAssistsMin" : float('nan'),
        "RedHeavyweaponsDeathsMin" : float('nan'),
        "RedHeavyweaponsDPM" : float('nan'),
        "RedHeavyweaponsDTM" : float('nan'),
        "RedHeavyweaponsHPM" : float('nan'),
        "RedEngineerKillsMin" : float('nan'),
        "RedEngineerAssistsMin" : float('nan'),
        "RedEngineerDeathsMin" : float('nan'),
        "RedEngineerDPM" : float('nan'),
        "RedEngineerDTM" : float('nan'),
        "RedEngineerHPM" : float('nan'),
        "RedMedicKillsMin" : float('nan'),
        "RedMedicAssistsMin" : float('nan'),
        "RedMedicDeathsMin" : float('nan'),
        "RedMedicDPM" : float('nan'),
        "RedMedicDTM" : float('nan'),
        "RedMedicHPM" : float('nan'),
        "RedSniperKillsMin" : float('nan'),
        "RedSniperAssistsMin" : float('nan'),
        "RedSniperDeathsMin" : float('nan'),
        "RedSniperDPM" : float('nan'),
        "RedSniperDTM" : float('nan'),
        "RedSniperHPM" : float('nan'),
        "RedSpyKillsMin" : float('nan'),
        "RedSpyAssistsMin" : float('nan'),
        "RedSpyDeathsMin" : float('nan'),
        "RedSpyDPM" : float('nan'),
        "RedSpyDTM" : float('nan'),
        "RedSpyHPM" : float('nan'),
        "RedChargesMin" : float('nan'),
        "RedDropsMin" : float('nan'),
        "BlueScoutKillsMin" : float('nan'),
        "BlueScoutAssistsMin" : float('nan'),
        "BlueScoutDeathsMin" : float('nan'),
        "BlueScoutDPM" : float('nan'),
        "BlueScoutDTM" : float('nan'),
        "BlueScoutHPM" : float('nan'),
        "BlueSoldierKillsMin" : float('nan'),
        "BlueSoldierAssistsMin" : float('nan'),
        "BlueSoldierDeathsMin" : float('nan'),
        "BlueSoldierDPM" : float('nan'),
        "BlueSoldierDTM" : float('nan'),
        "BlueSoldierHPM" : float('nan'),
        "BluePyroKillsMin" : float('nan'),
        "BluePyroAssistsMin" : float('nan'),
        "BluePyroDeathsMin" : float('nan'),
        "BluePyroDPM" : float('nan'),
        "BluePyroDTM" : float('nan'),
        "BluePyroHPM" : float('nan'),
        "BlueDemomanKillsMin" : float('nan'),
        "BlueDemomanAssistsMin" : float('nan'),
        "BlueDemomanDeathsMin" : float('nan'),
        "BlueDemomanDPM" : float('nan'),
        "BlueDemomanDTM" : float('nan'),
        "BlueDemomanHPM" : float('nan'),
        "BlueHeavyweaponsKillsMin" : float('nan'),
        "BlueHeavyweaponsAssistsMin" : float('nan'),
        "BlueHeavyweaponsDeathsMin" : float('nan'),
        "BlueHeavyweaponsDPM" : float('nan'),
        "BlueHeavyweaponsDTM" : float('nan'),
        "BlueHeavyweaponsHPM" : float('nan'),
        "BlueEngineerKillsMin" : float('nan'),
        "BlueEngineerAssistsMin" : float('nan'),
        "BlueEngineerDeathsMin" : float('nan'),
        "BlueEngineerDPM" : float('nan'),
        "BlueEngineerDTM" : float('nan'),
        "BlueEngineerHPM" : float('nan'),
        "BlueMedicKillsMin" : float('nan'),
        "BlueMedicAssistsMin" : float('nan'),
        "BlueMedicDeathsMin" : float('nan'),
        "BlueMedicDPM" : float('nan'),
        "BlueMedicDTM" : float('nan'),
        "BlueMedicHPM" : float('nan'),
        "BlueSniperKillsMin" : float('nan'),
        "BlueSniperAssistsMin" : float('nan'),
        "BlueSniperDeathsMin" : float('nan'),
        "BlueSniperDPM" : float('nan'),
        "BlueSniperDTM" : float('nan'),
        "BlueSniperHPM" : float('nan'),
        "BlueSpyKillsMin" : float('nan'),
        "BlueSpyAssistsMin" : float('nan'),
        "BlueSpyDeathsMin" : float('nan'),
        "BlueSpyDPM" : float('nan'),
        "BlueSpyDTM" : float('nan'),
        "BlueSpyHPM" : float('nan'),
        "BlueChargesMin" : float('nan'),
        "BlueDropsMin" : float('nan'),
        # "AvgRedTime" : float('nan'),
        # "AvgBlueTime" : float('nan'),
        "RedScore" : float('nan'),
        "BlueScore" : float('nan'),        
        # "KOTH?" : float('nan'),
        "Map" : "",
        "Length" : float('nan'),
        "vVal" : float('nan')

    }

    stats["LogID"] = log_id

    try: 
        time = data["length"]
        stats["Length"] = data["length"]

        for player in player_stats:
            # print(player)
            if len(player_stats[player]["class_stats"]) == 1:
                type_player = player_stats[player]["team"] + player_stats[player]["class_stats"][0]["type"].capitalize()
            else:
                # print(f"This got ran for {player}")
                id = -1
                max_time = -1
                for index, class_played in enumerate(player_stats[player]["class_stats"]):
                    if class_played["total_time"] > max_time:
                        max_time = class_played["total_time"]
                        id = index
                type_player = player_stats[player]["team"] + player_stats[player]["class_stats"][id]["type"].capitalize()



            if str(type_player) in ["Unknown", "Undefined"]:
                    continue
                
            stats[type_player + "KillsMin"] = 60 * player_stats[player]["kills"] / time
            stats[type_player + "AssistsMin"] = 60 * player_stats[player]["assists"] / time
            stats[type_player + "DeathsMin"] = 60 * player_stats[player]["deaths"] / time
            stats[type_player + "DPM"] = 60 * player_stats[player]["dmg"] / time
            stats[type_player + "DTM"] = 60 * player_stats[player]["dt"] / time

            total_healed = 0

            for healer in data["healspread"]:
                if player in data["healspread"][healer].keys():
                    total_healed += data["healspread"][healer][player]

            stats[type_player + "HPM"] = 60 * total_healed / time


        # Note: In the main data for logs.tf charges, vaccinator charges are considered
        # charges. Vaccinator charges have been exlcuded from the data.

        red_uber = 0
        blue_uber = 0

        red_cap_time = 0
        blue_cap_time = 0 

        for round in data["rounds"]:
            # first_cap = True
            # prev_time = 0
            for event in round["events"]:
                if event["type"] == "charge" and event["medigun"] in ["medigun", "kritzkrieg", "quickfix"]:
                    if event["team"] == "Red":
                        red_uber += 1
                    else:
                        blue_uber += 1
                    
                # if event["type"] == "pointcap":
                #     if not first_cap:
                #         if event["team"] == "Blue":
                #             red_cap_time += event["time"] - prev_time

                #         elif event["team"] == "Red":
                #             blue_cap_time += event["time"] - prev_time

                #         prev_time = event["time"]

                #     else:
                #         prev_time = event["time"]
                #         first_cap = False
                    


        stats["RedChargesMin"] = 60 * red_uber / time
        stats["BlueChargesMin"] = 60 * blue_uber / time
        stats["RedDropsMin"] = 60 * data["teams"]["Red"]["drops"] / time
        stats["BlueDropsMin"] = 60 * data["teams"]["Blue"]["drops"] / time
        stats["RedScore"] = data["teams"]["Red"]["score"]
        stats["BlueScore"] = data["teams"]["Blue"]["score"]
        stats["AvgRedTime"] = red_cap_time
        stats["AvgBlueTime"] = blue_cap_time

        stats["Map"] = data["info"]["map"]
        stats["Date"] = data["info"]["date"]

        stats["vVal"] = find_optival_v_val(stats["BlueScore"], stats["RedScore"])


    except Exception as e:
        raise e
        print(e, stats["LogID"])
    return stats


if __name__ == "__main__":
    # previously_saved_logs = [entry.name for entry in os.scandir("deep-saved-logs") if entry.is_file()]

    # for index, log in enumerate(previously_saved_logs):
    with open(f"deep-saved-logs/{1223633}.json", 'r') as file:
        game = json.load(file)
    info = cleanse_data2(1223633, game)
    pprint.pprint(info)
        # info["LogID"] = sub(r'\.json$', '', log)
        # if info["KOTH?"] == 1:
        #     df = pd.DataFrame(info, index=[0])
        #     print(df.sample())

        # if index > 10:
        #     break