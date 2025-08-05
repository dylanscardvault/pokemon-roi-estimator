from src.data_loader import scrape_ebay_prices
from src.feature_engineering import create_features
from src.model import train_model
from email.message import EmailMessage
import smtplib
import pandas as pd

# Step 1: Define card names to monitor
card_names = ["Charizard V", "Pikachu Holo", "Blastoise EX", "Eevee Promo", "Mewtwo GX"]

# Step 2: Scrape live prices from eBay
card_data = []
for card in card_names:
    prices = scrape_ebay_prices(card)
    if prices:
        avg_price = sum(prices) / len(prices)
        card_data.append({
            "card_name": card,
            "current_price": avg_price,
            "price_30d_ago": avg_price * 0.9,  # simulate 10% increase
            "psa_population": 300,
            "is_holo": "charizard" in card.lower() or "pikachu" in card.lower(),
            "rarity": "Rare",
            "card_age_days": 300
        })

# Step 3: Convert to DataFrame
df = pd.DataFrame(card_data)

# Step 4: Feature engineering
df = create_features(df)

# Step 5: Train model
features = ["price_30d_ago", "psa_population", "card_age_days", "rarity_score"]
X = df[features]
y = df["current_price"]
model = train_model(X, y)

# Step 6: Predict future price and ROI
df["predicted_price"] = model.predict(X)
df["expected_roi"] = (df["predicted_price"] - df["current_price"]) / df["current_price"]

# Step 7: Send alerts
def send_email_alert(card_name, roi):
    msg = EmailMessage()
    msg.set_content(f"🚨 Undervalued card: {card_name}\nExpected ROI: {roi:.2%}")
    msg["Subject"] = "Pokemon ROI Alert"
    msg["From"] = "your_email@gmail.com"
    msg["To"] = "your_email@gmail.com"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("your_email@gmail.com", "your_app_password")  # Use an App Password
        smtp.send_message(msg)

# Trigger alerts for ROI > 25%
for _, row in df.iterrows():
    if row["expected_roi"] > 0.25:
        send_email_alert(row["card_name"], row["expected_roi"])

# Save predictions
df.to_csv("data/processed/weekly_predictions.csv", index=False)
print("✅ Weekly ROI predictions saved and alerts sent.")
