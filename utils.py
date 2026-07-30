import pandas as pd
import numpy as np


# Load and Clean Data
def load_data(file='customer_tickets.csv'):
    

    df = pd.read_csv(file)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # Convert dates
    df["created_date"] = pd.to_datetime(
        df["created_date"], errors="coerce"
    )

    df["resolved_date"] = pd.to_datetime(
        df["resolved_date"], errors="coerce"
    )

    # SLA flag
    df["sla_flag"] = (
        df["sla_breached"]
        .astype(str)
        .str.lower()
        .eq("yes")
    )

    # Remove duplicate ticket IDs
    df = df.drop_duplicates(subset="ticket_id")

    # Remove invalid resolution time
    df.loc[
        df["resolution_time_hours"] < 0,
        "resolution_time_hours",
    ] = np.nan

    return df



# KPI Metrics

def get_kpis(df):

    total_tickets = len(df)

    sla_rate = df["sla_flag"].mean() * 100

    avg_resolution = df["resolution_time_hours"].mean()

    avg_csat = df["csat_score"].mean()

    reopened = (
        (df["status"] == "Reopened").mean() * 100
    )

    return {
        "Total Tickets": total_tickets,
        "SLA Breach %": round(sla_rate, 2),
        "Avg Resolution": round(avg_resolution, 2),
        "Avg CSAT": round(avg_csat, 2),
        "Reopened %": round(reopened, 2),
    }



# SLA by Category

def sla_by_category(df):

    return (
        df.groupby("category")
        .agg(
            Tickets=("ticket_id", "count"),
            SLA_Breach_Rate=("sla_flag", "mean"),
            Avg_Resolution=(
                "resolution_time_hours",
                "mean",
            ),
        )
        .reset_index()
        .sort_values(
            "SLA_Breach_Rate",
            ascending=False,
        )
    )



# SLA by Region

def sla_by_region(df):

    return (
        df.groupby("region")
        .agg(
            Tickets=("ticket_id", "count"),
            SLA_Breach_Rate=("sla_flag", "mean"),
            Avg_Resolution=(
                "resolution_time_hours",
                "mean",
            ),
        )
        .reset_index()
        .sort_values(
            "SLA_Breach_Rate",
            ascending=False,
        )
    )



# Priority Analysis

def priority_resolution(df):

    return (
        df.groupby("priority")
        .agg(
            Avg_Resolution=(
                "resolution_time_hours",
                "mean",
            ),
            Tickets=("ticket_id", "count"),
        )
        .reset_index()
    )



# Agent Performance

def agent_performance(df):

    return (
        df.groupby("agent_id")
        .agg(
            Tickets=("ticket_id", "count"),
            Avg_Resolution=(
                "resolution_time_hours",
                "mean",
            ),
            Avg_CSAT=("csat_score", "mean"),
            SLA_Breach=("sla_flag", "mean"),
        )
        .reset_index()
    )



# Agent Deviation

def agent_deviation(df):

    expected = (
        df.groupby("priority")[
            "resolution_time_hours"
        ]
        .mean()
    )

    actual = (
        df.groupby(
            ["agent_id", "priority"]
        )["resolution_time_hours"]
        .mean()
        .reset_index()
    )

    actual["Expected"] = actual[
        "priority"
    ].map(expected)

    actual["Deviation"] = (
        actual["resolution_time_hours"]
        - actual["Expected"]
    )

    return actual.sort_values(
        "Deviation",
        ascending=False,
    )



# Customer Analysis

def customer_summary(df):

    return (
        df.groupby("customer_id")
        .agg(
            Tickets=("ticket_id", "count"),
            Avg_CSAT=("csat_score", "mean"),
            Reopened=(
                "status",
                lambda x: (x == "Reopened").sum(),
            ),
        )
        .reset_index()
        .sort_values(
            ["Reopened", "Avg_CSAT"],
            ascending=[False, True],
        )
    )



# Weekly SLA Trend

def weekly_sla(df):

    weekly = (
        df.groupby(
            pd.Grouper(
                key="created_date",
                freq="W",
            )
        )["sla_flag"]
        .mean()
        .reset_index()
    )

    weekly.rename(
        columns={
            "sla_flag": "SLA_Breach_Rate"
        },
        inplace=True,
    )

    return weekly



# Data Quality Report

def data_quality(df):

    report = pd.DataFrame(
        {
            "Issue": [
                "Duplicate Tickets",
                "Missing Values",
                "Missing Resolution Time",
                "Missing CSAT",
                "Negative Resolution Time",
            ],
            "Count": [
                df.duplicated(
                    subset="ticket_id"
                ).sum(),
                df.isnull().sum().sum(),
                df[
                    "resolution_time_hours"
                ].isna().sum(),
                df["csat_score"]
                .isna()
                .sum(),
                (
                    df[
                        "resolution_time_hours"
                    ]
                    < 0
                ).sum(),
            ],
        }
    )

    return report
