"""
Customer Segmentation Classification - Main Script

This is the main entry point for the customer segmentation project.
It orchestrates the complete workflow:
1. Data Preparation - Load and clean data
2. Data Exploration - Analyze dataset characteristics
3. Product Categorization - Cluster products into categories
4. Customer Categorization - Segment customers based on behavior
5. Classification - Train multiple classifiers
6. Prediction Testing - Validate on test data
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from modules import (
    DataPreparation, DataExploration, ProductCategorization,
    CustomerCategorization, CustomerClassifier, PredictionTester
)
from config.config import INPUT_FILE


def main():
    """Execute the main customer segmentation pipeline."""
    
    print('='*70)
    print('CUSTOMER SEGMENTATION AND CLASSIFICATION')
    print('='*70)
    
    # ============================================================
    # STEP 1: DATA PREPARATION
    # ============================================================
    print('\n[STEP 1] DATA PREPARATION')
    print('-'*70)
    
    data_prep = DataPreparation(str(INPUT_FILE))
    df_initial = data_prep.load_data()
    data_prep.remove_null_customers()
    data_prep.remove_duplicates()
    data_prep.process_cancellations()
    data_prep.add_total_price()
    df_cleaned = data_prep.get_cleaned_data()
    
    # ============================================================
    # STEP 2: DATA EXPLORATION
    # ============================================================
    print('\n[STEP 2] DATA EXPLORATION')
    print('-'*70)
    
    data_exploration = DataExploration(df_initial, df_cleaned)
    
    print('\nBasic data information:')
    print(data_exploration.get_data_info())
    
    print('\nCountry analysis:')
    countries = data_exploration.analyze_countries()
    print(f'Top 5 countries: {countries.head()}')
    
    print('\nCustomers and products:')
    summary = data_exploration.analyze_customers_products()
    print(summary)
    
    # Prepare basket data for later use
    basket_price = data_prep.prepare_basket_data()
    
    # ============================================================
    # STEP 3: PRODUCT CATEGORIZATION
    # ============================================================
    print('\n[STEP 3] PRODUCT CATEGORIZATION')
    print('-'*70)
    
    product_cat = ProductCategorization(df_cleaned)
    
    # Extract keywords from product descriptions
    print('\nExtracting keywords from product descriptions...')
    keywords, keywords_roots, keywords_select, count_keywords = \
        product_cat.extract_keywords('Description')
    
    # Filter keywords
    print('\nFiltering keywords...')
    list_products = product_cat.filter_keywords(keywords_select, count_keywords)
    
    # Encode products
    print('\nEncoding products with one-hot encoding...')
    X_products = product_cat.encode_products(list_products)
    
    # Cluster products
    print('\nClustering products...')
    clusters_products = product_cat.cluster_products(n_clusters=5)
    
    print('\nProduct cluster distribution:')
    print(product_cat.get_cluster_distribution())
    
    product_clusters = product_cat.map_products_to_clusters()
    
    # ============================================================
    # STEP 4: CUSTOMER CATEGORIZATION
    # ============================================================
    print('\n[STEP 4] CUSTOMER CATEGORIZATION')
    print('-'*70)
    
    customer_cat = CustomerCategorization(df_cleaned, product_clusters)
    
    customer_cat.add_product_categories()
    customer_cat.create_category_amounts()
    
    # Prepare customer-level data
    print('\nPreparing customer-level data...')
    basket_price_updated = customer_cat.prepare_basket_data()
    
    # Split training and test data
    print('\nSplitting data into training (10 months) and test (2 months)...')
    set_train, set_test = customer_cat.split_train_test()
    
    # Aggregate customer statistics
    print('\nAggregating customer statistics...')
    transactions_per_user = customer_cat.aggregate_customer_data()
    
    # Cluster customers
    print('\nClustering customers...')
    clusters_customers = customer_cat.cluster_customers(n_clusters=11)
    
    print('\nCustomer cluster distribution:')
    print(customer_cat.get_cluster_distribution())
    
    print('\nCustomer cluster profiles:')
    print(customer_cat.get_cluster_profiles())
    
    # ============================================================
    # STEP 5: CUSTOMER CLASSIFICATION
    # ============================================================
    print('\n[STEP 5] TRAINING CLASSIFIERS')
    print('-'*70)
    
    # Prepare data for classification
    columns = ['mean', 'categ_0', 'categ_1', 'categ_2', 'categ_3', 'categ_4']
    X = customer_cat.selected_customers[columns]
    Y = customer_cat.selected_customers['cluster']
    
    # Train-test split using sklearn
    from sklearn.model_selection import train_test_split
    X_train, X_test, Y_train, Y_test = \
        train_test_split(X, Y, train_size=0.8, random_state=42)
    
    # Initialize classifier
    classifier = CustomerClassifier(X_train, X_test, Y_train, Y_test)
    
    # Train all classifiers
    print('\nTraining all classifiers...')
    classifier.train_all_classifiers()
    
    # Create voting classifier
    print('\nCreating voting classifier...')
    voting_clf = classifier.create_voting_classifier(
        estimator_names=['RandomForest', 'GradientBoosting', 'KNN']
    )
    
    # ============================================================
    # STEP 6: PREDICTION TESTING
    # ============================================================
    print('\n[STEP 6] TESTING PREDICTIONS')
    print('-'*70)
    
    predictor = PredictionTester(
        set_test, 
        customer_cat.get_scaler(),
        customer_cat.get_kmeans(),
        df_cleaned,
        product_clusters
    )
    
    # Test pipeline
    results = predictor.execute_pipeline(
        classifiers_dict=classifier.classifiers,
        voting_classifier=voting_clf
    )
    
    # ============================================================
    # FINAL SUMMARY
    # ============================================================
    print('\n' + '='*70)
    print('EXECUTION COMPLETED SUCCESSFULLY')
    print('='*70)
    
    print(f'\nTotal customers analyzed: {len(transactions_per_user)}')
    print(f'Total products: {len(df_cleaned["Description"].unique())}')
    print(f'Training transactions: {len(set_train)}')
    print(f'Test transactions: {len(set_test)}')
    
    return {
        'df_cleaned': df_cleaned,
        'basket_price': basket_price_updated,
        'product_clusters': product_clusters,
        'customer_clusters': clusters_customers,
        'transactions_per_user': transactions_per_user,
        'classifier': classifier,
        'voting_classifier': voting_clf,
        'test_results': results
    }


if __name__ == '__main__':
    results = main()
