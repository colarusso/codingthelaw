
# coding: utf-8

# ## The Idea
# I started looking through governmental websites because those information are more open to webscraping and therefore would not run into as much legal issues. I decided to work with the Massachusetts legislature website because although the information are public, not a lot of people will go through and read them. By tweeting them out, people can have easier access and also be aware just by reading the title of the tweet.

# In[35]:

# Load the module for visiting and reading websites.
import urllib.request
# Load the module for running regular expressions (regex).
import re 
# Load the module for date and time stuff.
import datetime
# Define the variable now as equal to the current date and time.
now = datetime.datetime.now()


# ## Testing the Idea
# My original idea was to tweet out the reports that are part of the Bills. I worked on understanding the page source and found a way to isolate the title and the url. Unfortunately, i went back to the same page, and the codes changed. I also spoke to Professor, and he stated that it would be also be harder to tweet out the new updates beacuse the bot right now would have to rescan the whole document and due to the set up of the page, the new tweet might not actually be the most updated one, just that it is different from the previous tweet. So i need to find another page source.

# ## The New Idea
# I went to the front page of the website and saw the "Most Popular" tables. In order to check that the content changes and the code stayed the same, I used a website call [Wayback Machine](https://archive.org/web/). I checked the same page in 2016 to see if the list changed and look at the page source. They seem fine to continue to the next step.
# 

# In[36]:

# Set the URLs you want to scrape.
url_1 = "https://malegislature.gov/"


# In[37]:

# Load the module for accessing Google Sheets.
import gspread
# Load the module needed for securely communicating with Google Sheets.
from oauth2client.service_account import ServiceAccountCredentials
# The scope for your access credentials
scope = ['https://spreadsheets.google.com/feeds']

# Your spreadsheet's ID
document_key = "1T4Eivm8C4BJ_MIo4PGFjkC2dj6fK9oRowapDouhhH6U"
# Your Google project's .json key
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../Sheetsbot-d365f0555548.json', scope)

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


# In[38]:

# download spreadsheet
import csv
csvfile = "output.csv"
list_of_lists = worksheet.get_all_values()
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)

import pandas as pd
output = pd.read_csv(csvfile)
output[:3]


# In[39]:

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


# ## Regex
# First I was able to isolate the code of the bill/general law and the link. But because the title name is a few lines of code away, it would be easier to use url 2 and isolate the title name seperately. Therefore, I have two of the same url but the regular expression are different. Then i combine them and created a tweet that will have the chapter of the general law or the bill no. of the bill, then the name of that bill and then the url that links to that bill. If a new bill or general law was added to the most popular list, the bot should be able to recognize the change and tweet out the newest addition.
# 
# 

# ## Regex second attempt
# While combining the code, I realize I am unable to grab the Bills but only the general law because the code shows up before the bills. I once again used the Wayback Machine to check if the general law or the bills changes more oftern. It turns out that the bills does and therefore, I decided to only tweet out the most popular bills. I also needed to isolate the title name for the bills instead of the general law. In order to do that I needed to continue my first regular expression because of the unique code &nbsp; which could isolae the title for the bills and not the general law. Therefore, I can use one url instead of two and have three outputs from one url. I then deleted the second url and the combination section.
# 
# 

# ## Read the contents of your first webpage
# 
# When you run the next cell, your program will visit the first URL you defined above. It will then print out that page's HTML. 

# In[40]:

p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()
print(p_1)


# ## Parse the site's contents
# 
# Using [Regex 101](https://regex101.com/) I tested my regex to parse the content. 
# There are three outputs. One is the end of the url. One is the bill code and one is the bill's title.

# In[41]:

res_1 = re.search(b"<td><a href=\"([^\"]*)\">([^<]*)&nbsp;[^\"]*[^=]*[^-]*[^\"]*[^=]*[^t]*[^\"]*[^\"]*\S([^\"]*)",p_1)
output_1 = res_1.group(1).decode('UTF-8')
output_2 = res_1.group(2).decode('UTF-8')
output_3 = res_1.group(3).decode('UTF-8')
print(output_1,output_2,output_3)


# In[42]:

# Print out the old values stored in your sheet 
# Note: The first time you run this code, it will be empty as nothing has yet to be stored in your sheet.
print("%s | %s | %s | %s"%(worksheet.row_values(worksheet.row_count)[1],worksheet.row_values(worksheet.row_count)[2],worksheet.row_values(worksheet.row_count)[3],worksheet.row_values(worksheet.row_count)[2]))


# In[43]:

# Print the new values pulled from your pages
print("%s | %s | %s | %s"%(now,output_1,output_2,output_3))


# ## Post to Twitter and Save to Google

# In[45]:

if (res_1 and (worksheet.row_values(worksheet.row_count)[1]) != output_1
          and (worksheet.row_values(worksheet.row_count)[2]) != output_2
          and (worksheet.row_values(worksheet.row_count)[3]) != output_3):
    # same as above but now comparing two values
    
    try:
        # Post to Twitter.
        status = api.PostUpdate('%s %s https://malegislature.gov%s'%(output_2,output_3,output_1))
        print(status.text)
    except TwitterError:
        # Post to Twitter.
        status = api.PostUpdate('Here we go again! %s %s https://malegislature.gov%s'%(output_2,output_3,output_1))
        print(status.text)

    # Save to Google only after Tweeting
    worksheet.append_row([now,output_1,output_2, output_3])

