
# coding: utf-8

# # My North Korea Twitter Bot
# By: [Anon Silpavuthi](http://www.linkedin.com/in/anon-silpavuthi-83001bb1)
# 
# Adapted from the notebook found at [How to Build a Law Bot](https://lawyerist.com/how-build-law-bot/)
# 
# ## Goals
# The goal of my twitter bot is to be able to get and update of what is trending on the news regarding North Korea. The bot will automatically scrape the headlines of the [North Korea News section](http://www.aljazeera.com/topics/country/north-korea.html) of [Aljazeera News](http://www.aljazeera.com/) and automatically tweet the headline as well as the link to read more into [this twitter account](https://twitter.com/NKNewsBot).
# 
# ## Why North Korea Bot?
# North Korea has been on the news a lot late lately. North Korea has a military nuclear weapons program and also has a significant amount of chemical and biological weapons. Since 2003, North Korea is no longer a party to the Treaty on the Non-Proliferation of Nuclear Weapons (NPT). The country has come under sanctions after conducting a number of nuclear tests, beginning in 2006. 
# 
# In the past few months, North Korea has been threatening many threats to several countries such as the United States, Japan, and South Korea. I believe that it is important to know what is going on with North Korea so I decided to create [this twitter bot](https://twitter.com/NKNewsBot) that would tweet a quick update of the headline of news regarding North Korea.
# 
# Click [here](http://theconversation.com/why-north-koreas-nuclear-threat-must-be-taken-more-seriously-than-ever-76592) to read more about North Korea's nuclear threat.
# 
# ## Computer Fraud and Abuse Act and Intellectual Property Rights
# To avoid a violation of the Computer Fraud and Abuse Act (CFAA), I checked the [robots.txt file](http://www.aljazeera.com/robots.txt) of [Al Jazeera's website](http://www.aljazeera.com/) as well as [terms and conditions of Al Jazeera's website](http://www.aljazeera.com/aboutus/2011/01/20111168582648190.html) to make sure that they don't have any terms that disallow data scraping of a specific portion of their websites.
# 
# To avoid infringing on any intellectual proper rights, on the [twitter description](https://twitter.com/NKNewsBot), I also make it clear that it is clear that I don't have any affiliation with Al Jazeera so I put the following sentences in the description. "I am a bot that alerts you about the trending North Korea headline on Al Jazeera news. I am not affiliated with Al Jazeera."
# 
# ## Process
# I actually didn't start with North Korea bot. My first idea was actually to create a bot that would tweet out an update whether there is a jury trial at the United States District Court for the District of Massachusetts.
# 
# However, I changed my mind because I found out that the data I was trying to scrape is actually a pdf which means that I wouldn't be able to scrape the source code of the page, I could still do it but I just have to take different steps. Another reason I changed my mind was because I think that having a bot that tweets out that there is a jury trial on a particular day is not as interesting as a bot that tweets out new information every day.
# 
# Consequently, the first thing that came into my mind is a news bot updating news about North Korea which as you see, I eneded up doing it. 
# 
# ### The Set Up (Google Spreadsheet and Twitter)
# Before I start with data scraping there are several things that I had to set up.
# First, I had to install all the necessary libraries that I need to run the codes. Second, I created [this google spreadsheet](https://docs.google.com/spreadsheets/d/164Ae9PtqxwxTwO2l9y9qxtN4ZIpKdPLsjlHl5wDJOuI/edit) as a place to store data from which the code scrapes. I also had to set up google project json key.
# 
# I then created a twitter account and proceed to the [application management page](https://apps.twitter.com/) to get the API access as well as all the necessary key that I need to gain access for this bot to tweet.
# 
# I then started by choosing the website to scrape which I found to be the most difficult steps of building this twitter bot. I find that a lot of news websites just don't allow people to scrape explicitly and some just make it very hard for people to scrape the information.
# 
# ### The Set Up 2 (Data Scraping)
# I ended up choosing Al Jazeera because the source code doesn't seem to be to difficult to scrape, they don't have any terms that explicitly disallow people to scrape a portion of their data, and also because they update the section frequently. I started by using [regular expression 101](https://regex101.com/) and play around with the source code to figure out what part of information of the page should I to scrape and what regular expression I have to use to scrape them.
# 
# I decided to scrape the top headline of the page which top-feature-overlay-cont under <h2></h2> of the source code. I actually had some problem with the regular expression but with Professor Colarusso's help, I ended up with this regular expression: (b"top-feature-overlay-cont\">.*<a href=\"(.*)\">.*top-sec-title\">(.*)</h2>
# 
# This is a two-data point scraping so it will scrape the top-sec-title which is the headline of the article and the the url in href= and it will tweet out both of them in a single tweet.
# 
# ## Testing
# I tested this several times to ensure that this code works properly and actually tweet out. Before I conducted the testing, I deleted the data from my google spreadsheet as well as the previous tweet on twitter. So far, I haven't run into any errors.
# 
# ## Future Improvement
# I planned to do two different news sources and not just Al Jazeera but I had to abandon the plan for now because I find that the headline on Al Jazeera and even the content are very similar to other major new sources when they report North Korea. Therefore, it is not very practical to tweet out two very similar information. 
# 
# In the future, a potential improvement might be choosing a distinctive news sources and somehow make sure that it doesn't tweet the same / similar information regarding North Korea.
# 
# 
# 
# 
# 

