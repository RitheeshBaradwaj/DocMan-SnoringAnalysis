#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import statsmodels.formula.api as smf
import statsmodels.api as sm
import pylab
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# In[2]:


snore = pd.read_csv("C:\\Users\\kumar\\snore12.csv")


# In[6]:


snore


# In[7]:


x = snore.iloc[:, :-1].values  ## independent variables
y=snore.iloc[:,10] ## dpendent variables


# #  exploratory data analysis

# In[8]:


# 1st business moment decision---central tendency
snore.mean()


# In[9]:


snore.median()


# In[10]:


snore.describe()


# In[11]:


# # 2-->Variance,Standard Deviation and Range:

# In[226]:


print("Variances:")
print("-------------------------------")
print(np.var(snore))
print("\nStandard Deviation:")
print("-------------------------------")
print(np.std(snore))


# In[9]:


""" we know data of any distribution lies between mean+sd and mean-sd
we can analyse where most data is distributed using variance and mean
"""


# In[10]:


snore.columns


# ####  3rd business movement decision skewness

# In[12]:


for c in snore.columns:
    if c == "name" or c=="sno" or c=='sex':
        continue
    else:
        print(c+":    "+ str(stats.skew(snore[c])))


# In[12]:


"""we obseve thatskwness is +ve mean>median
"""


# ####  4th business movement decison --- kurtosis

# In[13]:


for c in snore.columns:
    if c == "name" or c=="sno" or c=='sex':
        continue
    else:
        print(c+":    "+ str(stats.kurtosis(snore[c])))


# In[15]:


""" kutosis is less than 3 ,so less outliers,less standard deviation ,data set is perfect or 
we can consider this daata set"""


# In[14]:


### distributions based on sex


# In[13]:


for c in snore.columns:
    if c == "name" or c=="sno" or c=='sex':
        continue
    else:
        sns.FacetGrid(snore,hue="sex",height=5).map(sns.distplot,c).add_legend()
        plt.show()


# #####  BOX PLOTS TO SHOW OUTLIERS AS IT IS CONTINOUS DATA

# In[14]:


for c in snore.columns:
    if c == "name" or c=='sno ' or c=='sex':
        continue
    else:
        plt.boxplot(snore[c])
        plt.xlabel(c)
        plt.show()


# #### TO SHOW RELATION BETWEEN INDEPENDET VARIABLES

# In[18]:


sns.pairplot(snore.iloc[:,:-1])


# In[19]:


# all are not uniformly distributed ,may contain some outliers


# ##### as inputs from domain expert ahi value only depends on apneas count,hypoapneas count,ah total count and sleep time
# 

# ###  ahi value does not depend on name,sex so building model removing those

# In[156]:


snore.columns


# ## regression model 

# In[157]:


snore


# In[165]:


model=smf.ols('ahi~bmi+totalsleeptime+ahtotalcount+apneascount+hypopneascount+apneasindex+hypopnnore).easindex',data=sfit()


# In[166]:


model.params


# In[167]:


model.summary()


# In[16]:


### model.confint(0.05)


# In[20]:


### apneas index and hypopneas index became less significant
### so lets construct the model ignoring this and check others significance


# In[21]:


model1=smf.ols('ahi~totalsleeptime+apneascount+hypopneascount+bmi',data=snore).fit()


# In[22]:


model1.params


# In[23]:


model1.summary()


# In[24]:


model2=smf.ols('ahi~apneasindex+hypopneasindex+bmi+totalsleeptime',data=snore).fit()


# In[25]:


model2.summary()


# 

# In[26]:


sm.graphics.influence_plot(model1,criterion="cooks")
plt.plot()


# In[30]:


from statsmodels.formula.api import ols
m=ols('ahi~bmi+totalsleeptime+apneascount+hypopneascount+apneasindex+hypopneasindex',data=snore).fit()
infl=m.get_influence()
sm_fr=infl.summary_frame()


# In[31]:


sm_fr


# ### cooks_d values are less. .. there are no influential points

# In[35]:


### so apneas index and hypopneas index can be removed as they tend to overfit the model and have less significace


# ###  vif values are also high and removing those attributes

# In[34]:


## so our final model contains only bmi,apneascount,hypopneascount,totalsleeptime


# In[ ]:


# lets remove bmi and check  adjusted r-squared


# In[36]:


model3=smf.ols('ahi~apneascount+hypopneascount+totalsleeptime',data=snore).fit()


# In[37]:


model3.summary()


# In[38]:


### adjusted r squared for the model cotaining bmi,apneascount and hypopneas count is 0.907


# In[39]:


# including bmi


# In[40]:


model4=smf.ols('ahi~bmi+apneascount+hypopneascount+totalsleeptime',data=snore).fit()


# In[41]:


model4.summary()


# In[46]:


bmi_new=new_snore['bmi']
apneascount_new=new_snore['apneascount']
hypopneascount_new=new_snore['hypopneascount']
totalsleeptime_new=new_snore['totalsleeptime']
ahi_new=new_snore['ahi']


# In[47]:


model4=smf.ols('ahi_new~bmi_new+apneascount_new+hypopneascount_new+totalsleeptime_new',data=new_snore).fit()


# In[48]:


model4.summary()


# In[49]:


### after removing influential points bmi became signifiacnt 


# In[50]:


### final dtaset ----new_snore


# In[51]:


model_final=smf.ols('ahi_new~bmi_new+apneascount_new+hypopneascount_new+totalsleeptime_new',data=new_snore).fit()


# In[53]:


model_final.summary()


# #### multicollinearity is not exist in our final model

# In[59]:


model_final_pred=model_final.predict(new_snore)


# In[60]:


model_final_pred


# In[79]:


x=new_snore.iloc[:,3:9].values


# In[80]:


y=new_snore.iloc[:,10].values


# In[81]:


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=0)


# In[82]:


new_snore.columns


# In[83]:


new_snore
type(new_snore)


# In[93]:


from sklearn.linear_model import LinearRegression
regressor=LinearRegression()
regressor.fit(x_train,y_train)
accuracy=regressor.score(x_test,y_test)
print((accuracy*100))


# In[94]:


print("final model accuracy is 94.3%")


# In[ ]:




