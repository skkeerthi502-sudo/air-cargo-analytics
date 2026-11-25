import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

from scipy.stats import linregress, ttest_ind, mannwhitneyu

from analysis.data_cleaning import load_data, clean_data
from analysis.upload_data import process_uploaded_file
from analysis.upload_dashboard import render_upload_dashboard

from analysis.trend_analysis import (
    calculate_monthly_trend,
    calculate_yearly_trend,
    calculate_seasonal_trend
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Air Cargo Analytics",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# CINEMATIC UI CONFIGURATION
# ==========================================

def load_cinematic_css():

    css_path = Path(__file__).resolve().parent / "assets" / "cinematic.css"

    if css_path.exists():

        with open(css_path, "r", encoding="utf-8") as file:

            css_code = file.read()

        st.markdown(
            f"<style>{css_code}</style>",
            unsafe_allow_html=True
        )

    else:

        st.error(
            "Cinematic CSS file not found. "
            "Please check assets/cinematic.css"
        )


# APPLY CINEMATIC DESIGN

load_cinematic_css()


# ==========================================
# DESIGN CONFIGURATION
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #0B1120;
    color: #E5E7EB;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stMetric"] {
    background-color: #172337;
    border: 1px solid #263B55;
    padding: 20px;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #AAB8CA;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC;
}

h1, h2, h3 {
    color: #F8FAFC;
}

.stCaption {
    color: #94A3B8;
}

div[data-testid="stPlotlyChart"] {
    background-color: #111827;
    border-radius: 12px;
    padding: 8px;
}

hr {
    border-color: #263B55;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# COMMON CHART SETTINGS
# ==========================================

CHART_TEMPLATE = "plotly_dark"

CHART_COLORS = [
    "#4C9BE8",
    "#62B6A5",
    "#A78BFA",
    "#F4B860",
    "#E879A5",
    "#38BDF8",
    "#A3A3A3"
]


def style_chart(fig, height=400):

    fig.update_layout(
        template=CHART_TEMPLATE,
        height=height,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(
            color="#E5E7EB",
            family="Arial"
        ),
        title_font=dict(
            size=17,
            color="#F8FAFC"
        ),
        margin=dict(
            l=35,
            r=25,
            t=65,
            b=40
        ),
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_color="white"
        )
    )

    return fig


# ==========================================
# DASHBOARD PAGE NAVIGATION
# ==========================================

if "dashboard_page" not in st.session_state:
    st.session_state["dashboard_page"] = "original"


# ==========================================
# UPLOAD DASHBOARD PAGE
# ==========================================

