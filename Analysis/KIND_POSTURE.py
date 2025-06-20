import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns

# load the dataset
xlsx_path = "Data/박기희.xlsx"
df_his = pd.read_excel(xlsx_path, sheet_name='HISTORY', skiprows=8)

# clean REGDATE into python datetime format
df_his['REGDATE'] = pd.to_datetime(df_his['REGDATE'], errors='coerce')

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

# posture over time plot 
# to visualize the distribution of postures over time
df_his = df_his.sort_values('REGDATE')  # sort by REGDATE

# Set color palette manually
palette = {0: 'blue', 1: 'red'}  # 0 = Pee (blue), 1 = Poop (red)

plt.figure(figsize=(14, 6))
sns.scatterplot(data=df_his, x='REGDATE', y='POSTURE', hue='KIND', palette=palette, alpha=0.7)
plt.title('Posture Over Time (Colored by KIND)')
plt.xlabel('Time')
plt.ylabel('Posture')
plt.xticks(rotation=30)
plt.grid(True)

# Manually fix legend labels
handles, labels = plt.gca().get_legend_handles_labels()
new_labels = ['Pee (KIND=0)', 'Poop (KIND=1)']
plt.legend(handles=handles, labels=new_labels, title='KIND')

plt.tight_layout()
plt.show()

# transition analysis of postures 
df_his['prev_posture'] = df_his['POSTURE'].shift()
df_transition_poop = df_his[df_his['KIND']==1][['prev_posture', 'POSTURE']]
transition_counts_poop = df_transition_poop.value_counts().reset_index(name='count')
print(transition_counts_poop.head())

df_transition_pee = df_his[df_his['KIND']==0][['prev_posture', 'POSTURE']]
transition_counts_pee = df_transition_pee.value_counts().reset_index(name='count')
print(transition_counts_pee.head())