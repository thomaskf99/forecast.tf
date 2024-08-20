# Minimum log id is 151,744
# As of 2:28 AM EDT, June 29, 2024, the current max log is 3669363
from DataHandlerMethods import *
import argparse
from decimal import Decimal
import mysql.connector
import json
import time

parser = argparse.ArgumentParser()
parser.add_argument('--mod', type=int, required=True, help='Modulo of this running instance')
parser.add_argument('--instances', type=int, required=False, default=10, help='Number of running instances')
parser.add_argument('--batchsize', type=int, required=False, default=20, help='Batch upload size')



args = parser.parse_args()

mod = args.mod
instances = args.instances
batchsize = args.batchsize

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="forecasttf"
)

mycursor = mydb.cursor()
mycursor.execute("""
    SELECT log_id, log_title, unix_time, map from forecasttf.general 
    WHERE
    player_count = 18
    and
    (map not LIKE '%+%') and (map LIKE '%\_%' )
    and
    log_id NOT IN (SELECT log_id from forecasttf.hl)


                 """)

queries_result = mycursor.fetchall()

sql = """
INSERT INTO forecasttf.hl (log_id, log_title, unix_time, map, length, output) VALUES (%s,%s,%s,%s,%s, %s)
ON DUPLICATE KEY UPDATE
log_title = VALUES(log_title),
unix_time = VALUES(unix_time),
map = VALUES(map),
length = VALUES(length),
output = VALUES(output)"""


failedlogs = []

def upload_to_sql(log_id: int)->bool:
    try:

        log = make_api_request(f"http://logs.tf/json/{log_id}")
        val=(
            log_id,
            log["info"]["title"],
            log["info"]["date"],
            log["info"]["map"],
            log["length"],
            json.dumps(log, indent = 4),
        )
        batch.append(val)
        return True
    except Exception as e:
        print(e)
        failedlogs.append(log_id)
        return False

if __name__ == "__main__":
    time.sleep(3 * mod)
    count = 1
    batch = []
    for result in queries_result:
        log_id = result[0]
        if log_id % instances == mod:
            print(f"Testing log {log_id}")
            if upload_to_sql(log_id):
                print(f"Downloaded log {log_id}, count {count}")
                count+=1
        if len(batch) >= batchsize:

            
            try:
                mycursor.executemany(sql, batch)
                mydb.commit()
                print(mycursor.rowcount, "was inserted.")
            except Exception as e:
                print(e)
                count -= len(batch)
                print('Some previous logs were lost.')
            batch = []


