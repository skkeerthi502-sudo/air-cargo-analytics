import pandas as pd


# ==========================================
# REQUIRED AIR CARGO COLUMNS
# ==========================================

REQUIRED_COLUMNS = [
    "Activity Period",
    "Activity Period Start Date",
    "Operating Airline",
    "Operating Airline IATA Code",
    "Published Airline",
    "Published Airline IATA Code",
    "GEO Summary",
    "GEO Region",
    "Activity Type Code",
    "Cargo Type Code",
    "Cargo Aircraft Type",
    "Cargo Weight LBS",
    "Cargo Metric TONS"
]


# ==========================================
# LOAD UPLOADED CSV / EXCEL FILE
# ==========================================

def load_uploaded_file(uploaded_file):

    file_name = uploaded_file.name.lower()

    try:

        if file_name.endswith(".csv"):

            df = pd.read_csv(uploaded_file)

        elif file_name.endswith(".xlsx"):

            df = pd.read_excel(
                uploaded_file,
                engine="openpyxl"
            )

        else:

            raise ValueError(
                "Unsupported file format. "
                "Please upload CSV or XLSX files."
            )

        return df

    except Exception as error:

        raise ValueError(
            f"Unable to read uploaded file: {error}"
        )


# ==========================================
# VALIDATE DATASET COLUMNS
# ==========================================

def validate_uploaded_data(df):

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Required columns are missing: "
            + ", ".join(missing_columns)
        )

    if df.empty:

        raise ValueError(
            "Uploaded dataset is empty."
        )

    return True


# ==========================================
# CLEAN UPLOADED DATASET
# ==========================================

def clean_uploaded_data(df):

    df = df.copy()

    # Convert date column

    df["Activity Period Start Date"] = pd.to_datetime(
        df["Activity Period Start Date"],
        errors="coerce"
    )

    # Convert numeric columns

    numeric_columns = [
        "Activity Period",
        "Cargo Weight LBS",
        "Cargo Metric TONS"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove invalid dates and cargo values

    df = df.dropna(
        subset=[
            "Activity Period Start Date",
            "Cargo Metric TONS"
        ]
    )

    # Remove negative cargo values

    df = df[
        df["Cargo Metric TONS"] >= 0
    ]

    # Remove duplicate records

    df = df.drop_duplicates()

    # Reset index

    df = df.reset_index(drop=True)

    if df.empty:

        raise ValueError(
            "No valid records available after data cleaning."
        )

    return df


# ==========================================
# COMPLETE UPLOAD PROCESS
# ==========================================

def process_uploaded_file(uploaded_file):

    # Load dataset

    df = load_uploaded_file(uploaded_file)

    # Validate columns

    validate_uploaded_data(df)

    original_records = len(df)

    # Clean dataset

    cleaned_df = clean_uploaded_data(df)

    cleaned_records = len(cleaned_df)

    # Return dataset and summary

    summary = {

        "Original Records": original_records,

        "Cleaned Records": cleaned_records,

        "Removed Records": (
            original_records - cleaned_records
        ),

        "Total Columns": len(cleaned_df.columns)

    }

    return cleaned_df, summary