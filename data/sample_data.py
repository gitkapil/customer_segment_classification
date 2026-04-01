"""
Create sample data for testing the pipeline
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate realistic product descriptions with good variety
product_adjectives = ['Pink', 'Blue', 'Green', 'Red', 'White', 'Black', 'Silver', 'Gold', 'Large', 'Small', 'Vintage']
product_nouns = ['Candle', 'Frame', 'Mug', 'Pillow', 'Lamp', 'Vase', 'Box', 'Card', 'Cup', 'Plate', 'Cushion', 'Decoration', 'Wall Art', 'Tea Set', 'Plant Pot']
product_descriptors = ['Ceramic', 'Metal', 'Wooden', 'Glass', 'Fabric', 'Paper', 'Plastic']

# Create ~500 unique product descriptions
unique_products = []
for adj in product_adjectives:
    for noun in product_nouns:
        desc = np.random.choice(product_descriptors)
        unique_products.append(f"{adj} {desc} {noun}")

unique_products = list(set(unique_products))[:500]  # Get ~500 unique products

countries = ['UK', 'Netherlands', 'France', 'Germany', 'Sweden', 'Australia', 'USA', 'Japan']

# Generate sample data
n_records = 5000
dates = [datetime(2010, 12, 1) + timedelta(days=int(x)) for x in np.random.randint(0, 365, n_records)]

data = {
    'InvoiceNo': [f'536{i:06d}' for i in range(n_records)],
    'StockCode': [f'{np.random.randint(10000, 99999)}' for _ in range(n_records)],
    'Description': [np.random.choice(unique_products) for _ in range(n_records)],
    'Quantity': np.random.randint(1, 20, n_records),
    'InvoiceDate': dates,
    'UnitPrice': np.random.uniform(1, 100, n_records),
    'CustomerID': [str(12000 + np.random.randint(0, 500)) for _ in range(n_records)],
    'Country': [np.random.choice(countries) for _ in range(n_records)]
}

df = pd.DataFrame(data)
df.to_csv('data.csv', index=False)
print(f"Created sample data with {len(df)} records")
print(f"Unique products: {len(unique_products)}")
print(df.head())
