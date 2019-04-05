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

# Load task parameters
params = json.load(sys.stdin)
# email = params['email']

#query_url = "https://localhost:8080/pdb/query/v4"
#query = "?query=reports[certname]{latest_report? = true}"

response = requests.get("https://localhost:8080/pdb/query/v4%3Fquery%3Dreports%5Bcertname%5D%7Blatest_report%3F+%3D+true%7D")
print("Response:", response.text)
