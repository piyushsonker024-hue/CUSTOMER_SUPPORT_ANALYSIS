import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# Page Configuration
# ---------------------------------------
st.set_page_config(
    page_title="Customer Support Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Support Analytics Dashboard")
st.markdown("Analyze SLA performance, agent efficiency, customer satisfaction, and ticket trends.")

# ---------------------------------------
# Load Dataset
# ---------------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("customer_tickets.csv")

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # Convert date columns
    df["created_date"] = pd.to_datetime(
        df["created_date"],
        errors="coerce"
    )

    df["resolved_date"] = pd.to_datetime(
        df["resolved_date"],
        errors="coerce"
    )

    # SLA Flag
    df["sla_flag"] = (
        df["sla_breached"]
        .astype(str)
        .str.lower()
        .eq("yes")
    )

    return df


df = load_data()


st.sidebar.header("🔍 Filters")

# Region
regions = sorted(df["region"].dropna().unique())

selected_region = st.sidebar.multiselect(
    "Region",
    options=regions,
    default=regions
)

# Category
categories = sorted(df["category"].dropna().unique())

selected_category = st.sidebar.multiselect(
    "Category",
    options=categories,
    default=categories
)

# Priority
priorities = sorted(df["priority"].dropna().unique())

selected_priority = st.sidebar.multiselect(
    "Priority",
    options=priorities,
    default=priorities
)

# Agent
agents = sorted(df["agent_id"].dropna().unique())

selected_agent = st.sidebar.multiselect(
    "Agent",
    options=agents,
    default=agents
)

filtered_df = df[
    (df["region"].isin(selected_region)) &
    (df["category"].isin(selected_category)) &
    (df["priority"].isin(selected_priority)) &
    (df["agent_id"].isin(selected_agent))
]

st.markdown("## 📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_tickets = len(filtered_df)

sla_rate = filtered_df["sla_flag"].mean() * 100

avg_resolution = filtered_df["resolution_time_hours"].mean()

avg_csat = filtered_df["csat_score"].mean()

col1.metric(
    "Total Tickets",
    f"{total_tickets:,}"
)

col2.metric(
    "SLA Breach %",
    f"{sla_rate:.2f}%"
)

col3.metric(
    "Avg Resolution Time",
    f"{avg_resolution:.2f} hrs"
)

col4.metric(
    "Average CSAT",
    f"{avg_csat:.2f}"
)

st.markdown("---")

with st.expander("📄 Dataset Summary"):

    st.write(f"**Rows:** {filtered_df.shape[0]}")
    st.write(f"**Columns:** {filtered_df.shape[1]}")

    st.dataframe(filtered_df.head())

st.markdown("---")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        " Overview",
        " SLA Analysis",
        " Agent Analysis",
        " Customer Insights",
        " data Quality"
        " Weekly KPI"
    ]
)

# =====================================================
# TAB 1 : OVERVIEW
# =====================================================

