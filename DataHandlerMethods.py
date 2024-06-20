import requests
from re import search
import math
# https://logs.tf/about#json
# http://logs.tf/api/v1/log?title=X&uploader=Y&player=Z&limit=N&offset=N

def make_api_request(url : str, params={}) -> dict:
        
        # Requests the logs.tf API and returns the json data as a dictionary
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception("Request failed with status code: " + str(response.status_code))
        
        else:
             return response.json()

def cleanse_data(data: dict) -> dict:
    
    # Takes the dictionary and returns the cleaned data for analysis
    
    player_stats = data["players"]

    stats = {
        "Date" : float('nan'),
        "LogID" : float('nan'),
        "RedScout100KillsMin" : float('nan'),
        "RedScout100AssistsMin" : float('nan'),
        "RedScout100DeathsMin" : float('nan'),
        "RedScout100DPM" : float('nan'),
        "RedScout100DTM" : float('nan'),
        "RedScout100HPM" : float('nan'),
        "RedSoldier100KillsMin" : float('nan'),
        "RedSoldier100AssistsMin" : float('nan'),
        "RedSoldier100DeathsMin" : float('nan'),
        "RedSoldier100DPM" : float('nan'),
        "RedSoldier100DTM" : float('nan'),
        "RedSoldier100HPM" : float('nan'),
        "RedPyro100KillsMin" : float('nan'),
        "RedPyro100AssistsMin" : float('nan'),
        "RedPyro100DeathsMin" : float('nan'),
        "RedPyro100DPM" : float('nan'),
        "RedPyro100DTM" : float('nan'),
        "RedPyro100HPM" : float('nan'),
        "RedDemoman100KillsMin" : float('nan'),
        "RedDemoman100AssistsMin" : float('nan'),
        "RedDemoman100DeathsMin" : float('nan'),
        "RedDemoman100DPM" : float('nan'),
        "RedDemoman100DTM" : float('nan'),
        "RedDemoman100HPM" : float('nan'),
        "RedHeavyweapons100KillsMin" : float('nan'),
        "RedHeavyweapons100AssistsMin" : float('nan'),
        "RedHeavyweapons100DeathsMin" : float('nan'),
        "RedHeavyweapons100DPM" : float('nan'),
        "RedHeavyweapons100DTM" : float('nan'),
        "RedHeavyweapons100HPM" : float('nan'),
        "RedEngineer100KillsMin" : float('nan'),
        "RedEngineer100AssistsMin" : float('nan'),
        "RedEngineer100DeathsMin" : float('nan'),
        "RedEngineer100DPM" : float('nan'),
        "RedEngineer100DTM" : float('nan'),
        "RedEngineer100HPM" : float('nan'),
        "RedMedic100KillsMin" : float('nan'),
        "RedMedic100AssistsMin" : float('nan'),
        "RedMedic100DeathsMin" : float('nan'),
        "RedMedic100DPM" : float('nan'),
        "RedMedic100DTM" : float('nan'),
        "RedMedic100HPM" : float('nan'),
        "RedSniper100KillsMin" : float('nan'),
        "RedSniper100AssistsMin" : float('nan'),
        "RedSniper100DeathsMin" : float('nan'),
        "RedSniper100DPM" : float('nan'),
        "RedSniper100DTM" : float('nan'),
        "RedSniper100HPM" : float('nan'),
        "RedSpy100KillsMin" : float('nan'),
        "RedSpy100AssistsMin" : float('nan'),
        "RedSpy100DeathsMin" : float('nan'),
        "RedSpy100DPM" : float('nan'),
        "RedSpy100DTM" : float('nan'),
        "RedSpy100HPM" : float('nan'),
        "RedCharges" : float('nan'),
        "RedDrops" : float('nan'),
        "BlueScout100KillsMin" : float('nan'),
        "BlueScout100AssistsMin" : float('nan'),
        "BlueScout100DeathsMin" : float('nan'),
        "BlueScout100DPM" : float('nan'),
        "BlueScout100DTM" : float('nan'),
        "BlueScout100HPM" : float('nan'),
        "BlueSoldier100KillsMin" : float('nan'),
        "BlueSoldier100AssistsMin" : float('nan'),
        "BlueSoldier100DeathsMin" : float('nan'),
        "BlueSoldier100DPM" : float('nan'),
        "BlueSoldier100DTM" : float('nan'),
        "BlueSoldier100HPM" : float('nan'),
        "BluePyro100KillsMin" : float('nan'),
        "BluePyro100AssistsMin" : float('nan'),
        "BluePyro100DeathsMin" : float('nan'),
        "BluePyro100DPM" : float('nan'),
        "BluePyro100DTM" : float('nan'),
        "BluePyro100HPM" : float('nan'),
        "BlueDemoman100KillsMin" : float('nan'),
        "BlueDemoman100AssistsMin" : float('nan'),
        "BlueDemoman100DeathsMin" : float('nan'),
        "BlueDemoman100DPM" : float('nan'),
        "BlueDemoman100DTM" : float('nan'),
        "BlueDemoman100HPM" : float('nan'),
        "BlueHeavyweapons100KillsMin" : float('nan'),
        "BlueHeavyweapons100AssistsMin" : float('nan'),
        "BlueHeavyweapons100DeathsMin" : float('nan'),
        "BlueHeavyweapons100DPM" : float('nan'),
        "BlueHeavyweapons100DTM" : float('nan'),
        "BlueHeavyweapons100HPM" : float('nan'),
        "BlueEngineer100KillsMin" : float('nan'),
        "BlueEngineer100AssistsMin" : float('nan'),
        "BlueEngineer100DeathsMin" : float('nan'),
        "BlueEngineer100DPM" : float('nan'),
        "BlueEngineer100DTM" : float('nan'),
        "BlueEngineer100HPM" : float('nan'),
        "BlueMedic100KillsMin" : float('nan'),
        "BlueMedic100AssistsMin" : float('nan'),
        "BlueMedic100DeathsMin" : float('nan'),
        "BlueMedic100DPM" : float('nan'),
        "BlueMedic100DTM" : float('nan'),
        "BlueMedic100HPM" : float('nan'),
        "BlueSniper100KillsMin" : float('nan'),
        "BlueSniper100AssistsMin" : float('nan'),
        "BlueSniper100DeathsMin" : float('nan'),
        "BlueSniper100DPM" : float('nan'),
        "BlueSniper100DTM" : float('nan'),
        "BlueSniper100HPM" : float('nan'),
        "BlueSpy100KillsMin" : float('nan'),
        "BlueSpy100AssistsMin" : float('nan'),
        "BlueSpy100DeathsMin" : float('nan'),
        "BlueSpy100DPM" : float('nan'),
        "BlueSpy100DTM" : float('nan'),
        "BlueSpy100HPM" : float('nan'),
        "BlueCharges" : float('nan'),
        "BlueDrops" : float('nan'),
        "AvgRedTime" : float('nan'),
        "AvgBlueTime" : float('nan'),
        "RedScore" : float('nan'),
        "BlueScore" : float('nan'),        
        "KOTH?" : float('nan'),
        "Map" : "",
        "Length" : float('nan')

    }

    try: 
        time = data["length"]
        stats["Length"] = data["length"]

        for player in player_stats:
            type_player = player_stats[player]["team"] + player_stats[player]["class_stats"][0]["type"].capitalize()

            if str(type_player) in ["Unknown", "Undefined"]:
                    continue
                
            stats[type_player + "100KillsMin"] = 6000 * player_stats[player]["kills"] // time
            stats[type_player + "100AssistsMin"] = 6000 * player_stats[player]["assists"] // time
            stats[type_player + "100DeathsMin"] = 6000 * player_stats[player]["deaths"] // time
            stats[type_player + "100DPM"] = 6000 * player_stats[player]["dmg"] // time
            stats[type_player + "100DTM"] = 6000 * player_stats[player]["dt"] // time

            total_healed = 0

            for healer in data["healspread"]:
                if player in data["healspread"][healer].keys():
                    total_healed += data["healspread"][healer][player]

            stats[type_player + "100HPM"] = 6000 * total_healed // time



        # Note: In the main data for logs.tf charges, vaccinator charges are considered
        # charges. Vaccinator charges have been exlcuded from the data.

        red_uber = 0
        blue_uber = 0

        red_cap_time = 0
        blue_cap_time = 0 

        for round in data["rounds"]:
            first_cap = True
            prev_time = 0
            for event in round["events"]:
                if event["type"] == "charge" and event["medigun"] in ["medigun", "kritzkrieg", "quickfix"]:
                    if event["team"] == "Red":
                        red_uber += 1
                    else:
                        blue_uber += 1
                    
                if event["type"] == "pointcap":
                    if not first_cap:
                        if event["team"] == "Blue":
                            red_cap_time += event["time"] - prev_time

                        elif event["team"] == "Red":
                            blue_cap_time += event["time"] - prev_time

                        prev_time = event["time"]

                    else:
                        prev_time = event["time"]
                        first_cap = False
                    


        stats["RedCharges"] = red_uber
        stats["BlueCharges"] = blue_uber
        stats["RedDrops"] = data["teams"]["Red"]["drops"]
        stats["BlueDrops"] = data["teams"]["Blue"]["drops"]
        stats["RedScore"] = data["teams"]["Red"]["score"]
        stats["BlueScore"] = data["teams"]["Blue"]["score"]
        stats["AvgRedTime"] = red_cap_time
        stats["AvgBlueTime"] = blue_cap_time

        stats["Map"] = data["info"]["map"]



        map_prefix = search("^[^_]+(?=_)",stats["Map"]).group().upper()

        if map_prefix == "KOTH":
                stats["KOTH?"] = 1

        elif map_prefix in ["CP", "PL"]:
                stats["KOTH?"] = 0
    except Exception as e:
        print(e)
    return stats

