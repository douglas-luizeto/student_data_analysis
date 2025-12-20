Student Churn Analysis | Kumon Center

🇧🇷 Leia um resumo em Português | 🇺🇸 Jump to English Description

<div id="resumo-executivo-pt"></div>

🇧🇷 Resumo Executivo

Este projeto analisa a evasão de alunos (churn) em uma unidade do Kumon, utilizando dados históricos reais. O objetivo é diferenciar saídas naturais (conclusão de curso) de saídas problemáticas ("Bad Churn") e identificar padrões comportamentais que antecedem a desistência.
Stack: PostgreSQL (Engenharia de Features), Tableau (Dashboard Interativo) e Python (Modelagem Preditiva).

<div id="project-description"></div>

1. Project Description

This project focuses on solving a critical business problem for an educational center: student retention. Using real-world data from a Kumon franchise, we aimed to move beyond simple churn rates and understand the quality of student exits.

The solution was built using a hybrid architecture:

Data Engineering (SQL): Construction of a Star Schema and complex feature engineering (Window Functions) to create a robust Analytical Base Table (ABT).

Visual Analytics (Tableau): An interactive dashboard to monitor retention trends and student profiles.

Predictive Modeling (Python): A machine learning model to predict the probability of "Bad Churn" for active students.

2. Business Questions

The analysis is driven by five key strategic questions:

Overview: What is the real scale of the churn problem? Is it seasonal?

Target Definition: How can we algorithmically differentiate a "Natural Churn" (e.g., a student graduating) from a "Bad Churn" (premature dropout)?

Performance Correlation: Do students leave because they are struggling? How does consistency impact retention?

Profiling: Are specific demographics (e.g., adults, early childhood) more prone to churn?

Prediction: Can we flag at-risk students before they leave?

3. Data Modeling & Engineering

The raw data was transformed into a Star Schema in PostgreSQL to ensure data integrity and query performance.

Fact Table: fact_student_performance (Monthly snapshot of progress).

Dimensions: dim_student, dim_subject, dim_date, dim_grade.

To feed the BI and ML layers, an Analytical Base Table (ABT) was created using advanced SQL (Window Functions). This approach moved the "heavy lifting" to the database, ensuring consistency across reports.

4. Feature Rationale

Instead of relying solely on raw metrics (e.g., "number of sheets"), we engineered features to capture student behavior:

Feature

Rationale

bad_churn (Target)

A binary flag that identifies dropouts who left before reaching a significant milestone (e.g., Math Stage I), separating them from successful graduates.

consistency_cv

The Coefficient of Variation ($\sigma/\mu$) of sheets completed in the last 3 months. Measures stability. High variation suggests erratic study habits.

is_stalled

A flag indicating if a student failed to advance to a new lesson for consecutive months, signaling learning plateaus.

stages_to_adv

The distance between the student's current stage and the expected stage for their school grade. Measures the "gap" to the goal of being an advanced student.

life_stage

Categorical binning of age (Early Childhood, Primary, Adult) to capture life-cycle specific risks.

5. EDA & Insights (Tableau)

The exploratory analysis revealed that churn is not random. It is highly correlated with specific performance triggers.

📊 [Click here to view the Interactive Dashboard on Tableau Public] (Insert Link Here)

Key Insights:

The "Silent" Stagnation: Students who stall (do not advance lessons) for 2+ months have a drastically higher probability of churning, even if they continue to submit homework.

The Gap Trap: In Math, students who fall more than 2 stages behind their school grade level (stages_to_adv < -2) are the most vulnerable group.

Bad Churn Dominance: Over 85% of dropouts in Math and Portuguese were categorized as "Bad Churn," confirming that the center is losing students who have not yet extracted the method's full value.

6. Predictive Model

A Random Forest Classifier was trained to predict the probability of bad_churn in the upcoming month.

Target: bad_churn (1 = Risk, 0 = Safe/Natural Exit)

Key Predictors: stalled_run, cv_3 (Consistency), and stages_to_adv.

Performance:

Recall: [Insert %] (Prioritized metric to minimize false negatives).

AUC-ROC: [Insert Score].

Author: [Seu Nome]
Portfolio Project