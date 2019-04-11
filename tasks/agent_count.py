#!/bin/python

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
query = "?query=%5B%22from%22%2C%22facts%22%2C%5B%22extract%22%2C%5B%22certname%22%2C%22value%22%5D%2C%5B%22%3D%22%2C%22name%22%2C%22auto_certificate_age%22%5D%5D%5D"
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

try:
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

    df_sort_month = df2.sort_values(by='Month', ascending=False)
    df_sort_month['Month'] = df_sort_month['Month'].apply(lambda x: look_up[x])
    #df_sort = sort_dataframeby_monthorweek.Sort_Dataframeby_Month(df=df2,monthcolumnname='Month')
    Final = df_sort_month.sort_values(by='Year', ascending=False)

    #Convert Dataframe into CSV
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file = "/tmp/agent_count_" + date + ".csv"

    Final.to_csv(path_or_buf=file,index=False)
except Exception as e:
    print("Error creating dataframe: " + str(e))
    sys.exit(1)

# Send an email with the CSV file attached
sendMail([email_to],'Puppet Report <centos-template@autostructure.io>','Puppet agent_count Task Results','Attached is the agent_count report that was requests in a Puppet Task.',[file])
print("Successfully emailed CSV file to ", email_to)

# Clean up temporary CSV file after sending the email
# os.remove(file)
# print("Cleaned up temporary files")
