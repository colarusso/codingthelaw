
# coding: utf-8

# ## Insurance Law News Twitter Bot
# by [Devon Bodey](https://www.linkedin.com/in/devonbodey/)
# 
# 
# ### About
# This TwitterBot, [@InsureLawNews](https://twitter.com/InsureLawNews), was designed to monitor information on the Web and tweet out posts when changes in information occurs. This particular bot monitors two internet blogs that publish news on insurance law. These blogs highlight important information such as new legislation, policy reform, and notable court cases.
# 
# 
# ### Scraping and Saving
# In order for [@InsureLawNews](https://twitter.com/InsureLawNews) to publish tweets, I had to find sources to "scrape". Scraping is a technique that extracts data from web-sources. This scraped data is saved in a spreadsheet. The spreadsheet I used was a Google sheet via the API. A copy of this spreadsheet can be found [here](https://docs.google.com/spreadsheets/d/1owZJO_V-Wd1WT1QhP1PVLA2iGa37UezwY3aapWSO6VI/edit?usp=sharing). This Google spreadsheet compiles the information that has been scraped from the internet, logs it, and ensures that repeat tweets are not posted.
# 
# Prior to finding specific sources to scrape, it is important to run a search and make sure that the information being scraped is not prohibited under the CFAA. In order to test a source prior to scraping its information "robots.txt" can be added to the end of the web address. It is also important to look at the websites terms and conditions to verify that they have not expressly prohibited secondhand publication, or unpermitted use. In conducting a thorough search, I was luckily unable to find any information which indicated that the sources disallowed scraping of the information they publish.
# 
# To ensure the TwitterBot continually tweets information every time one of the blogs posts a new post, I included a regular expression into my code. To format this regular expression I used [regular expression](https://regex101.com). The regular expression I used differs for both blogs. However, both are coded to post the title of the blog post and the link to the source. 
# 
# 
# ### Tweet
# This TwitterBot scrapes and saves news updates that are posted on both ["Insurance Litigation and Regulatory Law" blog](http://www.insurancelitigationregulatorylaw.com) and ["Insurance Coverage Law Blog"](http://www.grinsurancecoveragelawblog.com). This information is  then posted on [Twitter](http://www.twitter.com). Anytime either blog publishes an update, the TwitterBot will tweet out this information. As above mentioned, the tweet will contain the title of the article, and a link to the source. Most tweets should contain the full title of the article, however, due to Twitter's 140 character limit, the TwitterBot is designed to tweet only tweet the first 108 characters of the article title. This avoids complication, and ensures that a majority of the article title, and a complete link will be seamlessly tweeted.
# 
# 
# 
# Adapted from the notebook found at [How to Build a Law Bot](https://lawyerist.com/how-build-law-bot/)

# In[90]:

# Load the module for visiting and reading websites.
import urllib.request
# Load the module for running regular expressions (regex).
import re 
# Load the module for date and time stuff.
import datetime
# Define the variable now as equal to the current date and time.
now = datetime.datetime.now()


# In[91]:

# Set the URL you want to scrape.
url_1 = "http://www.insurancelitigationregulatorylaw.com/category/court-cases/"
url_2 = "http://www.grinsurancecoveragelawblog.com"

# If you want to scrape data from multiple pages, you can, 
# just replicate the above and below but change url_1 to url_2 et al.


# In[92]:

# Load the module for accessing Google Sheets.
import gspread
# Load the module needed for securely communicating with Google Sheets.
from oauth2client.service_account import ServiceAccountCredentials
# The scope for your access credentials
scope = ['https://spreadsheets.google.com/feeds']

# Your spreadsheet's ID
document_key = "1owZJO_V-Wd1WT1QhP1PVLA2iGa37UezwY3aapWSO6VI" 
#              ^^^^^^^^^^^ SWAP OUT FOR YOUR DOCUMENT ID/KEY
# Your Google project's .json key
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../twitterbotkey.json', scope)
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


# In[93]:

# Print out the old values stored in your sheet 
# Note: The first time you run this code, it will be empty as nothing has yet to be stored in your sheet.

print(worksheet.row_values(worksheet.row_count))
#############################
# DELETE CELL AFTER TESTING
#############################


# In[94]:

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

# In[95]:

p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()
print(p_1)


# In[96]:

p_2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_2).read()
print(p_2)


# # Two Data Points, One Match
# 
# ---------------------------
# ## Parse the site's contents

# In[97]:

res_1 = re.search(b"entry-title.*href=\"(.*)\" .*>(.*)</a",p_1)
output_1 = res_1.group(1).decode('UTF-8')
print(output_1)
output_2 = res_1.group(2).decode('UTF-8')
print(output_2)
res_2 = re.search(b"url:\s\"(.*)\",\s*title: \"(.*)\"",p_2)
output_3 = res_2.group(1).decode('UTF-8')
print(output_3)
output_4 = res_2.group(2).decode('UTF-8')
print(output_4)


# In[98]:

print(output_4[0:110])


# ## Post to Twitter and Save to Google (Two Data Point, One Match)

# In[99]:

if (res_1 and ((worksheet.row_values(worksheet.row_count)[1]) != output_1
          and (worksheet.row_values(worksheet.row_count)[2]) != output_2)
           or ((worksheet.row_values(worksheet.row_count)[3]) != output_3
          and (worksheet.row_values(worksheet.row_count)[4]) != output_4)):
    # same as above but now comparing two values
    
    if ((worksheet.row_values(worksheet.row_count)[1]) != output_1
          and (worksheet.row_values(worksheet.row_count)[2]) != output_2):
        try:
            # Post to Twitter.
            status = api.PostUpdate('%s . . . %s'%(output_2[0:108],output_1))
            print(status.text)
        except TwitterError:
            # Post to Twitter.
            status = api.PostUpdate('%s . . . %s'%(output_2[0:108],output_1))
            print(status.text)

    if ((worksheet.row_values(worksheet.row_count)[3]) != output_3
          and (worksheet.row_values(worksheet.row_count)[4]) != output_4):
        try:
            # Post to Twitter.
            status = api.PostUpdate('%s . . . %s'%(output_4[0:108],output_3))
            print(status.text)
        except TwitterError:
            # Post to Twitter.
            status = api.PostUpdate('%s . . . %s'%(output_4[0:108],output_3))
            print(status.text)


    # Save to Google only after Tweeting
    worksheet.append_row([now,output_1,output_2,output_3,output_4])


# In[100]:

print(worksheet.row_values(worksheet.row_count))
#############################
# DELETE CELL AFTER TESTING
#############################


# 

# In[ ]:



