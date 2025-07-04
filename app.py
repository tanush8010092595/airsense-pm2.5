
import streamlit as st
import pandas as pd
from predict_pm25 import predict_pm25

# Load sample past data
df = pd.read_csv("sample_pm25_data.csv")

# Title
st.title("AirSense - Real-time PM2.5 Prediction Platform")

# Dropdown for city search (from data)
cities = ["New York", "Delhi", "Beijing", "London", "Tokyo", "Mumbai", "Paris"]
city = st.selectbox("Select a city", cities)

# AOD input for prediction
aod = st.slider("Enter AOD value to predict PM2.5", 0.1, 2.0, 0.5, 0.01)

# Predict button
if st.button("Predict PM2.5"):
    result = predict_pm25(aod)
    st.success(f"Predicted PM2.5 concentration for {city}: {result:.2f} µg/m³")

# Show past data table
st.subheader("📊 Past PM2.5 Data (sample)")
st.dataframe(df.head(20))

# Plot past data
st.line_chart(df[["datetime", "PM2.5"]].set_index("datetime"))