# In[9]:

# Load the module for visiting and reading websites.
import urllib.request
# Load the module for running regular expressions (regex).
import re 
# Load the module for date and time stuff.
import datetime
# Define the variable now as equal to the current date and time.
now = datetime.datetime.now()


# In[10]:

# Set the URL you want to scrape.
url_1 = "http://www.aljazeera.com/topics/country/north-korea.html"

# If you want to scrape data from multiple pages, you can, 
# just replicate the above and below but change url_1 to url_2 et al.


# In[11]:

# Load the module for accessing Google Sheets.
import gspread
# Load the module needed for securely communicating with Google Sheets.
from oauth2client.service_account import ServiceAccountCredentials
# The scope for your access credentials
scope = ['https://spreadsheets.google.com/feeds']

# Your spreadsheet's ID
document_key = "164Ae9PtqxwxTwO2l9y9qxtN4ZIpKdPLsjlHl5wDJOuI" 
#              ^^^^^^^^^^^ SWAP OUT FOR YOUR DOCUMENT ID/KEY
# Your Google project's .json key
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../SheetsBot-252f10f5aedd.json', scope)
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


# In[12]:

# Print out the old values stored in your sheet 
# Note: The first time you run this code, it will be empty as nothing has yet to be stored in your sheet.

print(worksheet.row_values(worksheet.row_count))
#############################
# DELETE CELL AFTER TESTING
#############################


# In[13]:

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

# In[14]:

p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()
print(p_1)


# # Two Data Points, One Match
# 
# ---------------------------
# ## Parse the site's contents

# In[15]:

res_1 = re.search(b"top-feature-overlay-cont\">.*<a href=\"(.*)\">.*top-sec-title\">(.*)</h2>",p_1)
output_1 = res_1.group(1).decode('UTF-8')
print(output_1)
output_2 = res_1.group(2).decode('UTF-8')
print(output_2)


# ## Post to Twitter and Save to Google (Two Data Point, One Match)

# In[16]:

if (res_1 and (worksheet.row_values(worksheet.row_count)[1]) != output_1
          and (worksheet.row_values(worksheet.row_count)[2]) != output_2):
    # same as above but now comparing two values
    
    try:
        # Post to Twitter.
        status = api.PostUpdate('Trending Today: %s http://www.aljazeera.com/%s'%(output_2,output_1))
        print(status.text)
    except TwitterError:
        # Post to Twitter.
        status = api.PostUpdate('Trending Update: %s http://www.aljazeera.com/%s'%(output_2,output_1))
        print(status.text)

    # Save to Google only after Tweeting
    worksheet.append_row([now,output_1,output_2])

