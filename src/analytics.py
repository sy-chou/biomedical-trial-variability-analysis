import statsmodels.api as sm
import os

try:
    from src import config
except ModuleNotFoundError:
    import config


def run_multivariable_regression(df, target_column):
    """
    Fits an Ordinary Least Squares (OLS) multivariable regression model
    using designated clinical predictors against a specified endpoint.
    """
    # Isolate predictors and append an intercept term (required by statsmodels)
    X = df[config.CLINICAL_PREDICTORS]
    X = sm.add_constant(X)

    y = df[target_column]

    # Initialize and fit the OLS architecture
    model = sm.OLS(y, X).fit()
    return model


def save_modeling_summary(raw_model, log_model):
    """
    Formats and writes the statistical results to a text summary file,
    demonstrating reproducible logging patterns.
    """
    output_path = os.path.join(config.RESULTS_DIR, "metrics_summary.txt")

    os.makedirs(config.RESULTS_DIR, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(
            "=====================================================================\n")
        f.write(
            "      BIOMEDICAL TRIAL PIPELINE: MULTIVARIABLE REGRESSION RESULTS     \n")
        f.write(
            "=====================================================================\n\n")
        f.write("--- MODEL 1: RAW TARGET SCALE ANCESTRY ---\n")
        f.write(raw_model.summary().as_text())
        f.write("\n\n")
        f.write("--- MODEL 2: LOG-TRANSFORMED TARGET SCALE (ROBUSTNESS CHECK) ---\n")
        f.write(log_model.summary().as_text())

    print(
        f"[SUCCESS] Performance data and summary charts written to: {output_path}")
