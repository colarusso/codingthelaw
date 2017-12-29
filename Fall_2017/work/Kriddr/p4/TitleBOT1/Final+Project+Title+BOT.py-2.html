
# coding: utf-8

# ## Final Project
# by [John Kelley](https://www.linkedin.com/in/john-kelley-9038a588/)
# 
# ## About
# 
# I designed this twitter bot, [@TitleBOT1](https://twitter.com/TitleBOT1), to increase public awareness of lost pets.  It serves as an alert mechanism for people in the area by tweeting out the moment a missing pet is posted on the website I chose [Landmark Auctions](https://www.landmarkauction.biz).  Hopefully the greater awareness will lead to more pets being found.
# 
# ## Process 
# 
# When we started this project the first step was to create our Twitter Bot Profile and sign up for a Google API account to link with our Twitter account and with the code you see below.  The next step was to find a website that allows Robots to scrape from them.  To figure this out, I checked websites' "Terms of Service" first to see if scraping or crawling was prohibited.  After that I checked the "/robots.txt" file to see what restrictions the website owner had placed, if any, on locations in the site where I could scrape. Eventually I found a suitable website that would provide good data, and I next looked into how to scrape it.  To do this we had to examine the website's HTML code to find the specific data we wanted to capture and pull into a tweet.  My twitter bot had trouble being able to pull data at first. The [Regex](http://regex101.com) software our class used in order to come up with a regular expression and  scrape data was not easy to learn by any means.  It took a lot of practice and fine tuning, and meeting with the professor to grasp a better understanding.  Eventually I was able to figure it out and now the Bot tweets every time a new pet is listed on the website.  It uses the following two Regular Expressions that I fabricated to scrape the newest Lost Pet's name and also to pull the link that specific pet's webpage. Additionally, the Bot puts the newly collected data onto a [Google Sheet](https://docs.google.com/spreadsheets/d/11jcpZVdXuElndZBDZ4UIswms9RjdjdBE_fWNHm3rLwg/edit#gid=0) that I created and linked with the bot. The Bot is able to communicate with the Google sheet because of a module we us called a .json file which can be seen referenced in the code below, as AnimalSaverBOT-883fa173fdff.json.  Now everytime the Bot scrapes data and tweets it, that information is stored with a timestamp on the Google Sheet.
# 
# ## Product
# 
# Overall, I believe this project was a success.  I had my doubts early on because I have not had any experience prior to taking this class.  Yet with a little bit of perserverance and determination, I was able to create a Twitter Bot that successfully scrapes information, tweets it to the public, and then records the data in an organized fashion on a Google Spreadsheet
# 

# In[1]:

# Load the module for visiting and reading websites.
import urllib.request
# Load the module for running regular expressions (regex).
import re 
# Load the module for date and time stuff.
import datetime
# Define the variable now as equal to the current date and time.
now = datetime.datetime.now()


# In[2]:

# Set the URL you want to scrape.
url_1 = "http://www.landmarkauction.biz"
url_2 = "https://www.timeanddate.com"

# If you want to scrape data from multiple pages, you can, 
# just replicate the above and below but change url_1 to url_2 et al.


# In[3]:

# Load the module for accessing Google Sheets.
import gspread
# Load the module needed for securely communicating with Google Sheets.
from oauth2client.service_account import ServiceAccountCredentials
# The scope for your access credentials
scope = ['https://spreadsheets.google.com/feeds']

# Your spreadsheet's ID
document_key = "11jcpZVdXuElndZBDZ4UIswms9RjdjdBE_fWNHm3rLwg" 
#              ^^^^^^^^^^^ SWAP OUT FOR YOUR DOCUMENT ID/KEY
# Your Google project's .json key
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../AnimalSaverBOT-883fa173fdff.json', scope)
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


# In[4]:

# Print out the old values stored in your sheet 
# Note: The first time you run this code, it will be empty as nothing has yet to be stored in your sheet.

print(worksheet.row_values(worksheet.row_count))
#############################
# DELETE CELL AFTER TESTING
#############################


# In[5]:

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


# In[6]:

p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()
print(p_1)


# In[7]:

p_2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_2).read()
print(p_2)


# In[8]:

