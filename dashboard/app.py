import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.preprocess import clean_data, feature_engineering
from src.analysis import get_metrics, monthly_spending, top_merchants, txn_type
from src.auth import create_users_table, register_user, login_user
from src.model import train_model, predict_category
from rag_system.ai_assistant import answer_question

# ---------- PAGE CONFIG ---------- #
st.set_page_config(page_title="Smart Expense Analyzer", layout="wide")

create_users_table()

# ---------- AUTH ---------- #
st.sidebar.title("🔐 Authentication")
menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# LOGIN
if choice == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("Invalid credentials")

# REGISTER
elif choice == "Register":
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Register"):
        if register_user(new_user, new_pass):
            st.success("Account created")
        else:
            st.warning("User already exists")

if not st.session_state["logged_in"]:
    st.stop()

# ---------- HEADER ---------- #
col1, col2 = st.columns([8,2])
with col1:
    st.title("💰 Smart Expense Analyzer")
    st.write(f"👋 Welcome {st.session_state['username']}")
with col2:
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

# ---------- FILE UPLOAD ---------- #
file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)
    df = clean_data(df)
    df = feature_engineering(df)

    # ---------- ML CATEGORY ---------- #
    model, vec = train_model(df)
    df["category"] = df["description"].apply(lambda x: predict_category(model, vec, x))

    # ---------- FILTERS ---------- #
    st.sidebar.header("Filters")

    start = st.sidebar.date_input("Start", df["date"].min())
    end = st.sidebar.date_input("End", df["date"].max())

    filtered = df[(df["date"]>=pd.to_datetime(start)) & (df["date"]<=pd.to_datetime(end))]

    # ---------- METRICS ---------- #
    total, avg, mx = get_metrics(filtered)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total", f"₹{total:,.0f}")
    c2.metric("Average", f"₹{avg:,.0f}")
    c3.metric("Max", f"₹{mx:,.0f}")

    st.markdown("---")

    # ---------- CHARTS ---------- #
    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("Monthly Trend")
        monthly = monthly_spending(filtered)
        fig, ax = plt.subplots(figsize=(3,2))
        monthly.plot(ax=ax)
        st.pyplot(fig)

    with col2:
        st.caption("Top Merchants")
        fig, ax = plt.subplots(figsize=(3,2))
        top_merchants(filtered).plot(kind="bar", ax=ax)
        st.pyplot(fig)

    with col3:
        st.caption("Category Split")
        fig, ax = plt.subplots(figsize=(3,2))
        filtered["category"].value_counts().plot(kind="pie", ax=ax)
        st.pyplot(fig)

    st.markdown("---")

    # ---------- AI ---------- #
    q = st.text_input("Ask AI")

    if q:
        st.success(answer_question(filtered, q))

    # ---------- DOWNLOAD ---------- #
    st.download_button("Download CSV", filtered.to_csv(index=False))