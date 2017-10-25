
# coding: utf-8

# Adapted from the notebook found at [How to Build a Law Bot](https://lawyerist.com/how-build-law-bot/)
# 
# ## My Bot
# My name is Justin Martino. I made a twitter bot that monitors the Lake Levels on Merrymeeting Lake, New Hampshire, here is the [link](https://twitter.com/MMLakeLevels). My Twitter Bot monitors the Merrymeeting Lake homepage. The Lake's homepage monitors the water level of the lake and updates whether the lake is rising, falling, freezing, or melting. This is updated on a monthly basis. My twitter bot will tweet out when the page has changed and link users to the Merrymeeting Lake webpage.
# 
# ## Process/Challenges
# 
# In order to do this, I had to scrape the Merrymeeting Lake Associations' webpage. The Lake Association updates the water level of the lake monthly. My code will scrape the webpage and note when the webpage has change (i.e, when the Lake level has been updated). When I first started this project I wanted to do scrape a webpage for a sports team and update after the teams games. However, because of the way the Boston Blades update their webpage I was unable to scrape their page. After succesfully scraping Merrymeeting Lakes webpage, I had to generate a regular expression that would pull out information or data that changed on the website. This was the most difficult part of the process because generating the correct code that capture what I was looking for was very challenging. Next, once I got the correct regular expression to capture what I was looking for I had to get the API credentials for my twitter account that would allow my twitter account to interact with my code and the google sheet I created to save the values it pulls off the webpage.
# 
# ## Looking Ahead
# 
# If I were to improve my twitter bot in the future there are definitley some aspects that would make my twitter bot more user friendly. First off, because I struggled creating a regular expression my expression is pretty basic and does not contain a large amount of detail. For example, I wanted to have my twitter bot to include in the tweet whether the lake has frozen, melted, dropped or rose in water level. However, my bot only tweets out As of (a certain date) with a link to the Merrymeeting Lake webpage. In addition, because the Lake's webpage also includes graphs and pictures of the lake while updating the levels of the lake it would be really great for the users of twitter to be able to see these graphs or pictures in the tweet. 

# In[ ]:

# Load the module for visiting and reading websites.
import urllib.request
# Load the module for running regular expressions (regex).
import re 
# Load the module for date and time stuff.
import datetime
# Define the variable now as equal to the current date and time.
now = datetime.datetime.now()


# In[ ]:

# Set the URLs you want to scrape.
url_1 = "http://mmlake.org/LakeWaterLevel.html"
url_2 = "http://mmlake.org/"


# In[ ]:

# Load the module for accessing Google Sheets.
import gspread
# Load the module needed for securely communicating with Google Sheets.
from oauth2client.service_account import ServiceAccountCredentials
# The scope for your access credentials
scope = ['https://spreadsheets.google.com/feeds']

# Your spreadsheet's ID
document_key = "1Kl-1YKoyN0oKa73zfIiixZxwbHdvMa7Blenmzhy3_U8"
# Your Google project's .json key
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../SheetsBot-7c811819a7a6.json', scope)

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


# In[ ]:

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

# In[38]:

p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()
print(p_1)


# ## Parse the site's contents
# 
# Scan the above HTML for the content you are trying to extract. Cut and paste the HTML above into the TEST STRING box over at [Regex 101](https://regex101.com/) and craft a regex that captures your desired content. 
# 
# Remember the parenthetical is the group you're pulling out. Once you have a working regex, plug it into the code below, and run the cell. If it worked, you'll see you scraped data as an output. 

# In[39]:

res_1 = re.search(b'As of ([^<]*)</p>',p_1)
output_1 = res_1.group(1).decode('UTF-8')
print(output_1)


# In[40]:

# Print out the old values stored in your sheet 
# Note: The first time you run this code, it will be empty as nothing has yet to be stored in your sheet.
print("%s | %s | %s | %s"%(worksheet.row_values(worksheet.row_count)[1],worksheet.row_values(worksheet.row_count)[2],worksheet.row_values(worksheet.row_count)[3],worksheet.row_values(worksheet.row_count)[2]))


# ## Post to Twitter and Save to Google

# In[42]:

if (worksheet.row_values(worksheet.row_count)[1] != output_1):
        try:
            status = api.PostUpdate('The Lake Level changed as of %s as seen here:http://mmlake.org/LakeWaterLevel.html'%(output_1))
            print(status.text)
        except TwitterError:
            # Post to Twitter.
            #print ('P1 Title: %s'%(output_1))
            status = api.PostUpdate('LOOK! The Level changed %s as seen here: http://mmlake.org/LakeWaterLevel.html'%(output_1))
            print(status.text)
            
        worksheet.append_row([now,output_1])

