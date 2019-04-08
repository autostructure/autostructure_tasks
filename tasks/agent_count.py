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

# Load task parameters
params = json.load(sys.stdin)
# email = params['email']

# Variables
query_url = "https://master.autostructure.io:8081/pdb/query/v4"
query = "?query=%5B%22from%22%2C%22facts%22%2C%5B%22extract%22%2C%5B%22certname%22%2C%22value%22%5D%2C%5B%22%3D%22%2C%22name%22%2C%22certificate_age%22%5D%5D%5D"
uri = query_url + query

# Get JSON Response
response = requests.get(uri, verify=False, headers={'X-Authentication': '0P0L-KwvYTVgy_NcOhQRN4Lw95fB7ibShVyxqd43BMIU'})
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
