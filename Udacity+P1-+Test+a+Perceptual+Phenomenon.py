
# coding: utf-8

# # Udacity P1

# # Background Info

# In a Stroop task, participants are presented with a list of words, with each word displayed in a color of ink. The participant’s task is to say out loud the color of the ink in which the word is printed. The task has two conditions: a congruent words condition, and an incongruent words condition. In the congruent words condition, the words being displayed are color words whose names match the colors in which they are printed: for example RED, BLUE. In the incongruent words condition, the words displayed are color words whose names do not match the colors in which they are printed: for example PURPLE, ORANGE. In each case, we measure the time it takes to name the ink colors in equally-sized lists. Each participant will go through and record a time from each condition.

# # Questions for Investigation

# As a general note, be sure to keep a record of any resources that you use or refer to in the creation of your project. You will need to report your sources as part of the project submission.
# 1. What is our independent variable? What is our dependent variable?
# 2. What is an appropriate set of hypotheses for this task? What kind of statistical test do you expect to perform? Justify your choices.
# Now it’s your chance to try out the Stroop task for yourself. Go to this link, which has a Java-based applet for performing the Stroop task. Record the times that you received on the task (you do not need to submit your times to the site.) Now, download this dataset which contains results from a number of participants in the task. Each row of the dataset contains the performance for one participant, with the first number their results on the congruent task and the second number their performance on the incongruent task.
# 3. Report some descriptive statistics regarding this dataset. Include at least one measure of central tendency and at least one measure of variability.
# 4. Provide one or two visualizations that show the distribution of the sample data. Write one or two sentences noting what you observe about the plot or plots.
# 5. Now, perform the statistical test and report your results. What is your confidence level and your critical statistic value? Do you reject the null hypothesis or fail to reject it? Come to a conclusion in terms of the experiment task. Did the results match up with your expectations?
# 6. Optional: What do you think is responsible for the effects observed? Can you think of an alternative or similar task that would result in a similar effect? Some research about the problem will be helpful for thinking about these two questions!

# # answer 1

# independent variable: task congruence/incongruence
#     
# dependent variable: task performance

# # answer 2

# null hypothesis:  there is no effective difference between congruent and incongruent task performance.
# 
# H0 =  μc - μi = 0 ... mu sub c ('c' for 'Congruent') is not different from mu sub i ('i' for 'Incongruent')
#       
#     In this formula, mu sub 'c' and 'i' represent the population means of congruent and incongruent task performance, respectively.
# 
# alternative hypothesis:  although it's acceptable to propose that congruent and incongruent task performance are effectively different, it's more sensible to assume directionality and propose that congruent task performance is lesser (in terms of seconds) than incongruent task performance.  The replication of this effect across many psychological studies lends support to this choice.   
# 
# HA = μc < μi ... mu sub c  is less than mu sub i 
# 
#     In this formula, mu sub 'c' and 'i' represent the population means of congruent and incongruent task performance, respectively.
# 
# 
# I will perform a dependent (paired), negative one-tailed t test for the following reasons:
# 
#     The congruent/incongruent performances are paired measurements for one set of subjects, and I will be testing whether the mean of the differences between the paired measurements is equal to 0.
#     
#     I expect the t-statistic to be on the negative side.  
#     
#     We have less than 30 samples and the sampling distribution does not approximate a perfectly normal distribution, though we assume it would if the sample size increases > 30...t tests are used to handle lower sample sizes, z tests are not.
#     
#     We don't know the population std, and therefore need to account for the extra error in using the sample std.
#     
# 
# my performance: congruent: 9.777 seconds --- incongruent: 28.291 seconds

# In[586]:

import csv as csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline


# In[587]:

#practicing with csv module for the sake of exercise
with open('stroopdatacopy.csv','w') as f_out:
    out_cols = ['Congruent','Incongruent']
    fi_writer = csv.DictWriter(f_out,fieldnames = out_cols)
    fi_writer.writeheader()
    with open('stroopdata.csv','r') as f_in:    
        fi_reader = csv.DictReader(f_in)
        for datarow in fi_reader:
            fi_writer.writerow(datarow)
dfs = pd.read_csv('stroopdatacopy.csv')
dfs.head()


# In[578]:

dfs.shape


# # answer 3

# In[93]:

dfs.describe()
#despite seeing measurements of central tendency conveniently this way...
#I will select individual measurments for the sake of exercise.


# In[361]:

np.mean(dfs)
#as expected, incongruent measurements have a higher average.


# In[86]:

np.median(dfs['Congruent'])


# In[85]:

np.median(dfs['Incongruent'])


# In[362]:

np.std(dfs)
#the incongruent measurements have a higher level of variance.  
#it appears as though differences between individual ability are more pronounced in the incongruent measurements.
#strange that numpy's .std() returns a different value than pandas .describe()


# In[89]:

np.std(dfs,ddof=1)
#I found information regarding this difference and used code from the below forum to align numpy with pandas:
#http://stackoverflow.com/questions/24984178/different-std-in-pandas-vs-numpy


# # answer 4

# In[462]:

sns.set_style('white')
plt.figure()
dfs.plot(kind='hist', alpha=0.8,bins=15,edgecolor='black')
plt.xlim(dfs['Congruent'].min(),dfs['Incongruent'].max())
plt.xlabel('Seconds')
plt.show()


# In[580]:

sns.distplot(dfs['Congruent'])
#because it's hard to tell whether or not the congruent measurements have a normal or right skewed distribution from this plot
#I'm generating another plot with default bin widths and kernel density estimator line.


# The congruent measurements have an approximate normal distribution, and the incongruent measurements have a right skew distribution.  The majority of congruent users are clustered around 14 seconds, and the majority of incongruent users are clustered around 21 seconds.  These visualizations dovetail nicely with the measurements of central tendency.

# # answer 5

# In[565]:

c = dfs.loc[:,'Congruent']
i = dfs.loc[:,'Incongruent']
d = c - i


# In[585]:

dm = np.mean(d) 
dstd = np.std(d,ddof=1)
l = len(d)
se = dstd/np.sqrt(l)
t = dm / se #here is our t-statistic
t


# In[568]:

cv = -1.714 #critical value


# In[571]:

ci1 = dm - cv*se #upper bound CI
ci1 


# In[572]:

ci2 = dm + cv*se #lower bound CI
ci2 


# Results:
# 
# With 23 degrees of freedom and a 0.05% significance level, the critical value is -1.714. 
# 
# Our t-statistic is well within the rejection region, and its p value is < 0.0001.  I used the below calculator for the p-value:
# http://www.graphpad.com/quickcalcs/pValue2/
# 
# The confidence interval is (-9.67,-6.26), meaning the population parameter is likely to fall within this range of values.
# 
# I reject the null hypothesis, and accept the alternative hypothesis:
# 
#     Congruent task performance is significantly less (in terms of seconds) than incongruent task performance.
# 
# This result matched up with my expectations.
# 

# # answer 6

# I think our brain's way of evaluating information is responsible.  It might be easier to evaluate words than interpret color, so prompting the brain to simultaneously process words and colors will result in greater performance time.  
# 
# A similar task might be using non-color words instead of color words.  If subjects aren't distracted by a meaningful relationship between the words and colors, perhaps they would be able to interpret the color faster.   
# 
# Stroop effect research:
# 
# https://faculty.washington.edu/chudler/words.html
# 
# https://www.verywell.com/what-is-the-stroop-effect-2795832

# In[ ]:



