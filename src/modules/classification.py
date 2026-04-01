"""
Classification Module

This module handles training and evaluation of customer classifiers.
Tasks:
- Train multiple classifier models (SVC, Logistic Regression, KNN, Decision Tree, Random Forest, GradientBoosting)
- Perform hyperparameter tuning with GridSearchCV
- Generate confusion matrices and learning curves
- Create ensemble classifier using VotingClassifier
"""

import numpy as np
import pandas as pd
from sklearn import model_selection, metrics
from sklearn.model_selection import GridSearchCV, learning_curve
from sklearn.svm import LinearSVC
from sklearn import linear_model, neighbors, tree, ensemble
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
import matplotlib.pyplot as plt


class ClassFit:
    """Wrapper class for training and evaluating classifiers."""
    
    def __init__(self, clf, params=None):
        """
        Initialize ClassFit.
        
        Parameters:
        -----------
        clf : sklearn classifier
            Classifier class to use
        params : dict
            Initial parameters for the classifier
        """
        if params:
            self.clf = clf(**params)
        else:
            self.clf = clf()
        self.grid = None
        self.predictions = None
    
    def train(self, x_train, y_train):
        """Train the classifier."""
        self.clf.fit(x_train, y_train)
    
    def predict(self, x):
        """Make predictions."""
        return self.clf.predict(x)
    
    def grid_search(self, parameters, Kfold=5):
        """
        Set up GridSearchCV for hyperparameter tuning.
        
        Parameters:
        -----------
        parameters : dict or list
            Parameter grid for GridSearchCV
        Kfold : int
            Number of cross-validation folds
        """
        self.grid = GridSearchCV(estimator=self.clf, param_grid=parameters, cv=Kfold)
    
    def grid_fit(self, X, Y):
        """Fit the model with GridSearchCV."""
        self.grid.fit(X, Y)
        print(f"Best parameters: {self.grid.best_params_}")
    
    def grid_predict(self, X, Y):
        """Make predictions and print accuracy."""
        self.predictions = self.grid.predict(X)
        accuracy = metrics.accuracy_score(Y, self.predictions)
        print(f"Accuracy: {accuracy:.2%}")
        return accuracy


