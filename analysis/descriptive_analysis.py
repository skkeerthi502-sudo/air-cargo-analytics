import pandas as pd
from analysis.data_cleaning import load_data, clean_data


def calculate_descriptive_statistics(df):

    cargo_column = "Cargo Metric TONS"

    if cargo_column not in df.columns:
        raise ValueError(f"Column '{cargo_column}' not found.")

    cargo_data = pd.to_numeric(
        df[cargo_column], errors="coerce"
    ).dropna()

    if cargo_data.empty:
        raise ValueError("No valid cargo data available.")

    mode_values = cargo_data.mode()

    statistics = {
        "Total Records": cargo_data.count(),
        "Mean": cargo_data.mean(),
        "Median": cargo_data.median(),
        "Mode": mode_values.tolist(),
        "Standard Deviation": cargo_data.std(),
        "Variance": cargo_data.var(),
        "Minimum": cargo_data.min(),
        "Maximum": cargo_data.max(),
        "Range": cargo_data.max() - cargo_data.min(),
        "Q1 (25%)": cargo_data.quantile(0.25),
        "Q2 (50%)": cargo_data.quantile(0.50),
        "Q3 (75%)": cargo_data.quantile(0.75),
        "Skewness": cargo_data.skew()
    }

    return statistics


if __name__ == "__main__":

    df = load_data()

    if df is not None:

        df = clean_data(df)

        results = calculate_descriptive_statistics(df)

        print("\n===================================")
        print("AIR CARGO DESCRIPTIVE STATISTICS")
        print("===================================")

        for metric, value in results.items():

            if isinstance(value, float):
                print(f"{metric}: {value:.4f}")

            else:
                print(f"{metric}: {value}")

        print("\nSTATISTICAL ANALYSIS COMPLETED!")