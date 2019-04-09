#!/bin/python

# Puppet Task Name: role_count
# Language: Python
# Created By: Jack Coleman
# Last MOdified: 4/9/2019

import json
import sys
import requests
import os
import csv
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

# This function will send emails with attachments
def sendMail(to, fro, subject, text, files=[],server="localhost"):
    assert type(to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(fro, to, msg.as_string() )
    smtp.close()

# Variables
params = json.load(sys.stdin)
email_to = params['email']
query_url = "https://master.autostructure.io:8081/pdb/query/v4"
query = "?query=%5B%22from%22%2C%22resources%22%2C%5B%22extract%22%2C%5B%5B%22function%22%2C%22count%22%5D%2C%22title%22%5D%2C%5B%22and%22%2C%5B%22%3D%22%2C%22type%22%2C%22Class%22%5D%2C%5B%22%7E%22%2C%22title%22%2C%22%5BRr%5Dole%22%5D%2C%5B%22subquery%22%2C%22nodes%22%2C%22certname%22%5D%5D%2C%5B%22group_by%22%2C%22title%22%5D%5D%5D"
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

# This section requests the PuppetDB for JSON data on the count of nodes classified with each role
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
role_count_json = json.loads(response.text)

# Convert the JSON data to CSV format and save in a temporary file
date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
file = "/tmp/role_count_" + date + ".csv"
with open(file, "wb") as csvfile:
    f = csv.writer(csvfile)
    f.writerow(["Role", "Nodes"])
    for data in role_count_json:
        f.writerow([data["title"], data["count"]])

# Send an email with the CSV file attached
sendMail([email_to],'Puppet Report <centos-template@autostructure.io>','Puppet role_count Task Results','Attached is the role_count report that was requests in a Puppet Task.',[file])
print("Successfully emailed CSV file to ", email_to)

# Clean up temporary CSV file after sending the email
os.remove(file)
print("Cleaned up temporary files")
