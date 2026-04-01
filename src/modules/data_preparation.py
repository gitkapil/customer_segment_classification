"""
Data Preparation Module

This module handles the initial data loading, cleaning, and preprocessing.
Tasks:
- Load data from CSV
- Handle missing values
- Remove duplicates
- Process cancellations
- Add calculated fields (TotalPrice, etc.)
"""

import pandas as pd
import numpy as np
from datetime import datetime


class DataPreparation:
    """
    Handles data loading and initial cleaning operations.
    """
    
    def __init__(self, filepath, encoding='ISO-8859-1'):
        """
        Initialize DataPreparation.
        
        Parameters:
        -----------
        filepath : str
            Path to the data CSV file
        encoding : str
            File encoding (default: ISO-8859-1)
        """
        self.filepath = filepath
        self.encoding = encoding
        self.df_initial = None
        self.df_cleaned = None
        
    def load_data(self):
        """Load the raw data from CSV file."""
        self.df_initial = pd.read_csv(
            self.filepath,
            encoding=self.encoding,
            dtype={'CustomerID': str, 'InvoiceID': str}
        )
        self.df_initial['InvoiceDate'] = pd.to_datetime(self.df_initial['InvoiceDate'])
        print(f'Dataframe dimensions: {self.df_initial.shape}')
        return self.df_initial
    
    def remove_null_customers(self):
        """Remove entries without CustomerID (~25% of data)."""
        initial_shape = self.df_initial.shape
        self.df_initial.dropna(axis=0, subset=['CustomerID'], inplace=True)
        print(f'Removed {initial_shape[0] - self.df_initial.shape[0]} rows without CustomerID')
        print(f'New dataframe dimensions: {self.df_initial.shape}')
        
    def remove_duplicates(self):
        """Remove duplicate entries."""
        duplicates = self.df_initial.duplicated().sum()
        self.df_initial.drop_duplicates(inplace=True)
        print(f'Removed {duplicates} duplicate entries')
        
    def process_cancellations(self):
        """
        Handle order cancellations by matching with original orders.
        Creates a QuantityCanceled field and removes cancellation entries.
        """
        self.df_cleaned = self.df_initial.copy(deep=True)
        self.df_cleaned['QuantityCanceled'] = 0
        
        entry_to_remove = []
        doubtfull_entry = []
        
        for index, col in self.df_initial.iterrows():
            if (col['Quantity'] > 0) or col['Description'] == 'Discount':
                continue
                
            df_test = self.df_initial[
                (self.df_initial['CustomerID'] == col['CustomerID']) &
                (self.df_initial['StockCode'] == col['StockCode']) &
                (self.df_initial['InvoiceDate'] < col['InvoiceDate']) &
                (self.df_initial['Quantity'] > 0)
            ].copy()
            
            if df_test.shape[0] == 0:
                doubtfull_entry.append(index)
            elif df_test.shape[0] == 1:
                index_order = df_test.index[0]
                self.df_cleaned.loc[index_order, 'QuantityCanceled'] = -col['Quantity']
                entry_to_remove.append(index)
            elif df_test.shape[0] > 1:
                df_test.sort_index(axis=0, ascending=False, inplace=True)
                for ind, val in df_test.iterrows():
                    if val['Quantity'] < -col['Quantity']:
                        continue
                    self.df_cleaned.loc[ind, 'QuantityCanceled'] = -col['Quantity']
                    entry_to_remove.append(index)
                    break
        
        self.df_cleaned.drop(entry_to_remove, axis=0, inplace=True)
        self.df_cleaned.drop(doubtfull_entry, axis=0, inplace=True)
        print(f'Processed cancellations: removed {len(entry_to_remove) + len(doubtfull_entry)} entries')
        
    def add_total_price(self):
        """Calculate total price for each item."""
        self.df_cleaned['TotalPrice'] = self.df_cleaned['UnitPrice'] * (
            self.df_cleaned['Quantity'] - self.df_cleaned['QuantityCanceled']
        )
        
    def prepare_basket_data(self):
        """
        Aggregate transaction data by customer and invoice.
        Creates basket_price dataframe with aggregated purchase information.
        """
        # Sum purchases per customer & invoice
        temp = self.df_cleaned.groupby(
            by=['CustomerID', 'InvoiceNo'], as_index=False
        )['TotalPrice'].sum()
        basket_price = temp.rename(columns={'TotalPrice': 'Basket Price'})
        
        # Get invoice date
        df_cleaned_copy = self.df_cleaned.copy()
        df_cleaned_copy['InvoiceDate_int'] = df_cleaned_copy['InvoiceDate'].astype('int64')
        temp_date = df_cleaned_copy.groupby(
            by=['CustomerID', 'InvoiceNo'], as_index=False
        )['InvoiceDate_int'].mean()
        basket_price['InvoiceDate'] = pd.to_datetime(temp_date['InvoiceDate_int'])
        
        # Select only positive basket prices
        basket_price = basket_price[basket_price['Basket Price'] > 0]
        
        return basket_price
    
    def get_cleaned_data(self):
        """Return cleaned dataframe."""
        return self.df_cleaned
    
    def execute_pipeline(self):
        """Execute complete data preparation pipeline."""
        self.load_data()
        self.remove_null_customers()
        self.remove_duplicates()
        self.process_cancellations()
        self.add_total_price()
        print('\nData preparation complete!')
        return self.df_cleaned