res_1 = re.search(b"data-title=\"(.*)\,.*\,.*\".<.*>\s*<\/div>\s*<div\sclass=\"clear\"><\/div>\s*<\/article>\s*<\/div>\s*<!",p_1)
output_2 = res_1.group(1).decode('UTF-8')
print(output_2)
res_1 = re.search(b"data-title=\".*\,\s*(.*,...).*\s*\d{5}\".<.*>\s*<\/div>\s*<div\sclass=\"clear\"><\/div>\s*<\/article>\s*<\/div>\s*<!",p_1)
output_3 = res_1.group(1).decode('UTF-8')
print(output_3)
res_1 = re.search(b"data-title=\".*(\d{5})\".<.*>\s*<\/div>\s*<div\sclass=\"clear\"><\/div>\s*<\/article>\s*<\/div>\s*<!",p_1)
output_4 = res_1.group(1).decode('UTF-8')
print(output_4)
res_1 = re.search(b">(.*)<\/time>\n.*\n\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n\n.*\n\n.*\n.*\n.*\n\n.*\n.*\n.*\n.*\n.*\n\n.*\n\n.*\n.*\n.*\n\n.*\n\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n\n.*\n\n.*\n.*\n.*\n.*\n\n.*\n\n\n.*\n.*\n.*\n\n.*\n{2}(?:.*\n){4}.*\n{2}.*data-title=\".*\".<.*>\s*<\/div>\s*<div\sclass=\"clear\"><\/div>\s*<\/article>\s*<\/div>\s*<!",p_1)
output_5 = res_1.group(1).decode('UTF-8')
print(output_5)
res_1 = re.search(b"<\/span><br><span id=\"ij2\">(.*)<\/span><br>",p_2)
output_1 = res_1.group(1).decode('UTF-8')
print(output_1)
res_1 = re.search(b"href=\"(.*\.biz\/)\"",p_1)
output_6 = res_1.group(1).decode('UTF-8')
print(output_6)


# ## Post to Twitter and Save to Google

# In[9]:

if (res_1 and (worksheet.row_values(worksheet.row_count)[1]) != output_1
          and (worksheet.row_values(worksheet.row_count)[2]) != output_2
          and (worksheet.row_values(worksheet.row_count)[3]) != output_3
          and (worksheet.row_values(worksheet.row_count)[4]) != output_4
          and (worksheet.row_values(worksheet.row_count)[5]) != output_5
          and (worksheet.row_values(worksheet.row_count)[6]) != output_6):
    # The above If statment, says to continue only if the we actuall got some data from the page
    # and the old sheet values and the new pulled values are not equal (!=) to eachother. 

    # Go ahead and tweet out the update. Here you need to know about a Twitter API limitation.
    # Twitter will not Tweet the same tweet a second time if it is too close to the first instance.
    # In such cases, it will throw an error. The `try:` and `except TwitterError:` constructions are
    # similar to If statements. However, they will try the first block of code first, and only try 
    # the second block if it runs into a Twitter error. Here, the second try tweaks the language
    # just enough that it isn't a duplicate Tweet.
    try:
        # Post to Twitter.
        #print ('P1 Title is %s'%(output_4))
        status = api.PostUpdate('%s %s - %s %s %s has a Foreclosure Auction Scheduled on %s.'%(output_6,output_1,output_2,output_3,output_4,output_5))
        print(status.text)
    except TwitterError:
        # Post to Twitter.
        #print ('P1 Title: %s'%(output_4))
        status = api.PostUpdate('%s %s - %s %s %s goes up for sale by the foreclosing bank on %s.'%(output_6,output_1, output_2,output_3,output_4,output_5))
        print(status.text)

    # Save to Google only after Tweeting
    worksheet.append_row([now,output_1,output_2,output_3,output_4,output_5,output_6])


# In[10]:

print(worksheet.row_values(worksheet.row_count))


# In[ ]:

import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds']
document_key = "11jcpZVdXuElndZBDZ4UIswms9RjdjdBE_fWNHm3rLwg"
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../AnimalSaverBOT-883fa173fdff.json', scope)
csvfile = "output.csv"
gc = gspread.authorize(credentials)
wks = gc.open_by_key(document_key)
worksheet = wks.worksheet("Sheet1")
list_of_lists = worksheet.get_all_values()
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)

import pandas as pd
output = pd.read_csv(csvfile)
output[:3]

