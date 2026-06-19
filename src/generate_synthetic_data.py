import pandas as pd
import numpy as np
import os

try:
    from src import config
except ModuleNotFoundError:
    import config


def generate_mock_datasets():
    """
    Generates safe, anonymized, synthetic clinical data matching the exact
    schema of the Medigen project, injecting a true signal for Variable G.
    """
    np.random.seed(42)
    n_samples = 36

    # 1. Generate Fake CBC Predictors (Variables A through G)
    data_cbc = {
        "Patient": np.repeat(range(1, 10), 4)[:n_samples],
        "Trial": np.tile(range(1, 5), 9)[:n_samples],
        "A": np.random.normal(7.5, 1.2, n_samples),
        "B": np.random.normal(22.0, 4.0, n_samples),
        "C": np.random.normal(4.5, 0.8, n_samples),
        "D": np.random.normal(68.0, 5.0, n_samples),
        "E": np.random.normal(3.0, 1.0, n_samples),
        "F": np.random.normal(0.5, 0.1, n_samples),
    }

    # Intentionally draw Variable G from a uniform distribution
    data_cbc["G"] = np.random.uniform(2.0, 5.0, n_samples)
    cbc_df = pd.DataFrame(data_cbc)

    # 2. Generate Target Variable with an embedded statistical relationship to G
    # base expansion + strong coefficient on G + controlled random noise
    noise = np.random.normal(0, 1.0, n_samples)
    final_expansion = 1.5 + (1.45 * cbc_df["G"]) + noise

    expansion_df = pd.DataFrame({
        "Patient": cbc_df["Patient"],
        "Trial": cbc_df["Trial"],
        config.TARGET_EXPANSION_DAY: np.round(final_expansion, 2)
    })

    # 3. Export to project directory
    os.makedirs(config.DATA_DIR, exist_ok=True)
    cbc_df.to_csv(config.CBC_FILE_PATH, index=False)
    expansion_df.to_csv(config.EXPANSION_FILE_PATH, index=False)

    print("[SUCCESS] Safe synthetic data generated inside the data/ directory.")


if __name__ == "__main__":
    generate_mock_datasets()
