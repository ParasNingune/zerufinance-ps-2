import os
import time
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import math

# --- Configuration ---
API_KEY = os.getenv("ETHERSCAN_API_KEY")
RATE_LIMIT = 0.2

# --- Utility Functions ---
def normalize_address(addr):
    return addr.lower() if addr.startswith("0x") else "0x" + addr.lower()

def load_wallets(file_path):
    try:
        df = pd.read_csv(file_path)
        return df.iloc[:, 0].apply(normalize_address).tolist()
    except Exception as e:
        print(f"Error loading wallets: {e}")
        return []

def safe_request(url, params):
    time.sleep(RATE_LIMIT)
    params['apikey'] = API_KEY
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        if data.get('status') != '1':
            print(f"API error for {params.get('address')} — Message: {data.get('message')}, Result: {data.get('result')}")
        return data.get('result', []) if data.get('status') == '1' else []
    except Exception as e:
        print(f"API request failed: {e}")
        return []

def get_tx_count(address):
    url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc"
    }
    txs = safe_request(url, params)
    print(f"Fetched {len(txs)} transactions for {address}")
    return len(txs)

# --- Risk Scoring Logic ---
def assign_risk_score(tx_count):
    if tx_count == 0:
        return 100
    elif tx_count < 5:
        return 200
    else:
        score = 300 + 150 * math.log10(tx_count)
        return min(int(score), 950)


def main():
    print("📊 Compound Risk Scoring Started")

    input_file = "data/wallets.csv"
    output_file = "output/wallet_scores.csv"

    if not os.path.exists(input_file):
        print("Wallets file not found.")
        return

    os.makedirs("output", exist_ok=True)
    wallets = load_wallets(input_file)
    results = []

    for i, wallet in enumerate(wallets):
        print(f"[{i+1}/{len(wallets)}] Processing {wallet}")
        tx_count = get_tx_count(wallet)
        score = assign_risk_score(tx_count)
        results.append({'wallet': wallet, 'tx_count': tx_count, 'risk_score': score})

    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)

    print("\nRisk scoring completed!")
    print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    main()
