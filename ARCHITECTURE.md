```
customerSegmentClassification/
│
├── 📄 README.md                    ⭐ START HERE - Complete documentation
├── 📄 QUICKSTART.md                ⭐ 5-minute setup guide  
├── 📄 PROJECT_SUMMARY.md           📋 Project reorganization summary
├── 📄 requirements.txt              📦 Python dependencies
│
├── 📁 src/                          💻 SOURCE CODE
│   ├── 📄 main.py                  🚀 Main execution script
│   │
│   ├── 📁 config/                  ⚙️  CONFIGURATION
│   │   ├── __init__.py
│   │   └── config.py               (Centralized settings)
│   │
│   └── 📁 modules/                 🔧 REUSABLE MODULES
│       ├── __init__.py             (Module imports)
│       ├── data_preparation.py     (Clean & load data)
│       ├── data_exploration.py     (Analyze dataset)
│       ├── product_categorization.py   (Cluster products)
│       ├── customer_categorization.py  (Segment customers)
│       ├── classification.py       (Train classifiers)
│       └── prediction.py           (Test models)
│
├── 📁 data/                        📊 DATA DIRECTORY
│   └── (Place data.csv here)
│
└── 📁 output/                      📈 RESULTS & OUTPUT
    └── (Generated files will appear here)


EXECUTION FLOW:
═════════════════════════════════════════════════════════════

    [1] Data Preparation       [2] Data Exploration
           ↓                            ↓
    - Load raw data      →    - Analyze countries
    - Remove nulls             - Customer statistics
    - Handle duplicates        - Cancellation patterns
    - Process cancellations    - Price distributions
           ↓
    [3] Product Categorization
           ↓
    - Extract keywords (NLP)
    - One-hot encode features
    - K-means clustering (5 groups)
           ↓
    [4] Customer Categorization
           ↓
    - Aggregate by customer
    - Calculate metrics
    - Split train/test
    - K-means clustering (11 groups)
           ↓
    [5] Classification Training
           ↓
    ┌─ Support Vector Machine
    ├─ Logistic Regression
    ├─ k-Nearest Neighbors
    ├─ Decision Tree
    ├─ Random Forest
    ├─ AdaBoost
    ├─ Gradient Boosting
    └─ Voting Ensemble (combined)
           ↓
    [6] Prediction Testing
           ↓
    - Validate on test data
    - Report accuracy (~75%)
    - Generate metrics


KEY MODULES:
════════════════════════════════════════════════════════════

┌─ DataPreparation
│  └─ Load, clean, handle cancellations
│
├─ DataExploration
│  └─ Analyze and visualize data
│
├─ ProductCategorization
│  └─ NLP + K-means for 5 product clusters
│
├─ CustomerCategorization
│  └─ Aggregate and segment into 11 customer groups
│
├─ CustomerClassifier
│  ├─ ClassFit (wrapper for all classifiers)
│  └─ Train 7 models + voting ensemble
│
└─ PredictionTester
   └─ Validate models on test data


QUICK START:
════════════════════════════════════════════════════════════

1. Install:
   pip install -r requirements.txt
   python -c "import nltk; nltk.download('punkt')"

2. Prepare Data:
   Place data.csv in data/ folder

3. Run:
   cd src
   python main.py

4. Results:
   Check console output & output/ folder


CONFIGURATION:
════════════════════════════════════════════════════════════

Edit src/config/config.py to customize:
- PRODUCT_CLUSTERS = 5         (Change product groups)
- CUSTOMER_CLUSTERS = 11       (Change customer segments)
- MIN_KEYWORD_COUNT = 13       (Keyword frequency filter)
- CV_FOLDS = 5                 (Cross-validation folds)


EXPECTED RESULTS:
════════════════════════════════════════════════════════════

✓ Product Clusters: 5 distinct categories
✓ Customer Segments: 11 unique groups
✓ Classification Accuracy: ~75% on test data
✓ Model Quality: Minimal overfitting
✓ Execution Time: 5-15 minutes


FOR NEW TEAM MEMBERS:
════════════════════════════════════════════════════════════

1. Read QUICKSTART.md (5 minutes)
2. Install dependencies (2 minutes)
3. Run pipeline (5-15 minutes)
4. Review README.md for details
5. Ask questions about specific modules
```
