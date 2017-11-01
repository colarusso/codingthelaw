
# coding: utf-8

# # Scraping and Twitter Bot
# By Charmaine Wood
# 
# I wrote a bot which is designed to monitor two websites and tweet the most recent news articles and bills related to marijuana in Massachusetts. The code for the bot can be found below. To write my bot, we had to develop a Google document and obtain the document key as well as the credtials associated with it. I also had to create a twitter that would be linked to the Google document and tweet out the information that is scraped with the regex I developed.
# 
# ## Process of Deciding on Subject Matter
# 
# It took me a while to decide what I wanted to work with for this project. I asked many people for their opinion before deciding on monitoring the regulation process of marijuana after legalization. I knew that I wanted to monitor something law related that was also new, that was when I decided that the process after legalization of marijuana would be interested. Especially since there has been a decline in follow through with implementation of dispensories for recreational use.
# 
# ## Refinement
# 
# There was very little to revise for this project. Many of the steps for development were straigth forward. The main issues I had revolved around the regex section. I read and reread many articles before my first attempt at creating one myself. I was out of my element with this and it took me mant attempts before I was able to develop something that began to find matches within my websites. It was actually very frustrating! I understood the concept but I just could not get it do what I wanted it to do. I started out simple and expended on it while looking out the inspect option of one specific articles on my websites. After finally developing a way to scrape my selected websites I became concerned of the possibility of being banned due to accessing the websites to often. In order to ensure this does not happen I decided to include a timer so that The site will only be scraped once a day and the new information will be tweeted.
# 
# ## Real-World Viability
# 
# I believe that the bot will be helpful to anyone curious about were Massachusetts stands in regards in marijuana. It will provide easy access to current bills so that the user will know his/her rights and have access to any current news related to marijuana use, whether it be medical or recreational.

# In[37]:


import urllib.request
import re 
import datetime
import time
now = datetime.datetime.now()


url_1 = "https://malegislature.gov/Bills"
url_2 = "http://norml.org/news/us-ma"


import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds']


document_key = "135EBa7vawuCh44cIoGdIkXUVhOX38YamvnAsNu93s0Y"
credentials = ServiceAccountCredentials.from_json_keyfile_name('../../../../../RightToSpark.json', scope)


gc = gspread.authorize(credentials)
wks = gc.open_by_key(document_key)


worksheet = wks.worksheet("Sheet1")

worksheet.resize(worksheet.row_count)

import csv
csvfile = "output_mine.csv"
list_of_lists = worksheet.get_all_values()
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)

import pandas as pd
output = pd.read_csv(csvfile)
output[:3]

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



while True:
    p_1 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_1).read()

    res_1 = re.finditer(b'<td><a href="(.*)".*</td>.*\r\n.*<td .*>(.*marijuana.*)</td>',p_1,re.IGNORECASE)
    column = 0
    for matchNum, match in enumerate(res_1):
        columns = [now]
        matchNum = matchNum + 1
        column = column + 1
        column2 = column + 1

        output_1_link = "https://malegislature.gov" + match.group(1).decode('UTF-8')
        output_1_title = match.group(2).decode('UTF-8')

        if (res_1 and (worksheet.row_values(worksheet.row_count)[1]) != output_1_title 
                  and (worksheet.row_values(worksheet.row_count)[2]) != output_1_link):

            try:
                status = api.PostUpdate('%s %s'%(output_1_title,output_1_link))
                print(status.text)
            except TwitterError:
                print('%s %s'%(output_1_title,output_1_link))

            columns.append(output_1_title)
            columns.append(output_1_link)

            worksheet.append_row(columns)

    p_2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url_2).read()
    res_2 = re.finditer(b'<a title="(.*)" href="(.*)".*>.*marijuana.*</a>',p_2, re.IGNORECASE)
    column = 0


    for matchNum, match in enumerate(res_2):
        columns = [now]
        matchNum = matchNum + 1

        output_2_title = match.group(1).decode('UTF-8')
        output_2_link = "http://norml.org" + match.group(2).decode('UTF-8')

        if output_2_link == "http://norml.org/":
            continue

        if (res_2 and (worksheet.row_values(worksheet.row_count)[3]) != output_2_title 
                  and (worksheet.row_values(worksheet.row_count)[4]) != output_2_link):

            try:
                status = api.PostUpdate('%s %s'%(output_2_title,output_2_link))
                print(status.text)
            except TwitterError:
                print('%s %s'%(output_2_title,output_2_link))

            columns.append(output_2_title)
            columns.append(output_2_link)

            worksheet.append_row(columns)
    time.sleep(86400) #check for updates once a day

