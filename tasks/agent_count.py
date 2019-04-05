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

import json
import sys
import requests
import os
import csv
import datetime

# Load task parameters
params = json.load(sys.stdin)
# email = params['email']

# Variables
query_url = "https://master.autostructure.io:8081/pdb/query/v4"
query = "?query=%5B%22from%22%2C%22facts%22%2C%5B%22extract%22%2C%5B%22certname%22%2C%22value%22%5D%2C%5B%22%3D%22%2C%22name%22%2C%22certificate_age%22%5D%5D%5D"
uri = query_url + query

# Get JSON Response
response = requests.get(uri, verify=False, headers={'X-Authentication': 'AMEB9PCp1KxHMxbHctkWaKy7M9TokFgrxWaR-zld52ny'})
#agent_count_json = json.loads(response.text)

# Convert JSON to CSV file
# date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
# file = "/tmp/role_count_" + date + ".csv"
# with open(file, "wb") as csvfile:
#     f = csv.writer(csvfile)
#     f.writerow(["Role", "Nodes"])
#     for data in role_count_json:
#         f.writerow([data["title"], data["count"]])

print("Response: ", response.text)
