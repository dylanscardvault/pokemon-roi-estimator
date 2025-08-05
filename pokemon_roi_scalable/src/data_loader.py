import pandas as pd
import random

def load_card_list():
    return pd.read_csv('data/card_master_list.csv')

def simulate_price_scraping(card_name):
    current_price = round(random.uniform(20, 150), 2)
    price_30d_ago = current_price * random.uniform(0.8, 0.95)
    return current_price, price_30d_ago
