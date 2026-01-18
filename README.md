# 📊 Data Cleaning & Analysis: UK-500 Dataset

## 📌 Project Overview
This project focuses on data cleaning, transformation, and exploratory analysis of the **UK-500** dataset.  
The main goal is to prepare raw data for further analysis by standardizing text fields, cleaning contact information, creating new features, and producing aggregated statistics.

**Data source:**  
https://s3-eu-west-1.amazonaws.com/shanebucket/downloads/uk-500.csv

---

## 1️⃣ Data Import & Initial Exploration

### What was done:
- Loaded the dataset using `pandas.read_csv`
- Performed an initial inspection:
  - `head()` — preview of the first rows
  - `info()` — structure and data types
  - `describe()` — statistics for numeric columns
  - `describe(include=object)` — statistics for text columns
  - Counted missing values using `isna().sum()`
  - Checked for duplicates with `duplicated()`

### Why:
This step helps to understand:
- available columns and data types;
- presence of missing values;
- existence of duplicates;
- which columns require cleaning or transformation.

---

## 2️⃣ Data Cleaning

### Column removal
A configurable list `COLUMNS_TO_DROP` was created to remove unnecessary columns if needed.

**Reasoning:**  
This approach keeps the code flexible and reusable without modifying the core logic.

---

### Text standardization
All text columns were cleaned by:
- trimming leading and trailing spaces;
- normalizing internal spacing;
- converting non-string values to strings when necessary.

Implemented via:
```python
standardize_text()