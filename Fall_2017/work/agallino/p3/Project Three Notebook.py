
# coding: utf-8

# # Project Three Notebook 
# 
# 
# 
# ## Process
# 
# Data Wrangling - For my project I used the Bureau of Labor Statistics and Immigration and Customs Enforcement (ICE) data. For the Labor Statistics I used the Consumer Price Index (CPI) from 1913 to 2013. Generally, the CPI is the costs of certain goods and services--often called a basket of goods--in an economy. When comparing the CPI from year to year for region to region, one can get an idea of inflation. Inflation is the rise in how much things cost from year to year. My data was the average of each year, averaged for the United States. From ICE I used total naturalized citizens each year from 1913 to 2013. Naturalized citizens are individuals who have gone through the process of becoming a citizen. The United States only naturalizes a certain number of individuals each year. The number is the total average for the given year. My target variable was CPI and my feature variable was the total naturalized citizens. 
# 
# Training and Cross Validation - I trained my data on 80% of the data. I used a holdout data of 20%. The training data suggested a very high correlation between naturalized citizens and an increase in CPI over time. (See Output 10). When I cross validated that with my hold out data the results were consistent. (See Output 11). My holdout data suggested an 86% accuracy with a correlation of .925. That suggests there is a correlation between the two variables and my feature variable was an accurate predictor of CPI 86% of the time. 
# 
# However, some potential for error along the way is that I averaged a lot of CPI data and over time it was averaged some nuance is lost along the way. Also, there is probably a lag between when citizens are naturalized and when CPI is increased. I am not entirely sure of the process for naturalization, but I believe that many who are naturalized have spent some time living in the United States before becoming naturalized. In either case, there most likely is a lag between naturalization and CPI. In future analysis I could one year off the naturalized variable with the CPI variable to see if the accuracy rate increases. In other words, if I use 1913 naturalized data to predict 1914 CPI, I might get a more accurate model. Further, naturalized citizens is one variable of many that could affect the CPI. For this to be a more accurate model, I would need to include other variables as well. Such variables could be if Congress increased government spending. If the President was Republican or Democrat. If taxes were raised that year. Was the economy in a boom or bust cycle? Many other variables could be used to more accurately predict CPI.
# 
# Working Model - As you can see in output 10 and 11 my data provides a working model to predict an increase in CPI given the variables used. While this may not be ready for real world application without adding some additional feature variables, the with an 86% accuracy rate and a .925 correlation suggests I am on to something. This could be a valuable tool to congress who sets the number of individuals who can be naturalized in a given year. This could be a powerful tool for law makers to control inflation. For example, if we are experiencing an increase in inflation beyond acceptable levels, they can reduce the number of individuals naturalized. Or, Congress can increase the number naturalized to stimulate the economy. Overall, predicting CPI accurately can be a valuable tool in making a more stable economy for the United States. 
# 
# 
# 
# 
# ## Load Some Stuff
# 
# This is where we load libraires and the like so we can do what we need. If you get an error saying a module is not loaded, open a new terminal/cmd line and try running: `pip install [module name]`. 

# In[1]:

import os
try:
    inputFunc = raw_input
except NameError:
    inputFunc = input

import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
import numpy as np
 
import seaborn as sns
from statsmodels.formula.api import ols

from sklearn import linear_model
from sklearn import metrics

from sklearn.linear_model import LogisticRegression
from patsy import dmatrices

import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt

import random



# Custom functions

def evaluate(pred, labels_test):
    acc = accuracy_score(pred, labels_test)
    print ("Accuracey: %s"%acc)
    tn, fp, fn, tp = confusion_matrix(labels_test, pred).ravel()

    recall = tp / (tp + fp)
    percision = tp / (tp + fn)
    f1 = (2 / ((1/recall)+(1/percision)))

    print ("")
    print ("True Negatives: %s"%tn)
    print ("False Positives: %s"%fp)
    print ("False Negatives: %s"%fn)
    print ("True Positives: %s"%tp)
    print ("Recall: %s"%recall)
    print ("Precision: %s"%percision)
    print ("F1 Score: %s"%f1)