def select_red_stats(data: dict) -> dict:
    stats = {
        "Scout100KillsMin" :    data["RedScout100KillsMin"],
        "Scout100AssistsMin" :    data["RedScout100AssistsMin"],
        "Scout100DeathsMin" :    data["RedScout100DeathsMin"],
        "Scout100DPM" :    data["RedScout100DPM"],
        "Scout100DTM" :    data["RedScout100DTM"],
        "Scout100HPM" :    data["RedScout100HPM"],
        "Soldier100KillsMin" :    data["RedSoldier100KillsMin"],
        "Soldier100AssistsMin" :    data["RedSoldier100AssistsMin"],
        "Soldier100DeathsMin" :    data["RedSoldier100DeathsMin"],
        "Soldier100DPM" :    data["RedSoldier100DPM"],
        "Soldier100DTM" :    data["RedSoldier100DTM"],
        "Soldier100HPM" :    data["RedSoldier100HPM"],
        "Pyro100KillsMin" :    data["RedPyro100KillsMin"],
        "Pyro100AssistsMin" :    data["RedPyro100AssistsMin"],
        "Pyro100DeathsMin" :    data["RedPyro100DeathsMin"],
        "Pyro100DPM" :    data["RedPyro100DPM"],
        "Pyro100DTM" :    data["RedPyro100DTM"],
        "Pyro100HPM" :    data["RedPyro100HPM"],
        "Demoman100KillsMin" :    data["RedDemoman100KillsMin"],
        "Demoman100AssistsMin" :    data["RedDemoman100AssistsMin"],
        "Demoman100DeathsMin" :    data["RedDemoman100DeathsMin"],
        "Demoman100DPM" :    data["RedDemoman100DPM"],
        "Demoman100DTM" :    data["RedDemoman100DTM"],
        "Demoman100HPM" :    data["RedDemoman100HPM"],
        "Heavyweapons100KillsMin" :    data["RedHeavyweapons100KillsMin"],
        "Heavyweapons100AssistsMin" :    data["RedHeavyweapons100AssistsMin"],
        "Heavyweapons100DeathsMin" :    data["RedHeavyweapons100DeathsMin"],
        "Heavyweapons100DPM" :    data["RedHeavyweapons100DPM"],
        "Heavyweapons100DTM" :    data["RedHeavyweapons100DTM"],
        "Heavyweapons100HPM" :    data["RedHeavyweapons100HPM"],
        "Engineer100KillsMin" :    data["RedEngineer100KillsMin"],
        "Engineer100AssistsMin" :    data["RedEngineer100AssistsMin"],
        "Engineer100DeathsMin" :    data["RedEngineer100DeathsMin"],
        "Engineer100DPM" :    data["RedEngineer100DPM"],
        "Engineer100DTM" :    data["RedEngineer100DTM"],
        "Engineer100HPM" :    data["RedEngineer100HPM"],
        "Medic100KillsMin" :    data["RedMedic100KillsMin"],
        "Medic100AssistsMin" :    data["RedMedic100AssistsMin"],
        "Medic100DeathsMin" :    data["RedMedic100DeathsMin"],
        "Medic100DPM" :    data["RedMedic100DPM"],
        "Medic100DTM" :    data["RedMedic100DTM"],
        "Medic100HPM" :    data["RedMedic100HPM"],
        "Sniper100KillsMin" :    data["RedSniper100KillsMin"],
        "Sniper100AssistsMin" :    data["RedSniper100AssistsMin"],
        "Sniper100DeathsMin" :    data["RedSniper100DeathsMin"],
        "Sniper100DPM" :    data["RedSniper100DPM"],
        "Sniper100DTM" :    data["RedSniper100DTM"],
        "Sniper100HPM" :    data["RedSniper100HPM"],
        "Spy100KillsMin" :    data["RedSpy100KillsMin"],
        "Spy100AssistsMin" :    data["RedSpy100AssistsMin"],
        "Spy100DeathsMin" :    data["RedSpy100DeathsMin"],
        "Spy100DPM" :    data["RedSpy100DPM"],
        "Spy100DTM" :    data["RedSpy100DTM"],
        "Spy100HPM" :    data["RedSpy100HPM"],
        "Charges" :    data["RedCharges"],
        "Drops" :    data["RedDrops"],
        "Length" : data["Length"]
    }
    return stats

