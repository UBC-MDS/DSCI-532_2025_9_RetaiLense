import pandas as pd

# Read parquet file 
df = pd.read_parquet('data/processed/processed_data.parquet')

# Ensure 'InvoiceDate' is converted to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