def plot_bound(Z_val,data,col1,col2,binary):
    # Z-val equals "Yes" value. E.g., "Y" or "1". 
    # data equals df
    # col1 and col2 defines which colums to use from data
    # Plot binary decision boundary. 
    # For this, we will assign a color to each
    # point in the mesh [x_min, m_max]x[y_min, y_max].
    
    x_min = float(data.iloc[:,[col1]].min())-float(data.iloc[:,[col1]].min())*0.10 
    x_max = float(data.iloc[:,[col1]].max()+float(data.iloc[:,[col1]].min())*0.10)
    y_min = 0.0; 
    y_max = float(training.iloc[:,[col2]].max())+float(training.iloc[:,[col2]].max())*0.10
    h_x = (x_max-x_min)/100  # step size in the mesh
    h_y = (y_max-y_min)/100  # step size in the mesh
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h_x), np.arange(y_min, y_max, h_y))
    if binary == 1:
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])   
        Z = np.where(Z=="Y",1,0)
    else:
        Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.pcolormesh(xx, yy, Z)
    plt.show()


# ## Data Cleaning
# 
# Here we load the data we collected and get it all ready to feed to our statistical model(s). That is, we are trying to make a table with one **target** column and one or more **features**. Here I'm loading happiness.csv from: https://data.somervillema.gov/Happiness/Somerville-Happiness-Survey-responses-2011-2013-20/w898-3dfm Note: you can find information on the data elements at this link. 
# 

# In[2]:

# Load and peek at your data. Change the file name as needed. 
raw_data_df = pd.read_csv('data.csv') 
raw_data_df.head()


# In[3]:

# You can explore unique entires by stating the column and using .unique() like this:
print(raw_data_df["Year"].unique())
print(raw_data_df["CPI"].unique())


# In[4]:

processed_data_df = raw_data_df


# In[5]:

# I'm now going to make a set of tables to be used in training some models
# The first set will be for linear regressions where the traget is numeric.
# Happiness
data_lin_df = processed_data_df[[
                               'Year', 
                               'CPI', 
                               'Naturalized'
                               ]].copy()
data_lin_df.head()


# In[6]:

processed_data_df.head()


# ## Taining and Validation
# 
# Above I created four datasets worth exploring: 
# - **`happy_lin_df`**. The data needed to access *happiness* along a continuous variable.
# - **`sat_lin_df`**. The data needed to access *satisfaction* along a continuous variable.
# - **`happy_class_df`**. The data needed to access *happiness* as a categorical variable.
# - **`sat_class_df`**. The data needed to access *satisfaction* as a categorical variable.
# 
# Let's take them each in turn. 

# In[7]:

# To make sure all of your columns are stored as numbers, use the pd.to_numeric method like so.
processed_data_df = processed_data_df.apply(pd.to_numeric, errors='coerce')
# errors='coerce' will set things that can't be converted to numbers to NaN
# so you'll want to drop these like so.
processed_data_df = processed_data_df.dropna()
processed_data_df.head()


# ## happy_lin_df
# 
# 

# In[8]:

data = data_lin_df

data_lin_df

holdout = data.sample(frac=0.20)
training = data.loc[~data.index.isin(holdout.index)]


# In[9]:

sns.lmplot(x="Naturalized", y="CPI", data=training, x_estimator=np.mean, order=1)


# In[10]:

model = ols("CPI ~ Year + Naturalized", training).fit()
#model = ols("happy ~ age + income + np.power(age, 2) + np.power(income, 2)", training).fit()
model.summary()


# In[11]:

# Rerun with SciKitLearn because it's easy to check accuracy
features_train = training.drop("CPI", axis=1).as_matrix(columns=None)
labels_train = training["CPI"].as_matrix(columns=None)

features_test = holdout.drop("CPI", axis=1).as_matrix(columns=None)
labels_test = holdout["CPI"].as_matrix(columns=None)

lm = linear_model.LinearRegression()
clf = lm.fit(features_train, labels_train)
pred = clf.predict(features_test)
accuracy = metrics.r2_score(labels_test, pred)
print("R squared:",lm.score(features_train,labels_train))
print("Accuracy:",accuracy)


# In[ ]:



