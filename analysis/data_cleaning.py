import pandas as pd
from database.db_connection import get_connection


# 1. Load Data from MySQL
def load_data():

    connection = get_connection()

    if connection is None:
        return None

    query = "SELECT * FROM air_cargo_dataset"

    try:
        df = pd.read_sql(query, connection)
        return df

    finally:
        connection.close()


# 2. Clean and Preprocess Data
def clean_data(df):

    # Convert date columns into datetime format
    df["Activity Period Start Date"] = pd.to_datetime(
        df["Activity Period Start Date"]
    )

    df["data_as_of"] = pd.to_datetime(df["data_as_of"])

    df["data_loaded_at"] = pd.to_datetime(df["data_loaded_at"])

    # Remove duplicate records
    df = df.drop_duplicates()

    return df


# 3. Execute Data Inspection and Cleaning
if __name__ == "__main__":

    df = load_data()

    if df is not None:

        print("\n--- ORIGINAL DATASET SHAPE ---")
        print(df.shape)

        print("\n--- COLUMN NAMES ---")
        print(df.columns.tolist())

        print("\n--- FIRST 5 RECORDS ---")
        print(df.head())

        print("\n--- ORIGINAL DATA TYPES ---")
        print(df.dtypes)

        print("\n--- MISSING VALUES ---")
        print(df.isnull().sum())

        # Apply Data Cleaning
        df = clean_data(df)

        print("\n--- CLEANED DATASET SHAPE ---")
        print(df.shape)

        print("\n--- UPDATED DATA TYPES ---")
        print(df.dtypes)

        print("\n--- DUPLICATE RECORDS ---")
        print(df.duplicated().sum())

        print("\n--- DATA CLEANING COMPLETED SUCCESSFULLY ---")