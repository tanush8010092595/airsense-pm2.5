
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
import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
from predict_pm25 import predict_pm25

st.set_page_config(page_title="AirSense - PM2.5 Monitor", layout="wide")

# Load Data
cities_df = pd.read_csv("global_cities.csv")
aod_df = pd.read_csv("aod_data.csv")
sample_df = pd.read_csv("sample_pm25_data.csv")

st.title("🌍 AirSense: Real-Time Satellite-Based Air Pollution Dashboard")

# Sidebar - User Input
st.sidebar.header("🔍 Select Location & Date")
selected_city = st.sidebar.selectbox("Choose a City", cities_df["city"].unique())
selected_date = st.sidebar.date_input("Select a Date")

# Get coordinates
coords = cities_df[cities_df["city"] == selected_city].iloc[0]
lat, lon = coords["latitude"], coords["longitude"]

# Match AOD value
selected_date_str = selected_date.strftime("%Y-%m-%d")
aod_match = aod_df[(aod_df["city"] == selected_city) & (aod_df["date"] == selected_date_str)]

if not aod_match.empty:
    aod_value = aod_match["AOD"].values[0]
    st.sidebar.success(f"AOD auto-filled: {aod_value}")
    pm25 = predict_pm25(aod_value)
    st.sidebar.info(f"Predicted PM2.5: {pm25:.2f} µg/m³")
else:
    st.sidebar.warning("AOD data not found for selected city/date.")
    aod_value = None
    pm25 = None

# Layout
col1, col2 = st.columns(2)

# Chart 1 - PM2.5 Trend (Line Chart)
with col1:
    st.subheader(f"📈 PM2.5 Trend in {selected_city}")
    trend_df = sample_df.copy()
    trend_df["datetime"] = pd.to_datetime(trend_df["datetime"])
    fig_line = px.line(trend_df, x="datetime", y="PM2.5", markers=True,
                       color_discrete_sequence=["red"], labels={"PM2.5": "PM2.5 (µg/m³)"},
                       title="Hourly PM2.5 Variation")
    st.plotly_chart(fig_line, use_container_width=True)

# Chart 2 - PM2.5 Comparison (Bar Chart)
with col2:
    st.subheader("📊 PM2.5 by City")
    bar_data = aod_df.copy()
    bar_data["PM2.5"] = bar_data["AOD"].apply(predict_pm25)
    fig_bar = px.bar(bar_data, x="city", y="PM2.5", color="PM2.5",
                     color_continuous_scale="rdylgn_r", title="Predicted PM2.5 by City")
    st.plotly_chart(fig_bar, use_container_width=True)

# Map - Global Pollution Visualization
st.subheader("🗺️ Global PM2.5 Map")
map_data = bar_data.merge(cities_df, on="city", how="left")
map_layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_data,
    get_position='[longitude, latitude]',
    get_fill_color='[255, (1 - PM2.5 / 150) * 255, 0, 160]',
    get_radius="PM2.5 * 100",
    pickable=True
)
view_state = pdk.ViewState(latitude=20.0, longitude=78.0, zoom=1.4)
st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/light-v9",
                         initial_view_state=view_state, layers=[map_layer]))

st.caption("🔬 Data Source: Simulated INSAT AOD & Sample PM2.5 | Built for ISRO Hackathon 2025")

# Plot past data
st.line_chart(df[["datetime", "PM2.5"]].set_index("datetime"))
