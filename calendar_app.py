import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Event Calendar", layout="wide")

st.title("📅 Basic Event Calendar")

# Initialize session state to store events
if "events" not in st.session_state:
    st.session_state["events"] = []

# --- Input Section ---
st.subheader("Add New Event")
with st.form("event_form"):
    title = st.text_input("Event Title", placeholder="e.g. Presidential Debate")
    date = st.date_input("Event Date", value=datetime.today())
    category = st.selectbox(
        "Category",
        ["Politics", "Finance", "Tech", "Culture", "Sports", "Holidays", "War/Crisis", "Other"]
    )
    source_url = st.text_input("Source URL (optional)", placeholder="https://...")
    submitted = st.form_submit_button("Add Event")

    if submitted:
        st.session_state["events"].append({
            "Title": title.strip(),
            "Date": date.strftime('%Y-%m-%d'),
            "Category": category,
            "Source URL": source_url.strip()
        })
        st.success("✅ Event added!")

# --- Display Section ---
st.subheader("📋 Upcoming Events")
if st.session_state["events"]:
    df = pd.DataFrame(st.session_state["events"])
    df = df.sort_values("Date")
    st.dataframe(df, use_container_width=True)
else:
    st.info("No events have been added yet.")
