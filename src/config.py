import os

# Base directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
FIGURES_DIR = os.path.join(RESULTS_DIR, "figures")

# Core Data File Paths
CBC_FILE_PATH = os.path.join(DATA_DIR, "cbc.csv")
EXPANSION_FILE_PATH = os.path.join(DATA_DIR, "expansionFold.csv")

# Pipeline Parameters
# Quantifies the primary clinical endpoint
TARGET_EXPANSION_DAY = "Day7_ExpansionFold"
SIGNIFICANCE_ALPHA = 0.05

# Feature Groups
CLINICAL_PREDICTORS = ["A", "B", "C", "D", "E", "F", "G"]