def select_blue_stats(data: dict) -> dict:
    stats = {
        "Scout100KillsMin" :    data["BlueScout100KillsMin"],
        "Scout100AssistsMin" :    data["BlueScout100AssistsMin"],
        "Scout100DeathsMin" :    data["BlueScout100DeathsMin"],
        "Scout100DPM" :    data["BlueScout100DPM"],
        "Scout100DTM" :    data["BlueScout100DTM"],
        "Scout100HPM" :    data["BlueScout100HPM"],
        "Soldier100KillsMin" :    data["BlueSoldier100KillsMin"],
        "Soldier100AssistsMin" :    data["BlueSoldier100AssistsMin"],
        "Soldier100DeathsMin" :    data["BlueSoldier100DeathsMin"],
        "Soldier100DPM" :    data["BlueSoldier100DPM"],
        "Soldier100DTM" :    data["BlueSoldier100DTM"],
        "Soldier100HPM" :    data["BlueSoldier100HPM"],
        "Pyro100KillsMin" :    data["BluePyro100KillsMin"],
        "Pyro100AssistsMin" :    data["BluePyro100AssistsMin"],
        "Pyro100DeathsMin" :    data["BluePyro100DeathsMin"],
        "Pyro100DPM" :    data["BluePyro100DPM"],
        "Pyro100DTM" :    data["BluePyro100DTM"],
        "Pyro100HPM" :    data["BluePyro100HPM"],
        "Demoman100KillsMin" :    data["BlueDemoman100KillsMin"],
        "Demoman100AssistsMin" :    data["BlueDemoman100AssistsMin"],
        "Demoman100DeathsMin" :    data["BlueDemoman100DeathsMin"],
        "Demoman100DPM" :    data["BlueDemoman100DPM"],
        "Demoman100DTM" :    data["BlueDemoman100DTM"],
        "Demoman100HPM" :    data["BlueDemoman100HPM"],
        "Heavyweapons100KillsMin" :    data["BlueHeavyweapons100KillsMin"],
        "Heavyweapons100AssistsMin" :    data["BlueHeavyweapons100AssistsMin"],
        "Heavyweapons100DeathsMin" :    data["BlueHeavyweapons100DeathsMin"],
        "Heavyweapons100DPM" :    data["BlueHeavyweapons100DPM"],
        "Heavyweapons100DTM" :    data["BlueHeavyweapons100DTM"],
        "Heavyweapons100HPM" :    data["BlueHeavyweapons100HPM"],
        "Engineer100KillsMin" :    data["BlueEngineer100KillsMin"],
        "Engineer100AssistsMin" :    data["BlueEngineer100AssistsMin"],
        "Engineer100DeathsMin" :    data["BlueEngineer100DeathsMin"],
        "Engineer100DPM" :    data["BlueEngineer100DPM"],
        "Engineer100DTM" :    data["BlueEngineer100DTM"],
        "Engineer100HPM" :    data["BlueEngineer100HPM"],
        "Medic100KillsMin" :    data["BlueMedic100KillsMin"],
        "Medic100AssistsMin" :    data["BlueMedic100AssistsMin"],
        "Medic100DeathsMin" :    data["BlueMedic100DeathsMin"],
        "Medic100DPM" :    data["BlueMedic100DPM"],
        "Medic100DTM" :    data["BlueMedic100DTM"],
        "Medic100HPM" :    data["BlueMedic100HPM"],
        "Sniper100KillsMin" :    data["BlueSniper100KillsMin"],
        "Sniper100AssistsMin" :    data["BlueSniper100AssistsMin"],
        "Sniper100DeathsMin" :    data["BlueSniper100DeathsMin"],
        "Sniper100DPM" :    data["BlueSniper100DPM"],
        "Sniper100DTM" :    data["BlueSniper100DTM"],
        "Sniper100HPM" :    data["BlueSniper100HPM"],
        "Spy100KillsMin" :    data["BlueSpy100KillsMin"],
        "Spy100AssistsMin" :    data["BlueSpy100AssistsMin"],
        "Spy100DeathsMin" :    data["BlueSpy100DeathsMin"],
        "Spy100DPM" :    data["BlueSpy100DPM"],
        "Spy100DTM" :    data["BlueSpy100DTM"],
        "Spy100HPM" :    data["BlueSpy100HPM"],
        "Charges" :    data["BlueCharges"],
        "Drops" :    data["BlueDrops"],
        "Length" : data["Length"]
    }
    return stats

