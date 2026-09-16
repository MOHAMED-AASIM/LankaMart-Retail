"""
LankaMart Retail Performance Dashboard
CIT308 Data Visualization — Mid Semester Evaluation

Run locally with:  streamlit run app.py
Requires:           pandas, plotly, streamlit  (see requirements.txt)
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA_PATH = Path(__file__).with_name("LankaMart_Retail_Transactions (1).csv")

st.set_page_config(page_title="LankaMart Performance Dashboard", layout="wide")


# ----------------------------------------------------------------------
# 1. DATA LOADING AND PREPARATION
# ----------------------------------------------------------------------
@st.cache_data
def load_and_clean_data(path: Path) -> pd.DataFrame:
    """Load the raw transaction file and apply documented cleaning steps.

    Cleaning steps (see report for justification):
      1. Drop exact duplicate order_id (1 row: LM26-0113 was recorded twice).
      2. Standardise the inconsistent category label 'electronic' -> 'Electronics'.
      3. Parse order_date to datetime and derive order_month for trend analysis.
      4. Derive profit_margin_pct = profit_lkr / revenue_lkr * 100.
      5. Derive delivery_band from delivery_days (Fast / Standard / Slow).
      6. Fill missing 'promotion' with the explicit label 'No Promotion'
         (NaN here means no promotion was applied, not that data is missing).
      7. customer_rating is left as NaN where missing (42 orders, 5.8%) and
         excluded automatically by pandas/plotly mean and box calculations —
         it is NOT imputed, to avoid inventing ratings customers never gave.
    """
    required_columns = {
        "order_id", "order_date", "province", "city", "sales_channel",
        "customer_segment", "product_category", "product_name", "units",
        "discount_pct", "revenue_lkr", "profit_lkr", "delivery_days",
        "customer_rating", "returned", "promotion",
    }

    try:
        df = pd.read_csv(path)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Data file not found: {path}") from exc

    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"The CSV is missing required columns: {missing}")

    # 1. Duplicates
    df = df.drop_duplicates(subset=["order_id"], keep="first").copy()

    # 2. Category label standardisation
    df["product_category"] = df["product_category"].replace({"electronic": "Electronics"})

    # 3. Date fields
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

    # 4. Calculated field: profit margin
    df["profit_margin_pct"] = (df["profit_lkr"] / df["revenue_lkr"] * 100).round(2)

    # 5. Calculated field: delivery performance band
    def band(d):
        if d <= 2:
            return "Fast (0-2 days)"
        elif d <= 5:
            return "Standard (3-5 days)"
        return "Slow (6+ days)"

    df["delivery_band"] = df["delivery_days"].apply(band)

    # 6. Promotion fill (categorical, not numeric — safe to label explicitly)
    df["promotion"] = df["promotion"].fillna("No Promotion")

    return df


try:
    df_raw = load_and_clean_data(DATA_PATH)
except (FileNotFoundError, ValueError) as exc:
    st.error(str(exc))
    st.stop()


# ----------------------------------------------------------------------
# 2. SIDEBAR CONTROLS (filters)
# ----------------------------------------------------------------------
st.sidebar.title("Filters")

min_date, max_date = df_raw["order_date"].min(), df_raw["order_date"].max()

provinces = sorted(df_raw["province"].unique())
categories = sorted(df_raw["product_category"].unique())
channels = sorted(df_raw["sales_channel"].unique())
segments = sorted(df_raw["customer_segment"].unique())


def reset_filters():
    """Restore every filter widget to its full-data default."""
    st.session_state["date_range"] = (min_date.date(), max_date.date())
    st.session_state["provinces"] = provinces
    st.session_state["categories"] = categories
    st.session_state["channels"] = channels
    st.session_state["segments"] = segments


if "date_range" not in st.session_state:
    reset_filters()

date_range = st.sidebar.date_input(
    "Order date range", min_value=min_date.date(),
    max_value=max_date.date(), key="date_range"
)

selected_provinces = st.sidebar.multiselect(
    "Province", provinces, key="provinces"
)

selected_categories = st.sidebar.multiselect(
    "Product category", categories, key="categories"
)

selected_channels = st.sidebar.multiselect(
    "Sales channel", channels, key="channels"
)

selected_segments = st.sidebar.multiselect(
    "Customer segment", segments, key="segments"
)

st.sidebar.button("Reset all filters", on_click=reset_filters)

# Treat an empty selection as no restriction instead of hiding every record.
selected_provinces = selected_provinces or provinces
selected_categories = selected_categories or categories
selected_channels = selected_channels or channels
selected_segments = selected_segments or segments

st.sidebar.caption(
    "Use the controls above to explore the data. All KPIs, charts and the "
    "detail table below respond to your selection. Click 'Reset all filters' "
    "to return to the full dataset."
)


# ----------------------------------------------------------------------
# 3. APPLY FILTERS (single source of truth for every chart/KPI below)
# ----------------------------------------------------------------------
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

mask = (
    (df_raw["order_date"] >= pd.to_datetime(start_date))
    & (df_raw["order_date"] <= pd.to_datetime(end_date))
    & (df_raw["province"].isin(selected_provinces))
    & (df_raw["product_category"].isin(selected_categories))
    & (df_raw["sales_channel"].isin(selected_channels))
    & (df_raw["customer_segment"].isin(selected_segments))
)
df = df_raw[mask]

st.title("LankaMart Retail Performance Dashboard")
st.caption(
    "How is LankaMart performing, where are the main risks or opportunities, "
    "and what action should management consider?"
)

if df.empty:
    st.warning("No records match the current filter selection. Adjust filters to see data.")
    st.stop()


# ----------------------------------------------------------------------
# 4. KPI INDICATORS
# ----------------------------------------------------------------------
total_revenue = df["revenue_lkr"].sum()
total_profit = df["profit_lkr"].sum()
profit_margin = total_profit / total_revenue * 100 if total_revenue else 0
return_rate = (df["returned"] == "Yes").mean() * 100

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", f"LKR {total_revenue:,.0f}")
k2.metric("Total Profit", f"LKR {total_profit:,.0f}")
k3.metric("Profit Margin", f"{profit_margin:.1f}%")
k4.metric("Return Rate", f"{return_rate:.1f}%", delta=f"{len(df[df['returned']=='Yes'])} orders",
          delta_color="inverse")

st.divider()


# ----------------------------------------------------------------------
# 5. VISUALISATIONS
# ----------------------------------------------------------------------
row1_col1, row1_col2 = st.columns(2)

# 5.1 Time trend: monthly revenue and profit
with row1_col1:
    monthly = df.groupby("order_month")[["revenue_lkr", "profit_lkr"]].sum().reset_index()
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=monthly["order_month"], y=monthly["revenue_lkr"],
                                    name="Revenue", mode="lines+markers"))
    fig_trend.add_trace(go.Scatter(x=monthly["order_month"], y=monthly["profit_lkr"],
                                    name="Profit", mode="lines+markers"))
    fig_trend.update_layout(title="Monthly Revenue and Profit Trend (LKR)",
                             xaxis_title="Month", yaxis_title="LKR", hovermode="x unified")
    st.plotly_chart(fig_trend, width="stretch")

# 5.2 Categorical comparison: revenue by product category
with row1_col2:
    cat_rev = df.groupby("product_category")["revenue_lkr"].sum().sort_values(ascending=True).reset_index()
    fig_cat = px.bar(cat_rev, x="revenue_lkr", y="product_category", orientation="h",
                      title="Revenue by Product Category (LKR)",
                      labels={"revenue_lkr": "Revenue (LKR)", "product_category": "Category"})
    st.plotly_chart(fig_cat, width="stretch")

row2_col1, row2_col2 = st.columns(2)

# 5.3 Geographical comparison: revenue by province
with row2_col1:
    prov_rev = df.groupby("province")["revenue_lkr"].sum().sort_values(ascending=False).reset_index()
    fig_prov = px.bar(prov_rev, x="province", y="revenue_lkr",
                       title="Revenue by Province (LKR)",
                       labels={"revenue_lkr": "Revenue (LKR)", "province": "Province"})
    fig_prov.update_xaxes(tickangle=-35)
    st.plotly_chart(fig_prov, width="stretch")

# 5.4 Relationship view: discount vs profit margin
with row2_col2:
    fig_scatter = px.scatter(df, x="discount_pct", y="profit_margin_pct", color="product_category",
                              title="Discount Level vs Profit Margin",
                              labels={"discount_pct": "Discount applied", "profit_margin_pct": "Profit margin (%)"},
                              hover_data=["order_id", "product_name"])
    st.plotly_chart(fig_scatter, width="stretch")

row3_col1, row3_col2 = st.columns(2)

# 5.5 Distribution view: delivery days by sales channel
with row3_col1:
    fig_box = px.box(df, x="sales_channel", y="delivery_days", color="sales_channel",
                      title="Delivery Time Distribution by Sales Channel",
                      labels={"delivery_days": "Delivery days", "sales_channel": "Channel"})
    st.plotly_chart(fig_box, width="stretch")

# 5.6 Return rate by category (extra managerial view)
with row3_col2:
    ret_cat = (df.groupby("product_category")["returned"]
               .apply(lambda x: (x == "Yes").mean() * 100)
               .sort_values(ascending=False).reset_index(name="return_rate_pct"))
    fig_ret = px.bar(ret_cat, x="product_category", y="return_rate_pct",
                      title="Return Rate by Product Category (%)",
                      labels={"return_rate_pct": "Return rate (%)", "product_category": "Category"})
    st.plotly_chart(fig_ret, width="stretch")

st.divider()


# ----------------------------------------------------------------------
# 6. DETAIL TABLE
# ----------------------------------------------------------------------
st.subheader("Detailed Records (current filter selection)")
detail_cols = ["order_id", "order_date", "province", "city", "sales_channel",
                "customer_segment", "product_category", "product_name", "units",
                "revenue_lkr", "profit_lkr", "profit_margin_pct", "delivery_days",
                "customer_rating", "returned", "promotion"]
st.dataframe(df[detail_cols].sort_values("order_date", ascending=False),
             width="stretch", height=320)
st.caption(f"Showing {len(df):,} of {len(df_raw):,} total orders under the current filter selection.")

st.divider()


# ----------------------------------------------------------------------
# 7. INSIGHTS AND RECOMMENDED ACTIONS
# ----------------------------------------------------------------------
st.subheader("Key Insights (based on current filter selection)")

top_cat = cat_rev.iloc[-1]
top_prov = prov_rev.iloc[0]
worst_return_cat = ret_cat.iloc[0]
corr = df["discount_pct"].corr(df["profit_margin_pct"])

st.markdown(f"""
- **{top_cat['product_category']}** is the leading revenue category at
  LKR {top_cat['revenue_lkr']:,.0f} in the current selection.
- **{top_prov['province']}** province contributes the most revenue
  (LKR {top_prov['revenue_lkr']:,.0f}).
- **{worst_return_cat['product_category']}** has the highest return rate at
  {worst_return_cat['return_rate_pct']:.1f}%, worth investigating for quality
  or fit issues.
- Discount level and profit margin move together with a correlation of
  **{corr:.2f}** — heavier discounting is associated with materially thinner
  margins across the selected orders.
""")
