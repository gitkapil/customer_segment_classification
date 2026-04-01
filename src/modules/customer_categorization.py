"""
Customer Categorization Module

This module handles customer segmentation based on purchasing behavior.
Tasks:
- Format transaction data by customer
- Group products into categories
- Split training and testing data
- Create customer clusters using K-means
"""

import pandas as pd
import numpy as np
import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA


class CustomerCategorization:
    """
    Handles customer segmentation through clustering and behavioral analysis.
    """
    
    def __init__(self, df_cleaned, product_clusters):
        """
        Initialize CustomerCategorization.
        
        Parameters:
        -----------
        df_cleaned : pd.DataFrame
            Cleaned transaction dataframe
        product_clusters : dict
            Mapping of products to cluster numbers
        """
        self.df_cleaned = df_cleaned.copy()
        self.product_clusters = product_clusters
        self.basket_price = None
        self.transactions_per_user = None
        self.selected_customers = None
        self.clusters_clients = None
        self.kmeans = None
        self.scaler = StandardScaler()
        self.n_clusters = 11
        
    def add_product_categories(self):
        """Add product category column to cleaned dataframe."""
        self.df_cleaned['categ_product'] = self.df_cleaned['Description'].map(
            self.product_clusters
        )
        
    def create_category_amounts(self):
        """Create amount columns for each product category."""
        for i in range(5):
            col = f'categ_{i}'
            df_temp = self.df_cleaned[self.df_cleaned['categ_product'] == i]
            price_temp = df_temp['UnitPrice'] * (df_temp['Quantity'] - df_temp['QuantityCanceled'])
            price_temp = price_temp.apply(lambda x: x if x > 0 else 0)
            self.df_cleaned.loc[:, col] = price_temp
            self.df_cleaned[col].fillna(0, inplace=True)
    
    def prepare_basket_data(self):
        """
        Aggregate transaction data into basket-level information.
        
        Returns:
        --------
        pd.DataFrame
            Dataframe with one row per transaction
        """
        # Sum purchases per customer & invoice
        temp = self.df_cleaned.groupby(
            by=['CustomerID', 'InvoiceNo'], as_index=False
        )['TotalPrice'].sum()
        basket_price = temp.rename(columns={'TotalPrice': 'Basket Price'})
        
        # Add category amounts
        for i in range(5):
            col = f'categ_{i}'
            temp = self.df_cleaned.groupby(
                by=['CustomerID', 'InvoiceNo'], as_index=False
            )[col].sum()
            basket_price.loc[:, col] = temp[col]
        
        # Add invoice date
        df_temp = self.df_cleaned.copy()
        df_temp['InvoiceDate_int'] = df_temp['InvoiceDate'].astype('int64')
        temp = df_temp.groupby(
            by=['CustomerID', 'InvoiceNo'], as_index=False
        )['InvoiceDate_int'].mean()
        basket_price['InvoiceDate'] = pd.to_datetime(temp['InvoiceDate_int'])
        
        # Select only positive basket prices
        basket_price = basket_price[basket_price['Basket Price'] > 0]
        
        self.basket_price = basket_price
        return basket_price
    
    def split_train_test(self, cutoff_date=datetime.date(2011, 10, 1)):
        """
        Split data into training (first 10 months) and test (last 2 months).
        
        Parameters:
        -----------
        cutoff_date : datetime.date
            Date to split training and test data
        
        Returns:
        --------
        tuple
            (training_data, test_data)
        """
        # Convert date to pandas Timestamp for comparison
        cutoff_date = pd.Timestamp(cutoff_date)
        set_training = self.basket_price[self.basket_price['InvoiceDate'] < cutoff_date]
        set_test = self.basket_price[self.basket_price['InvoiceDate'] >= cutoff_date]
        
        self.basket_price = set_training.copy(deep=True)
        
        print(f'Training set: {len(set_training)} transactions')
        print(f'Test set: {len(set_test)} transactions')
        
        return set_training, set_test
    
    def aggregate_customer_data(self):
        """
        Aggregate data at customer level.
        
        Returns:
        --------
        pd.DataFrame
            Customer-level statistics
        """
        # Count and amount statistics
        transactions_per_user = self.basket_price.groupby(
            by=['CustomerID']
        )['Basket Price'].agg(['count', 'min', 'max', 'mean', 'sum'])
        
        # Category percentages
        for i in range(5):
            col = f'categ_{i}'
            transactions_per_user.loc[:, col] = (
                self.basket_price.groupby(by=['CustomerID'])[col].sum() /
                transactions_per_user['sum'] * 100
            )
        
        transactions_per_user.reset_index(drop=False, inplace=True)
        
        # Add purchase timing info
        last_date = self.basket_price['InvoiceDate'].max().date()
        
        first_registration = pd.DataFrame(
            self.basket_price.groupby(by=['CustomerID'])['InvoiceDate'].min()
        )
        last_purchase = pd.DataFrame(
            self.basket_price.groupby(by=['CustomerID'])['InvoiceDate'].max()
        )
        
        test = first_registration.applymap(lambda x: (last_date - x.date()).days)
        test2 = last_purchase.applymap(lambda x: (last_date - x.date()).days)
        
        transactions_per_user['FirstPurchase'] = test.reset_index(drop=False)['InvoiceDate']
        transactions_per_user['LastPurchase'] = test2.reset_index(drop=False)['InvoiceDate']
        
        self.transactions_per_user = transactions_per_user
        return transactions_per_user
    
    def cluster_customers(self, n_clusters=11):
        """
        Perform K-means clustering on customer behavior data.
        
        Parameters:
        -----------
        n_clusters : int
            Number of customer clusters to create
        
        Returns:
        --------
        np.array
            Cluster assignments for customers
        """
        self.n_clusters = n_clusters
        
        # Select features for clustering
        list_cols = ['count', 'min', 'max', 'mean', 'categ_0', 'categ_1', 
                     'categ_2', 'categ_3', 'categ_4']
        self.selected_customers = self.transactions_per_user.copy(deep=True)
        
        matrix = self.selected_customers[list_cols].values
        
        # Standardize features
        self.scaler.fit(matrix)
        scaled_matrix = self.scaler.transform(matrix)
        
        # Perform K-means clustering
        self.kmeans = KMeans(init='k-means++', n_clusters=n_clusters, n_init=100)
        self.kmeans.fit(scaled_matrix)
        self.clusters_clients = self.kmeans.predict(scaled_matrix)
        
        silhouette_avg = silhouette_score(scaled_matrix, self.clusters_clients)
        print(f'Silhouette score: {silhouette_avg:.4f}')
        
        return self.clusters_clients
    
    def get_cluster_distribution(self):
        """Get distribution of customers across clusters."""
        return pd.Series(self.clusters_clients).value_counts().sort_index()
    
    def get_cluster_profiles(self):
        """
        Get statistical profiles of each customer cluster.
        
        Returns:
        --------
        pd.DataFrame
            Mean values for each cluster
        """
        self.selected_customers['cluster'] = self.clusters_clients
        
        merged_df = pd.DataFrame()
        list_cols = ['count', 'min', 'max', 'mean', 'categ_0', 'categ_1', 
                     'categ_2', 'categ_3', 'categ_4']
        
        for i in range(self.n_clusters):
            test = pd.DataFrame(
                self.selected_customers[self.selected_customers['cluster'] == i][list_cols].mean()
            ).T
            test['cluster'] = i
            test['size'] = self.selected_customers[
                self.selected_customers['cluster'] == i
            ].shape[0]
            merged_df = pd.concat([merged_df, test])
        
        return merged_df.reset_index(drop=True)
    
    def get_scaler(self):
        """Return the fitted StandardScaler for use in prediction."""
        return self.scaler
    
    def get_kmeans(self):
        """Return the fitted KMeans model for use in prediction."""
        return self.kmeans
