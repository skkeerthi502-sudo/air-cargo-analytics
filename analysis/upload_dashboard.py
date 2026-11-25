import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


# ==========================================
# UPLOADED DATASET DASHBOARD
# ==========================================

def render_upload_dashboard(df, summary):

    df = df.copy()

    # --------------------------------------
    # BACK BUTTON
    # --------------------------------------

    if st.button("← Back to Original Dashboard"):

        return True

    st.markdown("---")

    st.title("📊 Uploaded Dataset Analytics")

    st.caption(
        "Independent analysis of your uploaded Air Cargo dataset"
    )

    # --------------------------------------
    # SIDEBAR FILTERS
    # --------------------------------------

    st.sidebar.markdown("## 📂 Uploaded Dataset Filters")

    df["Year"] = (
        df["Activity Period Start Date"].dt.year
    )

    available_years = sorted(
        df["Year"].dropna().unique().tolist()
    )

    selected_years = st.sidebar.multiselect(
        "Select Year",
        available_years,
        default=available_years
    )

    airlines = sorted(
        df["Operating Airline"].dropna().unique().tolist()
    )

    selected_airlines = st.sidebar.multiselect(
        "Operating Airline",
        airlines,
        default=airlines
    )

    geo_options = sorted(
        df["GEO Summary"].dropna().unique().tolist()
    )

    selected_geo = st.sidebar.multiselect(
        "Geographical Summary",
        geo_options,
        default=geo_options
    )

    region_options = sorted(
        df["GEO Region"].dropna().unique().tolist()
    )

    selected_regions = st.sidebar.multiselect(
        "GEO Region",
        region_options,
        default=region_options
    )

    aircraft_options = sorted(
        df["Cargo Aircraft Type"].dropna().unique().tolist()
    )

    selected_aircraft = st.sidebar.multiselect(
        "Cargo Aircraft Type",
        aircraft_options,
        default=aircraft_options
    )

    # --------------------------------------
    # APPLY FILTERS
    # --------------------------------------

    filtered_df = df[
        (df["Year"].isin(selected_years))
        &
        (df["Operating Airline"].isin(selected_airlines))
        &
        (df["GEO Summary"].isin(selected_geo))
        &
        (df["GEO Region"].isin(selected_regions))
        &
        (df["Cargo Aircraft Type"].isin(selected_aircraft))
    ].copy()

    if filtered_df.empty:

        st.warning(
            "No records found for the selected filters."
        )

        return False

    # --------------------------------------
    # UPLOAD SUMMARY
    # --------------------------------------

    st.markdown("### 📁 Upload Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Original Records",
        f"{summary['Original Records']:,}"
    )

    col2.metric(
        "Cleaned Records",
        f"{summary['Cleaned Records']:,}"
    )

    col3.metric(
        "Removed Records",
        f"{summary['Removed Records']:,}"
    )

    col4.metric(
        "Total Columns",
        summary["Total Columns"]
    )

    st.markdown("---")

    # --------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------

    total_cargo = filtered_df["Cargo Metric TONS"].sum()

    total_records = len(filtered_df)

    total_airlines = filtered_df[
        "Operating Airline"
    ].nunique()

    total_regions = filtered_df[
        "GEO Region"
    ].nunique()

    domestic_cargo = filtered_df.loc[
        filtered_df["GEO Summary"].str.lower() == "domestic",
        "Cargo Metric TONS"
    ].sum()

    international_cargo = filtered_df.loc[
        filtered_df["GEO Summary"].str.lower() == "international",
        "Cargo Metric TONS"
    ].sum()

    # --------------------------------------
    # KPI DISPLAY
    # --------------------------------------

    st.markdown("## 📌 Key Performance Indicators")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Cargo Volume",
        f"{total_cargo:,.2f} MT"
    )

    col2.metric(
        "Total Records",
        f"{total_records:,}"
    )

    col3.metric(
        "Operating Airlines",
        total_airlines
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Geographical Regions",
        total_regions
    )

    col5.metric(
        "Domestic Cargo",
        f"{domestic_cargo:,.2f} MT"
    )

    col6.metric(
        "International Cargo",
        f"{international_cargo:,.2f} MT"
    )

    st.markdown("---")

    # ======================================
    # TREND ANALYSIS
    # ======================================

    st.markdown("## 📈 Cargo Trend Analysis")

    yearly_data = (
        filtered_df
        .groupby("Year", as_index=False)
        ["Cargo Metric TONS"]
        .sum()
    )

    monthly_data = (
        filtered_df
        .groupby(
            filtered_df["Activity Period Start Date"].dt.to_period("M")
        )
        ["Cargo Metric TONS"]
        .sum()
        .reset_index()
    )

    monthly_data.columns = [
        "Month",
        "Cargo Metric TONS"
    ]

    monthly_data["Month"] = (
        monthly_data["Month"].astype(str)
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            yearly_data,
            x="Year",
            y="Cargo Metric TONS",
            title="Yearly Cargo Volume",
            text_auto=".2f"
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Year",
            yaxis_title="Cargo Volume (MT)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.line(
            monthly_data,
            x="Month",
            y="Cargo Metric TONS",
            title="Monthly Cargo Trend",
            markers=True
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Month",
            yaxis_title="Cargo Volume (MT)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ======================================
    # DOMESTIC VS INTERNATIONAL
    # ======================================

    st.markdown("---")

    st.markdown("## 🌍 Domestic vs International Analysis")

    geo_data = (
        filtered_df
        .groupby("GEO Summary", as_index=False)
        .agg(
            Cargo_Volume=("Cargo Metric TONS", "sum"),
            Total_Records=("Cargo Metric TONS", "count")
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            geo_data,
            x="GEO Summary",
            y="Cargo_Volume",
            color="GEO Summary",
            title="Cargo Volume Comparison",
            text_auto=".2f"
        )

        fig.update_layout(
            template="plotly_dark",
            showlegend=False,
            yaxis_title="Cargo Volume (MT)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.pie(
            geo_data,
            names="GEO Summary",
            values="Total_Records",
            title="Operational Records Distribution",
            hole=0.45
        )

        fig.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ======================================
    # AIRLINE PERFORMANCE
    # ======================================

    st.markdown("---")

    st.markdown("## ✈️ Airline Performance")

    airline_data = (
        filtered_df
        .groupby("Operating Airline", as_index=False)
        ["Cargo Metric TONS"]
        .sum()
        .sort_values(
            "Cargo Metric TONS",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        airline_data,
        x="Cargo Metric TONS",
        y="Operating Airline",
        orientation="h",
        title="Top 10 Airlines by Cargo Volume",
        text_auto=".2f"
    )

    fig.update_layout(
        template="plotly_dark",
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Cargo Volume (MT)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ======================================
    # REGIONAL ANALYSIS
    # ======================================

    st.markdown("---")

    st.markdown("## 🗺️ Regional Cargo Analysis")

    region_data = (
        filtered_df
        .groupby("GEO Region", as_index=False)
        ["Cargo Metric TONS"]
        .sum()
        .sort_values(
            "Cargo Metric TONS",
            ascending=False
        )
    )

    fig = px.bar(
        region_data,
        x="GEO Region",
        y="Cargo Metric TONS",
        title="Cargo Volume by Geographical Region",
        text_auto=".2f"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Geographical Region",
        yaxis_title="Cargo Volume (MT)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ======================================
    # DESCRIPTIVE STATISTICS
    # ======================================

    st.markdown("---")

    st.markdown("## 📊 Descriptive Statistical Analysis")

    cargo = filtered_df["Cargo Metric TONS"].dropna()

    if not cargo.empty:

        stats_data = {

            "Mean": cargo.mean(),

            "Median": cargo.median(),

            "Standard Deviation": cargo.std(),

            "Variance": cargo.var(),

            "Minimum": cargo.min(),

            "Maximum": cargo.max(),

            "Range": cargo.max() - cargo.min(),

            "Skewness": cargo.skew()

        }

        stats_df = pd.DataFrame(
            stats_data.items(),
            columns=["Statistical Measure", "Value"]
        )

        st.dataframe(
            stats_df,
            use_container_width=True,
            hide_index=True
        )

        # Cargo distribution

        fig = px.histogram(
            filtered_df,
            x="Cargo Metric TONS",
            nbins=30,
            title="Cargo Volume Distribution"
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Cargo Volume (MT)",
            yaxis_title="Frequency"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ======================================
    # CORRELATION ANALYSIS
    # ======================================

    st.markdown("---")

    st.markdown("## 🔗 Correlation Analysis")

    correlation_data = (
        filtered_df
        .groupby(
            [
                "Operating Airline",
                "Activity Period"
            ],
            as_index=False
        )
        .agg(
            Cargo_Volume=("Cargo Metric TONS", "sum"),
            Activity_Records=("Cargo Metric TONS", "count")
        )
    )

    if len(correlation_data) >= 2:

        correlation = correlation_data[
            ["Cargo_Volume", "Activity_Records"]
        ].corr(method="pearson").iloc[0, 1]

        st.metric(
            "Pearson Correlation",
            f"{correlation:.4f}"
        )

        st.caption(
            "Measures the linear relationship between cargo volume "
            "and operational record count."
        )

    else:

        st.info(
            "At least two airline-period groups are required "
            "for correlation analysis."
        )

    # ======================================
    # DATASET EXPLORER
    # ======================================

    st.markdown("---")

    st.markdown("## 🗃️ Uploaded Dataset Explorer")

    st.write(
        f"Showing {len(filtered_df):,} records"
    )

    st.dataframe(
        filtered_df.drop(columns=["Year"]),
        use_container_width=True,
        height=400
    )

    # ======================================
    # DOWNLOAD CLEANED DATASET
    # ======================================

    csv_data = filtered_df.drop(
        columns=["Year"]
    ).to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Cleaned Dataset",
        data=csv_data,
        file_name="cleaned_air_cargo_dataset.csv",
        mime="text/csv"
    )

    st.markdown("---")

    st.success(
        "Uploaded dataset analysis completed successfully!"
    )

    return False