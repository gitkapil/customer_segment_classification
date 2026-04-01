"""
Product Categorization Module

This module handles product clustering and categorization.
Tasks:
- Extract keywords from product descriptions
- Encode product features (one-hot encoding)
- Perform K-means clustering on products
- Characterize product clusters
"""

import pandas as pd
import numpy as np
import nltk
from nltk.stem import SnowballStemmer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.decomposition import PCA


class ProductCategorization:
    """
    Handles product categorization through clustering and feature extraction.
    """
    
    def __init__(self, df_cleaned):
        """
        Initialize ProductCategorization.
        
        Parameters:
        -----------
        df_cleaned : pd.DataFrame
            Cleaned transaction dataframe
        """
        self.df_cleaned = df_cleaned
        self.liste_produits = None
        self.X = None
        self.clusters = None
        self.kmeans = None
        self.n_clusters = 5
        
    def extract_keywords(self, colonne='Description'):
        """
        Extract keywords from product descriptions using NLP.
        
        Parameters:
        -----------
        colonne : str
            Column name to extract keywords from
        
        Returns:
        --------
        tuple
            (keywords_list, keywords_roots, keywords_select, count_keywords)
        """
        is_noun = lambda pos: pos[:2] == 'NN'
        stemmer = SnowballStemmer("english")
        
        keywords_roots = {}
        count_keywords = {}
        
        for s in self.df_cleaned[colonne]:
            if pd.isnull(s):
                continue
            lines = s.lower()
            tokenized = nltk.word_tokenize(lines)
            nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
            
            for t in nouns:
                t = t.lower()
                racine = stemmer.stem(t)
                if racine in keywords_roots:
                    keywords_roots[racine].add(t)
                    count_keywords[racine] += 1
                else:
                    keywords_roots[racine] = {t}
                    count_keywords[racine] = 1
        
        keywords_select = {}
        for s in keywords_roots.keys():
            if len(keywords_roots[s]) > 1:
                min_length = 1000
                for k in keywords_roots[s]:
                    if len(k) < min_length:
                        clef = k
                        min_length = len(k)
                keywords_select[s] = clef
            else:
                keywords_select[s] = list(keywords_roots[s])[0]
        
        category_keys = list(keywords_select.values())
        print(f"Extracted {len(category_keys)} keywords from '{colonne}'")
        
        return category_keys, keywords_roots, keywords_select, count_keywords
    
    def filter_keywords(self, keywords_select, count_keywords, min_count=13, exclude_words=None):
        """
        Filter keywords by frequency and exclude unimportant words.
        
        Parameters:
        -----------
        keywords_select : dict
            Mapping of keyword roots to selected keywords
        count_keywords : dict
            Count of keyword occurrences
        min_count : int
            Minimum occurrence count (default: 13)
        exclude_words : list
            Words to exclude from analysis
        
        Returns:
        --------
        list
            Filtered keywords with their counts
        """
        if exclude_words is None:
            exclude_words = ['pink', 'blue', 'tag', 'green', 'orange']
        
        list_products = []
        for k, v in count_keywords.items():
            word = keywords_select[k]
            if word in exclude_words or len(word) < 3 or v < min_count:
                continue
            if ('+' in word) or ('/' in word):
                continue
            list_products.append([word, v])
        
        list_products.sort(key=lambda x: x[1], reverse=True)
        print(f'Retained {len(list_products)} keywords')
        return list_products
    
    def encode_products(self, list_products):
        """
        Create one-hot encoding matrix for products based on keywords and price.
        
        Parameters:
        -----------
        list_products : list
            Filtered keywords with counts
        
        Returns:
        --------
        pd.DataFrame
            Encoded product features matrix
        """
        self.liste_produits = self.df_cleaned['Description'].unique()
        self.X = pd.DataFrame()
        
        # Add keyword columns
        for key, occurence in list_products:
            self.X.loc[:, key] = list(
                map(lambda x: int(key.upper() in x), self.liste_produits)
            )
        
        # Add price range columns
        threshold = [0, 1, 2, 3, 5, 10]
        label_col = []
        
        for i in range(len(threshold)):
            if i == len(threshold) - 1:
                col = f'.>{threshold[i]}'
            else:
                col = f'{threshold[i]}<.<{threshold[i+1]}'
            label_col.append(col)
            self.X.loc[:, col] = 0
        
        for i, prod in enumerate(self.liste_produits):
            prix = self.df_cleaned[self.df_cleaned['Description'] == prod]['UnitPrice'].mean()
            j = 0
            while prix > threshold[j]:
                j += 1
                if j == len(threshold):
                    break
            self.X.loc[i, label_col[j-1]] = 1
        
        print(f'Created {self.X.shape[1]} features for {self.X.shape[0]} products')
        return self.X
    
    def cluster_products(self, n_clusters=5, min_silhouette=0.145):
        """
        Perform K-means clustering on product features.
        
        Parameters:
        -----------
        n_clusters : int
            Number of clusters to create
        min_silhouette : float
            Minimum silhouette score target
        
        Returns:
        --------
        np.array
            Cluster assignments for products
        """
        self.n_clusters = n_clusters
        matrix = self.X.values
        
        silhouette_avg = -1
        iterations = 0
        max_iterations = 50
        
        while silhouette_avg < min_silhouette and iterations < max_iterations:
            self.kmeans = KMeans(init='k-means++', n_clusters=n_clusters, n_init=30, random_state=42)
            self.kmeans.fit(matrix)
            self.clusters = self.kmeans.predict(matrix)
            
            # Only calculate silhouette score if we have at least 2 clusters with points
            unique_clusters = len(np.unique(self.clusters))
            if unique_clusters > 1:
                try:
                    silhouette_avg = silhouette_score(matrix, self.clusters)
                    print(f"Iteration {iterations + 1}: Silhouette score = {silhouette_avg:.4f}")
                except ValueError:
                    # If silhouette calculation fails, just accept this clustering
                    silhouette_avg = min_silhouette + 0.1
                    print(f"Iteration {iterations + 1}: Clustering accepted (silhouette calculation skipped)")
            else:
                # If only 1 cluster, restart
                print(f"Iteration {iterations + 1}: Only 1 cluster found, restarting...")
                silhouette_avg = -1
            
            iterations += 1
            
            if iterations >= max_iterations:
                print(f"Max iterations reached. Accepting clustering with {unique_clusters} clusters.")
                break
        
        return self.clusters
    
    def get_cluster_distribution(self):
        """Get distribution of products across clusters."""
        return pd.Series(self.clusters).value_counts().sort_index()
    
    def map_products_to_clusters(self):
        """Create mapping of products to cluster numbers."""
        corresp = dict(zip(self.liste_produits, self.clusters))
        return corresp
