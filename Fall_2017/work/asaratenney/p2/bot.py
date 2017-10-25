
# coding: utf-8

# ## EPA Regulation Watch
# by [Asara Tenney](https://www.linkedin.com/in/asarantenney)
# 
# ## About
# My [EPA Reg Watch Twitter](https://twitter.com/EPA_Reg_Watch) 
# 
# ## Google Spreadsheet 
# My [Google Sheet](https://docs.google.com/spreadsheets/d/10wCtE_3fedEyR-AFxHeTtdj4ABvDnfvcfJQa1EPvimc/edit?usp=sharing)
# 
# ## Process 
# First I made sure my project was in compliance with federal law under CFAA. Next, I made a twitter account with a nifty handle - EnviRegWatch. Then, I made a GoogleSheet Database to set a script to run on a schedule. This makes sure the Bot only tweets an article once. After that, I scraped a webpage, performed a regex, and got the relevant data onto the Google Sheet. Luckily, I didn't have too much trouble because my target site could be read by my scraper.
# Once my bot was drawing data from my intended target and successfully retrieving data from that target.. Presto it was ready to Tweet. 
# 
# Adapted from the notebook found at [How to Build a Law Bot](https://lawyerist.com/how-build-law-bot/)

# In[6]:

# Load the module for visiting and reading websites.
import urllib.request
# Load the module for running regular expressions (regex).
import re 
# Load the module for date and time stuff.
import datetime
# Define the variable now as equal to the current date and time.
now = datetime.datetime.now()


# In[13]:

# Set the URL you want to scrape.
url_1 = "http://www.npr.org/templates/search/index.php?searchinput=epa+regulation&tabId=all&dateId=&sort=date"

# If you want to scrape data from multiple pages, you can, 
# just replicate the above and below but change url_1 to url_2 et al.


# In[14]:

# Load the module for accessing Google Sheets.
import gspread
# Load the module needed for securely communicating with Google Sheets.
from oauth2client.service_account import ServiceAccountCredentials
# The scope for your access credentials
scope = ['https://spreadsheets.google.com/feeds']

# Your spreadsheet's ID
document_key = "10wCtE_3fedEyR-AFxHeTtdj4ABvDnfvcfJQa1EPvimc"
# Your Google project's .json key
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../My Project 91819-cffd05a25e34.json', scope)

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


# In[15]:

# Print out the old values stored in your sheet 
# Note: The first time you run this code, it will be empty as nothing has yet to be stored in your sheet.

print(worksheet.row_values(worksheet.row_count))
#############################
# DELETE CELL AFTER TESTING
#############################


# In[22]:

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

# In[17]:

p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()
print(p_1)


# ------------------------------------
# 
# # One Data Point, One Match
# 
# ## Parse the site's contents 
# 
# Scan the above HTML for the content you are trying to extract. Cut and paste the HTML above into the TEST STRING box over at [Regex 101](https://regex101.com/) and craft a regex that captures your desired content. Be sure to use the Python flavor.
# 
# Remember the parenthetical is the group you're pulling out. Once you have a working regex, plug it into the code below, and run the cell. If it worked, you'll see you scraped data as an output. 

# In[18]:

res_1 = re.search(b"<title>(.*)</title>",p_1)
output_1 = res_1.group(1).decode('UTF-8')
print(output_1)


# ## Post to Twitter and Save to Google

# In[ ]:

if (res_1 and (worksheet.row_values(worksheet.row_count)[1]) != output_1):
    # The above If statment, says to continue only if the we actuall got some data from the page
    # and the old sheet vales and the new pulled values are not equal (!=) to eachother. 

    # Go ahead and tweet out the update. Here you need to know about a Twitter API limitation.
    # Twitter will not Tweet the same tweet a second time if it is too close to the first instance.
    # In such cases, it will throw an error. The `try:` and `except TwitterError:` constructions are
    # similar to If statements. However, they will try the first block of code first, and only try 
    # the second block if it runs into a Twitter error. Here, the second try tweaks the language
    # just enough that it isn't a duplicate Tweet.
    try:
        # Post to Twitter.
        #print ('P1 Title is %s'%(output_1))
        status = api.PostUpdate('http://www.npr.org/%s'%(output_1))
        print(status.text)
    except TwitterError:
        # Post to Twitter.
        #print ('P1 Title: %s'%(output_1))
        status = api.PostUpdate('P1 Title: %s'%(output_1))
        print(status.text)

    # Save to Google only after Tweeting
    worksheet.append_row([now,output_1])


# In[ ]:

print(worksheet.row_values(worksheet.row_count))
#############################
# DELETE CELL AFTER TESTING
#############################


# # Two Data Points, One Match
# 
# ---------------------------
# ## Parse the site's contents

# In[19]:

res_1 = re.search(b"class=\"title\">\s*.*href=\"(.*)\">(.*)<",p_1)
output_1 = res_1.group(1).decode('UTF-8')
print(output_1)
output_2 = res_1.group(2).decode('UTF-8')
print(output_2)


# ## Post to Twitter and Save to Google (Two Data Point, One Match)

# In[23]:

if (res_1 and (worksheet.row_values(worksheet.row_count)[1]) != output_1
          and (worksheet.row_values(worksheet.row_count)[2]) != output_2):
    # same as above but now comparing two values
    
    try:
        # Post to Twitter.
        status = api.PostUpdate('%s %s'%(output_2,output_1))
        print(status.text)
    except TwitterError:
        # Post to Twitter.
        status = api.PostUpdate('%s %s'%(output_2,output_1))
        print(status.text)

    # Save to Google only after Tweeting
    worksheet.append_row([now,output_1,output_2])


# In[2]:

print(worksheet.row_values(worksheet.row_count))
#############################
# DELETE CELL AFTER TESTING
#############################


# # Two Data Points, Multiple Fixed Number of Matches
# 
# -------------------------------------------
# 
# ## Parse the site's contents and post to Twitter 

# In[ ]:

matches = re.finditer(b"<a href=\"([^\"]*)\"[^>]*>([^<]*)</a>",p_1)
column = 0
columns = [now]

for matchNum, match in enumerate(matches):
    matchNum = matchNum + 1
    column = column + 1
    column2 = column + 1
    
    output_1 = match.group(1).decode('UTF-8')
    output_2 = match.group(2).decode('UTF-8')
    
    if (res_1 and (worksheet.row_values(worksheet.row_count)[column]) != output_1 
              and (worksheet.row_values(worksheet.row_count)[column2]) != output_2):
        # same as above but now comparing the two values handled in this loop
        
        try:
            # Post to Twitter.
            status = api.PostUpdate('%s %s'%(output_2,output_1))
            print(status.text)
        except TwitterError:
            # Post to Twitter.
            status = api.PostUpdate('%s %s'%(output_2,output_1))
            print(status.text)
            
        columns.append(output_1)
        columns.append(output_2)
        
    column = column + 1

# Save to Google only after Tweeting
worksheet.append_row(columns)


# In[ ]:

print(worksheet.row_values(worksheet.row_count))
#############################
# DELETE CELL AFTER TESTING
#############################

