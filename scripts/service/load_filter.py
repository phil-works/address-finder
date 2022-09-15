#!/usr/bin/env -S python3 -u
import mysql.connector
import time
import datetime
import os
import yaml

#
# Setup Configs
#
with open(os.environ['HOME'] + "/config/godogwin-net.yaml", "r") as stream:
    try:
        gdwcfg = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


# setup database connector
mydb = mysql.connector.connect(
  host=gdwcfg["gdwdb"]["host"],
  user=gdwcfg["gdwdb"]["user"],
  password=gdwcfg["gdwdb"]["pwd"],
  database=gdwcfg["gdwdb"]["algodb"]
)

mycursor = mydb.cursor()

# Set the gloabal services config file.
services_config_file = gdwcfg["services_config_file"]

with open(services_config_file, "r") as fp:
    try:
        gd_data = yaml.safe_load(fp)
    except yaml.YAMLError as exc:
        print(exc)

path = gd_data["load_filter"]["path"]  #"/home/godogdev/address-finder/new/"
procpath = gd_data["load_filter"]["procpath"] #/home/godogdev/address-finder/processed/"
sqlloadfile = gd_data["load_filter"]["sqlloadfile"] #"/home/godogdev/docker/mysql/mysql-files/address_out.txt"
mysqlloadfile = gd_data["load_filter"]["mysqlloadfile"] # /var/lib/mysql-files/address_out.txt
highlimitfile = gd_data["load_filter"]["highlimitfile"] #"/home/godogdev/address-finder/limit-high.txt"
lowlimitfile = gd_data["load_filter"]["lowlimitfile"] #"/home/godogdev/address-finder/limit-low.txt"

#thefile = max(os.listdir("/home/godogdev/address-finder/new/"), key=os.path.getctime)
thefile = min(os.listdir(path), key=lambda x: datetime.datetime.strptime(time.ctime(os.path.getctime(os.path.join(path, x))), '%a %b %d %H:%M:%S %Y'))

os.system("cp " + path  + thefile + " " + sqlloadfile)

print("Loading addresses into database...")
sql = "load data infile '" + mysqlloadfile + "' into table unmatched fields terminated by '|' enclosed by '' lines terminated by '\n';"

mycursor.execute(sql)
processed_count = mycursor.rowcount
mydb.commit()

print("Commited database...")
with open(highlimitfile, 'r') as file:
    highs = int(file.read().rstrip())
with open(lowlimitfile, 'r') as file:
    lows = int(file.read().rstrip())

for len in range(highs,2,-1):
    print("Finding matches for length: " +  str(len) + "...")
    if len <= lows:
        limit_clause = "where  type != 'gdw_contest'"
    else:
        limit_clause = ""

    sql = "insert into search_matches  " + \
        "SELECT address, private_key, substring(address,1," +  str(len) + ") as match_part, " +  str(len) + " as match_len, sr.text as name, length(sr.text) as name_len , " + \
        "sr.search_request_id, sr.type, sr.text, sr.requestor, sr.on_behalf_of, sr.priority, sr.position, sr.txn_no, sr.requested_dt FROM  " + \
        "unmatched, search_requests sr, (select text, max(priority) as priority from search_requests  " + \
        limit_clause + " group by text having max(priority)  " + \
        ") msr where sr.text = msr.text and sr.priority = msr.priority and substring(address,1," +  str(len) + ") = sr.text  " + \
        "and length(sr.text) = " +  str(len) + " and address not in (select address from search_matches ) " + \
        "and sr.search_request_id not in (select distinct search_request_id from user_requests_matches where inprogress is not null)"
    mycursor.execute(sql)
    mydb.commit()

print("Truncating unmatched table...")
sql = "truncate table unmatched"
mycursor.execute(sql)
mydb.commit()

print("Storing GDW Matches into gdw_availables")
sql = "insert into gdw_available select * from search_matches where type = 'gdw_contest'"
mycursor.execute(sql)
mydb.commit()

print("Storing Matches into user_requests_matches")
sql = """insert into user_requests_matches 
(address, private_key, match_part, match_len, name, name_len, search_request_id, type, text, requestor, on_behalf_of, priority, position, txn_no, requested_dt) 
select 
address, private_key, match_part, match_len, name, name_len, search_request_id, type, text, requestor, on_behalf_of, priority, position, txn_no, requested_dt
from search_matches where type != 'gdw_contest'"""

mycursor.execute(sql)
mydb.commit()

print("Truncating matches table...")
sql = "truncate table search_matches"
mycursor.execute(sql)
mydb.commit()

print("Processed " + str(processed_count) + " records...")
sql = "insert into loader_log (record_amt) values (" + str(processed_count) + ")"
mycursor.execute(sql)
mydb.commit()

#os.system("mv " + path + thefile + " " + procpath + thefile)
os.remove(path + thefile)

if os.path.exists(sqlloadfile):
  os.remove(sqlloadfile)
else:
  print("The file does not exist") 

print("Finished")
