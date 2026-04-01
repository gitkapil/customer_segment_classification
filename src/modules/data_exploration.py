"""
Data Exploration Module

This module provides methods to explore and visualize the dataset.
Tasks:
- Analyze countries
- Count customers and products
- Handle cancellations
- Analyze basket prices
- Generate exploratory visualizations
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go


class DataExploration:
    """
    Handles exploratory data analysis of the e-commerce dataset.
    """
    
    def __init__(self, df_initial, df_cleaned):
        """
        Initialize DataExploration.
        
        Parameters:
        -----------
        df_initial : pd.DataFrame
            Initial raw dataframe
        df_cleaned : pd.DataFrame
            Cleaned dataframe
        """
        self.df_initial = df_initial
        self.df_cleaned = df_cleaned
        
    def get_data_info(self):
        """Print basic information about the dataset."""
        tab_info = pd.DataFrame(self.df_initial.dtypes).T.rename(index={0: 'column type'})
        tab_info = pd.concat([
            tab_info,
            pd.DataFrame(self.df_initial.isnull().sum()).T.rename(index={0: 'null values (nb)'}),
            pd.DataFrame(self.df_initial.isnull().sum() / self.df_initial.shape[0] * 100).T.rename(
                index={0: 'null values (%)'}
            )
        ])
        return tab_info
    
    def analyze_countries(self):
        """
        Analyze countries in the dataset.
        
        Returns:
        --------
        pd.Series
            Countries sorted by number of orders
        """
        temp = self.df_initial[['CustomerID', 'InvoiceNo', 'Country']].groupby(
            ['CustomerID', 'InvoiceNo', 'Country']
        ).count()
        temp = temp.reset_index(drop=False)
        countries = temp['Country'].value_counts()
        print(f'Number of countries: {len(countries)}')
        return countries
    
    def analyze_customers_products(self):
        """
        Analyze customers and products statistics.
        
        Returns:
        --------
        pd.DataFrame
            Summary statistics
        """
        summary = pd.DataFrame([{
            'products': len(self.df_initial['StockCode'].value_counts()),
            'transactions': len(self.df_initial['InvoiceNo'].value_counts()),
            'customers': len(self.df_initial['CustomerID'].value_counts()),
        }], columns=['products', 'transactions', 'customers'], index=['quantity'])
        return summary
    
    def analyze_cancellations(self, basket_data):
        """
        Analyze cancellation patterns.
        
        Parameters:
        -----------
        basket_data : pd.DataFrame
            Basket price dataframe
        
        Returns:
        --------
        dict
            Cancellation statistics
        """
        temp = basket_data.groupby(by=['CustomerID', 'InvoiceNo'], as_index=False)['Basket Price'].count()
        temp['order_canceled'] = temp['InvoiceNo'].apply(lambda x: int('C' in x))
        
        n_canceled = temp['order_canceled'].sum()
        n_total = temp.shape[0]
        
        stats = {
            'canceled_orders': n_canceled,
            'total_orders': n_total,
            'cancellation_rate': n_canceled / n_total * 100
        }
        
        return stats
    
    def analyze_special_stock_codes(self):
        """
        Identify and analyze special stock codes (non-numeric).
        
        Returns:
        --------
        list
            Special stock codes found
        """
        special_codes = self.df_cleaned[
            self.df_cleaned['StockCode'].str.contains('^[a-zA-Z]+', regex=True)
        ]['StockCode'].unique()
        
        result = {}
        for code in special_codes:
            desc = self.df_cleaned[self.df_cleaned['StockCode'] == code]['Description'].unique()[0]
            result[code] = desc
        
        return result
    
    def analyze_basket_prices(self, basket_data):
        """
        Analyze distribution of basket prices.
        
        Parameters:
        -----------
        basket_data : pd.DataFrame
            Basket price dataframe
        
        Returns:
        --------
        dict
            Price range distribution
        """
        price_range = [0, 50, 100, 200, 500, 1000, 5000, 50000]
        count_price = []
        
        for i, price in enumerate(price_range):
            if i == 0:
                continue
            val = basket_data[
                (basket_data['Basket Price'] < price) &
                (basket_data['Basket Price'] > price_range[i-1])
            ]['Basket Price'].count()
            count_price.append(val)
        
        result = {}
        for i, s in enumerate(count_price):
            key = f'{price_range[i]}-{price_range[i+1]}'
            result[key] = s
        
        return result
