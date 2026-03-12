import pandas as pd
df = pd.read_csv('customer_shopping_behavior.csv')
#print(df.head())
#print(df.info())
#print(df.describe())
#print(df.isnull().sum())
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
#print(df.isnull().sum())
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
#print(df.columns)
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})
#print(df.columns)
      #Create a column
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4,labels = labels)
#print(df[['age', 'age_group']].head(10))
# Purchase_frequency_days column creation

frequency_mapping ={
    'Daily' : 1,
    'Weekly' : 7,
    'Bi-Weekly' : 14,
    'Fortnightly' : 14,
    'Monthly' : 30,
    'Every 3 Months' : 90,
    'Quarterly' : 90,
    'Annually' : 365
}
df['Purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
print(df[['Purchase_frequency_days', 'frequency_of_purchases']].head(10))
print(df[['discount_applied', 'promo_code_used']].head(10))
print((df['discount_applied'] == df['promo_code_used']).all())
df = df.drop('promo_code_used', axis=1)
print(df.columns)