if st.session_state["dashboard_page"] == "upload":

    # ==========================================
    # CINEMATIC UPLOAD STUDIO HEADER
    # ==========================================

    st.markdown(
        """
        <div class="upload-page-header">
            <div class="upload-page-tag">✦ INDEPENDENT DATA WORKSPACE</div>
            <h1>🚀 Upload Studio</h1>
            <p>
                Import your own Air Cargo dataset and explore its
                operational insights in a separate analytics workspace.
            </p>
            <div class="upload-page-meta">
                CSV / XLSX &nbsp; | &nbsp; DATA VALIDATION &nbsp; | &nbsp;
                ORIGINAL MYSQL DATA PRESERVED
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ==========================================
    # CINEMATIC FILE UPLOAD AREA
    # ==========================================

    with st.container(key="upload_dropzone"):

        st.markdown("### 📂 Import Your Dataset")

        st.markdown(
            """
            Drag and drop your dataset below, or browse files
            from your computer.

            **Supported formats:** CSV and XLSX

            **Required structure:** 13 Air Cargo columns
            """
        )

        uploaded_file = st.file_uploader(
            "Choose your Air Cargo dataset",
            type=["csv", "xlsx"],
            key="air_cargo_file_uploader"
        )

    if uploaded_file is not None:

        try:
            uploaded_df, upload_summary = process_uploaded_file(uploaded_file)

            st.success("Dataset uploaded and cleaned successfully.")

            go_back = render_upload_dashboard(
                uploaded_df,
                upload_summary
            )

            if go_back:
                st.session_state["dashboard_page"] = "original"
                st.rerun()

        except Exception as error:
            st.error(f"Upload Error: {error}")

    else:
        st.info(
            "Please upload a CSV or XLSX file containing the required "
            "13 Air Cargo columns."
        )

    if uploaded_file is None:
        if st.button("← Back to Original Dashboard", key="upload_page_back"):
            st.session_state["dashboard_page"] = "original"
            st.rerun()

    st.stop()


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data(ttl=600)
def get_dataset():

    df = load_data()

    if df is not None:

        df = clean_data(df)

        numeric_columns = [
            "Cargo Metric TONS",
            "Cargo Weight LBS"
        ]

        for column in numeric_columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        df = df.dropna(
            subset=[
                "Activity Period Start Date",
                "Cargo Metric TONS"
            ]
        )

    return df


try:

    df = get_dataset()

    if df is None or df.empty:

        st.error("Unable to load data from MySQL.")
        st.stop()

except Exception as error:

    st.error(f"Database Error: {error}")
    st.stop()


# ==========================================
# CINEMATIC HERO SECTION
# ==========================================

hero_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    * {
        box-sizing: border-box;
    }

    html, body {
        margin: 0;
        padding: 0;
        background: transparent;
        font-family: Arial, Helvetica, sans-serif;
        overflow: hidden;
    }

    .hero-section {
        position: relative;
        overflow: hidden;
        min-height: 310px;
        padding: 48px 42px;
        border-radius: 24px;
        border: 1px solid rgba(96, 165, 250, 0.38);
        background:
            radial-gradient(circle at 85% 15%, rgba(59,130,246,.25), transparent 32%),
            radial-gradient(circle at 35% 110%, rgba(139,92,246,.20), transparent 35%),
            linear-gradient(120deg, #0f2341 0%, #172746 55%, #20234a 100%);
        box-shadow: 0 18px 48px rgba(0,0,0,.28),
                    inset 0 0 38px rgba(59,130,246,.07);
        animation: heroEnter 900ms ease-out both;
    }

    .hero-section::before,
    .hero-section::after {
        content: "";
        position: absolute;
        border-radius: 50%;
        filter: blur(55px);
        pointer-events: none;
        animation: glowFloat 7s ease-in-out infinite alternate;
    }

    .hero-section::before {
        width: 230px;
        height: 230px;
        right: -45px;
        top: -125px;
        background: rgba(59,130,246,.30);
    }

    .hero-section::after {
        width: 190px;
        height: 190px;
        left: 35%;
        bottom: -145px;
        background: rgba(139,92,246,.22);
        animation-delay: 1.5s;
    }

    .hero-content {
        position: relative;
        z-index: 1;
    }

    .hero-tag {
        display: inline-block;
        padding: 8px 15px;
        margin-bottom: 17px;
        color: #a8d1ff;
        background: rgba(59,130,246,.14);
        border: 1px solid rgba(96,165,250,.38);
        border-radius: 30px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
    }

    .hero-title {
        margin: 0 0 14px;
        color: #ffffff;
        font-size: clamp(29px, 4vw, 46px);
        font-weight: 800;
        line-height: 1.13;
        letter-spacing: .4px;
    }

    .hero-title span {
        color: #8fc5ff;
        background: linear-gradient(90deg, #60a5fa, #b5a2ff, #67e8f9);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        max-width: 760px;
        color: #c1d0e4;
        font-size: 14px;
        line-height: 1.75;
    }

    .hero-footer {
        margin-top: 22px;
        color: #91aaca;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.7px;
    }

    @keyframes heroEnter {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes glowFloat {
        from { transform: translate3d(0, 0, 0) scale(.92); }
        to   { transform: translate3d(-18px, 15px, 0) scale(1.12); }
    }

    @media (max-width: 640px) {
        .hero-section { padding: 32px 24px; min-height: 330px; }
        .hero-footer { line-height: 2; }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: .01ms !important;
            animation-iteration-count: 1 !important;
        }
    }
</style>
</head>
<body>
    <section class="hero-section">
        <div class="hero-content">
            <div class="hero-tag">✦ ADVANCED DATA ANALYTICS PLATFORM</div>
            <h1 class="hero-title">
                AIR CARGO<br>
                <span>OPERATIONS &amp; ANALYTICS</span>
            </h1>
            <div class="hero-description">
                Transform operational data into meaningful business intelligence.
                Explore airline performance, cargo movements, geographical
                distributions and advanced statistical insights.
            </div>
            <div class="hero-footer">
                PYTHON &nbsp; | &nbsp; MYSQL &nbsp; | &nbsp; STREAMLIT &nbsp; | &nbsp; POWERFUL ANALYTICS
            </div>
        </div>
    </section>
</body>
</html>
"""

st.components.v1.html(
    hero_html,
    height=335,
    scrolling=False
)

st.divider()

# ==========================================
# CINEMATIC UPLOAD STUDIO LAUNCHER
# ==========================================

with st.container(key="upload_launch_card"):

    col1, col2 = st.columns([3, 1])

    with col1:

        st.markdown("### 🚀 Explore Your Own Dataset")

        st.markdown(
            """
            Upload your CSV or Excel dataset and explore it
            through an independent analytics workspace.

            **Supported formats:** CSV | XLSX

            Your original MySQL database will remain unchanged.
            """
        )

    with col2:

        st.write("")

        if st.button(
            "✦ OPEN UPLOAD STUDIO",
            key="open_upload_studio",
            use_container_width=True
        ):

            st.session_state["dashboard_page"] = "upload"

            st.rerun()

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.title("🎛️ Dashboard Filters")

st.sidebar.caption("Filter the dataset to explore insights.")


def get_options(data, column):

    return sorted(
        data[column].dropna().unique().tolist(),
        key=str
    )


# Year Filter

available_years = sorted(
    df["Activity Period Start Date"].dt.year.unique()
)

selected_years = st.sidebar.multiselect(
    "📅 Select Year",
    available_years,
    default=available_years
)


# Airline Filter

available_airlines = get_options(
    df,
    "Operating Airline"
)

selected_airlines = st.sidebar.multiselect(
    "✈️ Operating Airline",
    available_airlines,
    default=available_airlines
)


# Domestic / International Filter

available_geo = get_options(
    df,
    "GEO Summary"
)

selected_geo = st.sidebar.multiselect(
    "🌍 GEO Summary",
    available_geo,
    default=available_geo
)


# Region Filter

available_regions = get_options(
    df,
    "GEO Region"
)

selected_regions = st.sidebar.multiselect(
    "📍 GEO Region",
    available_regions,
    default=available_regions
)


# Aircraft Filter

available_aircraft = get_options(
    df,
    "Cargo Aircraft Type"
)

selected_aircraft = st.sidebar.multiselect(
    "🛩️ Aircraft Type",
    available_aircraft,
    default=available_aircraft
)


# Activity Filter

available_activity = get_options(
    df,
    "Activity Type Code"
)

selected_activity = st.sidebar.multiselect(
    "⚙️ Activity Type",
    available_activity,
    default=available_activity
)


# Cargo Type Filter

available_cargo_type = get_options(
    df,
    "Cargo Type Code"
)

selected_cargo_type = st.sidebar.multiselect(
    "📦 Cargo Type",
    available_cargo_type,
    default=available_cargo_type
)


# ==========================================
# APPLY FILTERS
# ==========================================

filtered_df = df[
    (df["Activity Period Start Date"].dt.year.isin(selected_years))
    & (df["Operating Airline"].isin(selected_airlines))
    & (df["GEO Summary"].isin(selected_geo))
    & (df["GEO Region"].isin(selected_regions))
    & (df["Cargo Aircraft Type"].isin(selected_aircraft))
    & (df["Activity Type Code"].isin(selected_activity))
    & (df["Cargo Type Code"].isin(selected_cargo_type))
].copy()


if filtered_df.empty:

    st.warning(
        "No records available for the selected filters. "
        "Please change your filter selections."
    )

    st.stop()


# ==========================================
# KPI SECTION
# ==========================================

st.subheader("📊 Executive Overview")

total_cargo = filtered_df["Cargo Metric TONS"].sum()

total_records = len(filtered_df)

total_airlines = filtered_df["Operating Airline"].nunique()

total_regions = filtered_df["GEO Region"].nunique()

total_domestic = filtered_df.loc[
    filtered_df["GEO Summary"].str.lower() == "domestic",
    "Cargo Metric TONS"
].sum()

total_international = filtered_df.loc[
    filtered_df["GEO Summary"].str.lower() == "international",
    "Cargo Metric TONS"
].sum()


col1, col2, col3, col4 = st.columns(4)

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

col4.metric(
    "Geographical Regions",
    total_regions
)


col1, col2 = st.columns(2)

col1.metric(
    "Domestic Cargo",
    f"{total_domestic:,.2f} MT"
)

col2.metric(
    "International Cargo",
    f"{total_international:,.2f} MT"
)


st.divider()


# ==========================================
# CARGO TREND ANALYSIS
# ==========================================

st.subheader("📈 Cargo Trend Analysis")

yearly_data = calculate_yearly_trend(filtered_df)

monthly_data = calculate_monthly_trend(filtered_df)

seasonal_data = calculate_seasonal_trend(filtered_df)


# Yearly Chart

fig_yearly = px.bar(
    yearly_data,
    x="Year",
    y="Total_Cargo_TONS",
    text_auto=".2f",
    title="Year-wise Cargo Volume",
    color="Total_Cargo_TONS",
    color_continuous_scale=[
        "#1E3A5F",
        "#4C9BE8"
    ]
)

fig_yearly.update_layout(
    coloraxis_showscale=False,
    xaxis=dict(type="category")
)

style_chart(fig_yearly)

st.plotly_chart(
    fig_yearly,
    use_container_width=True
)


# Monthly and Seasonal Charts

col1, col2 = st.columns(2)


with col1:

    fig_monthly = px.line(
        monthly_data,
        x="Month",
        y="Total_Cargo_TONS",
        title="Monthly Cargo Volume Trend",
        markers=True
    )

    fig_monthly.update_traces(
        line=dict(
            color="#4C9BE8",
            width=3
        ),
        marker=dict(size=6)
    )

    style_chart(fig_monthly)

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )


with col2:

    fig_seasonal = px.bar(
        seasonal_data,
        x="Month_Name",
        y="Average_Cargo_TONS",
        title="Average Cargo Volume by Month",
        color="Average_Cargo_TONS",
        color_continuous_scale=[
            "#245C67",
            "#62B6A5"
        ],
        text_auto=".3f"
    )

    fig_seasonal.update_layout(
        coloraxis_showscale=False
    )

    style_chart(fig_seasonal)

    st.plotly_chart(
        fig_seasonal,
        use_container_width=True
    )


st.divider()


# ==========================================
# DOMESTIC VS INTERNATIONAL ANALYSIS
# ==========================================

st.subheader("🌍 Domestic vs International Analysis")


geo_data = filtered_df.groupby(
    "GEO Summary"
).agg(
    Total_Cargo=("Cargo Metric TONS", "sum"),
    Total_Records=("Cargo Metric TONS", "count"),
    Average_Cargo=("Cargo Metric TONS", "mean")
).reset_index()


col1, col2 = st.columns(2)


with col1:

    fig_geo = px.bar(
        geo_data,
        x="GEO Summary",
        y="Total_Cargo",
        color="GEO Summary",
        text_auto=".2f",
        title="Cargo Volume: Domestic vs International",
        color_discrete_sequence=[
            "#4C9BE8",
            "#62B6A5"
        ]
    )

    style_chart(fig_geo)

    st.plotly_chart(
        fig_geo,
        use_container_width=True
    )