class CustomerClassifier:
    """
    Trains and manages multiple customer classification models.
    """
    
    def __init__(self, X_train, X_test, Y_train, Y_test):
        """
        Initialize CustomerClassifier.
        
        Parameters:
        -----------
        X_train, X_test : pd.DataFrame or np.array
            Training and test features
        Y_train, Y_test : pd.Series or np.array
            Training and test labels
        """
        self.X_train = X_train
        self.X_test = X_test
        self.Y_train = Y_train
        self.Y_test = Y_test
        self.classifiers = {}
        self.voting_classifier = None
    
    def train_svc(self):
        """Train Support Vector Machine Classifier."""
        print('\n' + '='*50)
        print('Training Support Vector Machine')
        print('='*50)
        
        svc = ClassFit(clf=LinearSVC)
        svc.grid_search(parameters=[{'C': np.logspace(-2, 2, 10)}], Kfold=5)
        svc.grid_fit(X=self.X_train, Y=self.Y_train)
        svc.grid_predict(self.X_test, self.Y_test)
        
        self.classifiers['SVC'] = svc
        return svc
    
    def train_logistic_regression(self):
        """Train Logistic Regression Classifier."""
        print('\n' + '='*50)
        print('Training Logistic Regression')
        print('='*50)
        
        lr = ClassFit(clf=linear_model.LogisticRegression)
        lr.grid_search(parameters=[{'C': np.logspace(-2, 2, 20)}], Kfold=5)
        lr.grid_fit(X=self.X_train, Y=self.Y_train)
        lr.grid_predict(self.X_test, self.Y_test)
        
        self.classifiers['LogisticRegression'] = lr
        return lr
    
    def train_knn(self):
        """Train k-Nearest Neighbors Classifier."""
        print('\n' + '='*50)
        print('Training k-Nearest Neighbors')
        print('='*50)
        
        knn = ClassFit(clf=neighbors.KNeighborsClassifier)
        knn.grid_search(parameters=[{'n_neighbors': np.arange(1, 50, 1)}], Kfold=5)
        knn.grid_fit(X=self.X_train, Y=self.Y_train)
        knn.grid_predict(self.X_test, self.Y_test)
        
        self.classifiers['KNN'] = knn
        return knn
    
    def train_decision_tree(self):
        """Train Decision Tree Classifier."""
        print('\n' + '='*50)
        print('Training Decision Tree')
        print('='*50)
        
        tr = ClassFit(clf=tree.DecisionTreeClassifier)
        params = [{'criterion': ['entropy', 'gini'], 'max_features': ['sqrt', 'log2']}]
        tr.grid_search(parameters=params, Kfold=5)
        tr.grid_fit(X=self.X_train, Y=self.Y_train)
        tr.grid_predict(self.X_test, self.Y_test)
        
        self.classifiers['DecisionTree'] = tr
        return tr
    
    def train_random_forest(self):
        """Train Random Forest Classifier."""
        print('\n' + '='*50)
        print('Training Random Forest')
        print('='*50)
        
        rf = ClassFit(clf=ensemble.RandomForestClassifier)
        param_grid = {
            'criterion': ['entropy', 'gini'],
            'n_estimators': [20, 40, 60, 80, 100],
            'max_features': ['sqrt', 'log2']
        }
        rf.grid_search(parameters=param_grid, Kfold=5)
        rf.grid_fit(X=self.X_train, Y=self.Y_train)
        rf.grid_predict(self.X_test, self.Y_test)
        
        self.classifiers['RandomForest'] = rf
        return rf
    
    def train_adaboost(self):
        """Train AdaBoost Classifier."""
        print('\n' + '='*50)
        print('Training AdaBoost')
        print('='*50)
        
        ada = ClassFit(clf=AdaBoostClassifier)
        param_grid = {'n_estimators': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
        ada.grid_search(parameters=param_grid, Kfold=5)
        ada.grid_fit(X=self.X_train, Y=self.Y_train)
        ada.grid_predict(self.X_test, self.Y_test)
        
        self.classifiers['AdaBoost'] = ada
        return ada
    
    def train_gradient_boosting(self):
        """Train Gradient Boosting Classifier."""
        print('\n' + '='*50)
        print('Training Gradient Boosting')
        print('='*50)
        
        gb = ClassFit(clf=ensemble.GradientBoostingClassifier)
        param_grid = {'n_estimators': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
        gb.grid_search(parameters=param_grid, Kfold=5)
        gb.grid_fit(X=self.X_train, Y=self.Y_train)
        gb.grid_predict(self.X_test, self.Y_test)
        
        self.classifiers['GradientBoosting'] = gb
        return gb
    
    def create_voting_classifier(self, estimator_names=['RandomForest', 'GradientBoosting', 'KNN']):
        """
        Create ensemble VotingClassifier from best performing models.
        
        Parameters:
        -----------
        estimator_names : list
            Names of classifiers to include in voting
        """
        estimators = []
        for name in estimator_names:
            if name in self.classifiers:
                clf = self.classifiers[name]
                estimators.append((name, clf.grid.best_estimator_))
        
        self.voting_classifier = ensemble.VotingClassifier(
            estimators=estimators, voting='soft'
        )
        self.voting_classifier.fit(self.X_train, self.Y_train)
        
        predictions = self.voting_classifier.predict(self.X_test)
        accuracy = metrics.accuracy_score(self.Y_test, predictions)
        
        print(f"\nVoting Classifier Accuracy: {accuracy:.2%}")
        return self.voting_classifier
    
    def get_confusion_matrix(self, classifier_name='SVC'):
        """
        Get confusion matrix for a specific classifier.
        
        Parameters:
        -----------
        classifier_name : str
            Name of the classifier
        
        Returns:
        --------
        np.array
            Confusion matrix
        """
        if classifier_name in self.classifiers:
            clf = self.classifiers[classifier_name]
            return confusion_matrix(self.Y_test, clf.predictions)
        return None
    
    def train_all_classifiers(self):
        """Train all available classifiers."""
        self.train_svc()
        self.train_logistic_regression()
        self.train_knn()
        self.train_decision_tree()
        self.train_random_forest()
        self.train_adaboost()
        self.train_gradient_boosting()
