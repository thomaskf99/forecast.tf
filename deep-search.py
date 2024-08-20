# Minimum log id is 151,744
# As of 2:28 AM EDT, June 29, 2024, the current max log is 3669363
from DataHandlerMethods import *
import json
import time
import os
import threading

failedlogs = []

def save_to_json(log_id: int):
    try:

        log = make_api_request(f"http://logs.tf/json/{log_id}")

        with open(f"deep-saved-logs/{log_id}.json", 'w') as file:
            print(f"Saved log #{log_id}")
            json.dump(log, file, indent =4)

    except Exception as e:
        print(e)
        failedlogs.append(log_id)

def save_to_json_checked(mod: int, instances: int):
    print(f"Starting {mod+1}/{instances}")
    time.sleep(3 * mod)
    previously_saved_logs = [entry.name for entry in os.scandir("deep-saved-logs") if entry.is_file()]

    with open("shallow_logs_hl.json", 'r') as file:
        logs = json.load(file)
    for log in logs["info"]:
        id = log["id"]
        if id % instances == mod and (f"{id}.json" not in previously_saved_logs):
            save_to_json(id)


if __name__ == "__main__":

    instances = 3

    threads = []
    for i in range(instances):
        thread = threading.Thread(target=save_to_json_checked, args=(i,instances))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()