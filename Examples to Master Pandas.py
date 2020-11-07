# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 11:07:10 2020

@author: shubhs
"""

# 30 Examples to Master Pandas
# A comprehensive practical guide for learning Pandas

import os
os.chdir('C:/Users/s-s.kumar/Desktop/Personal/KaggleRequirements/Project')
os.listdir()

# reading the csv file into a pandas dataframe

import pandas as pd

df = pd.read_csv('Churn_Modelling.csv')
df.head()
df.shape
# Out[7]: (10000, 14)

df.columns
# Index(['RowNumber', 'CustomerId', 'Surname', 'CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance', 
#         'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 'Exited'],dtype='object')

# 1. Dropping columns

# The drop function is used to drop columns and rows.
# The axis parameter is set as 1 to drop columns and 0 for rows. 
# The inplace parameter is set as True to save the changes.

df.drop(['RowNumber', 'CustomerId', 'Surname', 'CreditScore'],axis=1,inplace=True)
df.shape
# Out[10]: (10000, 10)

# 2. Select particular columns while reading

# read only some of the columns from the csv file. 
# The list of columns is passed to the usecols parameter while reading. 

df_spec = pd.read_csv('Churn_Modelling.csv', usecols=['Gender', 'Age', 'Tenure', 'Balance'])
df_spec


# 3. Reading a part of the dataframe

df_partial = pd.read_csv('Churn_Modelling.csv', nrows=5000)
df_partial.shape


# The read_csv function allows reading a part of the dataframe in terms of the rows.
# Two options available are nrows and skiprows
# Using the nrows parameters, we created a dataframe that contains the first 5000 rows of the csv file.
# To select rows from the end of the file by using the skiprows parameter. 
# Skiprows=5000 means that we will skip the first 5000 rows while reading the csv file.

# 4. Sample

# After creating a dataframe, we may want to draw a small sample to work. 
# We can either use the n parameter or frac parameter to determine the sample size.
#    n: The number of rows in the sample
#    frac: The ratio of the sample size to the whole dataframe size

df_sample = df.sample(n=1500)
df_sample.shape
# Out[13]: (1500, 10)

df_sample2 = df.sample(frac=0.2)
df_sample2.shape
# Out[14]: (2000, 10)

# 5. Checking the missing values

# The isna or isnull function determines the missing values in a dataframe

df.isnull().sum()
df.isna().sum()

# 6. Adding missing values using loc and iloc

import numpy as np
# loc: selects with label
# iloc: selects with index

missing_index = np.random.randint(10000, size=20)

# We will use these indices to change some values as np.nan (missing value).

df.loc[missing_index, ['Balance','Geography']] = np.nan

df.iloc[missing_index, -1] = np.nan

df.isnull().sum()

# 7. Filling missing values

# The fillna function is used to fill the missing values. 
# We can use a specific value, an aggregate function (e.g. mean), or the previous or next value.

# Example by filling missing values with mode
df['Geography'].value_counts()

mode = df['Geography'].value_counts().index[0]
df['Geography'].fillna(value=mode, inplace=True)

# Example by filling missing values with mean
avg = df['Balance'].mean()
df['Balance'].fillna(value=avg, inplace = True)

# 8. Dropping missing values

# way to handle missing values is to drop them

df.dropna(axis=0, how='any', inplace=True)

# The axis=1 is used to drop columns with missing values. 
# We can also set a threshold value for the number of non-missing values required for a column or row to have. 
# For instance, thresh=5 means that a row must have at least 5 non-missing values not to be dropped. 
# The rows that have 4 or fewer missing values will be dropped.

# 9. Selecting rows based on conditions

# In some cases, we need the observations (i.e. rows) that fit some conditions. 

france_churn = df[(df.Geography == 'France') & (df.Exited == 1)]
france_churn.Geography.value_counts()

# 10. Describing the conditions with query

df2 = df.query('80000 < Balance < 100000')

# Let’s confirm the result by plotting a histogram of the balance column.

df2['Balance'].plot(kind='hist', figsize=(8,5))

# 11. Describing the conditions with isin

# it is better to use the isin method instead of separately writing the values.

df[df['Tenure'].isin([4,6,8,9])][:3]

df[df['Age'].isin([29,35,42])][:50]

# 12. The groupby function

# The code below will group the rows based on the geography-gender combinations and 
# then give us the average churn rate for each group.

df[['Geography','Gender','Exited']].groupby(['Geography','Gender']).mean()


# 13. Applying multiple aggregate functions with groupby

# The agg function allows applying multiple aggregate functions on the groups. 
# A list of the functions is passed as an argument.

df[['Geography','Gender','Exited']].groupby(['Geography','Gender']).agg(['mean','count', 'sum','min','max'])


# 14. Applying different aggregate functions to different groups

# We do not have to apply the same function to all columns. 
# For instance, we may want to see the average balance and the total number of churned customers in each country.
# We will pass a dictionary that indicates which functions are to be applied to which columns.

df_summary = df[['Geography','Exited','Balance']].groupby('Geography').agg({'Exited':'sum', 'Balance':'mean'})
df_summary.rename(columns={'Exited':'# of churned customers', 'Balance':'Average Balance of Customers'},inplace=True)
df_summary

# Alternative

# The NamedAgg function allows renaming the columns in the aggregation. The syntax is as follows:

df_summary_1 = df[['Geography','Exited','Balance']].groupby('Geography').agg(Number_of_churned_customers = pd.NamedAgg('Exited','sum'),
                                                                             Average_balance_of_customers = pd.NamedAgg('Balance','mean'))



# 15. Reset the index

# The index of the dataframes that the groupby returns consist of the group names. We can change it by resetting the index.

df_new = df[['Geography','Exited','Balance']].groupby(['Geography','Exited']).mean().reset_index()
df_new


# 16. Reset the index with a drop

# In some cases, we need to reset the index and get rid of the original index at the same time. 
# Consider a case where draw a sample from a dataframe. The sample will keep the index of the 
# original dataframe so we want to reset it.


df[['Geography','Exited','Balance']].sample(n=6).reset_index()

# The index is reset but the original is kept as a new column. We can drop it while resetting the index.

df[['Geography','Exited','Balance']].sample(n=6).reset_index(drop=True)


# 17. Set a particular column as the index

# We can set any column in the dataframe as the index.

df_new.set_index('Geography')


# 18. Inserting a new column

#We can add a new column to a dataframe as follows:

import numpy as np
group = np.random.randint(10, size=6)
df_new['Group'] = group
df_new

# If you want to put the new column at a specific position, you can use the insert function.

series = np.random.randint(10, size=6)
df_new.insert(0, 'Serial', series)
df_new

df_new.drop(['Group'], axis=1, inplace=True)
df_new

# 19. The where function

# It is used to replace values in rows or columns based on a condition. 
# The default replacement value is NaN but we can also specify the value to be put as a replacement.

df_new['Balance'] = df_new['Balance'].where(df_new['Group'] >= 4, 0)
df_new

# The values that fit the specified condition remain unchanged and the other values are replaced with the specified value.

# 20. The rank function

# It assigns a rank to the values. Let’s create a column that ranks the customers according to their balances.

df_new['rank'] = df_new['Balance'].rank(method='first', ascending=False).astype('int')
df_new

# 21. Number of unique values in a column

# It comes in handy when working with categorical variables. We may need to check the number of unique categories.
# We can either check the size of the series returned by the value counts function or use the nunique function

df.Geography.unique()
df.Geography.value_counts().size
df.Geography.nunique()

# 22. Memory usage

# It is simply done by the memory_usage function. The values show how much memory is used in bytes.

df.memory_usage()


# 23. The category data type

# By default, categorical data is stored with the object data type. 
# However, it may cause unnecessary memory usage especially when the categorical variable has low cardinality.

# Low cardinality means that a column has very few unique values compared to the number of rows. 
# For instance, the geography column has 3 unique values and 10000 rows.

# We can save memory by changing its data type as “category”.

df['Geography'] = df['Geography'].astype('category')
df.memory_usage()

# 24. Replacing values

# The replace function can be used to replace values in a dataframe.

df_new['Group'].replace(5, '81')

# We can use a dictionary to do multiple replacements.

df_new['Group'].replace({6:'82',8:'23'})

# 25. Drawing a histogram

# Pandas is not a data visualization library but it makes it pretty simple to create basic plots.

df['Balance'].plot(kind='hist', figsize=(10,6), title='Customer Balance')


# 26. Reducing the decimal points of floats

# Pandas may display an excessive amount of decimal points for floats. We can easily adjust it using the round function.

df_new.round(1) #number of desired decimal points

# 27. Changing the display options

# Instead of adjusting the display options manually at each time, we can change the default display options
# for various parameters.

# get_option: Returns what the current option is
# set_option: Changes the option
# max_colwidth: Maximum number of characters displayed in columns
# max_columns: Maximum number of columns to display
# max_rows: Maximum number of rows to display

pd.set_option("display.precision", 2)
df_new

# 28. Calculating the percentage change through a column

# The pct_change is used to calculate the percent change through the values in a series. 
# It is useful when calculating the percentage of change in a time series or sequential array of elements

ser = pd.Series([4,5,2,6,5,10,12])
ser.pct_change()

# 29. Filtering based on strings

# We may need to filter observations (rows) based on textual data such as the name of customers.

df_new['Name'] = ['Ram','Mike','John','Michael','Rose','Rajesh']
df_new

# Select the rows in which the customer name starts with ‘Mi’.
# We will use the startswith method of the str accessor.

df_new[df_new.Name.str.startswith('Mi')]

# The endswith function does the same filtering based on the characters at the end of strings.

# 30. Styling a dataframe

# We can achieve this by using the Style property which returns a styler object.
# It provides many options for formatting and displaying dataframes. 

# For instance, we can highlight the minimum or maximum values.
# It also allows for applying custom styling functions.

df_new.style.highlight_max(axis=0, color='darkgreen')


# Courtesy: Towardsdatascience.com article by Soner Yildirim

