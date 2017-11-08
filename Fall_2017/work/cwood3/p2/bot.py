
# coding: utf-8

# In[33]:


# Load the module for visiting and reading websites.
import urllib.request
# Load the module for running regular expressions (regex).
import re 
# Load the module for date and time stuff.
import datetime
# Define the variable now as equal to the current date and time.
now = datetime.datetime.now()

# Set the URLs you want to scrape.
url_1 = "https://malegislature.gov/Bills"
url_2 = "http://norml.org/news/us-ma"

# Load the module for accessing Google Sheets.
import gspread
# Load the module needed for securely communicating with Google Sheets.
from oauth2client.service_account import ServiceAccountCredentials
# The scope for your access credentials
scope = ['https://spreadsheets.google.com/feeds']

# Your spreadsheet's ID
document_key = "135EBa7vawuCh44cIoGdIkXUVhOX38YamvnAsNu93s0Y"
# Your Google project's .json key
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../RightToSpark.json', scope)

# Use your credentials to authorize yourself.
gc = gspread.authorize(credentials)
# Open up the Sheet with the defined ID.
wks = gc.open_by_key(document_key)

#########################################
#
#  NOTE: The name of the sheet you are 
#  trying to access should be in the 
#  parenthetical below (e.g., Data). By
#  Default this is probably "Sheet1".
#
#########################################
worksheet = wks.worksheet("Sheet1")

# Count the number of rows in your Sheet &
# resize to remove blank rows.
worksheet.resize(worksheet.row_count)

# download spreadsheet
import csv
csvfile = "output_mine.csv"
list_of_lists = worksheet.get_all_values()
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)

import pandas as pd
output = pd.read_csv(csvfile)
output[:3]

# Import the relevant Twitter libraries so you can use Twitter.
import twitter
from twitter import TwitterError

with open('../../../../../key.txt', 'r') as myfile:
    key=myfile.read()
    
with open('../../../../../secret.txt', 'r') as myfile:
    secret=myfile.read()
    
with open('../../../../../token_key.txt', 'r') as myfile:
    token_key=myfile.read()

with open('../../../../../token_secret.txt', 'r') as myfile:
    token_secret=myfile.read()

# Set you Twitter API credentials.
api = twitter.Api(consumer_key=key,
                  consumer_secret=secret,
                  access_token_key=token_key,
                  access_token_secret=token_secret)
#print(api.VerifyCredentials())

p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()

res_1 = re.finditer(b'<td><a href="(.*)".*</td>.*\r\n.*<td .*>(.*marijuana.*)</td>',p_1,re.IGNORECASE)
column = 0


for matchNum, match in enumerate(res_1):
    columns = [now]
    matchNum = matchNum + 1
    column = column + 1
    column2 = column + 1
    
    output_1_link = "https://malegislature.gov" + match.group(1).decode('UTF-8')
    output_1_title = match.group(2).decode('UTF-8')

    if (res_1 and (worksheet.row_values(worksheet.row_count)[1]) != output_1_title 
              and (worksheet.row_values(worksheet.row_count)[2]) != output_1_link):
        # same as above but now comparing the two values handled in this loop
        
        try:
            # Post to Twitter.
            status = api.PostUpdate('%s %s'%(output_1_title,output_1_link))
            print(status.text)
        except TwitterError:
            # Post to Twitter.
            #status = api.PostUpdate('%s %s'%(output_1_title,output_1_link))
            print('%s %s'%(output_1_title,output_1_link))
            
        columns.append(output_1_title)
        columns.append(output_1_link)
        
        # Save to Google only after Tweeting
        worksheet.append_row(columns)

p_2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_2).read()
res_2 = re.finditer(b'<a title="(.*)" href="(.*)".*>.*marijuana.*</a>',p_2, re.IGNORECASE)
column = 0


for matchNum, match in enumerate(res_2):
    columns = [now]
    matchNum = matchNum + 1
#     column = column + 1
#     column2 = column + 1
    
    output_2_title = match.group(1).decode('UTF-8')
    output_2_link = "http://norml.org" + match.group(2).decode('UTF-8')
    
    if output_2_link == "http://norml.org/":
        continue
        
    if (res_2 and (worksheet.row_values(worksheet.row_count)[3]) != output_2_title 
              and (worksheet.row_values(worksheet.row_count)[4]) != output_2_link):
        # same as above but now comparing the two values handled in this loop
        
        try:
            # Post to Twitter.
            status = api.PostUpdate('%s %s'%(output_2_title,output_2_link))
            print(status.text)
        except TwitterError:
            # Post to Twitter.
            #status = api.PostUpdate('%s %s'%(output_1_title,output_1_link))
            print('%s %s'%(output_2_title,output_2_link))
            
        columns.append(output_2_title)
        columns.append(output_2_link)
        
        # Save to Google only after Tweeting
        worksheet.append_row(columns)

