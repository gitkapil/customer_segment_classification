"""
Prediction Testing Module

This module handles testing and validation of trained models on unseen data.
Tasks:
- Format test data in the same way as training data
- Apply trained classifiers to test data
- Evaluate prediction accuracy
- Compare predictions with actual customer categories
"""

import pandas as pd
import numpy as np
import datetime
from sklearn.metrics import accuracy_score


class PredictionTester:
    """
    Tests trained classifiers on unseen test data.
    """
    
    def __init__(self, set_test, scaler, kmeans, df_cleaned, product_clusters):
        """
        Initialize PredictionTester.
        
        Parameters:
        -----------
        set_test : pd.DataFrame
            Test set basket data
        scaler : StandardScaler
            Fitted StandardScaler for feature normalization
        kmeans : KMeans
            Fitted KMeans model for customer clustering
        df_cleaned : pd.DataFrame
            Cleaned transaction dataframe
        product_clusters : dict
            Mapping of products to cluster numbers
        """
        self.set_test = set_test
        self.scaler = scaler
        self.kmeans = kmeans
        self.df_cleaned = df_cleaned
        self.product_clusters = product_clusters
        self.transactions_per_user_test = None
        self.Y_test = None
        self.X_test = None
        
    def prepare_test_data(self, time_correction_factor=5):
        """
        Format test data similarly to training data.
        
        Parameters:
        -----------
        time_correction_factor : float
            Factor to correct for time period difference (default: 5)
        
        Returns:
        --------
        pd.DataFrame
            Prepared test data
        """
        basket_price = self.set_test.copy(deep=True)
        
        # Aggregate by customer
        transactions_per_user = basket_price.groupby(
            by=['CustomerID']
        )['Basket Price'].agg(['count', 'min', 'max', 'mean', 'sum'])
        
        # Category percentages
        for i in range(5):
            col = f'categ_{i}'
            transactions_per_user.loc[:, col] = (
                basket_price.groupby(by=['CustomerID'])[col].sum() /
                transactions_per_user['sum'] * 100
            )
        
        transactions_per_user.reset_index(drop=False, inplace=True)
        
        # Correct for time period difference (test is only 2 months vs 10 months training)
        transactions_per_user['count'] = time_correction_factor * transactions_per_user['count']
        transactions_per_user['sum'] = transactions_per_user['count'] * transactions_per_user['mean']
        
        self.transactions_per_user_test = transactions_per_user
        return transactions_per_user
    
    def assign_actual_categories(self):
        """
        Assign actual customer categories using KMeans.
        
        Returns:
        --------
        np.array
            Actual cluster assignments for test customers
        """
        list_cols = ['count', 'min', 'max', 'mean', 'categ_0', 'categ_1', 
                     'categ_2', 'categ_3', 'categ_4']
        
        matrix_test = self.transactions_per_user_test[list_cols].values
        scaled_test_matrix = self.scaler.transform(matrix_test)
        
        self.Y_test = self.kmeans.predict(scaled_test_matrix)
        return self.Y_test
    
    def prepare_features(self):
        """
        Prepare features for classifier prediction.
        
        Returns:
        --------
        pd.DataFrame
            Feature matrix for prediction
        """
        columns = ['mean', 'categ_0', 'categ_1', 'categ_2', 'categ_3', 'categ_4']
        self.X_test = self.transactions_per_user_test[columns]
        return self.X_test
    
    def test_classifier(self, classifier, classifier_name='Classifier'):
        """
        Test a classifier on the test set.
        
        Parameters:
        -----------
        classifier : fitted classifier
            Trained classifier to test
        classifier_name : str
            Name of the classifier for reporting
        
        Returns:
        --------
        float
            Accuracy score
        """
        predictions = classifier.predict(self.X_test)
        accuracy = accuracy_score(self.Y_test, predictions)
        
        print(f'{classifier_name}: Accuracy = {accuracy:.2%}')
        return accuracy
    
    def test_all_classifiers(self, classifiers_dict):
        """
        Test all classifiers on test data.
        
        Parameters:
        -----------
        classifiers_dict : dict
            Dictionary of classifiers {name: classifier_object}
        
        Returns:
        --------
        dict
            Accuracy scores for each classifier
        """
        results = {}
        
        for name, clf_wrapper in classifiers_dict.items():
            # For ClassFit objects, use the grid.best_estimator_
            if hasattr(clf_wrapper, 'grid') and clf_wrapper.grid is not None:
                clf = clf_wrapper.grid.best_estimator_
            else:
                clf = clf_wrapper
            
            predictions = clf.predict(self.X_test)
            accuracy = accuracy_score(self.Y_test, predictions)
            results[name] = accuracy
            
            print(f'{name}: Accuracy = {accuracy:.2%}')
        
        return results
    
    def test_voting_classifier(self, voting_classifier):
        """
        Test ensemble VotingClassifier.
        
        Parameters:
        -----------
        voting_classifier : VotingClassifier
            Trained voting classifier
        
        Returns:
        --------
        float
            Accuracy score
        """
        predictions = voting_classifier.predict(self.X_test)
        accuracy = accuracy_score(self.Y_test, predictions)
        
        print(f'\nVoting Classifier Test Accuracy: {accuracy:.2%}')
        return accuracy
    
    def execute_pipeline(self, classifiers_dict=None, voting_classifier=None):
        """
        Execute complete test pipeline.
        
        Parameters:
        -----------
        classifiers_dict : dict
            Dictionary of classifiers to test
        voting_classifier : VotingClassifier
            Ensemble voting classifier
        
        Returns:
        --------
        dict
            Results dictionary with accuracy scores
        """
        print('\n' + '='*60)
        print('TESTING CLASSIFIERS ON TEST DATA')
        print('='*60)
        
        self.prepare_test_data()
        self.assign_actual_categories()
        self.prepare_features()
        
        results = {}
        
        if classifiers_dict:
            results['individual'] = self.test_all_classifiers(classifiers_dict)
        
        if voting_classifier:
            results['voting'] = self.test_voting_classifier(voting_classifier)
        
        return results