def average_stats(many_logs: list) -> dict:
    
    new_dict = {}

    num_logs = len(many_logs)

    for log in many_logs:
        for key in log.keys():
            log[key] *= log["Length"]
        log["Length"] = math.sqrt(log["Length"]) 
        log["Charges"] /= log["Length"]
        log["Drops"] /= log["Length"]

    
    for log in many_logs:
        for key in log.keys():
            if key in new_dict.keys():
                new_dict[key] += log[key]
            else:
                new_dict[key] = log[key]

    t = new_dict["Length"]
    for key in new_dict.keys():
        new_dict[key] /= t
    new_dict["Charges"] *= t
    new_dict["Drops"] *= t
    new_dict["Length"] *= t

    new_dict["Charges"] /= num_logs
    new_dict["Drops"] /= num_logs

    return new_dict

def combine_blue_and_red_aggregates(blue_average: dict, red_average:dict) -> dict:
    stats = {
        "RedScout100KillsMin" : red_average["Scout100KillsMin"],
        "RedScout100AssistsMin" : red_average["Scout100AssistsMin"],
        "RedScout100DeathsMin" : red_average["Scout100DeathsMin"],
        "RedScout100DPM" : red_average["Scout100DPM"],
        "RedScout100DTM" : red_average["Scout100DTM"],
        "RedScout100HPM" : red_average["Scout100HPM"],
        "RedSoldier100KillsMin" : red_average["Soldier100KillsMin"],
        "RedSoldier100AssistsMin" : red_average["Soldier100AssistsMin"],
        "RedSoldier100DeathsMin" : red_average["Soldier100DeathsMin"],
        "RedSoldier100DPM" : red_average["Soldier100DPM"],
        "RedSoldier100DTM" : red_average["Soldier100DTM"],
        "RedSoldier100HPM" : red_average["Soldier100HPM"],
        "RedPyro100KillsMin" : red_average["Pyro100KillsMin"],
        "RedPyro100AssistsMin" : red_average["Pyro100AssistsMin"],
        "RedPyro100DeathsMin" : red_average["Pyro100DeathsMin"],
        "RedPyro100DPM" : red_average["Pyro100DPM"],
        "RedPyro100DTM" : red_average["Pyro100DTM"],
        "RedPyro100HPM" : red_average["Pyro100HPM"],
        "RedDemoman100KillsMin" : red_average["Demoman100KillsMin"],
        "RedDemoman100AssistsMin" : red_average["Demoman100AssistsMin"],
        "RedDemoman100DeathsMin" : red_average["Demoman100DeathsMin"],
        "RedDemoman100DPM" : red_average["Demoman100DPM"],
        "RedDemoman100DTM" : red_average["Demoman100DTM"],
        "RedDemoman100HPM" : red_average["Demoman100HPM"],
        "RedHeavyweapons100KillsMin" : red_average["Heavyweapons100KillsMin"],
        "RedHeavyweapons100AssistsMin" : red_average["Heavyweapons100AssistsMin"],
        "RedHeavyweapons100DeathsMin" : red_average["Heavyweapons100DeathsMin"],
        "RedHeavyweapons100DPM" : red_average["Heavyweapons100DPM"],
        "RedHeavyweapons100DTM" : red_average["Heavyweapons100DTM"],
        "RedHeavyweapons100HPM" : red_average["Heavyweapons100HPM"],
        "RedEngineer100KillsMin" : red_average["Engineer100KillsMin"],
        "RedEngineer100AssistsMin" : red_average["Engineer100AssistsMin"],
        "RedEngineer100DeathsMin" : red_average["Engineer100DeathsMin"],
        "RedEngineer100DPM" : red_average["Engineer100DPM"],
        "RedEngineer100DTM" : red_average["Engineer100DTM"],
        "RedEngineer100HPM" : red_average["Engineer100HPM"],
        "RedMedic100KillsMin" : red_average["Medic100KillsMin"],
        "RedMedic100AssistsMin" : red_average["Medic100AssistsMin"],
        "RedMedic100DeathsMin" : red_average["Medic100DeathsMin"],
        "RedMedic100DPM" : red_average["Medic100DPM"],
        "RedMedic100DTM" : red_average["Medic100DTM"],
        "RedMedic100HPM" : red_average["Medic100HPM"],
        "RedSniper100KillsMin" : red_average["Sniper100KillsMin"],
        "RedSniper100AssistsMin" : red_average["Sniper100AssistsMin"],
        "RedSniper100DeathsMin" : red_average["Sniper100DeathsMin"],
        "RedSniper100DPM" : red_average["Sniper100DPM"],
        "RedSniper100DTM" : red_average["Sniper100DTM"],
        "RedSniper100HPM" : red_average["Sniper100HPM"],
        "RedSpy100KillsMin" : red_average["Spy100KillsMin"],
        "RedSpy100AssistsMin" : red_average["Spy100AssistsMin"],
        "RedSpy100DeathsMin" : red_average["Spy100DeathsMin"],
        "RedSpy100DPM" : red_average["Spy100DPM"],
        "RedSpy100DTM" : red_average["Spy100DTM"],
        "RedSpy100HPM" : red_average["Spy100HPM"],
        "RedCharges" : red_average["Charges"],
        "RedDrops" : red_average["Drops"],
        "BlueScout100KillsMin" : blue_average["Scout100KillsMin"],
        "BlueScout100AssistsMin" : blue_average["Scout100AssistsMin"],
        "BlueScout100DeathsMin" : blue_average["Scout100DeathsMin"],
        "BlueScout100DPM" : blue_average["Scout100DPM"],
        "BlueScout100DTM" : blue_average["Scout100DTM"],
        "BlueScout100HPM" : blue_average["Scout100HPM"],
        "BlueSoldier100KillsMin" : blue_average["Soldier100KillsMin"],
        "BlueSoldier100AssistsMin" : blue_average["Soldier100AssistsMin"],
        "BlueSoldier100DeathsMin" : blue_average["Soldier100DeathsMin"],
        "BlueSoldier100DPM" : blue_average["Soldier100DPM"],
        "BlueSoldier100DTM" : blue_average["Soldier100DTM"],
        "BlueSoldier100HPM" : blue_average["Soldier100HPM"],
        "BluePyro100KillsMin" : blue_average["Pyro100KillsMin"],
        "BluePyro100AssistsMin" : blue_average["Pyro100AssistsMin"],
        "BluePyro100DeathsMin" : blue_average["Pyro100DeathsMin"],
        "BluePyro100DPM" : blue_average["Pyro100DPM"],
        "BluePyro100DTM" : blue_average["Pyro100DTM"],
        "BluePyro100HPM" : blue_average["Pyro100HPM"],
        "BlueDemoman100KillsMin" : blue_average["Demoman100KillsMin"],
        "BlueDemoman100AssistsMin" : blue_average["Demoman100AssistsMin"],
        "BlueDemoman100DeathsMin" : blue_average["Demoman100DeathsMin"],
        "BlueDemoman100DPM" : blue_average["Demoman100DPM"],
        "BlueDemoman100DTM" : blue_average["Demoman100DTM"],
        "BlueDemoman100HPM" : blue_average["Demoman100HPM"],
        "BlueHeavyweapons100KillsMin" : blue_average["Heavyweapons100KillsMin"],
        "BlueHeavyweapons100AssistsMin" : blue_average["Heavyweapons100AssistsMin"],
        "BlueHeavyweapons100DeathsMin" : blue_average["Heavyweapons100DeathsMin"],
        "BlueHeavyweapons100DPM" : blue_average["Heavyweapons100DPM"],
        "BlueHeavyweapons100DTM" : blue_average["Heavyweapons100DTM"],
        "BlueHeavyweapons100HPM" : blue_average["Heavyweapons100HPM"],
        "BlueEngineer100KillsMin" : blue_average["Engineer100KillsMin"],
        "BlueEngineer100AssistsMin" : blue_average["Engineer100AssistsMin"],
        "BlueEngineer100DeathsMin" : blue_average["Engineer100DeathsMin"],
        "BlueEngineer100DPM" : blue_average["Engineer100DPM"],
        "BlueEngineer100DTM" : blue_average["Engineer100DTM"],
        "BlueEngineer100HPM" : blue_average["Engineer100HPM"],
        "BlueMedic100KillsMin" : blue_average["Medic100KillsMin"],
        "BlueMedic100AssistsMin" : blue_average["Medic100AssistsMin"],
        "BlueMedic100DeathsMin" : blue_average["Medic100DeathsMin"],
        "BlueMedic100DPM" : blue_average["Medic100DPM"],
        "BlueMedic100DTM" : blue_average["Medic100DTM"],
        "BlueMedic100HPM" : blue_average["Medic100HPM"],
        "BlueSniper100KillsMin" : blue_average["Sniper100KillsMin"],
        "BlueSniper100AssistsMin" : blue_average["Sniper100AssistsMin"],
        "BlueSniper100DeathsMin" : blue_average["Sniper100DeathsMin"],
        "BlueSniper100DPM" : blue_average["Sniper100DPM"],
        "BlueSniper100DTM" : blue_average["Sniper100DTM"],
        "BlueSniper100HPM" : blue_average["Sniper100HPM"],
        "BlueSpy100KillsMin" : blue_average["Spy100KillsMin"],
        "BlueSpy100AssistsMin" : blue_average["Spy100AssistsMin"],
        "BlueSpy100DeathsMin" : blue_average["Spy100DeathsMin"],
        "BlueSpy100DPM" : blue_average["Spy100DPM"],
        "BlueSpy100DTM" : blue_average["Spy100DTM"],
        "BlueSpy100HPM" : blue_average["Spy100HPM"],
        "BlueCharges" : blue_average["Charges"],
        "BlueDrops" : blue_average["Drops"]
    }
    return stats

if __name__ == "__main__":
    j = [select_red_stats(cleanse_data(make_api_request("https://logs.tf/json/3645252"))), select_red_stats(cleanse_data(make_api_request("https://logs.tf/json/3645251")))]
    print(j[0])
    print()
    print(j[1])
    print()
    print(average_stats(j))
    