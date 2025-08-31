import pandas as pd

df = pd.read_csv('datasets/collected_data/Forbes_Global_2000_(2024).csv', encoding='latin1')

# Number of null values in each column
print(df.isnull().sum())

# Display all rows where 'Industry' is null
null_industry_rows = df[df['Industry'].isnull()]
print(null_industry_rows)

# Manually set the 'Industry' field for 2 null values
df.loc[[1276, 1367], 'Industry'] = ['Health Care Equipment & Services', 'Capital Goods']

# Drop the last row to keep the top 2000
df = df.iloc[:-1]  

# Drop the unnecessary columns
df = df.drop(['Founded', 'Headquarters', 'CEO', 'Employees'], axis = 1)

# Save the DataFrame to CSV 
df.to_csv(r"datasets/preprocessed_data/Forbes_Global_2000_(2024)_Preprocessed.csv", index=False)

