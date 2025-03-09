import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
day_df = pd.read_csv("../data/day.csv")
hour_df = pd.read_csv("../data/hour.csv")

# Convert date column
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Sidebar filters
st.sidebar.header("Filter Data")
start_date, end_date = st.sidebar.date_input("Select Date Range", [day_df["dteday"].min(), day_df["dteday"].max()])

day_df_filtered = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & (day_df["dteday"] <= pd.to_datetime(end_date))]

# Dashboard Title
st.title("Bike Sharing Dashboard")

# Weathersit Analysis
st.subheader("Impact of Weather on Bike Rentals")
weather_stats = day_df_filtered.groupby("weathersit")["cnt"].agg(["mean", "sum", "max", "min"]).reset_index()
st.dataframe(weather_stats)

fig, ax = plt.subplots()
sns.boxplot(x="weathersit", y="cnt", data=day_df_filtered, ax=ax)
ax.set_title("Weather Condition vs Bike Rentals")
st.pyplot(fig)

# Working Day Analysis
st.subheader("Bike Rentals on Working and Non-Working Days")
workingday_stats = day_df_filtered.groupby("workingday")["cnt"].agg(["mean", "sum", "max", "min"]).reset_index()
st.dataframe(workingday_stats)

fig, ax = plt.subplots()
sns.barplot(x="workingday", y="cnt", data=day_df_filtered, ax=ax)
ax.set_title("Bike Rentals on Working vs Non-Working Days")
st.pyplot(fig)

# Weekday Analysis
st.subheader("Bike Rentals by Day of the Week")
weekday_rentals = day_df_filtered.groupby("weekday")["cnt"].agg(["mean", "sum", "max", "min"]).reset_index()
st.dataframe(weekday_rentals)

fig, ax = plt.subplots()
sns.lineplot(x="weekday", y="mean", data=weekday_rentals, marker='o', color='skyblue', ax=ax)
ax.set_title("Average Bike Rentals per Day of the Week")
st.pyplot(fig)

# Seasonal Analysis
st.subheader("Seasonal Bike Rental Trends")
agg_data = day_df_filtered.groupby("season").agg({"casual": ["sum", "mean"], "registered": ["sum", "mean"]})
st.dataframe(agg_data)

fig, axes = plt.subplots(2, 2, figsize=(12, 6))

sns.barplot(x=agg_data.index, y=agg_data["casual"]["sum"], color='skyblue', ax=axes[0, 0])
axes[0, 0].set_title("Total Casual Users by Season")

sns.barplot(x=agg_data.index, y=agg_data["registered"]["sum"], color='lightgreen', ax=axes[0, 1])
axes[0, 1].set_title("Total Registered Users by Season")

sns.barplot(x=agg_data.index, y=agg_data["casual"]["mean"], color='orange', ax=axes[1, 0])
axes[1, 0].set_title("Average Casual Users by Season")

sns.barplot(x=agg_data.index, y=agg_data["registered"]["mean"], color='coral', ax=axes[1, 1])
axes[1, 1].set_title("Average Registered Users by Season")

plt.tight_layout()
st.pyplot(fig)
