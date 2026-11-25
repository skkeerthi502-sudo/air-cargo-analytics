import numpy as np
import pandas as pd
from scipy.stats import linregress

from analysis.data_cleaning import load_data, clean_data


def perform_regression_analysis(df):

    # Prepare monthly cargo data
    df["Cargo Metric TONS"] = pd.to_numeric(
        df["Cargo Metric TONS"], errors="coerce"
    )

    monthly_data = df.groupby(
        df["Activity Period Start Date"].dt.to_period("M")
    )["Cargo Metric TONS"].sum().reset_index()

    monthly_data.columns = ["Month", "Total_Cargo_TONS"]

    monthly_data = monthly_data.dropna()

    # Create numerical time index
    monthly_data["Time_Index"] = np.arange(
        len(monthly_data)
    )

    # Chronological 80:20 split
    split_index = int(len(monthly_data) * 0.80)

    train_data = monthly_data.iloc[:split_index]
    test_data = monthly_data.iloc[split_index:]

    # Train Linear Regression Model
    model = linregress(
        train_data["Time_Index"],
        train_data["Total_Cargo_TONS"]
    )

    # Predict test data
    actual = test_data["Total_Cargo_TONS"].to_numpy()

    predicted = (
        model.slope * test_data["Time_Index"].to_numpy()
        + model.intercept
    )

    # Calculate evaluation metrics
    mae = np.mean(np.abs(actual - predicted))

    rmse = np.sqrt(np.mean((actual - predicted) ** 2))

    ss_res = np.sum((actual - predicted) ** 2)

    ss_tot = np.sum((actual - np.mean(actual)) ** 2)

    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else np.nan

    results = {
        "Total Months": len(monthly_data),
        "Training Months": len(train_data),
        "Testing Months": len(test_data),
        "Regression Slope": model.slope,
        "Regression Intercept": model.intercept,
        "Model R-Squared": r2,
        "Mean Absolute Error (MAE)": mae,
        "Root Mean Squared Error (RMSE)": rmse
    }

    return results


if __name__ == "__main__":

    df = load_data()

    if df is not None:

        df = clean_data(df)

        results = perform_regression_analysis(df)

        print("\n===================================")
        print("AIR CARGO REGRESSION ANALYSIS")
        print("===================================")

        for metric, value in results.items():

            if isinstance(value, (float, np.floating)):
                print(f"{metric}: {value:.4f}")

            else:
                print(f"{metric}: {value}")

        print("\nREGRESSION ANALYSIS COMPLETED!")