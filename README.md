# 🛒 LankaMart Retail Performance Dashboard

A **Retail Performance Analytics Dashboard** developed using **Python, Streamlit, Pandas, and Plotly** for analyzing LankaMart's retail transaction data.

The dashboard helps users explore sales performance, profitability, customer returns, delivery performance, product categories, provinces, and sales channels through interactive visualizations and filters.

## 📊 Project Overview

**LankaMart Retail Performance Dashboard** is a data visualization project developed for the **CIT308 Data Visualization — Mid Semester Evaluation**.

The application provides an interactive interface where users can filter the dataset and dynamically analyze:

* Revenue
* Profit
* Profit margin
* Return rate
* Monthly sales and profit trends
* Revenue by product category
* Revenue by province
* Discount vs. profit margin
* Delivery time by sales channel
* Return rate by product category
* Detailed transaction records

## ✨ Features

### 🔍 Interactive Filters

Users can filter the dashboard by:

* Order date range
* Province
* Product category
* Sales channel
* Customer segment

A **Reset all filters** option is also available.

### 📌 KPI Dashboard

The dashboard displays four main KPIs:

* **Total Revenue**
* **Total Profit**
* **Profit Margin**
* **Return Rate**

### 📈 Visualizations

The dashboard includes:

1. **Monthly Revenue and Profit Trend**
2. **Revenue by Product Category**
3. **Revenue by Province**
4. **Discount Level vs. Profit Margin**
5. **Delivery Time Distribution by Sales Channel**
6. **Return Rate by Product Category**

### 📋 Detailed Transaction Data

Users can view filtered transaction records containing information such as:

* Order ID
* Order date
* Province
* City
* Sales channel
* Customer segment
* Product category
* Product name
* Units
* Revenue
* Profit
* Profit margin
* Delivery days
* Customer rating
* Return status
* Promotion

## 🧹 Data Cleaning & Preparation

The application performs several data preparation steps before visualization:

* Removes duplicate `order_id` records
* Standardizes the `electronic` category to `Electronics`
* Converts `order_date` into a datetime format
* Creates an `order_month` field
* Calculates `profit_margin_pct`
* Creates delivery performance bands
* Replaces missing promotion values with `No Promotion`
* Keeps missing customer ratings as `NaN` rather than artificially filling them

These cleaning steps are implemented directly in the dashboard's data-loading workflow.

## 🛠️ Technologies Used

| Technology           | Purpose                      |
| -------------------- | ---------------------------- |
| Python               | Application development      |
| Streamlit            | Interactive dashboard        |
| Pandas               | Data processing and analysis |
| Plotly Express       | Data visualization           |
| Plotly Graph Objects | Advanced charts              |
| Git & GitHub         | Version control              |

## 📁 Project Structure

```text
LankaMart-Retail/
│
├── app.py
├── LankaMart_Retail_Transactions (1).csv
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/MOHAMED-AASIM/LankaMart-Retail.git
```

### 2. Navigate to the project

```bash
cd LankaMart-Retail
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the Dashboard

Run the following command:

```bash
streamlit run app.py
```

The project is designed to run locally using Streamlit.

After running the command, Streamlit will provide a local URL such as:

```text
http://localhost:8501
```

Open the URL in your browser to access the dashboard.

## 📊 Dashboard Workflow

```text
Retail Transaction Dataset
          ↓
     Data Loading
          ↓
    Data Validation
          ↓
     Data Cleaning
          ↓
   Feature Engineering
          ↓
      User Filters
          ↓
   Filtered Dataset
          ↓
 ┌────────┴─────────┐
 ↓                  ↓
KPI Analysis    Visualizations
 ↓                  ↓
 └────────┬─────────┘
          ↓
 Detailed Records
          ↓
   Key Insights
          ↓
Management Analysis
```

## 🔎 Analytical Workflow

### 1. Data Loading

The application loads the LankaMart transaction CSV file using Pandas.

### 2. Data Validation

The application checks whether the required transaction columns are available before processing the dataset.

### 3. Data Cleaning

Duplicate orders, inconsistent category names, dates, promotions, and missing customer ratings are handled during preprocessing.

### 4. Feature Engineering

Additional analytical fields are created:

```text
order_month
profit_margin_pct
delivery_band
```

### 5. Filtering

Users select the required date range, province, category, sales channel, and customer segment.

### 6. KPI Calculation

The filtered data is used to calculate revenue, profit, profit margin, and return rate.

### 7. Visualization

Interactive Plotly charts present trends, comparisons, distributions, and relationships.

### 8. Insights

The dashboard automatically identifies the leading revenue category, highest-revenue province, highest-return category, and the correlation between discounting and profit margin.

## 📌 Key Analytical Questions

The dashboard is designed to help answer questions such as:

* How much revenue is LankaMart generating?
* How much profit is being generated?
* Which product category generates the most revenue?
* Which province contributes the most revenue?
* How does discounting relate to profit margin?
* Which sales channel has different delivery-time patterns?
* Which product category has the highest return rate?
* How do results change when filters are applied?

## 🎯 Project Objective

The main objective is to transform raw retail transaction data into an **interactive business intelligence dashboard** that supports data exploration and management-level analysis.

## 👨‍💻 Author

**Mohamed Aasim**

Cloud Computing Undergraduate
Sri Lanka Technological Campus (SLTC)

GitHub:
https://github.com/MOHAMED-AASIM

---

⭐ If you find this project useful, consider giving the repository a star.
