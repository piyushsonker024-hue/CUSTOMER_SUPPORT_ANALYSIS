# Customer Support Analytics Dashboard

## Project Overview

This project analyzes a customer support ticket dataset to identify SLA performance issues, agent efficiency, customer satisfaction trends, and overall support operations.

The analysis answers five business questions provided in the assignment and presents the key insights through an interactive Streamlit dashboard.

---

## Project Structure

```
CustomerSupportProject/
│
├── app.py                         # Streamlit Dashboard
├── Customer_Support_Analysis.ipynb # Data Analysis Notebook
├── BUSINESS_ANSWERS.md            # Answers to Business Questions
├── customer_tickets.csv           # Dataset
├── requirements.txt               # Python Dependencies
└── README.md                      # Project Documentation
```

---

## Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Streamlit

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd CustomerSupportProject
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser.

---

## Project Approach

I followed a structured data analysis workflow:

### Step 1 — Data Understanding

- Loaded the customer ticket dataset.
- Reviewed columns, data types, and overall dataset structure.

### Step 2 — Data Cleaning

Performed basic data quality checks, including:

- Standardized column names
- Converted date columns to datetime format
- Removed duplicate ticket IDs
- Identified missing values
- Excluded invalid resolution times
- Created an SLA breach flag for analysis

### Step 3 — Exploratory Data Analysis

Analyzed:

- Ticket distribution
- Category distribution
- Priority distribution
- Regional performance
- Resolution times
- Customer satisfaction

### Step 4 — Business Analysis

Answered the five business questions using calculations and aggregations rather than manual observation.

The analysis included:

- SLA Breach Rate by Category
- SLA Breach Rate by Region
- Resolution Time by Priority
- Agent Performance
- Customer Reopened Tickets
- Customer Satisfaction
- Data Quality Assessment
- Weekly SLA Trend

### Step 5 — Dashboard Development

Developed an interactive Streamlit dashboard with:

- Sidebar filters
- KPI summary cards
- Interactive Plotly charts
- Business insights
- Weekly KPI monitoring

---

## Business Questions Addressed

1. Which category or region has the worst SLA breach rate?

2. Is there a relationship between priority and resolution time?

3. Which customers frequently reopen tickets or have low CSAT?

4. What data quality issues exist in the dataset?

5. Which weekly KPI should be monitored to detect support problems early?

---

## Key Dashboard Features

- Interactive filters
- KPI Cards
- Ticket Distribution
- SLA Analysis
- Agent Performance
- Customer Insights
- Data Quality Report
- Weekly SLA Monitoring

---

## Recommended KPI

The recommended operational KPI is:

**Weekly SLA Breach Rate**

This metric provides an early indication of operational issues before they impact customer satisfaction.

---

## Author

**Name:** Piyush 

**Assignment:** Customer Support Analytics Dashboard
