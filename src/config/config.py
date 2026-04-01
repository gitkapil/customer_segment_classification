"""
Configuration Module

Central configuration for the customer segmentation project.
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directory
DATA_DIR = PROJECT_ROOT / 'data'
INPUT_FILE = DATA_DIR / 'data.csv'

# Output directory
OUTPUT_DIR = PROJECT_ROOT / 'output'

# Model parameters
PRODUCT_CLUSTERS = 5
CUSTOMER_CLUSTERS = 11
MIN_KEYWORD_COUNT = 13
TRAIN_TEST_SPLIT_DATE = '2011-10-01'

# Classifier parameters
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

# Logging
LOG_FILE = OUTPUT_DIR / 'execution.log'

# Create directories if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
