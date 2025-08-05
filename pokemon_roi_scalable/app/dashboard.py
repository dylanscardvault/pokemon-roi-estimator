import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pokemon ROI Dashboard", layout="wide")
st.title("🌟 Pokemon ROI Dashboard (Scalable Version)")

df = pd.read_csv('data/processed/weekly_predictions.csv')

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Tracked Cards", value=len(df))
with col2:
    st.metric(label="Average ROI", value=f"{df['expected_roi'].mean()*100:.2f}%")
with col3:
    top_card = df.sort_values('expected_roi', ascending=False).iloc[0]
    st.metric(label="Top ROI Card", value=top_card['card_name'], delta=f"{top_card['expected_roi']*100:.2f}%")

st.subheader("🔢 Detailed ROI Predictions")
roi_threshold = st.slider("Show cards with ROI >", 0, 100, 20)
filtered_df = df[df['expected_roi']*100 > roi_threshold]
st.dataframe(filtered_df.sort_values('expected_roi', ascending=False))
