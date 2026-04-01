# Customer Segmentation Classification

A comprehensive Python project for e-commerce customer segmentation and classification using machine learning.


## Project Overview

This project analyzes e-commerce purchase data to:
1. **Cluster Products** into 5 categories based on product descriptions using NLP and K-means
2. **Segment Customers** into 11 groups based on purchasing behavior
3. **Train Multiple Classifiers** to predict customer segments from their first purchase
4. **Validate Predictions** on held-out test data

## Project Structure

```
customerSegmentClassification/
├── src/
│   ├── config/
│   │   └── config.py              # Configuration settings
│   ├── modules/
│   │   ├── __init__.py            # Module exports
│   │   ├── data_preparation.py    # Data loading and cleaning
│   │   ├── data_exploration.py    # Exploratory data analysis
│   │   ├── product_categorization.py  # Product clustering
│   │   ├── customer_categorization.py # Customer segmentation
│   │   ├── classification.py      # Classifier training
│   │   └── prediction.py          # Prediction testing
│   ├── main.py                    # Main pipeline execution script
│   └── dashboard.py               # Interactive dashboard generator
├── data/                          # Data directory (place data.csv here)
│   └── sample_data.py             # Sample data generator for testing
├── output/                        # Output directory for results
│   └── dashboard.html             # Interactive management dashboard
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── QUICKSTART.md                  # Quick start guide
├── ARCHITECTURE.md                # Architecture documentation
└── PROJECT_SUMMARY.md             # Project summary and conversion notes
```



## Installation & Setup

### Prerequisites
- Python 3.7+
- pip or conda

### Step 1: Create a Virtual Environment (Recommended)

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n customer-seg python=3.9
conda activate customer-seg
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Additionally, download required NLTK data:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### Step 3: Prepare Your Data

Place your e-commerce dataset as `data/data.csv` with the following columns:
- `InvoiceNo`: Transaction ID
- `StockCode`: Product code
- `Description`: Product description
- `Quantity`: Quantity purchased
- `InvoiceDate`: Transaction date
- `UnitPrice`: Price per unit
- `CustomerID`: Customer ID
- `Country`: Customer country

The expected format matches the Kaggle Online Retail Dataset.

## Usage

### Running the Complete Pipeline

```bash
cd src
python main.py
```

This will execute all stages of the pipeline:
1. Load and clean data
2. Explore dataset characteristics
3. Cluster products into categories
4. Segment customers into groups
5. Train 7 different classifiers + voting ensemble
6. Test predictions on held-out data

### Generating the Interactive Dashboard

To create an interactive dashboard for management presentations:

```bash
cd src
python dashboard.py
```

This generates an HTML dashboard with:
- **6 Interactive Visualizations**:
  1. Top 10 countries by transaction count
  2. Top 10 countries by revenue
  3. Product price distribution
  4. Transaction timeline
  5. Transaction amount distribution
  6. Top 10 customers by transaction volume

- **Key Metrics Summary**:
  - Total customers and transactions
  - Unique products and countries
  - Average transaction value
  - Total revenue
  - Date range coverage

- **Features**:
  - Hover for detailed information
  - Export charts as PNG
  - Responsive design (desktop & mobile)
  - Professional gradient styling

**Output:** `output/dashboard.html` - Open in any web browser to view and share with stakeholders.

### Using Individual Modules

You can also use the modules independently:

```python
from src.modules import DataPreparation, ProductCategorization

# Data preparation
data_prep = DataPreparation('data/data.csv')
df_cleaned = data_prep.execute_pipeline()

# Product categorization
product_cat = ProductCategorization(df_cleaned)
clusters = product_cat.cluster_products(n_clusters=5)
```

## Modules Overview

### 1. **DataPreparation** (`data_preparation.py`)
Handles initial data loading and cleaning:
- Loads data from CSV
- Removes entries without CustomerID
- Removes duplicates
- Processes order cancellations
- Calculates total prices

### 2. **DataExploration** (`data_exploration.py`)
Provides exploratory data analysis:
- Country distribution analysis
- Customer and product statistics
- Cancellation pattern analysis
- Basket price distribution

### 3. **ProductCategorization** (`product_categorization.py`)
Clusters products into 5 categories:
- Extracts keywords from product descriptions using NLP
- Performs one-hot encoding with price ranges
- K-means clustering with silhouette score optimization
- Generates cluster profiles

### 4. **CustomerCategorization** (`customer_categorization.py`)
Segments customers into 11 groups:
- Aggregates transaction data to customer level
- Splits data into training (10 months) and test (2 months)
- Calculates customer metrics (frequency, spending, category preferences)
- K-means clustering with standardized features

### 5. **CustomerClassifier** (`classification.py`)
Trains and evaluates multiple classifiers:
- **Support Vector Machine (SVC)**
- **Logistic Regression**
- **k-Nearest Neighbors (KNN)**
- **Decision Tree**
- **Random Forest**
- **AdaBoost**
- **Gradient Boosting**
- **Voting Ensemble** (combines top 3 models)

All models use GridSearchCV for hyperparameter tuning.

### 6. **PredictionTester** (`prediction.py`)
Validates trained models on test data:
- Formats test data consistently with training data
- Assigns actual customer categories
- Tests all trained classifiers
- Reports accuracy metrics

## Output

After running the pipeline, check:
- **Console Output**: Detailed execution logs and accuracy metrics
- **output/ Directory**: Generated results and visualizations

## Expected Results

Based on the notebook analysis:
- **Product Clusters**: 5 distinct product categories identified
- **Customer Segments**: 11 customer clusters with distinct purchasing patterns
- **Classification Accuracy**: ~75% on test data with voting classifier

## Key Findings

1. **Data Quality**: 
   - ~25% of transactions lack customer ID (removed)
   - ~16% of orders are cancellations
   - Successfully matched cancellations with original orders

2. **Product Categories**:
   - Cluster 0: Gifts and decorative items
   - Cluster 1-4: Various product types (luxury items, essentials, etc.)

3. **Customer Segments**:
   - High-frequency buyers vs. one-time customers
   - Category-focused vs. diverse purchasers
   - High-value vs. budget customers

4. **Model Performance**:
   - Voting ensemble outperforms individual classifiers
   - Stable predictions with minimal overfitting
   - Best features: mean basket price and category preferences

## Configuration

Edit `src/config/config.py` to customize:
- Number of product clusters (default: 5)
- Number of customer clusters (default: 11)
- Minimum keyword frequency (default: 13)
- Train-test split date (default: 2011-10-01)
- Cross-validation folds (default: 5)

## Troubleshooting

**ModuleNotFoundError**: Make sure you're running from the project root and Python path includes `src/`

**NLTK Data Missing**: Run `nltk.download()` to install required data

**Memory Issues**: Reduce dataset size or adjust K-means n_init parameter

## Future Enhancements

- [x] Create visualization dashboard (✅ Completed)
- [ ] Add model persistence (save/load trained models)
- [ ] Implement real-time prediction API
- [ ] Add time-series analysis for seasonality
- [ ] Incorporate customer demographics
- [ ] A/B testing framework for marketing strategies

## References

**Original Notebook:** `customer-segmentation.ipynb`
- Author: F. Daniel (September 2017)
- Source: Jupyter Notebook conversion to production Python project
- Dataset: Kaggle Online Retail Dataset
- The entire notebook logic has been refactored into modular, reusable components

## License

This project is for educational purposes.

## Author Notes

This project converts a comprehensive Jupyter notebook into a modular, production-ready Python package with:
- Clean separation of concerns
- Reusable modules
- Easy configuration management
- Comprehensive documentation
- Extensible architecture for future enhancements
