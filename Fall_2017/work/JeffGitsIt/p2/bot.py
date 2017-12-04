
# coding: utf-8

# Adapted from the notebook found at [How to Build a Law Bot](https://lawyerist.com/how-build-law-bot/)
# 
# # History Twitter Bot
# By [Jeff Price](http://www.linkedin.com/in/jpjeffprice) 
# 
# This Twitter Bot is designed to scrape the Wikipedia Engilish main page, gather an item from the "On This Day..." section, and tweet it out at @ThisDayHist.
# 
# ## Source Analysis
# I began by analyzing Wikipedia’s robots.txt file and looking through the [Terms of Use](https://wikimediafoundation.org/wiki/Terms_of_Use/en) page to ensure scraping the desired data would be permissible.
# 
# ## Regular Expressions
# Perhaps the most difficult part of this project was trying to figure out how to use [regular expressions](https://regex101.com/) (regex) to pull out data from the (very long) block of code that is the Wikipedia main page. I began by finding the part of the code containing the "On This Day..." material, but had trouble getting the regex search to narrow in on the desired content without capturing other material. My first attempt was to simply include more and more of the code preceding the target material until I had a unique string that would only trip the search where I wanted it to. The problem was, the Wikipedia main page is so full of links, and so sparse on static content, that this string of code wouldn’t survive one of the daily page updates.
# 
# ## Refinement
# With the help of Professor Colarusso, I was able to key in on the "four digit year and dash" sequence that preceded the “On This Day…” content, which was found nowhere else on the Wikipedia main page. This solved the search portion of the regular expression, but then I ran into the problem that each historical note after the year was in a different format, with varying lengths of text and numbers of links. I spent much time trying to devise a way to capture just the overall text for one historical note, but was unable to reliably scrape anything but one of the title links.
# 
# ## Additional Issues
# I also some minor problems with the other code blocks, mostly having to do with adjustments required by the number and labels of my variables (e.g., I needed to add output_2 in several places and delete other variables). When errors would crop up, I didn’t always remember to search for this issue. Finally, it turns out that even though I thought I was converting the Mac-default Rich Text Format text files into plain text by adjusting the file extension from .rtf to .txt (and agreeing to “convert” the files on the corresponding pop up), this was insufficient to reformat the text files. With some trouble shooting help from Professor Colarusso, I was able to see this format conversion was incomplete, and the proper reformatting solved the final major issue of my bot.
# 
# ## Future Improvements
# The bot does scrape, save to a Google sheet, and tweet. However, right now it only tweets the year and title of one event. As such, this bot will currently only tweet twice a day a similar message about the same event. It also only tweets a title from the historical note, which is usually just a noun (e.g., a person’s name, a place, etc). While this information is incomplete, it might make a curious person Google the noun and the year to see what happened.
# 
# In the future, I want to refine the regular expression to accurately capture the full text of the relevant historical note (though the Twitter character limit might constrain this), and perhaps even link to the corresponding Wikipedia article. Further, the “On This Day…” section displays around five historical events of note each day, as well as a handful of notable holidays and anniversaries from around the world. Ideally, I would be able to scrape and tweet out each of these historical facts at various times during the day. For example, the bot could be set to scrape the “On This Day…” section once an hour, tweeting out a novel event until it runs out of material.
# 

# In[70]:

# Load the module for visiting and reading websites.
import urllib.request
# Load the module for running regular expressions (regex).
import re 
# Load the module for date and time stuff.
import datetime
# Define the variable now as equal to the current date and time.
now = datetime.datetime.now()


# In[71]:

# Set the URLs you want to scrape.
url_1 = "https://en.wikipedia.org/wiki/Main_Page"


# In[72]:

# Load the module for accessing Google Sheets.
import gspread
# Load the module needed for securely communicating with Google Sheets.
from oauth2client.service_account import ServiceAccountCredentials
# The scope for your access credentials
scope = ['https://spreadsheets.google.com/feeds']

# Your spreadsheet's ID
document_key = "1DhNhP6p3xH83mi8UDWXNG_b-EocOJCZVHVUGS6YWLcc"
# Your Google project's .json key
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../SheetsBot-ce4e7f1dda77.json', scope)

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


# In[74]:

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


# In[75]:

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


# ## Read the contents of your first webpage
# 
# When you run the next cell, your program will visit the first URL you defined above. It will then print out that page's HTML. 

# In[76]:

p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()
print(p_1)


# ## Parse the site's contents
# 
# Scan the above HTML for the content you are trying to extract. Cut and paste the HTML above into the TEST STRING box over at [Regex 101](https://regex101.com/) and craft a regex that captures your desired content. 
# 
# Remember the parenthetical is the group you're pulling out. Once you have a working regex, plug it into the code below, and run the cell. If it worked, you'll see you scraped data as an output. 

# In[77]:

res_1 = re.search(b'>(\d{4})</a>\s\xe2\x80\x93\s<a href=".*"\stitle="(.*)".*</li>\n<li>',p_1)
print(res_1.group(1).decode('UTF-8'))
print(res_1.group(2).decode('UTF-8'))


# ## Read the contents of your second webpage
# 
# Same deal as above, but now we're looking at your second URL. 

# In[ ]:




# ## Parse the site's contents
# 
# Again, the same as above, but with a new regex on a new page.

# In[ ]:




# ## Combine Stuff
# 
# Now we're going to take the values you found above and do something with them. The new thing you'll be seeing in this code is the If statement. In Python, if you type `if [some evaluation]:` then the code directly below that statement and indented once will run only if that evaluation is true. For example:

# In[78]:

# The If statment below says: If the variable res_1 actually exists, do what follows.
if res_1: 
    # Make sure res_1 is in a format we can read (that's the "decode" part)
    # output_1 equal to regex match on page one.
    output_1 = res_1.group(1).decode('UTF-8')
    output_2 = res_1.group(2).decode('UTF-8')


# In[79]:

# Print out the old values stored in your sheet 
# Note: The first time you run this code, it will be empty as nothing has yet to be stored in your sheet.
print("%s | %s | %s | %s"%(worksheet.row_values(worksheet.row_count)[1],worksheet.row_values(worksheet.row_count)[2],worksheet.row_values(worksheet.row_count)[3],worksheet.row_values(worksheet.row_count)[2]))


# In[80]:

# Print the new values pulled from your pages
print("%s | %s"%(output_1,output_2))


# ## Post to Twitter and Save to Google

# In[82]:

if res_1: 
    # Again, the above tells the program to continue with what follows only if res_1 exists
    
    if ((worksheet.row_values(worksheet.row_count)[1]) != output_1) or ((worksheet.row_values(worksheet.row_count)[2]) != output_2):
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
                status = api.PostUpdate('On this day in %s this happened: %s'%(output_1, output_2))
                print(status.text)
            except TwitterError:
                # Post to Twitter.
                status = api.PostUpdate('In %s on this day, this happened: %s'%(output_1, output_2))
                print(status.text)

        
                
        worksheet.append_row([output_1,output_2])


# In[ ]:



