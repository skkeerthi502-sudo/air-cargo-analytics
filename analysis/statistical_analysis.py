import pandas as pd
from scipy.stats import ttest_ind, mannwhitneyu

from analysis.data_cleaning import load_data, clean_data


def perform_hypothesis_testing(df):

    # Prepare required columns
    df["Cargo Metric TONS"] = pd.to_numeric(
        df["Cargo Metric TONS"],
        errors="coerce"
    )

    df["GEO Summary"] = (
        df["GEO Summary"].astype(str).str.strip()
    )

    df = df.dropna(
        subset=["Cargo Metric TONS", "GEO Summary"]
    )

    # Separate Domestic and International cargo
    domestic = df.loc[
        df["GEO Summary"].str.lower() == "domestic",
        "Cargo Metric TONS"
    ]

    international = df.loc[
        df["GEO Summary"].str.lower() == "international",
        "Cargo Metric TONS"
    ]

    if len(domestic) < 2 or len(international) < 2:
        raise ValueError(
            "Insufficient Domestic or International records."
        )

    # Hypotheses
    # H0: Domestic and International mean cargo volumes are equal.
    # H1: Domestic and International mean cargo volumes are different.

    # 1. Welch's Independent Samples T-Test
    t_statistic, t_p_value = ttest_ind(
        domestic,
        international,
        equal_var=False
    )

    # 2. Mann-Whitney U Test
    u_statistic, u_p_value = mannwhitneyu(
        domestic,
        international,
        alternative="two-sided"
    )

    # Significance level
    alpha = 0.05

    # Results
    results = {

        "Domestic Records": len(domestic),

        "International Records": len(international),

        "Domestic Mean Cargo (MT)": domestic.mean(),

        "International Mean Cargo (MT)": international.mean(),

        "Domestic Median Cargo (MT)": domestic.median(),

        "International Median Cargo (MT)": international.median(),

        "T-Test Statistic": t_statistic,

        "T-Test P-Value": t_p_value,

        "Mann-Whitney U Statistic": u_statistic,

        "Mann-Whitney P-Value": u_p_value,

        "Significance Level": alpha
    }

    return results


if __name__ == "__main__":

    df = load_data()

    if df is not None:

        df = clean_data(df)

        results = perform_hypothesis_testing(df)

        print("\n===================================")
        print("AIR CARGO HYPOTHESIS TESTING")
        print("===================================")

        print("\n--- HYPOTHESES ---")

        print("H0: Domestic and International mean cargo volumes are equal.")

        print("H1: Domestic and International mean cargo volumes are different.")

        print("\n--- STATISTICAL RESULTS ---")

        for metric, value in results.items():

            if isinstance(value, float):

                if "P-Value" in metric:
                    print(f"{metric}: {value:.6e}")

                else:
                    print(f"{metric}: {value:.4f}")

            else:
                print(f"{metric}: {value}")

        print("\n--- HYPOTHESIS TEST INTERPRETATION ---")

        if results["T-Test P-Value"] < 0.05:

            print(
                "Welch's T-Test: Reject H0. "
                "A statistically significant difference exists "
                "between the two group means."
            )

        else:

            print(
                "Welch's T-Test: Fail to reject H0. "
                "There is insufficient evidence of a difference "
                "between the two group means."
            )

        if results["Mann-Whitney P-Value"] < 0.05:

            print(
                "Mann-Whitney Test: Reject H0. "
                "The two groups show a statistically significant "
                "difference in their distributions."
            )

        else:

            print(
                "Mann-Whitney Test: Fail to reject H0. "
                "There is insufficient evidence of a difference "
                "between the two groups' distributions."
            )

        print("\nHYPOTHESIS TESTING COMPLETED SUCCESSFULLY!")