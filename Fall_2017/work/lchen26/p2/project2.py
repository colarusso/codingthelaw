
# coding: utf-8

# # Cambridge Weather and Daily Wiki Bot by Loren Chen
# 
# 
# ## Twitter Bot Purpose
# 
#    The goal of my [Twitter Bot](https://twitter.com/weatherwiki_bot) is to be able to reguarly notify users the current temperature and humidity in Cambridge as well as a daily featured Wikipedia article. The sites I used are as follows:
# [Cambridge Weather](http://forecast.weather.gov/MapClick.php?lat=42.36715360000011&lon=-71.10340049999996#.Wd6C8VuPJEY)
# [Wikipedia Main Page](https://en.wikipedia.org/wiki/Main_Page)
# The data will be vary if a change is detected. For the Wikipedia article, it will change every day, while the temperature and humidity will likely change multiple times during the day.
# 
# ## Project Notes
# 
#    There were several steps I partook to ensure that my twitter bot worked as intended. First, I conducted a search to make sure that the two target sites' terms of service and robots.txt explicitly allowed or did not disallow scraping. The Wikipedia page is public domain, and Weather.com did not disallow the scraping of this specific weather data. Second, I crafted the code needed to scrape the information from the sites using regular expressions. To format these expressions, I obtained the page sources of the sites and used a [regular expression formatter](https://regex101.com) to come up with the necessary regular expressions. Both regular expressions are different since they are scraping different information. Third, I imported api keys for the twitter bot to be able to read the code and display the information obtained. (The API keys will be sent via other means) In addition, I created a [spreadsheet](https://docs.google.com/spreadsheets/d/1MgQXqAakTpZQSUYj4hdjVppncTXg3AD-LDi8ZeBjRMw/) which tracks the changes that the bot has received. Finally, I tested the bot several times to ensure that it worked, tweaking several parts including deleting previous tweets and clearing the spreadsheet. (Several of the tweets remain on the twitter account remain remain as proof of concept.) I believe that the bot properly displays the information I set out to scrape.
#    
# 
# ## Challenges and Future Goals
#    There were two challenges that I encountered while testing my twitter bot. The first was framing my regular expressions. The regular expressions are meant to pinpoint several pieces of the page source, and at first it wasn't picking up the proper code or scraping too much. After much trial-and-error, I tweaked and refined the regular expressions to a point where it can consistently scrape the proper data. The other was determining what information I was to scrape. Each of the sites had a lot of useful information I could scrape. For weather, in addition to temperature and humidity, I could scrape wind speed and visibility. For Wikipedia, in addition to the featured article, I could scrape interesting facts or number of edits. The data I decided to scrape was determined based on what I felt would be most useful to the public.
#    If I were to improve upon this at a later date, I would add more pieces of data for the Wikipedia articles, such as more variation in articles, and I would perhaps look for data in the sites that may update more frequently.

# In[83]:

import urllib.request
import re 
import datetime
now = datetime.datetime.now()


# In[84]:

url_1 = "https://en.wikipedia.org/wiki/Main_Page"
url_2 = "http://forecast.weather.gov/MapClick.php?lat=42.36715360000011&lon=-71.10340049999996#.Wd6C8VuPJEY"


# In[85]:

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds']
document_key = "1MgQXqAakTpZQSUYj4hdjVppncTXg3AD-LDi8ZeBjRMw"
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../SheetsBot-51db789eba6b.json', scope)

gc = gspread.authorize(credentials)
wks = gc.open_by_key(document_key)

worksheet = wks.worksheet("Sheet1")
worksheet.resize(worksheet.row_count)


# In[86]:

import csv
csvfile = "output.csv"
list_of_lists = worksheet.get_all_values()
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)

import pandas as pd
output = pd.read_csv(csvfile)
output[:3]


# In[87]:

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


# In[88]:

p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()
print(p_1)


# In[89]:

res_1 = re.search(b'<li><a href=\"(\/wiki\/[^\"]*)\"[^>]*>([^<]*)<\/a><\/li>',p_1)
output_1= res_1.group(1).decode('UTF-8')
output_2 = res_1.group(2).decode('UTF-8')
print(output_1,output_2)


# In[90]:

p_2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_2).read()
print(p_2)


# In[91]:

res_2 = re.search(b"<p class=\"myforecast-current-lrg\">(\d+).*</p>",p_2)
res_3 = re.search(b"<td>(\d+%)",p_2)
output_3 = res_2.group(1).decode('UTF-8')
output_4 = res_3.group(1).decode('UTF-8')
print(output_3)
print(output_4)


# In[92]:

print("%s | %s | %s | %s | %s"%(worksheet.row_values(worksheet.row_count)[0],worksheet.row_values(worksheet.row_count)[1],worksheet.row_values(worksheet.row_count)[2],worksheet.row_values(worksheet.row_count)[3],worksheet.row_values(worksheet.row_count)[4]))


# In[93]:

if ((worksheet.row_values(worksheet.row_count)[1]) != output_1
    or (worksheet.row_values(worksheet.row_count)[2]) != output_2 
    or (worksheet.row_values(worksheet.row_count)[3]) != output_3
    or (worksheet.row_values(worksheet.row_count)[4]) != output_4 ):    
    try:
        status = api.PostUpdate('It\'s %s °F in Cambridge, MA and the humidity is %s, and here\'s a Wikipedia article on %s: http://www.wikipedia.org%s'%(output_3,output_4,output_2,output_1))
        print(status.text)
    except TwitterError:
        status = api.PostUpdate('It is %s °F in Cambridge, MA and the humidity is %s, and today\'s Wikipedia article is about %s: http://www.wikipedia.org%s'%(output_3,output_4,output_2,output_1))
        print(status.text)
        
    worksheet.append_row([now, output_1,output_2,output_3,output_4])


# In[94]:

print(worksheet.row_values(worksheet.row_count))


# 

# 

# In[ ]:




# 

# 

# 

# In[ ]:




# In[ ]:




# In[ ]:




# 
