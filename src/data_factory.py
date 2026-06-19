import pandas as pd
import sys
import os

# Import pathing rules from our config module
try:
    from src import config
except ModuleNotFoundError:
    import config


def load_and_merge_clinical_data():
    """
    Loads CBC metrics and expansion profiles, verifying files exist,
    and performs a cohort-level inner join on Patient and Trial identifiers.
    """
    # 1. Verification checks
    if not os.path.exists(config.CBC_FILE_PATH) or not os.path.exists(config.EXPANSION_FILE_PATH):
        print(f"[ERROR] Data files not found in target data folder.")
        print(
            f"Looking for:\n - {config.CBC_FILE_PATH}\n - {config.EXPANSION_FILE_PATH}")
        sys.exit(1)

    print("[INFO] Local data assets verified. Initiating parsing pipeline...")

    # 2. Parse delimiters safely (mimicking R's read_delim handling)
    cbc_df = pd.read_csv(config.CBC_FILE_PATH, sep=None, engine='python')
    expansion_df = pd.read_csv(
        config.EXPANSION_FILE_PATH, sep=None, engine='python')

    # 3. Standardize column selections to keep footprint light
    target_day = config.TARGET_EXPANSION_DAY
    columns_to_keep = ["Patient", "Trial", target_day]

    if target_day not in expansion_df.columns:
        raise KeyError(
            f"Target execution day '{target_day}' missing from expansion dataset columns.")

    trimmed_expansion = expansion_df[columns_to_keep].rename(
        columns={target_day: "FinalExpansion"}
    )

    # 4. Cohort-level inner join execution
    merged_cohort = pd.merge(
        cbc_df,
        trimmed_expansion,
        on=["Patient", "Trial"],
        how="inner"
    )

    print(
        f"[SUCCESS] Cohort integration complete. Synchronized matrix shape: {merged_cohort.shape}")
    return merged_cohort


if __name__ == "__main__":
    # Internal module unit-test block
    df = load_and_merge_clinical_data()
    print(df.head(3))