with col2:

    fig_geo_records = px.pie(
        geo_data,
        names="GEO Summary",
        values="Total_Records",
        hole=0.55,
        title="Operational Records Distribution",
        color_discrete_sequence=[
            "#4C9BE8",
            "#62B6A5"
        ]
    )

    style_chart(fig_geo_records)

    st.plotly_chart(
        fig_geo_records,
        use_container_width=True
    )


st.dataframe(
    geo_data.round(4),
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================
# AIRLINE PERFORMANCE ANALYSIS
# ==========================================

st.subheader("✈️ Airline Performance Analysis")


airline_data = filtered_df.groupby(
    "Operating Airline"
).agg(
    Total_Cargo=("Cargo Metric TONS", "sum"),
    Total_Records=("Cargo Metric TONS", "count"),
    Average_Cargo=("Cargo Metric TONS", "mean")
).reset_index()


top_airlines = airline_data.nlargest(
    10,
    "Total_Cargo"
)


fig_airline = px.bar(
    top_airlines.sort_values("Total_Cargo"),
    x="Total_Cargo",
    y="Operating Airline",
    orientation="h",
    title="Top 10 Airlines by Cargo Volume",
    color="Total_Cargo",
    color_continuous_scale=[
        "#1E3A5F",
        "#4C9BE8"
    ]
)

fig_airline.update_layout(
    coloraxis_showscale=False
)

style_chart(fig_airline, height=500)

st.plotly_chart(
    fig_airline,
    use_container_width=True
)


st.divider()


# ==========================================
# REGIONAL CARGO ANALYSIS
# ==========================================

st.subheader("📍 Regional Cargo Analysis")


region_data = filtered_df.groupby(
    "GEO Region"
).agg(
    Total_Cargo=("Cargo Metric TONS", "sum"),
    Total_Records=("Cargo Metric TONS", "count")
).reset_index()


fig_region = px.bar(
    region_data.sort_values("Total_Cargo"),
    x="Total_Cargo",
    y="GEO Region",
    orientation="h",
    title="Cargo Volume by Geographical Region",
    color="Total_Cargo",
    color_continuous_scale=[
        "#245C67",
        "#62B6A5"
    ]
)

fig_region.update_layout(
    coloraxis_showscale=False
)

style_chart(fig_region, height=450)

st.plotly_chart(
    fig_region,
    use_container_width=True
)


st.divider()


# ==========================================
# CORRELATION ANALYSIS
# ==========================================

st.subheader("📊 Correlation Analysis")


correlation_data = filtered_df.groupby(
    [
        "Operating Airline",
        pd.Grouper(
            key="Activity Period Start Date",
            freq="MS"
        )
    ]
).agg(
    Total_Cargo=("Cargo Metric TONS", "sum"),
    Activity_Records=("Cargo Metric TONS", "count")
).reset_index()


if (
    len(correlation_data) >= 2
    and correlation_data["Total_Cargo"].nunique() > 1
    and correlation_data["Activity_Records"].nunique() > 1
):

    correlation_value = correlation_data[
        "Total_Cargo"
    ].corr(
        correlation_data["Activity_Records"]
    )

    col1, col2 = st.columns([1, 3])

    with col1:

        st.metric(
            "Cargo vs Activity Records",
            f"{correlation_value:.4f}"
        )

        st.caption(
            "Pearson correlation coefficient"
        )

    with col2:

        fig_correlation = px.scatter(
            correlation_data,
            x="Activity_Records",
            y="Total_Cargo",
            title="Cargo Volume vs Activity Records",
            opacity=0.6
        )

        fig_correlation.update_traces(
            marker=dict(
                color="#4C9BE8",
                size=7
            )
        )

        style_chart(fig_correlation)

        st.plotly_chart(
            fig_correlation,
            use_container_width=True
        )

else:

    st.info(
        "Insufficient variation in the selected data "
        "to calculate correlation."
    )


st.divider()


# ==========================================
# REGRESSION ANALYSIS
# ==========================================

st.subheader("📉 Regression Analysis")


regression_monthly = filtered_df.groupby(
    pd.Grouper(
        key="Activity Period Start Date",
        freq="MS"
    )
)["Cargo Metric TONS"].sum().reset_index()


regression_monthly.columns = [
    "Month",
    "Actual"
]


if len(regression_monthly) >= 5:

    regression_monthly["Time_Index"] = np.arange(
        len(regression_monthly)
    )

    split_index = int(
        len(regression_monthly) * 0.80
    )

    train_data = regression_monthly.iloc[
        :split_index
    ]

    test_data = regression_monthly.iloc[
        split_index:
    ].copy()


    model = linregress(
        train_data["Time_Index"],
        train_data["Actual"]
    )


    test_data["Predicted"] = (
        model.slope * test_data["Time_Index"]
        + model.intercept
    )


    actual = test_data["Actual"].to_numpy()

    predicted = test_data["Predicted"].to_numpy()


    mae = np.mean(
        np.abs(actual - predicted)
    )

    rmse = np.sqrt(
        np.mean((actual - predicted) ** 2)
    )

    ss_res = np.sum(
        (actual - predicted) ** 2
    )

    ss_tot = np.sum(
        (actual - np.mean(actual)) ** 2
    )

    r2 = (
        1 - ss_res / ss_tot
        if ss_tot != 0
        else np.nan
    )


    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Model R²",
        f"{r2:.4f}"
    )

    col2.metric(
        "MAE",
        f"{mae:.2f} MT"
    )

    col3.metric(
        "RMSE",
        f"{rmse:.2f} MT"
    )


    test_data["Month"] = (
        test_data["Month"].dt.strftime("%b %Y")
    )


    fig_regression = px.line(
        test_data,
        x="Month",
        y=["Actual", "Predicted"],
        markers=True,
        title="Actual vs Predicted Cargo Volume"
    )

    fig_regression.update_layout(
        yaxis_title="Cargo Volume (MT)",
        xaxis_title="Month",
        legend_title="Measurement"
    )

    style_chart(fig_regression)

    st.plotly_chart(
        fig_regression,
        use_container_width=True
    )


