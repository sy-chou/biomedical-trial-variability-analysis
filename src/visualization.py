import matplotlib.pyplot as plt
import seaborn as sns
import os

try:
    from src import config
except ModuleNotFoundError:
    import config


def plot_target_distribution(df, target_column="log_FinalExpansion"):
    """
    Generates a publication-grade histogram of the target variable to visually
    validate the normalization of the distribution.
    """
    os.makedirs(config.FIGURES_DIR, exist_ok=True)

    # Set a clean, academic style
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 5))

    # Plot histogram with a Kernel Density Estimate (KDE) line
    sns.histplot(df[target_column], bins=10, kde=True,
                 color="#4C72B0", edgecolor="black")

    plt.title(f"Distribution of {target_column} (Normalized)",
              fontsize=14, pad=15, fontweight='bold')
    plt.xlabel("Log-Transformed Expansion Fold", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.tight_layout()

    output_path = os.path.join(config.FIGURES_DIR, "target_distribution.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"[VISUALIZATION] Distribution plot saved to: {output_path}")


def plot_feature_coefficients(model, title_suffix="Log Model"):
    """
    Creates a coefficient impact plot (Forest Plot) for the OLS model, 
    visually highlighting statistical significance and confidence intervals.
    """
    os.makedirs(config.FIGURES_DIR, exist_ok=True)
    sns.set_theme(style="whitegrid")

    # Extract coefficients and 95% confidence intervals, dropping the intercept
    params = model.params.drop("const")
    conf = model.conf_int().drop("const")
    errors = params - conf[0]
    pvalues = model.pvalues.drop("const")

    plt.figure(figsize=(9, 5))

    # Plot the error bars
    plt.errorbar(
        x=params.index,
        y=params.values,
        yerr=errors.values,
        fmt='o',
        color='#333333',
        ecolor='gray',
        capsize=5,
        markersize=8,
        elinewidth=2
    )

    # Highlight significant variables (p < 0.05) by circling them in red
    for i, (feature, p_val) in enumerate(pvalues.items()):
        if p_val < config.SIGNIFICANCE_ALPHA:
            plt.plot(i, params[feature], 'ro', markersize=12,
                     fillstyle='none', markeredgewidth=2)
            plt.text(i, params[feature] + (errors[feature] * 1.1), f"p={p_val:.3f}",
                     color='red', ha='center', va='bottom', fontweight='bold')

    # Add a horizontal line at 0 (the null hypothesis line)
    plt.axhline(0, color='black', linestyle='--', linewidth=1.5, alpha=0.7)

    plt.title(
        f"Predictor Coefficients on Cell Expansion ({title_suffix})", fontsize=14, pad=15, fontweight='bold')
    plt.xlabel("Clinical Predictors (CBC Variables)", fontsize=12)
    plt.ylabel("Impact on Expansion (Coefficient β)", fontsize=12)
    plt.tight_layout()

    output_filename = f"feature_coefficients_{title_suffix.lower().replace(' ', '_')}.png"
    output_path = os.path.join(config.FIGURES_DIR, output_filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"[VISUALIZATION] Coefficient plot saved to: {output_path}")
