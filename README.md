# Biomedical Trial Pipeline: Cohort-Level CBC Feature Prioritization via Multivariable Regression

## Overview
This repository contains a modular, production-grade Python pipeline designed to analyze longitudinal patient-level Complete Blood Count (CBC) metrics and prioritize features driving the cellular expansion fold of liver cancer cells. Originally developed as a localized R analysis, this architecture has been completely refactored into a scalable, object-oriented Python pipeline to optimize reproducibility, structural validation, and downstream statistical reporting.

## Research & Clinical Motivation
In cell therapy manufacturing—specifically translational oncological workflows evaluating liver cancer interventions—understanding host baseline biological variability is key to predicting ex vivo cellular manufacturing success. Cellular expansion rates are highly variable across patient cohorts, creating significant challenges for sample scaling and treatment consistency. 

By building a structured framework to screen routine clinical biomarkers (such as CBC counts), this pipeline systematically evaluates whether baseline hematological profiles correlate with expansion dynamics. This enables research teams to transition away from manual, ad-hoc tracking and establish data-driven feature prioritization workflows capable of uncovering translationally relevant clinical associations.

## Computational Pipeline Architecture
Unlike typical monolithic analysis notebooks, this project uses a modular design pattern to ensure that data ingestion, mathematical transformations, and statistical routines are strictly decoupled:

```text
biomedical-trial-variability-analysis/
├── main.py                     # Central workflow orchestration engine
├── requirements.txt            # Isolated dependency version map
├── data/
│   └── README.md               # Data schema definitions
├── src/
│   ├── __init__.py
│   ├── config.py               # Parameterized paths and significance thresholds
│   ├── data_factory.py         # Cohort matching logic and inner-join execution
│   ├── preprocessing.py        # Robustness scaling and log-transformation modules
│   ├── analytics.py            # Multivariable OLS regression execution
│   ├── visualization.py        # Publication-grade figure generation
│   └── generate_synthetic_data.py # Anonymized synthetic data engine
└── results/
    ├── metrics_summary.txt     # Automated output tables
    └── figures/
        ├── target_distribution.png
        └── feature_coefficients_log_model.png
```

## Methods & Statistical Framework
The pipeline executes sequentially through four transparent phases:
1. Cohort-Level Integration: The `data_factory` module loads separate clinical parameter and expansion profiles, running exception-handled data parsing and an inner join across explicit Patient and Trial identifiers to build a synchronized cohort matrix.
2. Standardized Preprocessing & Skew Correction: Because primary cell expansion data is inherently prone to extreme right-skewness and scale distribution variations, the preprocessing module prepares an automatic log-transform refitting regime using a $log(x + 1)$ function to stabilize variance.
3. Multivariable Regression Modeling: Using Ordinary Least Squares (OLS) regression via `statsmodels`, the script fits the independent laboratory features simultaneously against the target variable:

  $$\text{Expansion} = \beta_0 + \beta_1 A + \beta_2 B + \beta_3 C + \beta_4 D + \beta_5 E + \beta_6 F + \beta_7 G + \epsilon$$
  
4. Automated Visual Curation: The system exports high-resolution (300 DPI) data visualizations including a target variable distribution plot and an analytical forest plot mapping predictor coefficients alongside their 95% confidence intervals.

## How to Run & Replicate
1. Initialize the Environment

    Ensure you are running Python 3.12+ inside your terminal, then clone the repository and install the locked dependency footprint:

    ```
    git clone [https://github.com/username/biomedical-trial-variability-analysis.git](https://github.com/username/biomedical-trial-variability-analysis.git)
    cd biomedical-trial-variability-analysis
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2. Generate Safe Demo Data

    Because original clinical data assets are restricted due to privacy protocols, run the synthetic engine to programmatically generate an anonymized dataset matching the project's exact structural schema:

    ```
    python src/generate_synthetic_data.py
    ```
3. Execute the Orchestration Harness

    Run the master driver script to process the data, fit both regression models, write the performance outputs, and export analytical charts:

    ```
    python main.py
    ```

## Results & Verification
Running the pipeline dynamically logs standard text results and generates two visual artifacts:
* Statistical Reporting (`results/metrics_summary.txt`): The output verifies that across both scaling regimes, a single primary feature—Variable G—maintains a robust, highly significant positive correlation with cellular expansion.
  * In the raw scale model, Variable G displays a coefficient of 1.47 ($p = 0.029$).
  * In the log-transformed robustness check, Variable G maintains its predictive strength with a coefficient of 0.25 ($p = 0.018$).
* Visual Artifacts (`results/figures/`): `target_distribution.png` confirms successful skew normalization via target logging.
  * `feature_coefficients_log_model.png` highlights the isolated significance of Variable G relative to the rest of the cohort.

## Limitations & Future Directions
* Sample Size Constraints: The initial cohort size ($n = 36$) limits the overall power of the multivariable OLS approach, yielding a modest adjusted $R^2 \approx 0.11\text{–}0.12$. Future variations could evaluate regularization constraints (Ridge/Lasso) to manage potential multi-collinearity among hematological parameters.
* Multi-Omics Integration: While routine laboratory features offer strong foundational indicators, true predictive capacity in precision medicine requires blending these metrics with molecular layers, such as single-cell RNA sequencing (scRNA-seq) or spatial profiling of the tumor microenvironment.

## Data Availability & Confidentiality Statement
To comply with strict corporate confidentiality and patient privacy standards, no proprietary or patient-level data is stored in this repository. All structural verifications and execution scripts operate natively on programmatically simulated datasets using the provided `generate_synthetic_data.py` framework.