with tab1:

    st.header("📈 Overview")

    col1, col2 = st.columns(2)

    # -------------------------------
    # Ticket Category Distribution
    # -------------------------------
    with col1:

        category_count = (
            filtered_df["category"]
            .value_counts()
            .reset_index()
        )

        category_count.columns = ["Category", "Tickets"]

        fig = px.bar(
            category_count,
            x="Category",
            y="Tickets",
            color="Tickets",
            title="Tickets by Category",
            text_auto=True
        )

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Priority Distribution
    # -------------------------------
    with col2:

        priority_count = (
            filtered_df["priority"]
            .value_counts()
            .reset_index()
        )

        priority_count.columns = ["Priority", "Tickets"]

        fig = px.pie(
            priority_count,
            names="Priority",
            values="Tickets",
            title="Priority Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # -------------------------------
    # Monthly Ticket Trend
    # -------------------------------

    monthly = filtered_df.copy()

    monthly["Month"] = monthly["created_date"].dt.to_period("M").astype(str)

    monthly = (
        monthly.groupby("Month")
        .size()
        .reset_index(name="Tickets")
    )

    fig = px.line(
        monthly,
        x="Month",
        y="Tickets",
        markers=True,
        title="Monthly Ticket Trend"
    )

    st.plotly_chart(fig, use_container_width=True)





# =====================================================
# TAB 2 : SLA ANALYSIS
# =====================================================

with tab2:

    st.header("🚨 SLA Analysis")

    st.write(
        """
        This section answers:

        **Which category or region has the worst SLA breach rate?**
        """
    )

    # --------------------------------------
    # SLA by Category
    # --------------------------------------

    category_sla = (
        filtered_df
        .groupby("category")["sla_flag"]
        .mean()
        .reset_index()
    )

    category_sla["SLA Breach %"] = (
        category_sla["sla_flag"] * 100
    )

    fig = px.bar(
        category_sla.sort_values(
            "SLA Breach %",
            ascending=False
        ),
        x="category",
        y="SLA Breach %",
        color="SLA Breach %",
        text_auto=".1f",
        title="SLA Breach Rate by Category"
    )

    st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------
    # Worst Category
    # --------------------------------------

    worst_category = (
        category_sla.sort_values(
            "SLA Breach %",
            ascending=False
        )
        .iloc[0]
    )

    st.warning(
        f"""
        Highest SLA Breach Category

        **{worst_category['category']}**

        Breach Rate: **{worst_category['SLA Breach %']:.2f}%**
        """
    )



    # --------------------------------------
    # SLA by Region
    # --------------------------------------

    region_sla = (
        filtered_df
        .groupby("region")["sla_flag"]
        .mean()
        .reset_index()
    )

    region_sla["SLA Breach %"] = (
        region_sla["sla_flag"] * 100
    )

    fig = px.bar(
        region_sla.sort_values(
            "SLA Breach %",
            ascending=False
        ),
        x="region",
        y="SLA Breach %",
        color="SLA Breach %",
        text_auto=".1f",
        title="SLA Breach Rate by Region"
    )

    st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------
    # Worst Region
    # --------------------------------------

    worst_region = (
        region_sla.sort_values(
            "SLA Breach %",
            ascending=False
        )
        .iloc[0]
    )

    st.warning(
        f"""
        Highest SLA Breach Region

        **{worst_region['region']}**

        Breach Rate: **{worst_region['SLA Breach %']:.2f}%**
        """
    )



    # --------------------------------------
    # Average Resolution Time by Category
    # --------------------------------------

    resolution = (
        filtered_df
        .groupby("category")["resolution_time_hours"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        resolution,
        x="category",
        y="resolution_time_hours",
        color="resolution_time_hours",
        title="Average Resolution Time by Category",
        text_auto=".1f"
    )

    st.plotly_chart(fig, use_container_width=True)



    # --------------------------------------
    # Business Insight
    # --------------------------------------

    st.info(
        """
        **Business Insight**

        • Categories with high SLA breach rates and long resolution times
        should be investigated first.

        • If one region consistently has higher breaches than others,
        it may indicate staffing or workload imbalance.

        • Compare these results with agent performance (next tab)
        to understand what is driving the breaches.
        """
    )

    # =====================================================
# TAB 3 : AGENT ANALYSIS
# =====================================================

with tab3:

    st.header("👨‍💼 Agent Performance")

    st.markdown("""
    **Business Question 2**

    *Is there a relationship between priority and resolution time?*

    *Which agents deviate from that pattern?*
    """)

    # ------------------------------------
    # Average Resolution by Priority
    # ------------------------------------

    priority_resolution = (
        filtered_df
        .groupby("priority")["resolution_time_hours"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        priority_resolution,
        x="priority",
        y="resolution_time_hours",
        color="priority",
        text_auto=".1f",
        title="Average Resolution Time by Priority"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.success(
        """
        Higher-priority tickets should have shorter
        resolution times than low-priority tickets.
        """
    )

    st.markdown("---")

    # ------------------------------------
    # Agent Performance
    # ------------------------------------

    agent_summary = (
        filtered_df
        .groupby("agent_id")
        .agg(
            Tickets=("ticket_id", "count"),
            Avg_Resolution=("resolution_time_hours", "mean"),
            Avg_CSAT=("csat_score", "mean"),
            SLA_Breach=("sla_flag", "mean")
        )
        .reset_index()
    )

    agent_summary["SLA_Breach"] *= 100

    st.subheader("Agent Performance")

    st.dataframe(
        agent_summary.sort_values(
            "Avg_Resolution"
        ),
        use_container_width=True
    )

    # ------------------------------------
    # Agent Deviation
    # ------------------------------------

    expected = (
        filtered_df
        .groupby("priority")["resolution_time_hours"]
        .mean()
    )

    deviation = (
        filtered_df
        .groupby(["agent_id", "priority"])
        ["resolution_time_hours"]
        .mean()
        .reset_index()
    )

    deviation["Expected"] = deviation["priority"].map(expected)

    deviation["Deviation"] = (
        deviation["resolution_time_hours"]
        - deviation["Expected"]
    )

    st.subheader("Agent Deviation from Expected Resolution Time")

    st.dataframe(
        deviation.sort_values(
            "Deviation",
            ascending=False
        ),
        use_container_width=True
    )



# =====================================================
# TAB 4 : CUSTOMER INSIGHTS
# =====================================================

with tab4:

    st.header("😊 Customer Insights")

    st.markdown("""
    **Business Question 3**

    Which customers have

    - Frequent reopened tickets?

    - Low CSAT?
    """)

    customer = (
        filtered_df
        .groupby("customer_id")
        .agg(
            Tickets=("ticket_id", "count"),
            Avg_CSAT=("csat_score", "mean"),
            Reopened=("status",
                      lambda x: (x == "Reopened").sum())
        )
        .reset_index()
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Top Reopened Customers")

        st.dataframe(
            customer.sort_values(
                "Reopened",
                ascending=False
            ).head(10),
            use_container_width=True
        )

    with col2:

        st.subheader("Lowest CSAT Customers")

        st.dataframe(
            customer.sort_values(
                "Avg_CSAT"
            ).head(10),
            use_container_width=True
        )

    st.info(
        """
        Customers with both

        • High reopened tickets

        • Low CSAT

        should be investigated first.

        Compare these customers with

        - assigned agents

        - issue category

        to identify the root cause.
        """
    )



# =====================================================
# TAB 5 : DATA QUALITY
# =====================================================

with tab5:

    st.header("🧹 Data Quality Report")

    st.markdown("""
    **Business Question 4**

    Before trusting the analysis,
    let's evaluate the data quality.
    """)

    quality = pd.DataFrame({

        "Issue":[
            "Missing Values",
            "Duplicate Ticket IDs",
            "Missing Resolution Time",
            "Missing CSAT",
            "Negative Resolution Time"
        ],

        "Count":[
            filtered_df.isna().sum().sum(),
            filtered_df.duplicated(
                subset="ticket_id"
            ).sum(),
            filtered_df["resolution_time_hours"]
                .isna()
                .sum(),
            filtered_df["csat_score"]
                .isna()
                .sum(),
            (
                filtered_df["resolution_time_hours"] < 0
            ).sum()
        ]

    })

    st.table(quality)

    st.success(
        """
        Data Cleaning Performed

        ✔ Standardized column names

        ✔ Converted dates

        ✔ Removed duplicate tickets

        ✔ Created SLA flag

        ✔ Invalid values excluded from analysis
        """
    )

    # =====================================================
# TAB 6 : WEEKLY KPI
# =====================================================

with tab6:

    st.header("📅 Weekly KPI Monitoring")

    st.markdown("""
    **Business Question 5**

    **If you could track exactly one metric every week to catch support
    problems early, what would it be?**
    """)

    # ------------------------------------------
    # Weekly SLA Breach Trend
    # ------------------------------------------

    weekly_sla = (
        filtered_df
        .groupby(
            pd.Grouper(
                key="created_date",
                freq="W"
            )
        )["sla_flag"]
        .mean()
        .reset_index()
    )

    weekly_sla["SLA Breach %"] = weekly_sla["sla_flag"] * 100

    fig = px.line(
        weekly_sla,
        x="created_date",
        y="SLA Breach %",
        markers=True,
        title="Weekly SLA Breach Rate"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------
    # Weekly Ticket Volume
    # ------------------------------------------

    weekly_volume = (
        filtered_df
        .groupby(
            pd.Grouper(
                key="created_date",
                freq="W"
            )
        )
        .size()
        .reset_index(name="Tickets")
    )

    fig = px.bar(
        weekly_volume,
        x="created_date",
        y="Tickets",
        title="Weekly Ticket Volume"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------
    # Business Recommendation
    # ------------------------------------------

    st.success("""
### 📌 Recommendation

Monitor **Weekly SLA Breach Rate** as the primary KPI.

Why?

- It highlights operational issues before CSAT drops.
- It reflects workload and staffing problems.
- It identifies process bottlenecks early.
- It is easy to communicate to stakeholders.
""")

# =====================================================
# DASHBOARD SUMMARY
# =====================================================

st.markdown("---")
st.header("📋 Dashboard Summary")

# Calculate summary values
category_sla = (
    filtered_df.groupby("category")["sla_flag"]
    .mean()
    .reset_index()
)

category_sla["SLA Breach %"] = category_sla["sla_flag"] * 100

region_sla = (
    filtered_df.groupby("region")["sla_flag"]
    .mean()
    .reset_index()
)

region_sla["SLA Breach %"] = region_sla["sla_flag"] * 100

priority_resolution = (
    filtered_df.groupby("priority")["resolution_time_hours"]
    .mean()
    .reset_index()
)

customer_summary = (
    filtered_df.groupby("customer_id")
    .agg(
        Reopened=("status", lambda x: (x == "Reopened").sum()),
        Avg_CSAT=("csat_score", "mean")
    )
    .reset_index()
)

worst_category = category_sla.sort_values(
    "SLA Breach %",
    ascending=False
).iloc[0]

worst_region = region_sla.sort_values(
    "SLA Breach %",
    ascending=False
).iloc[0]

highest_priority = priority_resolution.sort_values(
    "resolution_time_hours"
).iloc[0]

most_reopened = customer_summary.sort_values(
    "Reopened",
    ascending=False
).iloc[0]

lowest_csat = customer_summary.sort_values(
    "Avg_CSAT"
).iloc[0]

st.markdown(f"""
### Key Findings

**1. SLA Performance**
- Worst category: **{worst_category['category']}**
- SLA Breach Rate: **{worst_category['SLA Breach %']:.2f}%**

**2. Regional Performance**
- Worst region: **{worst_region['region']}**
- SLA Breach Rate: **{worst_region['SLA Breach %']:.2f}%**

**3. Resolution Performance**
- Fastest priority: **{highest_priority['priority']}**
- Average Resolution Time: **{highest_priority['resolution_time_hours']:.2f} hours**

**4. Customer Experience**
- Customer with most reopened tickets: **{most_reopened['customer_id']}**
- Customer with lowest CSAT: **{lowest_csat['customer_id']}**

**5. Recommended Weekly KPI**
- ✅ Weekly SLA Breach Rate
""")


    