
# coding: utf-8

# # Project 2 - Executive Order Twitter Bot
# 
# ## Background
#    The purpose of this [Twitter Bot](https://twitter.com/mmckeown76), known as the EO BOT! was created to update people on the enactment of new Presidential Executive Orders.  The EO BOT! checks the [White House](https://www.whitehouse.gov/briefing-room/presidential-actions/executive-orders) website to see if another Executive Order has been enacted and includes in a follow up tweet a link to the Order.  
# 
# ## Development
#    The project began with an initial brainstorm as to what would be a fun subject for the twitter bot to track as well as something that would be useful to the twitter community.  Inspired by the short snippets of political news provided by outlets such as [whatthefuckjusthappenedtoday.com](whatthefuckjusthappenedtoday.com), I was interested in developing something that would monitor some level of government activity.  Given our President's record number of Executive Orders at this point and given their large impact on many people, I thought it would be interested to create a bot that would announce when a new one was created and provide information about it.  
#    The first step in creating the bot was to look to see whether or not scraping the White House website would violate any securities laws by reading their robot.txt file.  Unable to find one, I was able to find a site containing their [Copyright Policy](https://www.whitehouse.gov/copyright).  This site states that by law, the information on the White House are not protexted by copyright.  
#    The second step in creating the bot was to decide what information would be best to scrape from the White House site.  Based on the character limitations of Twitter, I thought it best to publish the "headline" from the announcement of the Executive Order as that typically contains information about the nature/substance of the Order.  Additionally, I thought it best to include a link to the Order itself.  In order to accomplish this, I wrote a regular expression that would parse the site for the text of the headlines for the links to Executive Orders as well as the target of the link.  When developing the regular expression, one challenge I found was distinguishing which links on the site we wanted to target.  Fortunately, the header style for the Executive Order links are unique and that was the easiest way to target the correct text & link.  
#    Finally, the code saved the new data to an [excel sheet](https://docs.google.com/spreadsheets/d/1i3K8_eEzyr4i6pA-rBiagA4FKG177B88JtUT8V6fkwo/edit?usp=sharing) as well as published it via two different tweets on Twitter.  One challenge that I encountered when developing this bot was the character limit per tweet.  Ideally I would have liked to combine both tweets but unfortunately due to the limited character count and the fact that the link to the Executive Order is counted towards the character count, it was necessary to seperate them.  Fortuantely, the result was ultimately the same.  After completing the code, I cleaned up the comments and also deleted several chunks of code and cells that were extrenuous.  
#    
#    The EO BOT! successfully searches the White House website to see if a new Executive Order was enacted, saves the title and link to an excel sheet, and publishes the information on twitter!  

# In[225]:

import urllib.request
import re 
import datetime
now = datetime.datetime.now()


# In[226]:

url_1 = "https://www.whitehouse.gov/briefing-room/presidential-actions/executive-orders"
url_2 = "https://www.whitehouse.gov/briefing-room/presidential-actions/executive-orders"


# In[227]:

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds']
document_key = "1i3K8_eEzyr4i6pA-rBiagA4FKG177B88JtUT8V6fkwo"
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../Twitter Bot-7f427da82901.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open_by_key(document_key)
worksheet = wks.worksheet("Sheet1")
worksheet.resize(worksheet.row_count)


# In[228]:

import csv
csvfile = "output.sav"
list_of_lists = worksheet.get_all_values()
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)
import pandas as pd
output = pd.read_csv(csvfile)
output[:3]


# In[229]:

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


# In[230]:

p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()
print(p_1)


# In[239]:

res_1 = re.search(b'>(\w+\s.*)<\/a><\/h3>',p_1)
print(res_1.group(1).decode('UTF-8'))
res_2 = re.search(b'<a href="(\/the-press-office\/.*)">',p_2)
print(res_2.group(1).decode('UTF-8'))


# In[234]:

if res_1 and res_2: 
    output_1 = res_1.group(1).decode('UTF-8')
    output_2 = 'https://www.whitehouse.gov' + res_2.group(1).decode('UTF-8')
    both = output_1 + " AND " + output_2


# In[235]:

print("%s | %s | %s | %s"%(worksheet.row_values(worksheet.row_count)[1],worksheet.row_values(worksheet.row_count)[2],worksheet.row_values(worksheet.row_count)[3],worksheet.row_values(worksheet.row_count)[2]))


# In[236]:

print("%s | %s | %s | %s"%(now,output_1,output_2,both))


# In[238]:

if res_1 and res_2: 
    if (float(worksheet.row_values(worksheet.row_count)[1]) != output_1) or (float(worksheet.row_values(worksheet.row_count)[2]) != output_2):
        if (float(worksheet.row_values(worksheet.row_count)[1]) != output_1):
            try:
                status = api.PostUpdate('A New Order!  %s'%(output_1))
                print(status.text)
            except TwitterError:
                status = api.PostUpdate('Another One!  %s'%(output_1))
                print(status.text)         
        if ((float(worksheet.row_values(worksheet.row_count)[2]) != output_2)):
            try:
                status = api.PostUpdate('Check out the link! %s'%(output_2))
                print(status.text)
            except TwitterError:
                status = api.PostUpdate("Here's the link! %s"%(output_2))
                print(status.text)
        worksheet.append_row([now,output_1,output_2,titles])


# In[ ]:




# In[ ]:




# In[ ]:



