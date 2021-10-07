#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
pd.options.display.float_format = '{:.5f}'.format


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
#    ### General Properties

# In[2]:


gun_data = pd.DataFrame(data=pd.read_csv('gun_data.csv'))
census_data = pd.DataFrame(data=pd.read_csv('U.S. Census Data.csv'))


# In[3]:


census_data


# In[4]:


gun_data


# In[5]:


len(gun_data['state'].unique())


# In[6]:


len(census_data.iloc[0]) - 2


# In[7]:


gun_data['state'].unique()


# In[8]:


census_data.iloc[0]


# In[9]:


gun_data.dtypes


# ### Data Cleaning

# In[10]:


gun_data = gun_data.astype({'month': 'datetime64'})


# In[11]:


census_data = census_data.T


# In[12]:


census_data.columns = census_data.iloc[0]


# In[13]:


census_data = census_data.drop('Fact')


# In[14]:


census_data = census_data.drop('Fact Note')


# In[15]:


census_data


# In[16]:


gun_data = gun_data.set_index(gun_data['state'])


# In[17]:


gun_data


# In[18]:


gun_data = gun_data.drop(['District of Columbia', 'Guam', 'Mariana Islands', 'Puerto Rico', 'Virgin Islands'])


# In[19]:


gun_data = gun_data.set_index(gun_data['month'])


# In[20]:


gun_data = gun_data.drop(gun_data.loc['2011-01':].index)


# In[21]:


gun_data = gun_data.drop(gun_data.loc[:'2015-12'].index)


# In[22]:


gun_data = gun_data[['month', 'state', 'permit']]


# In[23]:


gun_data = gun_data.pivot(index='state', columns='month')


# In[24]:


gun_data


# In[25]:


census_data_sample = census_data[['Population estimates, July 1, 2016', 'Population estimates base, April 1, 2010', 'Population, percent change - April 1, 2010 to July 1, 2016', 'Population, Census, April 1, 2010', "Bachelor's degree or higher, percent of persons age 25 years+, 2011-2015", 'Median household income, 2011-2015']]


# In[26]:


census_data_sample = census_data_sample.astype({'Population estimates, July 1, 2016': 'int64', 
                                                'Population estimates base, April 1, 2010': 'int64',
                                                'Population, percent change - April 1, 2010 to July 1, 2016': 'float64', 
                                                'Population, Census, April 1, 2010': 'int64',
                                                "Bachelor's degree or higher, percent of persons age 25 years+, 2011-2015": 'float64',
                                                'Median household income, 2011-2015': 'int64'})


# In[27]:


gun_permits_mean = pd.DataFrame(gun_data.mean(axis=1), columns=['mean permits'])


# In[28]:


gun_permits_mean = gun_permits_mean.join(census_data_sample[["Bachelor's degree or higher, percent of persons age 25 years+, 2011-2015", 
     'Population estimates base, April 1, 2010', 'Population estimates, July 1, 2016', 'Median household income, 2011-2015']])


# In[29]:


gun_permits_mean['permits/pop percentage'] = gun_permits_mean['mean permits'].div(gun_permits_mean[['Population estimates base, April 1, 2010', 
                                                                                                    'Population estimates, July 1, 2016']].mean(axis=1))


# <a id='eda'></a>
# ## Exploratory Data Analysis

# ### What is the correlation between the median household income and the ratio of gun permits to population per state?

# In[30]:


plt.figure(figsize=(15.5,8))
plt.xticks(rotation=-60)
gun_temp = gun_permits_mean.sort_values('Median household income, 2011-2015')
gun_temp['Percent income relative to max income'] = ((gun_temp['Median household income, 2011-2015'])/max(gun_temp['Median household income, 2011-2015']))*100
sns.barplot(x=gun_temp.index, y=(gun_temp['Percent income relative to max income']))


# In[31]:


gun_temp['Median household income, 2011-2015']


# In[32]:


plt.figure(figsize=(15.5,8))
plt.xticks(rotation=-60)
gun_temp = gun_permits_mean.sort_values('mean permits')
gun_temp['Percent permits relative to max permits'] = ((gun_temp['mean permits'])/max(gun_temp['mean permits']))*100
sns.barplot(x=gun_temp.index, y=(gun_temp['Percent permits relative to max permits']))


# In[33]:


gun_temp['mean permits']


# In[34]:


plt.figure(figsize=(15.5,8))
plt.xticks(rotation=-60)
gun_temp = gun_permits_mean.sort_values('permits/pop percentage')
sns.barplot(x=gun_temp.index, y=gun_temp['permits/pop percentage']).set_title('Permits/Pop Percentage by State')


# In[35]:


gun_permits_mean = gun_permits_mean.drop(gun_permits_mean[gun_permits_mean['permits/pop percentage'] > .02].index)
gun_permits_mean = gun_permits_mean.drop(gun_permits_mean[gun_permits_mean['permits/pop percentage'] == 0].index)


# In[36]:


plt.figure(figsize=(15.5,8))
sns.regplot(gun_permits_mean['permits/pop percentage'], gun_permits_mean['Median household income, 2011-2015'])


# In[37]:


gun_permits_mean['permits/pop percentage'].corr(gun_permits_mean['Median household income, 2011-2015'])


# In[38]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




