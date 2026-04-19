import streamlit as st
import csv
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

st.title("💸 Smart Expense Tracker")

# ---------------- ADD EXPENSE ----------------
st.header("Add Expense")

amount = st.number_input("Amount", min_value=0.0)
category = st.selectbox("Category", ["Food", "Travel", "Rent", "Shopping", "Other"])
date = st.date_input("Date")
note = st.text_input("Note")

if st.button("Add"):
    if amount == 0 or not category:
        st.error("Please fill all fields properly")
    else:
        with open("expenses.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([amount, category, str(date), note])
        st.success("Expense Added!")

# ---------------- VIEW + FILTER ----------------
st.header("All Expenses")

try:
    df = pd.read_csv("expenses.csv", header=None)
    df.columns = ["Amount", "Category", "Date", "Note"]

    # convert date
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # remove bad rows
    df = df.dropna(subset=["Date"])

    # ---- MONTH FILTER ----
    months = df["Date"].dt.to_period("M").astype(str).unique()
    selected_month = st.selectbox("Select Month", months)

    filtered_df = df[df["Date"].dt.to_period("M").astype(str) == selected_month]

    # clean date display
    filtered_df["Date"] = filtered_df["Date"].dt.date

    # ---------------- TABLE WITH DELETE ----------------
    st.subheader("All Expenses")

    # Header
    col1, col2, col3, col4, col5, col6 = st.columns([1,2,2,2,2,1])
    col1.write("ID")
    col2.write("Amount")
    col3.write("Category")
    col4.write("Date")
    col5.write("Note")
    col6.write("Delete")

    for i, row in filtered_df.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([1,2,2,2,2,1])

        col1.write(i)
        col2.write(row["Amount"])
        col3.write(row["Category"])
        col4.write(row["Date"])
        col5.write(row["Note"])

        # 🗑️ Delete Button
        if col6.button("🗑️", key=f"del_{i}"):
            df = df.drop(i)
            df.to_csv("expenses.csv", index=False, header=False)
            st.rerun()

    # ---------------- TOTAL ----------------
    st.subheader("💰 Total Expense (Selected Month)")
    st.write(f"₹ {filtered_df['Amount'].sum():.2f}")

    # ---------------- BAR CHART ----------------
    st.subheader("📊 Category-wise Spending")
    st.bar_chart(filtered_df.groupby("Category")["Amount"].sum())

    # ---------------- PIE CHART ----------------
    st.subheader("🥧 Expense Distribution")
    st.pyplot(filtered_df.groupby("Category")["Amount"].sum().plot.pie(autopct="%1.1f%%").figure)

    # ---------------- ML PREDICTION ----------------
    st.subheader("📈 Next Month Expense Prediction")

    monthly = df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum().reset_index()
    monthly["Date"] = monthly["Date"].astype(str)

    if len(monthly) > 1:
        monthly["MonthIndex"] = range(len(monthly))

        X = monthly["MonthIndex"].values.reshape(-1, 1)
        y = monthly["Amount"].values

        model = LinearRegression()
        model.fit(X, y)

        next_month = np.array([[len(monthly)]])
        prediction = model.predict(next_month)

        st.success(f"Estimated Expense for Next Month: ₹ {prediction[0]:.2f}")
    else:
        st.warning("Not enough data for prediction")

except FileNotFoundError:
    st.warning("No data found. Please add expenses first.")