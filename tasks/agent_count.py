#!/bin/python

# Puppet Task Name:
#
# This is where you put the shell code for your task.
#
# You can write Puppet tasks in any language you want and it's easy to
# adapt an existing Python, PowerShell, Ruby, etc. script. Learn more at:
# https://puppet.com/docs/bolt/0.x/writing_tasks.html
#
# Puppet tasks make it easy for you to enable others to use your script. Tasks
# describe what it does, explains parameters and which are required or optional,
# as well as validates parameter type. For examples, if parameter "instances"
# must be an integer and the optional "datacenter" parameter must be one of
# portland, sydney, belfast or singapore then the .json file
# would include:
#   "parameters": {
#     "instances": {
#       "description": "Number of instances to create",
#       "type": "Integer"
#     },
#     "datacenter": {
#       "description": "Datacenter where instances will be created",
#       "type": "Enum[portland, sydney, belfast, singapore]"
#     }
#   }
# Learn more at: https://puppet.com/docs/bolt/0.x/writing_tasks.html#ariaid-title11
#

# Based on the following data:
# [
# {"certname":"box150.autostructure.io","value":{"day":9,"year":2019,"month":3}},
# {"certname":"manager001.autostructure.io","value":{"day":12,"year":2018,"month":12}},
# {"certname":"splunk.autostructure.io","value":{"day":25,"year":2019,"month":3}},
# {"certname":"nfs001.autostructure.io","value":{"day":4,"year":2019,"month":1}},
# {"certname":"manager004.autostructure.io","value":{"day":10,"year":2019,"month":1}},
# {"certname":"master.autostructure.io","value":{"day":18,"year":2019,"month":3}},
# {"certname":"win-0kk9knd43u1","value":{"day":6,"year":2019,"month":3}},
# {"certname":"nameserver.autostructure.io","value":{"day":19,"year":2018,"month":1}},
# {"certname":"worker003.autostructure.io","value":{"day":12,"year":2018,"month":12}},
# {"certname":"worker005.autostructure.io","value":{"day":3,"year":2019,"month":1}},
# {"certname":"worker001.autostructure.io","value":{"day":12,"year":2018,"month":12}},
# {"certname":"rp.autostructure.io","value":{"day":27,"year":2017,"month":3}},
# {"certname":"cdpe-hardware-23.autostructure.io","value":{"day":8,"year":2019,"month":3}},
# {"certname":"manager003.autostructure.io","value":{"day":12,"year":2018,"month":12}}
# ]
#
# We should get a CSV like this:
# Month, Agents Installed
# March 2017, 1
# April 2017, 0
# May 2017, 0
# June 2017, 0
# July 2017, 0
# August 2017, 0
# September 2017, 0
# October 2017, 0
# November 2017, 0
# December 2017, 0
# January 2018, 1
# February 2018, 0
# March 2018, 0
# April 2018, 0
# May 2018, 0
# June 2018, 0
# July 2018, 0
# August 2018, 0
# September 2018, 0
# October 2018, 0
# November 2018, 0
# December 2018, 4
# January 2019, 3
# February 2019, 0
# March 2019, 5


import json
import sys
import requests
import os
import csv
import datetime
import pandas as pd
from pandas.io.json import json_normalize
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

# Variables
params = json.load(sys.stdin)
email_to = params['email']
query_url = "https://master.autostructure.io:8081/pdb/query/v4"
query = "?query=%5B%22from%22%2C%22facts%22%2C%5B%22extract%22%2C%5B%22certname%22%2C%22value%22%5D%2C%5B%22%3D%22%2C%22name%22%2C%22certificate_age%22%5D%5D%5D"
uri = query_url + query

# This section generates a token for authentication
login = {'login':params['user'],'password':params['password']}
token_url = 'https://master.autostructure.io:4433/rbac-api/v1/auth/token'
try:
    token_response = requests.post(token_url,json=login,verify=False)
    token_response.raise_for_status()
except requests.exceptions.ConnectionError as Connerr:
    print("A connection error occurred:",Connerr)
    sys.exit(1)
except requests.exceptions.HTTPError as HTTPerr:
    print("An HTTP Error occurred:",HTTPerr)
    sys.exit(1)
except requests.exceptions.Timeout as Timeerr:
    print("A timeout error occurred:",Timeerr)
    sys.exit(1)
except requests.exceptions.RequestException as Requesterr:
    print("An error occurred:",Requesterr)
    sys.exit(1)
if (token_response.ok):
    print("Authentication token generated successfully")
    print("HTTP Status Code: ",token_response.status_code)
token_json = json.loads(token_response.text)
token = token_json['token']

# This section requests the PuppetDB for JSON data on each node's certificate_age fact
try:
    response = requests.get(uri, verify=False, headers={'X-Authentication':token})
    response.raise_for_status()
except requests.exceptions.ConnectionError as Connerr:
    print("A connection error occurred:",Connerr)
    sys.exit(1)
except requests.exceptions.HTTPError as HTTPerr:
    print("An HTTP Error occurred:",HTTPerr)
    sys.exit(1)
except requests.exceptions.Timeout as Timeerr:
    print("A timeout error occurred:",Timeerr)
    sys.exit(1)
except requests.exceptions.RequestException as Requesterr:
    print("An error occurred:",Requesterr)
    sys.exit(1)
if(response.ok):
    print("Data successfully retrieved from PuppetDB")
    print("HTTP Status Code:",response.status_code)
else:
    print("Data not successfully retrieved from PuppetDB")
    print("HTTP Status Code:",response.status_code)
agent_count_json = json.loads(response.text)

# Import JSON as a Dataframe
df = pd.DataFrame.from_dict(json_normalize(agent_count_json), orient ='columns')

# Create new dataframe with the columns we want
df2 = pd.DataFrame()
df2['Month'] = df['value.month']
df2['Year'] = df['value.year']
df2['Agents'] = df['certname']
df2 = df2.groupby(by=['Month','Year'], as_index=False).agg({'Agents': pd.Series.nunique})

#Convert numbers to month abbreviations for clarity
look_up = { 1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
            6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

df2['Month'] = df2['Month'].apply(lambda x: look_up[x])
df2.sort_values(by='Year', ascending=False)

#Convert Dataframe into CSV
date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
file = "/tmp/agent_count_" + date + ".csv"

df2.to_csv(path_or_buf=file)

# Send an email with the CSV file attached
sendMail([email_to],'Puppet Report <centos-template@autostructure.io>','Puppet agent_count Task Results','Attached is the agent_count report that was requests in a Puppet Task.',[file])
print("Successfully emailed CSV file to ", email_to)

# Clean up temporary CSV file after sending the email
os.remove(file)
print("Cleaned up temporary files")
