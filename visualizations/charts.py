import plotly.express as px
import plotly.graph_objects as go


# Common chart theme
CHART_TEMPLATE = "plotly_dark"


# 1. Year-wise Cargo Volume
def yearly_cargo_chart(yearly_data):

    fig = px.bar(
        yearly_data,
        x="Year",
        y="Total_Cargo_TONS",
        title="Year-wise Cargo Volume",
        labels={
            "Year": "Year",
            "Total_Cargo_TONS": "Cargo Volume (MT)"
        },
        text_auto=".2f",
        template=CHART_TEMPLATE
    )

    fig.update_traces(
        marker_color="#4C9BE8",
        textposition="outside"
    )

    fig.update_layout(
        xaxis=dict(type="category"),
        showlegend=False
    )

    return fig


# 2. Monthly Cargo Trend
def monthly_cargo_chart(monthly_data):

    fig = px.line(
        monthly_data,
        x="Month",
        y="Total_Cargo_TONS",
        title="Monthly Cargo Volume Trend",
        labels={
            "Month": "Month",
            "Total_Cargo_TONS": "Cargo Volume (MT)"
        },
        template=CHART_TEMPLATE,
        markers=True
    )

    fig.update_traces(
        line=dict(color="#4C9BE8", width=2),
        marker=dict(size=5)
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Cargo Volume (MT)"
    )

    return fig


# 3. Seasonal Cargo Analysis
def seasonal_cargo_chart(seasonal_data):

    fig = px.bar(
        seasonal_data,
        x="Month_Name",
        y="Average_Cargo_TONS",
        title="Average Cargo Volume by Month",
        labels={
            "Month_Name": "Month",
            "Average_Cargo_TONS": "Average Cargo (MT)"
        },
        text_auto=".3f",
        template=CHART_TEMPLATE
    )

    fig.update_traces(
        marker_color="#62B6A5",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Average Cargo (MT)"
    )

    return fig


# 4. Correlation Scatter Plot
def correlation_chart(df):

    fig = px.scatter(
        df,
        x="Cargo Weight LBS",
        y="Cargo Metric TONS",
        title="Cargo Weight vs Cargo Metric Tons",
        labels={
            "Cargo Weight LBS": "Cargo Weight (LBS)",
            "Cargo Metric TONS": "Cargo Volume (MT)"
        },
        template=CHART_TEMPLATE,
        opacity=0.5
    )

    fig.update_traces(
        marker=dict(color="#4C9BE8", size=5)
    )

    return fig


# 5. Regression Actual vs Predicted
def regression_chart(prediction_data):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=prediction_data["Month"],
            y=prediction_data["Actual"],
            mode="lines+markers",
            name="Actual Cargo"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=prediction_data["Month"],
            y=prediction_data["Predicted"],
            mode="lines+markers",
            name="Predicted Cargo"
        )
    )

    fig.update_layout(
        title="Actual vs Predicted Cargo Volume",
        xaxis_title="Month",
        yaxis_title="Cargo Volume (MT)",
        template=CHART_TEMPLATE
    )

    return fig