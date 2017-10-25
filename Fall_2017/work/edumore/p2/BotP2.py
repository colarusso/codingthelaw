
# coding: utf-8

# ## Boston Medical Malpractice Twitter Bot
# by [Erica Dumore](https://www.linkedin.com/in/erica-dumore-62b306a2/)
# 
# ## About
# 
# I currently work as a law clerk at a medical malpractice law firm in the Greater Boston area. Enjoying my work and the area of law, I decided to create a Twitter Bot, [@Boston_MedMal](https://twitter.com/Boston_MedMal), that would tweet out updates on current medical malpractice legal issues. The twitter bot does this by scraping posts from two Boston legal blogs. Whenever the blogs release a new post relating to medical malpractice, whether it is a current case decision, a settlement award, or discussing an ongoing issue, the twitter bot will tweet out the title of the blog article and a link that viewers are able to click to read the full blog article. 
# 
# My goal for this twitter bot is to make it easy for those interested in this area of the law to be able to stay up to date on the current issues and decisions in medical malpractice in the Greater Boston area.
# 
# ## Google Spreadsheet
# 
# For this project I had to create a google spreadsheet using microsoft excel. After creating the spreadsheet I had to generate a document ID key (1-sYU2ur4kpERjl0dFr_ZcpsVRMWG_J1n98r9ExDOClE) that would allow me to link my spreadsheet to my twitter bot. My spreadsheet,[My Twitter Bot](https://docs.google.com/spreadsheets/d/1-sYU2ur4kpERjl0dFr_ZcpsVRMWG_J1n98r9ExDOClE/edit?usp=sharing), allows my twitter bot to scrape the two blog websites for new article posts and records the posts to twitter through timestamps to ensure each blog article is only tweeted once. 
# 
# ## Process
# 
# Before creating my twitter bot I brainstormed different ways to gather information to be tweeted. I had the idea of what I wanted my twitter bot to relate to, the area of medical malpractice, but I was not sure what I wanted my bot to scrape. After some hunting online I found [blawg](https://blawgsearch.justia.com/blogs/countries/united-states/massachusetts?page=1&sortby=popularity&dispmode=expanded&popmode=week), a legal blog search engine. From there I found two legal blogs that published articles that related to medical malpractice in the Boston area. The two blogs can be found in the links below:
# 
# [Blog 1](https://www.bostoninjurylawyerblog.com/category/medical-malpractice)
# 
# [Blog 2](https://www.bostonpersonalinjuryattorneyblog.com/category/medical-malpractice)
# 
# After finding what I wanted my twitter bot to scrape and checking to make sure these two blogs were able to be scraped without violating any federal laws (they both were!), I began the process of creating the twitter bot's twitter account, [@Boston_MedMal](https://twitter.com/Boston_MedMal). 
# 
# After creating the account and the google spreadsheet discussed above, I linked the twitter account, my code, and the spreadsheet using the generated documentation key, two additional private keys, and two tokens (API's). Theses API's allowed my code to access twitter and my spreadsheet so that it could scrape the two blog sites and gather the information, the article title and link, to be tweeted out. 
# 
# Once my code was set up to link the three processes together to be able to generate a tweet, I had to write code so that my twitter would know what to tweet. Because I was gathering information from legal blogs, I was able to use the blogs feeds to gain the blogs code. Once I had the blogs code I looked for the expressions that came before the title of the article and before the link that I wanted to tweet. Then, using regular expressions I placed the code I wanted my twitter bot to search for between the appropriate brackets. This told my bot that whenever it saw white space and then a title or a link, followed by additional white space, it should tweet. 
# 
# After a few trial and errors on getting the proper expression I was able to get the code to generate the appropriate title and link which told me I was on the right track to tweeting! Because I was using two different legal blogs I had to write code that would tell my bot to tweet from one blog if it could scrap new information or if it did not find new information to tweet from the second blog if it could scrap new information from that blog. Although this stage gave me the most hiccups, I was able to get my bot to tweet from both blogs! 
# 
# The biggest hiccup I encountered in the above mentioned stage was making sure that all of my output numbers corresponded to the appropriate website. Once I was able to get the outputs sorted out and all of my regular expressions were working, my bot scrapped information and tweeted the latest two articles posted by each blog. 
# 
# To ensure everything was continuing to work correctly, I deleted my tweets and cleared my spreadsheet multiple times. I ran into a problem after clearing my spreadsheet and generating my second blogs code. Because I had made the mistake of not adding additional columns to my excel spreadsheet no information was being saved in the spreadsheet, even though the blog articles were being tweeted. Once I added the additional columns so that both blogs had space to generate the information in the spread sheet, cleared my tweets and reset my code, I was able to tweet the latest blog posts of both blogs and have the information saved into my spreadsheet ensuring these articles would not be scraped and posted to my twitter account again. 
# 
# I then cleared my spreadsheet and deleted my twitter bots tweets once more to make certain my twitter bot was able to tweet. The tweets that appear on @Boston_MedMal today are a result of this process. 
# 
# This project was adapted from the notebook found at [How to Build a Law Bot](https://lawyerist.com/how-build-law-bot/).

