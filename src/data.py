import pandas as pd

# Read CSV file 
#df = pd.read_csv('data/processed/processed_data.csv')
df = pd.read_parquet('data/processed/processed_data.parquet')

# Ensure 'InvoiceDate' is converted to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create Month-Year column
#df['MonthYear'] = df['InvoiceDate'].dt.strftime('%b-%Y')