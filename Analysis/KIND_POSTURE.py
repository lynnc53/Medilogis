import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns

# load the dataset
xlsx_path = "Data/양순희.xlsx"
df_his = pd.read_excel(xlsx_path, sheet_name='HISTORY', skiprows=8)

# table of KIND by posture 
table = pd.crosstab(df_his['POSTURE'], df_his['KIND']).dropna()
print(f"Contingency table: \n{table}")

# bar-graph of KIND by POSTURE 
grouped = df_his.groupby(['POSTURE', 'KIND']).size().unstack(fill_value=0)
grouped.plot(kind='bar', figsize=(12, 6), width=0.8)
plt.title("Bar plot of KIND by POSTURE")
plt.xlabel("Posture")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.legend(title='KIND', labels=['Pee', 'Poop'])
plt.tight_layout()
plt.show()