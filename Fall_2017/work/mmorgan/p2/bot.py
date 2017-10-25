
# coding: utf-8

# ## My Twitter Bot
# 
# My twitter bot tweets out if the US flag is supposed to be at half staff for either a holiday, or by proclomation. From the website us.halfstaff.org it scrapes for country wide event date for the current or upcoming half-staff notification, and from flagnotify.com it scrapes for upcoming dates for flags at half-staff for particular states. It then tweets out the cominbed information including countrywide and state notifications. 
# 
# The scraping for us.halfstaff.org looks at the most recent posting for notifications and grabs the date. For flagnotify.com the bot scrapes the upcoming notifications for the top post for the date and state. Any changes to these and it should update the google sheet and send out a tweet with the new information.
# 
# I had many iterations of the bot scraping from different websites, but finally found two with the information I wanted in an available form. At first I scraped two parts of the us.halfstaff.org website for the information date, reason for the half-staff, and by whom it was declared, but without any new updates, the parse code I had for the declaration may not have worked, so instead I switched the second parse to individual states and had to get rid of the reason to shorten the tweet to be able to be sent, but added a link to more information on why it was to be half-staff.
# 

# In[161]:

import urllib.request
import re 
import datetime
now = datetime.datetime.now()


# In[162]:

url_1 = "http://www.us.halfstaff.org/"
url_2 = "http://flagnotify.com/scheduled.aspx"


# In[163]:

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds']

document_key = "17x26DRzJFIDYJxTnULtV0wUpuWLPrt5Y7W9hnZGZTUY"
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../TweetyBot-b2d02f67ab13.json', scope)

gc = gspread.authorize(credentials)
wks = gc.open_by_key(document_key)

worksheet = wks.worksheet("Sheet1")

worksheet.resize(worksheet.row_count)


# In[164]:


import csv
csvfile = "output.csv"
list_of_lists = worksheet.get_all_values()
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)

import pandas as pd
output = pd.read_csv(csvfile)
output[:3]


# In[165]:

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

api = twitter.Api(consumer_key=key,
                  consumer_secret=secret,
                  access_token_key=token_key,
                  access_token_secret=token_secret)


# In[166]:

p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()
print(p_1)


# In[167]:

res_1 = re.search(b'\t<div class=\"date\">START: <strong>(.*)</strong></div>',p_1)
print(res_1.group(1).decode('UTF-8'))


# In[168]:

p_2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_2).read()
print(p_2)


# In[169]:

res_2 = re.search(b'<td  style = \"font-weight:normal;\">(\D*)</td>',p_2)  
print (res_2.group(1).decode('UTF-8'))


# In[170]:

p_3 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_2).read()
print(p_3)


# In[171]:

res_3 = re.search(b'weight:bold;\">(.*)</td>',p_3)  
print (res_3.group(1).decode('UTF-8'))


# In[172]:

if res_1 and res_2 and res_3: 
    output_1 = res_1.group(1).decode('UTF-8')
    output_2 = res_2.group(1).decode('UTF-8')
    output_3 = res_3.group(1).decode('UTF-8')
    titles = output_1 + " and in " + output_2 + " on " + output_3 + ". For more information visit https://goo.gl/7fQNMg"
print("%s | %s | %s | %s | %s"%(worksheet.row_values(worksheet.row_count)[1],worksheet.row_values(worksheet.row_count)[2],worksheet.row_values(worksheet.row_count)[3],worksheet.row_values(worksheet.row_count)[4],worksheet.row_values(worksheet.row_count)[2]))


# In[173]:

print("%s | %s | %s | %s | %s"%(worksheet.row_values(worksheet.row_count)[1],worksheet.row_values(worksheet.row_count)[2],worksheet.row_values(worksheet.row_count)[3],worksheet.row_values(worksheet.row_count)[4],worksheet.row_values(worksheet.row_count)[2]))


# In[174]:

print("%s | %s | %s | %s | %s"%(now,output_1,output_2,output_3,titles))


# In[175]:

if res_1 and res_2: 
 
    
    if (float(worksheet.row_values(worksheet.row_count)[1]) != output_1) or (float(worksheet.row_values(worksheet.row_count)[2]) != output_2):
        
        if (float(worksheet.row_values(worksheet.row_count)[1]) != output_1):
 
            try:
                #print ('Titles: %s'%(output_2))
                status = api.PostUpdate('US Flags are Half-Staff countrywide on %s'%(titles))
                print(status.text)
            except TwitterError:
                #print ('T1 + T2: %s'%(output_2))
                status = api.PostUpdate('US Flags to be Half-Staff countrywide on %s'%(titles))
                print(status.text)
                
        worksheet.append_row([now,output_1,output_2,output_3,titles])


# In[ ]:



