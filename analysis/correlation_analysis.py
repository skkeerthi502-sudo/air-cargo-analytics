import pandas as pd
from scipy.stats import pearsonr, spearmanr

from analysis.data_cleaning import load_data, clean_data


def perform_correlation_analysis(df):

    # Convert required columns to numeric
    df["Cargo Metric TONS"] = pd.to_numeric(
        df["Cargo Metric TONS"], errors="coerce"
    )

    df["Cargo Weight LBS"] = pd.to_numeric(
        df["Cargo Weight LBS"], errors="coerce"
    )

    # --------------------------------
    # 1. Cargo Weight vs Cargo Tons
    # --------------------------------

    cargo_data = df[
        ["Cargo Weight LBS", "Cargo Metric TONS"]
    ].dropna()

    pearson_cargo, _ = pearsonr(
        cargo_data["Cargo Weight LBS"],
        cargo_data["Cargo Metric TONS"]
    )

    # --------------------------------
    # 2. Monthly Cargo vs Activity Records
    # --------------------------------

    df["Month"] = (
        df["Activity Period Start Date"].dt.to_period("M")
    )

    monthly_data = df.groupby("Month").agg(
        Total_Cargo_TONS=("Cargo Metric TONS", "sum"),
        Activity_Records=("Cargo Metric TONS", "count")
    ).reset_index()

    pearson_monthly, pearson_p = pearsonr(
        monthly_data["Total_Cargo_TONS"],
        monthly_data["Activity_Records"]
    )

    spearman_monthly, spearman_p = spearmanr(
        monthly_data["Total_Cargo_TONS"],
        monthly_data["Activity_Records"]
    )

    return {
        "Cargo Weight vs Cargo Tons Correlation": pearson_cargo,
        "Monthly Cargo vs Activity Records - Pearson": pearson_monthly,
        "Monthly Cargo vs Activity Records - Spearman": spearman_monthly,
        "Pearson P-value": pearson_p,
        "Spearman P-value": spearman_p,
        "Total Months Analysed": len(monthly_data)
    }


if __name__ == "__main__":

    df = load_data()

    if df is not None:

        df = clean_data(df)

        results = perform_correlation_analysis(df)

        print("\n===================================")
        print("AIR CARGO CORRELATION ANALYSIS")
        print("===================================")

        for metric, value in results.items():

            if isinstance(value, float):
                print(f"{metric}: {value:.4f}")

            else:
                print(f"{metric}: {value}")

        print("\nCORRELATION ANALYSIS COMPLETED!")