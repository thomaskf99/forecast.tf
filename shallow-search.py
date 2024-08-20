import json
from DataHandlerMethods import *

def shallow_search(entry: int, depth: int, prev_logs: list) -> list:
    for i in range(entry, depth):

        print(f"Request #{i+1} out of {depth}")

        try:
            matches = make_api_request(f"http://logs.tf/api/v1/log?limit=10000&offset={i}0000")
        except:

        # If the API request fails, it will simply repeat, assuming that the failure was a connection error

            i-=1
            continue
        for log in matches["logs"]:
            if log["players"] == 18:
                prev_logs.append(log)

    return prev_logs
if __name__ == "__main__":
    logs = shallow_search(0,360, [])

    with open("shallow_logs_hl.json", 'w') as file:
        json.dump({"count": len(logs), "info" : logs}, file, indent =4)