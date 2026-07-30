import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px


conn = sqlite3.connect(
    "jobs.db"
)

df = pd.read_sql(
    "SELECT * FROM jobs",
    conn
)

st.set_page_config(
    page_title="AI Job Agent",
    layout="wide"
)

st.title(
    "🚀 AI Job Agent Dashboard"
)

status_filter = st.selectbox(
    "Status",
    [
        "all",
        "applied",
        "failed",
        "pending"
    ]
)

if status_filter != "all":

    df = df[
        df["status"]
        == status_filter
    ]

st.divider()

# metrics

col1, col2, col3, col4 = st.columns(4)

applied = len(
    df[df["status"] == "applied"]
)

failed = len(
    df[df["status"] == "failed"]
)

pending = len(
    df[df["status"] == "pending"]
)

interviews = len(
    df[df["interview"] == 1]
)

col1.metric(
    "Applied",
    applied
)

col2.metric(
    "Failed",
    failed
)

col3.metric(
    "Pending",
    pending
)

col4.metric(
    "Interviews",
    interviews
)

st.divider()

status_count = (
    df["status"]
    .value_counts()
    .reset_index()
)

fig = px.pie(
    status_count,
    values="count",
    names="status",
    title="Application Results"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader(
    "Job Match Scores"
)

st.bar_chart(
    df["score"]
)

st.divider()

# Interview rate calculation
if len(df) > 0 and "interview" in df.columns:
    total_applied = len(df[df["status"] == "applied"])
    total_interviews = len(df[df["interview"] == 1])
    
    if total_applied > 0:
        interview_rate = (total_interviews / total_applied) * 100
        st.metric(
            "Interview Rate",
            f"{interview_rate:.1f}%",
            help=f"{total_interviews} interviews from {total_applied} applications"
        )

st.divider()

st.subheader(
    "Job Applications"
)

st.dataframe(df)

st.divider()

st.subheader(
    "System Logs"
)

try:

    with open(
        "job_agent.log",
        "r"
    ) as f:

        logs = f.read()

    st.text_area(
        "Logs",
        logs,
        height=300
    )

except:
    st.warning(
        "No logs found."
    )