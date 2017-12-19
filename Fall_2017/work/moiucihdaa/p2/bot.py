
# coding: utf-8

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
# Now we're getting into the bot's code. This is what will run every time your bot is called. To make sure it behaves as expected, replace the placeholder values found below in the `document_key`, `credentials`, `consumer_key`, `consumer_secret`, `access_token_key`, and `access_token_secret` variables with relevant values (e.g., your access credentials). 
# 
# You will need to create a new Google Sheet (same instructions as [last time](https://lawyerist.com/126074/online-forms-meet-local-document-automation-cut-and-paste-coding/)). You **MUST** add a first row with headings. If you don't, the below code won't work. In this example, just make four columns filled with zeros. Also, delete rows 2-999. This is because the code below appends values to the end of your sheet. So if you fail to remove rows 2-999, values will be appended to row 1000. Additionally, it looks at the last row of the sheet for your old values. So if you fail to delete 2-999, instead of seeing your row of zeros, it will look at the blank row 999.
# 
# As for a Twitter account and Twitter credentials, follow the instruction in [this post](https://lawyerist.com/?p=127093). 
# 
# *NOTE: You should be reading all of the comments (i.e., text following a #)*

# In[209]:

# Load the module for visiting and reading websites.
import urllib.request
# Load the module for running regular expressions (regex).
import re 
# Load the module for date and time stuff.
import datetime
# Define the variable now as equal to the current date and time.
now = datetime.datetime.now()


# In[210]:

# Set the URLs you want to scrape.
url_1 = "https://www.whitehouse.gov/briefing-room/presidential-actions/executive-orders"
url_2 = "https://www.whitehouse.gov/briefing-room/presidential-actions/executive-orders"


# In[211]:

# Load the module for accessing Google Sheets.
import gspread
# Load the module needed for securely communicating with Google Sheets.
from oauth2client.service_account import ServiceAccountCredentials
# The scope for your access credentials
scope = ['https://spreadsheets.google.com/feeds']

# Your spreadsheet's ID
document_key = "1i3K8_eEzyr4i6pA-rBiagA4FKG177B88JtUT8V6fkwo"
# Your Google project's .json key
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../Twitter Bot-7f427da82901.json', scope)

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


# In[212]:

# download spreadsheet
import csv
csvfile = "output.sav"
list_of_lists = worksheet.get_all_values()
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)

import pandas as pd
output = pd.read_csv(csvfile)
output[:3]


# In[213]:

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

# In[214]:

p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()
print(p_1)


# ## Parse the site's contents
# 
# Scan the above HTML for the content you are trying to extract. Cut and paste the HTML above into the TEST STRING box over at [Regex 101](https://regex101.com/) and craft a regex that captures your desired content. 
# 
# Remember the parenthetical is the group you're pulling out. Once you have a working regex, plug it into the code below, and run the cell. If it worked, you'll see you scraped data as an output. 

# In[215]:

res_1 = re.search(b'>(\w+\s.*)<\/a><\/h3>',p_1)
print(res_1.group(1).decode('UTF-8'))


# ## Read the contents of your second webpage
# 
# Same deal as above, but now we're looking at your second URL. 

# In[216]:

p_2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_2).read()
print(p_2)


# ## Parse the site's contents
# 
# Again, the same as above, but with a new regex on a new page.

# In[217]:

res_2 = re.search(b'<a href="(\/the-press-office\/.*)">',p_2)
print(res_2.group(1).decode('UTF-8'))


# ## Combine Stuff
# 
# Now we're going to take the values you found above and do something with them. The new thing you'll be seeing in this code is the If statement. In Python, if you type `if [some evaluation]:` then the code directly below that statement and indented once will run only if that evaluation is true. For example:

# In[218]:

# The If statment below says: If the variables res_1 and res_2 actually exist, do what follows.
if res_1 and res_2: 
    # Make sure res_1 is in a format we can read (that's the "decode" part)
    # output_1 equal to regex match on page one.
    output_1 = res_1.group(1).decode('UTF-8')
    # Do the same thing as above but for res_2
    output_2 = 'https://www.whitehouse.gov' + res_2.group(1).decode('UTF-8')
    # Combine titles. Then store the value in the variable named "titles."
    titles = output_1 + " AND " + output_2


# In[219]:

# Print out the old values stored in your sheet 
# Note: The first time you run this code, it will be empty as nothing has yet to be stored in your sheet.
print("%s | %s | %s | %s"%(worksheet.row_values(worksheet.row_count)[1],worksheet.row_values(worksheet.row_count)[2],worksheet.row_values(worksheet.row_count)[3],worksheet.row_values(worksheet.row_count)[2]))


# In[220]:

# Print the new values pulled from your pages
print("%s | %s | %s | %s"%(now,output_1,output_2,titles))


# ## Post to Twitter and Save to Google

# In[221]:

if res_1 and res_2: 
    # Again, the above tells the program to continue with what follows only if res_1 and res_2 exist
    
    if (float(worksheet.row_values(worksheet.row_count)[1]) != output_1) or (float(worksheet.row_values(worksheet.row_count)[2]) != output_2):
        # The above If statment, says to continue only if the old sheet vales and 
        # the new pulled values are not equal (!=) to eachother. 
        
        if (float(worksheet.row_values(worksheet.row_count)[1]) != output_1):
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
                status = api.PostUpdate('A New Order!  %s'%(output_1),'%s'%(output_2))
                print(status.text)
            except TwitterError:
                # Post to Twitter.
                #print ('P1 Title: %s'%(output_1))
                status = api.PostUpdate('Another One!  %s'%(output_1))
                print(status.text)

        # What follows is effctivly the above but for the second value.         
        if ((float(worksheet.row_values(worksheet.row_count)[2]) != output_2)):

            try:
                #print ('P2 Title is %s'%(output_2))
                status = api.PostUpdate('Check out the link! %s'%(output_2))
                print(status.text)
            except TwitterError:
                #print ('P2 Title: %s'%(output_2))
                status = api.PostUpdate('Here"s the link! %s'%(output_2))
                print(status.text)
                
        worksheet.append_row([now,output_1,output_2,titles])


# In[ ]:




# In[ ]:




# In[ ]:



