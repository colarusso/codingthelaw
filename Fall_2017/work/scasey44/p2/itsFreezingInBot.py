
# coding: utf-8

# Adapted from the notebook found at [How to Build a Law Bot](https://lawyerist.com/how-build-law-bot/)
# 
# The following bot is called "It's freezing in..."  It looks at five weather stations in Alaska, and if it is freezing there, and it is colder than the last check, it tweets out the temperature with the weather station.  I used weather underground weather stations for five different stations in Alaska, so there would be a better chance that it would actually be freezing there.
# 
# The biggest challenge in this project was the regular expression.  I had a more literal string initially that worked fine on the regex site, but it wouldn't work in my code.  Instead I had to use some wild cards to get rid of the literal parts of the string. If I spent more time with it, I think I could get a more eloquent solution, but the wild card version is fine for the purpose of this bot.  
# 
# Other challenges included getting familiar with gspread.  I felt the API was a bit incomplete and could have included more exams.  There weren't many useful tutorials either, but the API did make manipulating google spreadsheets rather easy. 
# 
# The following links are for the spreadsheet and the twitter account.
# https://docs.google.com/spreadsheets/d/1o1UXtdUHmBjZ2lpY5j1WUVZMj6b2SzTsUVcN6PU6YPE/edit?usp=sharing
# https://twitter.com/itsFreezingIn
# 
# ## Import modules and set variables
# 
# 
# Now we're getting into the bot's code. This is what will run every time your bot is called. 
# 
# You will need to create a new Google Sheet (same instructions as [last time](https://lawyerist.com/126074/online-forms-meet-local-document-automation-cut-and-paste-coding/)). Delete rows 2-999. This is because the code below appends values to the end of your sheet. So if you fail to remove rows 2-999, values will be appended to row 1000. Additionally, it looks at the last row of the sheet for your old values. So right off the bat it will be looking at your one solitary row. Also, delete columns D through Z to avoind having to print a bunch of empty columns.
# 
# As for a Twitter account and Twitter credentials, follow the instruction in [this post](https://lawyerist.com/?p=127093). 

# In[117]:


# Load the module for visiting and reading websites.
import urllib.request
# Load the module for running regular expressions (regex).
import re 
# Load the module for date and time stuff.
import datetime
# Define the variable now as equal to the current date and time.
now = datetime.datetime.now()


# In[125]:


#Weather station URL List
url_list = ["https://www.wunderground.com/personal-weather-station/dashboard?ID=KAKALASK2#history", 
            "https://www.wunderground.com/personal-weather-station/dashboard?ID=KAKALASK3#history",
            "https://www.wunderground.com/personal-weather-station/dashboard?ID=KAKALASK5#history",
            "https://www.wunderground.com/personal-weather-station/dashboard?ID=KAKALASK6#history",
            "https://www.wunderground.com/personal-weather-station/dashboard?ID=KAKALASK8#history"
           ]
#Weather station list
station_list = ["KALASKA2", "KALASKA3", "KALASKA5", "KALASKA6", "KALASKA8"]


# In[119]:


# Load the module for accessing Google Sheets.
import gspread
# Load the module needed for securely communicating with Google Sheets.
from oauth2client.service_account import ServiceAccountCredentials
# The scope for your access credentials
scope = ['https://spreadsheets.google.com/feeds']

# Your spreadsheet's ID
document_key = "1o1UXtdUHmBjZ2lpY5j1WUVZMj6b2SzTsUVcN6PU6YPE" 
#              ^^^^^^^^^^^ SWAP OUT FOR YOUR DOCUMENT ID/KEY
# Your Google project's .json key
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../Sheetsbot-45b52a7afea6.json', scope)
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


# In[120]:


# Print out the old values stored in your sheet 
# Note: The first time you run this code, it will be empty as nothing has yet to be stored in your sheet.

print(worksheet.row_values(worksheet.row_count))
#############################
# DELETE CELL AFTER TESTING
#############################


# In[121]:


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


# ## Read the contents of each webpage and store the results in a list
# Iterate through the url_list, read the contents, and store the contents in our results_list for later use.

# In[122]:


results_list = []
for item in url_list:
    results_list.append(urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(item).read())
    


# ------------------------------------
# 
# # Get the current temperature from each of the weather stations
# 
# Iterate through the list of site html and parse out the current temperature and put it in our temp_list.

# In[123]:


temp_list = [];
for idx in results_list:
    res_1 = re.search(b"<div id=.*curTemp.*>\n\t<span class=.*temperature.*>\n\t\t<span class=.*wx-value.*>(.*)</span>",idx)
    output_1 = res_1.group(1).decode('UTF-8')
    temp_list.append(output_1)
    print(output_1)


# ## Post to Google and determine if we are going to tweet it out.  We only tweet when it's colder than the last check and it's freezing there.

# In[124]:


#Append the new data to the spreadsheet and then compare the last two rows to see if it's colder.  If it is, then we will tweet it out.
worksheet.append_row(temp_list)
row_vals = worksheet.row_values(worksheet.row_count)
row_vals2 = worksheet.row_values(worksheet.row_count-1)

count=0;

#Iterate through the two lists
while count < worksheet.col_count:
    
    if(float(row_vals[count]) > 32.0):
        count+=1
        continue
    #Have to account for the chance of an empty value
    if row_vals[count] is not None and row_vals2[count] is not None:
        #Is it colder at a particular weather station?
        if (row_vals[count]< row_vals2[count]):
            place = station_list[count]
            postText = "It's freezing in %s!!!  It's %s degrees fahrenheit outside!!!"%(place, row_vals[count])
            try:
               # Post to Twitter.
                status = api.PostUpdate(postText)
                print(status.text)
            except TwitterError:
                # Post to Twitter.
                status = api.PostUpdate(postText)
                print(status.text)
    count+=1