else:

    st.info(
        "At least 5 monthly observations are required "
        "for regression analysis."
    )


st.divider()


# ==========================================
# HYPOTHESIS TESTING
# ==========================================

st.subheader("🧪 Hypothesis Testing")

st.markdown(
    """
    **Research Question:** Is there a statistically significant
    difference between Domestic and International cargo volumes?

    - H0: Both groups have equal mean cargo volumes.
    - H1: Both groups have different mean cargo volumes.
    """
)


domestic = filtered_df.loc[
    filtered_df["GEO Summary"].str.lower() == "domestic",
    "Cargo Metric TONS"
].dropna()


international = filtered_df.loc[
    filtered_df["GEO Summary"].str.lower() == "international",
    "Cargo Metric TONS"
].dropna()


if len(domestic) >= 2 and len(international) >= 2:

    t_stat, t_p_value = ttest_ind(
        domestic,
        international,
        equal_var=False
    )

    u_stat, u_p_value = mannwhitneyu(
        domestic,
        international,
        alternative="two-sided"
    )


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Domestic Mean",
        f"{domestic.mean():.4f} MT"
    )

    col2.metric(
        "International Mean",
        f"{international.mean():.4f} MT"
    )

    col3.metric(
        "Welch T-Test P-Value",
        f"{t_p_value:.6f}"
    )

    col4.metric(
        "Mann-Whitney P-Value",
        f"{u_p_value:.6e}"
    )


    if t_p_value < 0.05:

        st.success(
            "Welch's T-Test: Reject H0. "
            "A statistically significant difference "
            "exists between the group means."
        )

    else:

        st.info(
            "Welch's T-Test: Fail to reject H0."
        )


    if u_p_value < 0.05:

        st.success(
            "Mann-Whitney Test: Reject H0. "
            "A statistically significant difference "
            "exists between the group distributions."
        )

    else:

        st.info(
            "Mann-Whitney Test: Fail to reject H0."
        )


else:

    st.info(
        "Select both Domestic and International categories "
        "to perform hypothesis testing."
    )


st.divider()


# ==========================================
# DATASET EXPLORER
# ==========================================

st.subheader("📋 Dataset Explorer")


st.caption(
    "Explore the filtered air cargo dataset."
)


st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


st.caption(
    f"Displaying {len(filtered_df):,} records "
    f"across {len(filtered_df.columns)} columns."
)


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#94A3B8;">

    <h4>✈️ Air Cargo Operations & Statistical Analytics</h4>

    Developed using Python | MySQL | Pandas |
    SciPy | Streamlit | Plotly

    </div>   
    """,
    unsafe_allow_html=True
)
