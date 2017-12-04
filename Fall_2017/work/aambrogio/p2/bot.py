
# coding: utf-8

# ## My Twitter Bot: Keeping Up with Massachusetts Elections and Candidates
# By Alessandra Ambrogio
# 
# http://elections.mytimetovote.com/dates/massachusetts.html (https://goo.gl/axTtaJ)
# 
# https://uselections.com/ma/ma.htm (https://goo.gl/LNguu7)
# 
# The goal of my Twitter Bot is to be able to check these two sites, one for any updates at all so people can check on election date information (new and old) and the latter for specific updates to that page in order to see changes to candidates and candidate information. Everyone deserves a resource, especially one resource that points to a myriad of resources instead of requiring people to remember large amounts of information.
# 
# ## Notes About Work Product based on Project 2 Rubric
# 
# I have conducted an analysis of the two target sites’ terms of service and robots.txt files and have determined that scraping is either explicitly allowed, not disallowed or otherwise permissible. The information is the type that is public domain, so if I did miss anything while conducting my analysis, the content I specificially scrape should be either explicitly allowed, not disallowed or otherwise permissible.
# 
# My Twitter Bot regularly parses multiple pieces of content, specifically information regarding whether one link's contents have changed at all and information about the date that the content of the other page was updated. Results are saved to a Google Sheet.
# 
# My Twitter Bot regularly produces tweets based on the interplay of changes in the content it parses. 
# 
# Hopefully, I have provided enough information so that you can see the work that was done on this twitter bot. To note, I used a shortify think through Google to shorten the links that would tweet, a trick taught to me by a classmate (Matthew) who I am also grateful to for his help. I would be remiss if I did not thank Professor Colarusso for all of his help with fixing bugs and more, so thank you! Finally, welcome to my first Twitter Bot!
# 
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

# Set the URLs you want to scrape.
url_1 = "http://elections.mytimetovote.com/dates/massachusetts.html"
url_2 = "https://uselections.com/ma/ma.htm"


# In[3]:

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds']

# Your spreadsheet's ID
document_key = "1pHSLeu4M5n03mHM1gPjzkZlMeMFRLoFoEbq5zYvmjFE"
# Your Google project's .json key
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../Twitter Bot P2-ce6234e6a3b1.json', scope)

# Use your credentials to authorize yourself.
gc = gspread.authorize(credentials)
# Open up the Sheet with the defined ID.
wks = gc.open_by_key(document_key)

worksheet = wks.worksheet("Sheet1")

worksheet.resize(worksheet.row_count)


# In[4]:

import csv
csvfile = "output.csv"
list_of_lists = worksheet.get_all_values()
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)

import pandas as pd
output = pd.read_csv(csvfile)
output[:3]


# In[5]:

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


# ## Read the contents of your first webpage
# 
# When you run the next cell, your program will visit the first URL you defined above. It will then print out that page's HTML. 

# In[6]:

p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()
print(p_1)


# ## Parse the site's contents
# 
# Scan the above HTML for the content you are trying to extract. Cut and paste the HTML above into the TEST STRING box over at [Regex 101](https://regex101.com/) and craft a regex that captures your desired content. 
# 
# Remember the parenthetical is the group you're pulling out. Once you have a working regex, plug it into the code below, and run the cell. If it worked, you'll see you scraped data as an output. 

# In[7]:

output_1 = p_1
print (output_1)


# ## Read the contents of your second webpage
# 
# Same deal as above, but now we're looking at your second URL. 

# In[8]:

p_2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_2).read()
print(p_2)


# ## Parse the site's contents
# 
# Again, the same as above, but with a new regex on a new page.

# In[9]:

res_2 = re.search(b'<a href=.*>(.*)\S(last update)',p_2)
output_2 = res_2.group(1).decode('UTF-8')
print(output_2)


# ## Combine Stuff
# 
# Now we're going to take the values you found above and do something with them. The new thing you'll be seeing in this code is the If statement. In Python, if you type `if [some evaluation]:` then the code directly below that statement and indented once will run only if that evaluation is true. For example:

# In[10]:

# The If statment below says: If the variables res_1 and res_2 actually exist, do what follows.
if output_1 and res_2: 
    # Make sure res_1 is in a format we can read (that's the "decode" part)
    # output_1 equal to regex match on page one.
    output_1 = p_1
    # Do the same thing as above but for res_2
    output_2 = res_2.group(1).decode('UTF-8')
    # Combine titles. Then store the value in the variable named "titles."
    #titles = output_1 + " AND " + output_2


# ## Post to Twitter and Save to Google

# In[12]:

if p_1 and res_2: 
    # Again, the above tells the program to continue with what follows only if res_1 and res_2 exist
    
    if ((worksheet.row_values(worksheet.row_count)[1] != output_1) or (worksheet.row_values(worksheet.row_count)[2] != output_2)):
        # The above If statment, says to continue only if the old sheet vales and 
        # the new pulled values are not equal (!=) to eachother. 
        
        if ((worksheet.row_values(worksheet.row_count)[1]) != output_1):
            # The above If statment says to continue only if the first value is 
            # different from the last version stored in the sheet.
                            
            # Go ahead and tweet out the update. Here you need to know about a Twitter API limitation.
            # Twitter will not Tweet the same tweet a second time if it is too close to the first instance.
            # In such cases, it will throw an error. The `try:` and `except TwitterError:` constructions are
            # similar to If statements. However, they will try the first block of code first, and only try 
            # the second block if it runs into a Twitter error. Here, the second try tweaks the language
            # just enough that it isn't a duplicate Tweet.
            try:
                # Post to Twitter.
                #print ('P1 Title is %s'%(output_1))
                status = api.PostUpdate('The contents of the link changed: https://goo.gl/axTtaJ')
                print(status.text)
            except TwitterError:
                # Post to Twitter.
                #print ('P1 Title: %s'%(output_1))
                status = api.PostUpdate('Again, the contents have changed: https://goo.gl/axTtaJ')
                print(status.text)

        # What follows is effctivly the above but for the second value.         
        if (((worksheet.row_values(worksheet.row_count)[2]) != output_2)):

            try:
                #print ('P2 Title is %s'%(output_2))
                status = api.PostUpdate('https://goo.gl/LNguu7 was updated on %s'%(output_2))
                print(status.text)
            except TwitterError:
                #print ('P2 Title: %s'%(output_2))
                status = api.PostUpdate('Again, https://goo.gl/LNguu7 was updated on %s'%(output_2))
                print(status.text)
                                
        worksheet.append_row([now,output_1,output_2])


# In[ ]:




# In[ ]:



