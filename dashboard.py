import streamlit as st
import pandas as pd

# Load latest predictions
df = pd.read_csv('weekly_predictions.csv')

st.set_page_config(page_title="Pokemon ROI Dashboard", layout="wide")

st.title("🌟 Pokemon ROI Dashboard")

# KPI Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Tracked Cards", value=len(df))

with col2:
    avg_roi = df['expected_roi'].mean() * 100
    st.metric(label="Average ROI", value=f"{avg_roi:.2f}%")

with col3:
    top_card = df.sort_values('expected_roi', ascending=False).iloc[0]
    st.metric(label="Top ROI Card", value=top_card['card_name'], delta=f"{top_card['expected_roi']*100:.2f}%")

# Detailed ROI Table
st.subheader("🔢 Detailed ROI Predictions")
st.dataframe(df.sort_values('expected_roi', ascending=False).reset_index(drop=True))

# Filter: Show cards with ROI > threshold
roi_threshold = st.slider("Filter cards with ROI greater than:", min_value=0, max_value=100, value=20)
filtered_df = df[df['expected_roi'] * 100 > roi_threshold]

st.subheader(f"🔍 Cards with ROI > {roi_threshold}%")
st.table(filtered_df[['card_name', 'current_price', 'expected_roi']].sort_values('expected_roi', ascending=False))

st.caption("© Dylan's Auto ROI System")
