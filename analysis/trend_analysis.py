import pandas as pd

from analysis.data_cleaning import load_data, clean_data


# 1. Monthly Cargo Trend
def calculate_monthly_trend(df):

    monthly_data = df.groupby(
        df["Activity Period Start Date"].dt.to_period("M")
    ).agg(
        Total_Cargo_TONS=("Cargo Metric TONS", "sum"),
        Total_Records=("Cargo Metric TONS", "count")
    ).reset_index()

    monthly_data["Month"] = (
        monthly_data["Activity Period Start Date"].astype(str)
    )

    monthly_data["MoM_Growth_Percentage"] = (
        monthly_data["Total_Cargo_TONS"].pct_change() * 100
    )

    return monthly_data


# 2. Yearly Cargo Trend
def calculate_yearly_trend(df):

    yearly_data = df.groupby(
        df["Activity Period Start Date"].dt.year
    ).agg(
        Total_Cargo_TONS=("Cargo Metric TONS", "sum"),
        Total_Records=("Cargo Metric TONS", "count")
    ).reset_index()

    yearly_data.rename(
        columns={"Activity Period Start Date": "Year"},
        inplace=True
    )

    return yearly_data


# 3. Seasonal Monthly Analysis
def calculate_seasonal_trend(df):

    seasonal_data = df.groupby(
        df["Activity Period Start Date"].dt.month
    ).agg(
        Average_Cargo_TONS=("Cargo Metric TONS", "mean"),
        Total_Cargo_TONS=("Cargo Metric TONS", "sum")
    ).reset_index()

    seasonal_data.rename(
        columns={"Activity Period Start Date": "Month_Number"},
        inplace=True
    )

    month_names = {
        1: "January", 2: "February", 3: "March",
        4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September",
        10: "October", 11: "November", 12: "December"
    }

    seasonal_data["Month_Name"] = (
        seasonal_data["Month_Number"].map(month_names)
    )

    return seasonal_data


# 4. Execute Trend Analysis
if __name__ == "__main__":

    df = load_data()

    if df is not None:

        df = clean_data(df)

        df["Cargo Metric TONS"] = pd.to_numeric(
            df["Cargo Metric TONS"], errors="coerce"
        )

        df = df.dropna(
            subset=["Activity Period Start Date", "Cargo Metric TONS"]
        )

        monthly_data = calculate_monthly_trend(df)
        yearly_data = calculate_yearly_trend(df)
        seasonal_data = calculate_seasonal_trend(df)

        print("\n===================================")
        print("AIR CARGO TREND ANALYSIS")
        print("===================================")

        print("\n--- YEAR-WISE CARGO TREND ---")
        print(yearly_data.to_string(index=False))

        print("\n--- FIRST 12 MONTHLY RECORDS ---")
        print(monthly_data.head(12).to_string(index=False))

        print("\n--- MONTH-WISE SEASONAL ANALYSIS ---")
        print(seasonal_data.to_string(index=False))

        print("\n--- HIGHEST CARGO YEAR ---")

        highest_year = yearly_data.loc[
            yearly_data["Total_Cargo_TONS"].idxmax()
        ]

        print(
            f"Year: {int(highest_year['Year'])} | "
            f"Cargo: {highest_year['Total_Cargo_TONS']:.4f} MT"
        )

        print("\n--- HIGHEST AVERAGE CARGO MONTH ---")

        highest_month = seasonal_data.loc[
            seasonal_data["Average_Cargo_TONS"].idxmax()
        ]

        print(
            f"Month: {highest_month['Month_Name']} | "
            f"Average Cargo: "
            f"{highest_month['Average_Cargo_TONS']:.4f} MT"
        )

        print("\nTREND ANALYSIS COMPLETED SUCCESSFULLY!")