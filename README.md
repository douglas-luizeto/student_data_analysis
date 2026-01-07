# 📊 Student Retention & Churn Analysis: A Data-Driven Case Study

🇧🇷 [Resumo Executivo em Português](#resumo-executivo-pt-br) | 🇺🇸 [Executive Summary in English](#executive-summary-en)

## 🔗 Live Dashboard

Check out the interactive visualizations on Tableau Public:
👉 [View Full Dashboard Here](https://public.tableau.com/views/student_data_analysis/1_BaseErosion?:language=pt-BR&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## 🇧🇷 Resumo Executivo <a name="resumo-executivo-pt-br"></a>

Este projeto investiga a dinâmica de retenção de alunos de uma unidade Kumon entre **Fevereiro de 2022 e Setembro de 2025**. A análise identifica que a unidade enfrenta uma **"Erosão de Base"**, onde a saída de alunos antigos (Legacy) não está sendo compensada pela retenção de novos alunos (Orgânicos).

### Principais Descobertas:

**Mortalidade Infantil:** **52% dos novos alunos** desistem nos primeiros **6 meses**.

**Gargalo Pedagógico:** Matemática representa **49% do "Bad Churn"**, com risco crítico na transição para a adolescência (11-15 anos).

**A "Bala de Prata":** **75% da evasão** em Matemática ocorre em alunos que estão mais de **2,5 estágios atrás de sua série escolar**. O "gap" pedagógico é o maior preditor de desmotivação.

**Paradoxo da Consistência:** Alunos prestes a desistir apresentam uma estabilidade mecânica (**"Inércia"**), enquanto alunos estáveis variam mais o ritmo devido aos desafios reais do material.

**Recomendações:** Gestão agressiva de expectativas no onboarding, intervenção obrigatória no 3º mês de matrícula e monitoramento de alunos com baixa variabilidade de desempenho (CV3).

## 🎯 Project Overview <a id="executive-summary-en"></a>

This project investigates the student retention dynamics of a Kumon Learning Center from **February 2022 to September 2025**. The goal is to identify the **root causes of Bad Churn** (premature dropout) and provide actionable strategic recommendations to **stabilize the student base** and ensure **long-term growth**.

## 🛠️ Tech Stack & Methodology

**Data Engineering:** PostgreSQL (Window Functions, CTEs, Feature Engineering).

**Database Automation:** Python (Schema creation and data population scripts).

**Data Visualization:** Tableau (Cohort Analysis, Survival Curves, Performance Dashboards).

**Framework:** Exploratory Data Analysis (EDA) based on Tukey’s principles, focusing on robust statistics (Medians, IQR, and Coefficient of Variation).

## 📋 Detailed Analysis

### Part 1: The Global Problem - "Base Erosion"

The center faces a critical challenge of student base erosion. Although it received **132 "Legacy" students** via transfer in 2022, the subsequent organic growth (**223 enrollments**) has not been sufficient to compensate for departures.

**Accumulated Churn: 69%** (of which **55%** is classified as **Bad Churn**).

**Infant Mortality: 52%** of new organic students drop out within the first **6 months**.

**Key Finding:** The center is consuming its legacy capital without successfully maturing the new intake of students.

### Part 2: Demographic Profiling - "Who is leaving?"

**Primary Audience: 74%** of the base consists of **school-age children and teenagers**.

**The Bottlenecks:** Mathematics accounts for **44%** of all bad churn in the primary audience, while Portuguese accounts for **16%**.

**Pedagogical "Walls":** Retention drops sharply at specific stages: Math Stage B (**Column Addition/Subtraction**), Portuguese Stage AI (**Post-literacy**), and Japanese Stages 4A-2A (**Initial Literacy**).

### Part 3: Velocity Analysis - "The 6 Months Window"

A "Critical Leakage" occurs during the second quarter of enrollment.

**IC3 (3-Month Continuity): 71%** average.

**IC9 (9-Month Continuity):** Drops to **51%**.

**Median Tenure: 3 to 6 months.**

**Insight:** Initial onboarding works, but the transition to "new content" fails to sustain engagement, resulting in a **Lifetime Value (LTV) insufficient** for profitability.

### Part 4: Causal Analysis - "The Silver Bullet"

**The Silver Bullet (Stages until Advanced):** **75%** of bad churn in Math occurs in students who are more than **2.5 stages behind** their school grade level.

**Starting Behind:** **78%** of Math students begin more than **4 stages behind** their grade level.

**Reactive Churn:** **91%** of dropouts leave before completing **6 months of stagnation.** They quit reactively at the first sign of increased difficulty.

**The Consistency Paradox:** Bad churn shows a lower CV3 (**0.39**) than natural churn (**0.71**), indicating "Inertia Stability" (mechanical study without challenge).

## ⚙️ Data Pipeline & Engineering

To enable this analysis, a custom data pipeline was developed:

**Schema Design:** A star-schema database was implemented in PostgreSQL via Python scripts to ensure data integrity and query performance.

**Feature Engineering (features.sql):**

**Window Functions:** Used to calculate months_enrolled, continuity indexes (IC3, IC9), avg_sheets_3 (lagged averages), and cv_3.

**Advanced Logic:** Implemented the bad_churn logic based on age/subject/stage-grade cutoffs and the stages_to_adv metric to measure the school gap.

## 💡 Strategic Recommendations

**Expectation Management:** Visual "Victory Line" schedules for students with a gap > 2.5 stages.

**Month 3 Intervention:** Mandatory feedback session to address the "Critical Leakage" period.

**"Suspicious Consistency" Alert:** Monitor students with very low CV3 (**< 0.40**) as a red flag for disengagement.

**Pedagogical "Wall" Protocol:** Extra support during Math Stage B and Portuguese Stage AI.

**Japanese Engagement:** Weekly celebratory feedback for beginners (Stages 4A-2A).
___

Developed as part of the "Student Data Analysis" Portfolio Project.