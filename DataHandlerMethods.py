import requests
from re import search

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
    "Map" : ""

  }

  try: 
    time = data["length"]

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