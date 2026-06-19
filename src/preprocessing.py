import numpy as np
import pandas as pd


def transform_target_variable(df, target_column="FinalExpansion"):
    """
    Applies a log(x + 1) transformation to the target variable to mitigate
    the effects of distribution skewness in clinical measurements.
    """
    processed_df = df.copy()
    log_col_name = f"log_{target_column}"

    # Programmatic log1p transformation mimicking R's log1p framework
    processed_df[log_col_name] = np.log1p(processed_df[target_column])

    print(
        f"[INFO] Robustness check preparation: Target variable transformed into '{log_col_name}'.")
    return processed_df
