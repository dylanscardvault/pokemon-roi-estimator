import pandas as pd
from src.data_loader import load_card_list, simulate_price_scraping

# Load card master list
cards = load_card_list()

# Simulate scraping prices & ROI calculation
card_data = []
for _, row in cards.iterrows():
    current_price, price_30d_ago = simulate_price_scraping(row['card_name'])
    roi = (current_price - price_30d_ago) / price_30d_ago
    card_data.append({ 'card_name': row['card_name'], 'current_price': current_price, 'price_30d_ago': price_30d_ago, 'expected_roi': roi })

df = pd.DataFrame(card_data)
df.to_csv('data/processed/weekly_predictions.csv', index=False)
print("✅ Predictions saved for dashboard.")
