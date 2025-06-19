# import necessary libraries 
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
from scipy.stats import pearsonr 
from scipy.stats import chi2_contingency

# load the dataset 
xlsx_path = 'Data/정성희.xlsx'
df_his = pd.read_excel(xlsx_path, sheet_name='HISTORY', skiprows=8)
df_val = pd.read_excel(xlsx_path, sheet_name = 'VALUE', skiprows=8)

# clean REGDATE into python datatime format 
df_his['REGDATE'] = pd.to_datetime(df_his['REGDATE'], errors='coerce')
df_val['TIME'] = pd.to_datetime(df_val['TIME'], errors='coerce')

# # display the first few rows of the dataset 
# print(df_his.head())
# print(df_val.head())

# earson correlation 
df_his['hour'] = df_his['REGDATE'].dt.hour # extract hour from REGDATE]

df_corr = df_his[['hour', 'KIND']].dropna() # drop rows with NaN values in 'hour' or 'KIND'

corr, p = pearsonr(df_corr['hour'], df_corr['KIND']) # calculate pearson correlation 
print(f"Pearson correlation between hour and KIND: \n{corr}, p-value: {p}")

# chi=squared test based on time of day 
df_his['time_of_day'] = pd.cut(df_his['hour'], bins=[0,6,12,18,24], labels=['Night', 'Morning', 'Afternoon', 'Evening']) # segment hours into time of day categories 

# create a crosstab and diaplay the results 
table = pd.crosstab(df_his['time_of_day'], df_his['KIND']) 
print(f"Contingency table: \n{table}")

# using crosstab to perform chi-squared test 
chi2, p, dof, expected = chi2_contingency(table)
print(f"Chi-square test: \nχ² = {chi2:.2f}, p = {p:.4f}")

# visualize the crosstable results 
grouped = df_his.groupby(['time_of_day','KIND']).size().unstack(fill_value=0)
grouped.plot(kind='bar', figsize=(12, 6), width=0.8)
plt.title("Bar plot of KIND by time of day")
plt.xlabel("Time of Day")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.legend(title='KIND', labels=['Pee', 'Poop'])
plt.tight_layout()
plt.show()