# Student Churn & Retention Analysis (Kumon Center)

## Objective

This project analyzes historical student data from a Kumon center in Brazil to develop a machine learning model that predicts student churn. The primary goal is to provide actionable insights to stakeholders, helping them identify at-risk students and implement targeted retention strategies.

## Data

The dataset consists of monthly performance reports for students from **February 2022** to **September 2025**. It includes:

**Student Profile**: Anonymized ID, age (from date of birth), date of enrollment, school grade, and subject (Math, English, Portuguese, Japanese).

**Academic Performance**: Current learning stage, specific lesson, pages completed, and a proficiency indicator ("advanced", which indicates whether the student is ahead of their school grade).

**Monthly Status**: Status codes (ST1, ST2) indicating if the student is active, concluding, or temporarily absent.

## Key Business Questions

This analysis focuses on answering the following questions:

**Churn Definition**: What differentiates a "good" churn (e.g., course completion) from a "bad" one (e.g., premature dropout)?

**Prediction**: How likely is a given student to churn in the next month?

**Diagnosis**: What are the key drivers and most significant factors that lead to churn?

**Actionable Insights**: What interventions can be suggested for specific high-risk students?

**Strategy**: What general policies could be implemented to improve overall student retention?

## Project Workflow

This project follows a comprehensive data science pipeline, from data ingestion to model deployment.

**1. Data Cleaning & Preparation:**

- Handle duplicates, missing values (imputation), and outliers.

- Crucially, decode proprietary status codes (ST1, ST2, Adiantado) into meaningful categories.

**2. Database Modeling & ETL (PostgreSQL):**

- Design a Star Schema (Kimball methodology) with a central FatoHistoricoAluno table and dimensions like DimAluno, DimDisciplina, and DimData.

- Build a Python script (SQLAlchemy) to perform the ETL process, loading the cleaned data into the PostgreSQL database.

**3. Feature Engineering (SQL & Pandas):**

- Use SQL Window Functions during data extraction to create historical features efficiently (e.g., LAG(LicaoAtual), AVG(FolhasUtilizadas) over 3 months, COUNT(MesesNoEstagio)).

- Use Pandas to engineer more complex features (e.g., progress velocity, performance consistency).

**4 Exploratory Data Analysis (EDA):**

- Define churn operationally (e.g., a student active in month M who does not appear in M+1 and is not 'Concluinte').

- Analyze and profile different churn segments ("Good Churn" vs. "Bad Churn").

- Visualize relationships between features and churn probability.

**5. Predictive Modeling (Scikit-learn):**

- Target: Binary classification (Will churn = 1, Will not churn = 0) for the next month.

- Validation: Use TimeSeriesSplit cross-validation to respect the temporal nature of the data and prevent look-ahead bias.

- Models: Start with a Logistic Regression (baseline) and compare against Random Forest and XGBoost for performance and interpretability.

- Evaluation: Focus on AUC-ROC, Precision, and Recall for the minority (churn) class.

**6. Insights & Visualization (Power BI):**

- Identify key churn drivers using model-agnostic methods (e.g., SHAP values).

- Create an interactive Power BI dashboard to:

- List students currently at high risk of churning.

- Visualize the primary factors contributing to their risk.

- Display overall retention KPIs.

**7. Model Deployment (Azure):**

- Save the final trained model (joblib).

- Develop a serverless API using Azure Functions that takes a student's current features as a JSON input and returns their real-time churn probability.

## 1. Data Cleaning & Preparation

## 2. Database Modeling & ETL (PostgreSQL)

## 3. Feature Engineering (SQL & Pandas)

## 4. Exploratory Data Analysis (EDA)

## 5. Predictive Modeling

## 6. Insights & Visualization (Power BI)

## 7. Model Deployment (Azure)