# In[22]:


# Load the module for visiting and reading websites.
import urllib.request
# Load the module for running regular expressions (regex).
import re 
# Load the module for date and time stuff.
import datetime
# Define the variable now as equal to the current date and time.
now = datetime.datetime.now()


# In[23]:


# Set the URL you want to scrape.
#url_1 = "https://www.bostoninjurylawyerblog.com/category/medical-malpractice"
url_1 ="https://www.bostonpersonalinjuryattorneyblog.com/category/medical-malpractice/feed"
url_2 = "https://www.bostoninjurylawyerblog.com/category/medical-malpractice/feed"

# If you want to scrape data from multiple pages, you can, 
# just replicate the above and below but change url_1 to url_2 et al.


# In[24]:


# Load the module for accessing Google Sheets.
import gspread
# Load the module needed for securely communicating with Google Sheets.
from oauth2client.service_account import ServiceAccountCredentials
# The scope for your access credentials
scope = ['https://spreadsheets.google.com/feeds']

# Your spreadsheet's ID
document_key = "1-sYU2ur4kpERjl0dFr_ZcpsVRMWG_J1n98r9ExDOClE" 
#              ^^^^^^^^^^^ SWAP OUT FOR YOUR DOCUMENT ID/KEY
# Your Google project's .json key
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../CodingProject2-517c5ae88a4a.json', scope)
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


# In[26]:


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

# In[27]:


p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()
print(p_1)


# In[28]:


p_2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_2).read()
print(p_2)


# ------------------------------------
# 
# # One Data Point, One Match
# 
# ## Parse the site's contents 
# 
# Scan the above HTML for the content you are trying to extract. Cut and paste the HTML above into the TEST STRING box over at [Regex 101](https://regex101.com/) and craft a regex that captures your desired content. Be sure to use the Python flavor.
# 
# Remember the parenthetical is the group you're pulling out. Once you have a working regex, plug it into the code below, and run the cell. If it worked, you'll see you scraped data as an output. 

# In[29]:


res_1 = re.search(b"item>\s*<title>(.*)</title>\s*<link>(.*)</link>",p_1)
output_1 = res_1.group(1).decode('UTF-8')
output_2 = res_1.group(2).decode('UTF-8')
print(output_1)
print(output_2)


# In[30]:


res_2 = re.search(b"item>\s*<title>(.*)</title>\s*<link>(.*)</link>",p_2)
output_3 = res_2.group(1).decode('UTF-8')
output_4 = res_2.group(2).decode('UTF-8')
print(output_3)
print(output_4)


# ## Post to Twitter and Save to Google (Two Data Point, One Match)

# In[31]:


if ((res_1 and (worksheet.row_values(worksheet.row_count)[1]) != output_1
          and (worksheet.row_values(worksheet.row_count)[2]) != output_2)
    or
    (res_2 and (worksheet.row_values(worksheet.row_count)[3]) != output_3
          and (worksheet.row_values(worksheet.row_count)[4]) != output_4)):
    # same as above but now comparing two values
    
    if (res_1 and (worksheet.row_values(worksheet.row_count)[1]) != output_1
          and (worksheet.row_values(worksheet.row_count)[2]) != output_2):

        try:
            # Post to Twitter.
            status = api.PostUpdate('%s %s'%(output_1,output_2))
            print(status.text)
        except TwitterError:
            # Post to Twitter.
            status = api.PostUpdate('%s %s'%(output_1,output_2))
            print(status.text)        

    if (res_2 and (worksheet.row_values(worksheet.row_count)[3]) != output_3
          and (worksheet.row_values(worksheet.row_count)[4]) != output_4):

        try:
            # Post to Twitter.
            status = api.PostUpdate('%s %s'%(output_3,output_4))
            print(status.text)
        except TwitterError:
            # Post to Twitter.
            status = api.PostUpdate('%s %s'%(output_3,output_4))
            print(status.text)        

    # Save to Google only after Tweeting
    worksheet.append_row([now,output_1,output_2,output_3,output_4])    

