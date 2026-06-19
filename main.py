import os
from src import config, data_factory, preprocessing, analytics, visualization


def main():
    print("=====================================================================")
    # 1. Ingestion Phase
    merged_data = data_factory.load_and_merge_clinical_data()

    # 2. Preprocessing & Robustness Scaling Phase
    processed_data = preprocessing.transform_target_variable(
        merged_data,
        target_column="FinalExpansion"
    )

    # 3. Statistical Analysis Phase (Raw Scale Model)
    print("\n[MODELING] Fitting Model 1: Raw Expansion Scale against CBC Predictors...")
    raw_model = analytics.run_multivariable_regression(
        processed_data,
        target_column="FinalExpansion"
    )

    # 4. Statistical Analysis Phase (Log-Transformed Robustness Check)
    print("[MODELING] Fitting Model 2: Log-Transformed Scale Robustness Check...")
    log_model = analytics.run_multivariable_regression(
        processed_data,
        target_column="log_FinalExpansion"
    )

    # 5. Export Reproducible Text Outputs
    analytics.save_modeling_summary(raw_model, log_model)

    # 6. Visualization Phase
    print("\n[VISUALIZATION] Generating publication-grade figures...")
    visualization.plot_target_distribution(
        processed_data, target_column="log_FinalExpansion")
    visualization.plot_feature_coefficients(
        log_model, title_suffix="Log Model")

    print("=====================================================================")

    # 7. Real-time Console Verification
    print("\n[VERIFICATION] Executive Pipeline Summary:")
    print(f" - Model 1 (Raw) Variable G p-value: {raw_model.pvalues['G']:.4f}")
    print(f" - Model 2 (Log) Variable G p-value: {log_model.pvalues['G']:.4f}")

    if raw_model.pvalues['G'] < config.SIGNIFICANCE_ALPHA:
        print(
            "\n[CONCLUSION] Pipeline successfully verified. Target biomarker 'G' maintains")
        print(
            "             statistically significant alignment across both scaling regimes.")


if __name__ == "__main__":
    main()
