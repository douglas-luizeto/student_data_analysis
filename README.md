📊 Student Retention & Churn Analysis: A Data-Driven Case Study

🇧🇷 Leia o Resumo Executivo em Português | 🇺🇸 Read the Executive Summary in English

🇧🇷 Resumo Executivo <a name="resumo-executivo-pt-br"></a>

Este projeto investiga a dinâmica de retenção de alunos de uma unidade Kumon entre Fevereiro de 2022 e Setembro de 2025. A análise identifica que a unidade enfrenta uma "Erosão de Base", onde a saída de alunos antigos (Legacy) não está sendo compensada pela retenção de novos alunos (Orgânicos).

Principais Descobertas:

Mortalidade Infantil: 52% dos novos alunos desistem nos primeiros 6 meses.

Gargalo Pedagógico: Matemática representa 49% do "Bad Churn", com risco crítico na transição para a adolescência (11-15 anos).

A "Bala de Prata": 75% da evasão em Matemática ocorre em alunos que estão mais de 2,5 estágios atrás de sua série escolar. O "gap" pedagógico é o maior preditor de desmotivação.

Paradoxo da Consistência: Alunos prestes a desistir apresentam uma estabilidade mecânica ("Inércia"), enquanto alunos estáveis variam mais o ritmo devido aos desafios reais do material.

Recomendações: Gestão agressiva de expectativas no onboarding, intervenção obrigatória no 4º mês de matrícula e monitoramento de alunos com baixa variabilidade de desempenho (CV3).

🎯 Project Overview <a name="executive-summary-en"></a>

This project investigates the student retention dynamics of a Kumon Learning Center from February 2022 to September 2025. The goal is to identify the root causes of Bad Churn (premature dropout) and provide actionable strategic recommendations to stabilize the student base and ensure long-term growth.

🛠️ Tech Stack & Methodology

Data Engineering: PostgreSQL (Window Functions, CTEs, Feature Engineering).

Data Visualization: Tableau (Cohort Analysis, Survival Curves, Performance Dashboards).

Framework: Exploratory Data Analysis (EDA) based on Tukey’s principles, focusing on robust statistics (Medians, IQR, and Coefficient of Variation).

📋 Executive Summary

Part 1: The Global Problem - "Base Erosion"

The center faces a critical challenge of student base erosion. Although it received 132 "Legacy" students via transfer in 2022 (a mature and stable group), the subsequent organic growth (223 enrollments) has not been sufficient to compensate for departures.

Accumulated Churn: 69% (of which 55% is classified as Bad Churn).

Infant Mortality: 52% of new organic students drop out within the first 6 months.

Key Finding: The center is consuming its legacy capital without successfully maturing the new intake of students.

Part 2: Demographic Profiling - "Who is leaving?"

Primary Audience: 74% of the base consists of school-age children and teenagers.

The Math and Literacy Bottlenecks: Mathematics accounts for 44% of all bad churn in the primary audience, while Portuguese accounts for 16% (considering only school-age children). 

Pedagogical "Walls": Retention drops sharply at specific stages:

Math: Stage B (Column Addition/Subtraction).

Portuguese: Stage AI (Post-literacy). Students often leave once they learn to read, failing to perceive the value of advanced interpretation levels.

Japanese: High risk during the initial literacy phase (Stages 4A-2A).

Part 3: Velocity Analysis - "The 90-Day Window"

A "Critical Leakage" occurs during the second quarter of enrollment.

IC3 (3-Month Continuity): 81% average.

IC9 (9-Month Continuity): Drops to 54%.

Median Tenure: 5 to 7 months.

Insight: The initial onboarding works, but the transition to "new content" (heavy study routine) fails to sustain engagement, resulting in a Lifetime Value (LTV) that is insufficient for profitability.

Part 4: Causal Analysis - "The Silver Bullet"

The Consistency Paradox: Bad churn in Math shows a lower CV3 (0.39) than natural churn (0.71). This indicates "Inertia Stability"—students study mechanically without being challenged until they eventually quit.

Reactive Churn: 91% of dropouts leave before completing 6 months of stagnation. They don't stay long enough to be "bored"; they quit reactively at the first sign of increased difficulty.

The Silver Bullet (Distance to Advanced): 75% of bad churn in Math occurs in students who are more than 2.5 stages behind their school grade level. The pedagogical gap is the primary driver of demotivation.

💡 Strategic Recommendations

Expectation Management (Gap Focus): Implement a "Victory Line" visual schedule for students with a school gap > 2.5 stages to celebrate immediate progress.

Month 4 Intervention: Mandatory feedback session for all organic students at the 4-month mark to address the "Critical Leakage" identified.

"Suspicious Consistency" Alert: Monitor students with very low CV3 (< 0.40). Lack of variance in early stages is a red flag for latent disengagement.

Pedagogical "Wall" Protocol: Extra support and adjusted workload when entering Math Stages B and E, and Portuguese Stage AI.

Post-Literacy Marketing (Portuguese): Internal campaign highlighting the benefits of "Fluency and Interpretation" once basic literacy is achieved.

Japanese Engagement: Weekly celebratory feedback for beginners (4A-2A) to mitigate the high cognitive cost of learning new scripts.

🚧 Current Status

The project is currently transitioning from Data Engineering & Diagnosis to the Visualization Phase. Future work includes building interactive Tableau dashboards to support these findings.

Developed as part of the "Student Data Analysis" Project

------------------------------------------

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