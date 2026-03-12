import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# ============================================
# STEP 1: READ CSV
# ============================================
df = pd.read_csv('customer_shopping_behavior.csv')

# ============================================
# STEP 2: DATA CLEANING
# ============================================

# Fill missing review ratings with median
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(
    lambda x: x.fillna(x.median())
)

# Clean column names - lowercase and replace spaces
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')

# Rename purchase amount column
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})

# Add age group column
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)

# Add purchase frequency days column
frequency_mapping = {
    'Daily'          : 1,
    'Weekly'         : 7,
    'Bi-Weekly'      : 14,
    'Fortnightly'    : 14,
    'Monthly'        : 30,
    'Every 3 Months' : 90,
    'Quarterly'      : 90,
    'Annually'       : 365
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

# Drop duplicate column
df = df.drop('promo_code_used', axis=1)

# ============================================
# STEP 3: VERIFY CLEANING
# ============================================
print("Cleaned data shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())

# ============================================
# STEP 4: CONNECT TO SQL SERVER
# ============================================
connection_url = URL.create(
    "mssql+pyodbc",
    query={
        "odbc_connect": (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=customer_behavior;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    }
)
engine = create_engine(connection_url)
print("Connection Successful!")

# ============================================
# STEP 5: UPLOAD CLEANED DATA TO SQL SERVER
# ============================================
with engine.begin() as conn:
    df.to_sql('customers', conn, if_exists='replace', index=False)

print("Cleaned data uploaded successfully!")
