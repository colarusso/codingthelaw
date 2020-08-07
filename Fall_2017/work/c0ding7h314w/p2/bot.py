
# coding: utf-8

# ## Twitter Bot
# 
# By Christopher Lacenere 
# 
# I wrote a Twitter bot that tweets the current temperature and weather conditions in Boston when they change.  It is called "Sunny Beantown!" and you can find it [here](https://twitter.com/Christo47726466?lang=en).  The Python code can be found [here](https://www.codingthelaw.org/Fall_2017/work/c0ding7h314w/p2/bot.py).  To write my bot, we used a Jupyter notebook with Python code supplied by Professor Colarusso.  We had to create a Google spreadsheet that could be accessed through Google's API as well as create keys to allow us to post automatically to Twitter.  The Google spreadsheet can be found [here](https://docs.google.com/spreadsheets/d/1e--PT9vz0Z0UcfrfX6TePwW93bFY0nKrZruws3uoo6M/edit?usp=sharing).
# 
# My bot scrapes data from from a Personal Weather Station from Wunderground.com.  The Terms of Service allow use of this data for non-commercial use and requires attribution of its source, which I have done on my Twitter page.  The Terms of Service can be found [here](https://www.wunderground.com/company/legal).  No robot.txt files were found.
# 
# The bot itself regularly (every 5 minutes) scrapes and saves to a Google spreadsheet two data points, temperature and weather conditions, from the web page of a Boston Personal Weather Station that can be found [here](https://www.wunderground.com/personal-weather-station/dashboard?ID=KMABOSTO197&cm_ven=localwx_pwsdash#history).  It then produces tweets when the parsed content changes.  I did make one minor modification to the code provided such that when either the temperature OR the whether conditions change, a tweet will be produced.  The original code required both values to change.
# 
# I found the project's development to be difficult at times.  The first web page that I wanted to monitor would not parse for some reason.  I then found a web page that would parse, but next found the designing of a regular expression to uniquely pull out the data points I needed to be difficult.  Eventually, through a lot of trial and eerror, along with the help of Professor Colarusso, I was able to arrive at the regular expression I needed.
# 
# Adapted from the notebook found at [How to Build a Law Bot](https://lawyerist.com/how-build-law-bot/)
# 
# ## Install libraries
# 
# If you haven't already, you may need to install some dependencies. On the command line, run the following to install/update gspread, oauth2client, PyOpenSSL, and python-twitter.
# ```
# pip install gspread
# pip install --upgrade oauth2client
# pip install PyOpenSSL
# pip install python-twitter
# ```
# Library installs are one and done. So after doing this once, you should be all set. 
# 
# ## Import modules and set variables
# 
# Now we're getting into the bot's code. This is what will run every time your bot is called. 
# 
# You will need to create a new Google Sheet (same instructions as [last time](https://lawyerist.com/126074/online-forms-meet-local-document-automation-cut-and-paste-coding/)). Delete rows 2-999. This is because the code below appends values to the end of your sheet. So if you fail to remove rows 2-999, values will be appended to row 1000. Additionally, it looks at the last row of the sheet for your old values. So right off the bat it will be looking at your one solitary row. Also, delete columns D through Z to avoind having to print a bunch of empty columns.
# 
# As for a Twitter account and Twitter credentials, follow the instruction in [this post](https://lawyerist.com/?p=127093). 

# In[120]:

# Load the module for visiting and reading websites.
import urllib.request
# Load the module for running regular expressions (regex).
import re 
# Load the module for date and time stuff.
import datetime
# Define the variable now as equal to the current date and time.
now = datetime.datetime.now()


# In[121]:

# Set the URL you want to scrape.
url_1 = "https://www.wunderground.com/personal-weather-station/dashboard?ID=KMABOSTO197&cm_ven=localwx_pwsdash#history"

# If you want to scrape data from multiple pages, you can, 
# just replicate the above and below but change url_1 to url_2 et al.


# In[122]:

# Load the module for accessing Google Sheets.
import gspread
# Load the module needed for securely communicating with Google Sheets.
from oauth2client.service_account import ServiceAccountCredentials
# The scope for your access credentials
scope = ['https://spreadsheets.google.com/feeds']

# Your spreadsheet's ID
document_key = "1e--PT9vz0Z0UcfrfX6TePwW93bFY0nKrZruws3uoo6M" 
#              ^^^^^^^^^^^ SWAP OUT FOR YOUR DOCUMENT ID/KEY
# Your Google project's .json key
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../sheetsbot-0c1136d448eb.json', scope)
#                                                                              ^^^^^^^^ SWAP OUT FOR YOUR JSON KEY
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


# In[123]:

# Import the relevant Twitter libraries so you can use Twitter.
import twitter
from twitter import TwitterError

# create the following four text files and add them to the same diretctry as you 
# Google API key. In each file add the appropriate value found when retrieving your 
# Twitter credentials

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


# ## Read the contents of your first webpage
# 
# When you run the next cell, your program will visit the first URL you defined above. It will then print out that page's HTML. 

# In[124]:

p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()
print(p_1)


# # Two Data Points, One Match
# 
# ---------------------------
# ## Parse the site's contents

# In[125]:

res_1 = re.search(b"\"metar\".*\s*\"condition\":\"(.*)\",\s*\"temperature\":\s(.+),",p_1)
output_1 = res_1.group(1).decode('UTF-8')
print(output_1)
output_2 = res_1.group(2).decode('UTF-8')
print(output_2)


# ## Post to Twitter and Save to Google (Two Data Point, One Match)

# In[127]:

if (res_1 and (worksheet.row_values(worksheet.row_count)[1]) != output_1
          or (worksheet.row_values(worksheet.row_count)[2]) != output_2):
    # same as above but now comparing two values
    
    try:
        # Post to Twitter.
        status = api.PostUpdate('It is currently %s degrees Farenheit in Boston with %s conditions.'%(output_2,output_1))
        print(status.text)
    except TwitterError:
        # Post to Twitter.
        status = api.PostUpdate('It is currently %s degrees Farenheit in Boston with %s conditions.'%(output_2,output_1))
        print(status.text)

    # Save to Google only after Tweeting
    worksheet.append_row([now,output_1,output_2])


# In[ ]:



