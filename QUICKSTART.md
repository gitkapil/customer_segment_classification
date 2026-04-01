# Quick Start Guide

## For New Team Members

This project is a **production-ready Python conversion** of the **`customer-segmentation.ipynb`** Jupyter notebook.

The notebook has been refactored into a professional project with:
- 7 modular components (1,521 lines of code)
- Comprehensive documentation
- Centralized configuration
- Complete ML pipeline

### 1. First Time Setup (5 minutes)

```bash
# Navigate to project directory
cd /Users/test/Music/customerSegmentClassification

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download required NLP data
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### 2. Prepare Your Data

- Get the `data.csv` file (online retail dataset or similar)
- Place it in the `data/` folder
- Ensure it has these columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

### 3. Run the Analysis

```bash
cd src
python main.py
```

Expected execution time: 5-15 minutes depending on dataset size

### 4. Check Results

- Look at console output for accuracy metrics
- Results are saved in the `output/` folder

---

## Project Organization

**Data Flow:**
```
Raw Data (data.csv)
    ↓
Data Preparation (cleaning, cancellations)
    ↓
Data Exploration (statistics, analysis)
    ↓
Product Categorization (NLP + clustering)
    ↓
Customer Categorization (segmentation)
    ↓
Classification Training (7 classifiers)
    ↓
Prediction Testing (validation)
    ↓
Results & Metrics
```

---

## Module Quick Reference

| Module | Purpose | Key Classes |
|--------|---------|------------|
| `data_preparation.py` | Load & clean data | `DataPreparation` |
| `data_exploration.py` | Analyze dataset | `DataExploration` |
| `product_categorization.py` | Cluster products | `ProductCategorization` |
| `customer_categorization.py` | Segment customers | `CustomerCategorization` |
| `classification.py` | Train classifiers | `CustomerClassifier`, `ClassFit` |
| `prediction.py` | Test models | `PredictionTester` |

---

## Common Tasks

### Want to change number of clusters?
Edit `src/config/config.py`:
```python
PRODUCT_CLUSTERS = 5      # Change to desired number
CUSTOMER_CLUSTERS = 11    # Change to desired number
```

### Want to use only specific classifiers?
Edit `src/main.py`, in STEP 5:
```python
# Comment out classifiers you don't need
classifier.train_svc()
classifier.train_logistic_regression()
# etc...
```

### Want to test a specific classifier?
```python
from src.modules import CustomerClassifier

# After training
clf = classifier.classifiers['RandomForest']
predictions = clf.grid.best_estimator_.predict(X_test)
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'src'` | Make sure you're in the correct directory and Python path includes src/ |
| `FileNotFoundError: data.csv` | Place your data file in the `data/` folder |
| `nltk.tokenize.punkt` error | Run `python -c "import nltk; nltk.download('punkt')"` |
| Memory error on large datasets | Reduce data size or increase system RAM |

---

## Key Metrics to Monitor

After execution, look for:
- ✓ **Silhouette Scores**: Should be > 0.1 for good clustering
- ✓ **Classification Accuracy**: Should be > 70% on test data
- ✓ **Cluster Distribution**: Should be reasonably balanced
- ✓ **No convergence warnings**: Check console output

---

## Next Steps

1. ✅ Understand the data structure
2. ✅ Run the complete pipeline
3. ✅ Analyze results and insights
4. ✅ Customize parameters as needed
5. ✅ Export results for reporting

Good luck! 🚀
