import pandas as pd

from analysis.upload_data import process_uploaded_file


# ==========================================
# CREATE SAMPLE AIR CARGO DATASET
# ==========================================

sample_data = {

    "Activity Period": [202401, 202402, 202403],

    "Activity Period Start Date": [
        "2024-01-01",
        "2024-02-01",
        "2024-03-01"
    ],

    "Operating Airline": [
        "Airline A",
        "Airline B",
        "Airline A"
    ],

    "Operating Airline IATA Code": [
        "AA", "BB", "AA"
    ],

    "Published Airline": [
        "Airline A",
        "Airline B",
        "Airline A"
    ],

    "Published Airline IATA Code": [
        "AA", "BB", "AA"
    ],

    "GEO Summary": [
        "Domestic",
        "International",
        "Domestic"
    ],

    "GEO Region": [
        "US",
        "Asia",
        "US"
    ],

    "Activity Type Code": [
        "Enplaned",
        "Enplaned",
        "Deplaned"
    ],

    "Cargo Type Code": [
        "Cargo",
        "Cargo",
        "Cargo"
    ],

    "Cargo Aircraft Type": [
        "Passenger",
        "Freighter",
        "Passenger"
    ],

    "Cargo Weight LBS": [
        1000,
        2000,
        1500
    ],

    "Cargo Metric TONS": [
        0.4536,
        0.9072,
        0.6804
    ]
}


# ==========================================
# SAVE SAMPLE CSV
# ==========================================

df = pd.DataFrame(sample_data)

df.to_csv(
    "sample_air_cargo.csv",
    index=False
)


# ==========================================
# TEST UPLOAD PROCESSING
# ==========================================

with open("sample_air_cargo.csv", "rb") as file:

    cleaned_df, summary = process_uploaded_file(file)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n========== UPLOAD TEST SUCCESSFUL ==========")

print("\nUPLOAD SUMMARY:")

for key, value in summary.items():

    print(f"{key}: {value}")


print("\nCLEANED DATASET:")

print(cleaned_df)


print("\nDATA TYPES:")

print(cleaned_df.dtypes)

print("\n============================================")