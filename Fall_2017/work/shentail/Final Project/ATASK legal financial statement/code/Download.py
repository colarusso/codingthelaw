
# coding: utf-8

# ## Preparation
# First I created a new google account.
# Then I begin creating three forms that I need for the project.
# I first need to figure out what questions I would need for the forms. SO i have to decipher the forms that I want as an end result and write out all the required questions for the google form.
# Notes:
# Create new google acc
# Make word version of 3 forms (financial statement and naturalization)
# 
# 3 google forms which feeds into 3 good sheets.
# Then build 
# First create documents templates (forms)
# Identify things you need to know
# Find identifier for the case 
# Find the overlaps
# 
# Cut and paste how to download and get key for new google account and download for the sheets.
# In P2
# 
# Went to meet with Professor to work out the codes below. Bring in codes from previous projects, I was able to import the data from the google forms I have created and have them download to a csv file. I imported 2 seperate documents, client information and financial statement. Then with a common identification code, I combined the information on both forms into one csv file.
# 

# In[1]:

# Load the module for date and time stuff.
import datetime
# Define the variable now as equal to the current date and time.
now = datetime.datetime.now()
# Import module to deal with tables et al.
import pandas as pd
# Import module to deal with csv files
import csv
# Load the module for accessing Google Sheets.
import gspread
# Load the module needed for securely communicating with Google Sheets.
from oauth2client.service_account import ServiceAccountCredentials
# The scope for your access credentials
scope = ['https://spreadsheets.google.com/feeds']
# Your Google project's .json key
credentials = ServiceAccountCredentials.from_json_keyfile_name('../keys/ATASK legal.json', scope)
# Use your credentials to authorize yourself.
gc = gspread.authorize(credentials)


# In[2]:

# Your spreadsheet's ID for client information
document_key = "10W0TTi2eGdkW58uT1l1Q2MmQngBozV04p6FH2uAAVI0"
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
worksheet = wks.worksheet("Form Responses 1")
csvfile_1 = "../data/Client info.csv"


# Count the number of rows in your Sheet &
# resize to remove blank rows.
worksheet.resize(worksheet.row_count)
list_of_lists = worksheet.get_all_values()
with open(csvfile_1, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)
output = pd.read_csv(csvfile_1)      


# In[3]:

# Your spreadsheet's ID for financial statement
document_key = "12qox0l9J6AXxhW-9vD19vXPSFpVMby7GHBghkHJhjis"
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
worksheet = wks.worksheet("Form Responses 1")
csvfile_2 = "../data/Client financial.csv"


# Count the number of rows in your Sheet &
# resize to remove blank rows.
worksheet.resize(worksheet.row_count)
list_of_lists = worksheet.get_all_values()
with open(csvfile_2, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)
output = pd.read_csv(csvfile_2) 


# In[4]:

# Your spreadsheet's ID for financial statement chinese
document_key = "1Sum2KW3XElXAGSGQ0f9gNM278wUiqUovoP03Cq-RmmE"
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
worksheet = wks.worksheet("Form Responses 1")
csvfile_3 = "../data/Client financial chinese.csv"


# Count the number of rows in your Sheet &
# resize to remove blank rows.
worksheet.resize(worksheet.row_count)
list_of_lists = worksheet.get_all_values()
with open(csvfile_3, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)
output = pd.read_csv(csvfile_3) 


# In[5]:

# Your spreadsheet's ID for financial statement vietnamese
document_key = "1zqVQcDQBl-WDLzSloQskxc1xo2L5JlLk9HZXoj1q480"
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
worksheet = wks.worksheet("Form Responses 1")
csvfile_4 = "../data/Client financial vietnamese.csv"


# Count the number of rows in your Sheet &
# resize to remove blank rows.
worksheet.resize(worksheet.row_count)
list_of_lists = worksheet.get_all_values()
with open(csvfile_4, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)
output = pd.read_csv(csvfile_4) 


# In[6]:

# Your spreadsheet's ID for financial statement khmer
document_key = "1CW-ze3D2BoqxXa0ghpZgOBy6LozdJ_dvXMYs6a8Kz60"
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
worksheet = wks.worksheet("Form Responses 1")
csvfile_5 = "../data/Client financial khmer.csv"


# Count the number of rows in your Sheet &
# resize to remove blank rows.
worksheet.resize(worksheet.row_count)
list_of_lists = worksheet.get_all_values()
with open(csvfile_5, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)
output = pd.read_csv(csvfile_5) 


# In[7]:

# Your spreadsheet's ID for financial statement hindi
document_key = "1v-CitX1JnfKH5XFSXOr2C2ZRjp3VZwFHn1VyrOoPRt8"
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
worksheet = wks.worksheet("Form Responses 1")
csvfile_6 = "../data/Client financial hindi.csv"


# Count the number of rows in your Sheet &
# resize to remove blank rows.
worksheet.resize(worksheet.row_count)
list_of_lists = worksheet.get_all_values()
with open(csvfile_6, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(list_of_lists)
output = pd.read_csv(csvfile_6) 


# In[8]:

file_1 = pd.read_csv(csvfile_1)
file_2 = pd.read_csv(csvfile_2)
file_3 = pd.read_csv(csvfile_3)
file_4 = pd.read_csv(csvfile_4)
file_5 = pd.read_csv(csvfile_5)
file_6 = pd.read_csv(csvfile_6)


# In[10]:

data=pd.merge(file_1, file_2, on='Client ID', how='left') 
data=pd.merge(data, file_3, on='Client ID', how='left')
data=pd.merge(data, file_4, on='Client ID', how='left')
data=pd.merge(data, file_5, on='Client ID', how='left')
data=pd.merge(data, file_6, on='Client ID', how='left')

data.to_csv("../data/combined.csv")

#data[:3]


# In[ ]:



