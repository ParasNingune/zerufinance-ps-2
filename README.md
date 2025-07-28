# Compound Protocol Risk Scoring Analysis

This project analyzes wallet transaction data from Compound V2/V3 protocol to generate risk scores for wallet addresses.


## 📌 Features

- ✅ Fetches historical transactions from Etherscan
- ✅ Normalizes Ethereum wallet addresses
- ✅ Applies a logarithmic risk scoring algorithm
- ✅ Outputs results in a clean CSV file
- ✅ Handles API rate limits gracefully

---

## 🧠 Risk Scoring Logic

The risk score is based on the number of transactions a wallet has performed:

```python
if tx_count == 0:
    return 100
elif tx_count < 5:
    return 200
else:
    score = 300 + 150 * math.log10(tx_count)
    return min(int(score), 950)

```

## Quick Start

### Run Python Script
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your Etherscan API key to .env file
echo "ETHERSCAN_API_KEY=your_api_key_here" > .env

# 3. Run the main script
python main.py
```

## 📁 Project Structure

```
zerufinance-ps-2/
├── data/
│   └── wallets.csv            # Input wallet addresses (first column only)
├── output/
│   └── wallet_scores.csv      # Output with wallet, tx_count, risk_score
├── main.py                    # Main script
└── README.md                  # This file
└── .env                     # API keys (create this file)
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/eth-risk-scoring.git
cd eth-risk-scoring
```

### 2. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. API Setup
Create `.env` file with your API keys:
```env
ETHERSCAN_API_KEY=your_etherscan_api_key
```

### 4. Prepare Input File
Place your wallet addresses in a file: data/wallets.csv
Only the first column will be read, and all addresses will be normalized.
Example:
```bash
0x742d35Cc6634C0532925a3b844Bc454e4438f44e
0x53d284357ec70cE289D6D64134DfAc8E511c8a3D
...
```

### 5. Run the Script
```bash
python3 main.py
```
## Output Format

**CSV file with columns:**
| wallet                                     | tx\_count | risk\_score |
| ------------------------------------------ | --------- | ----------- |
| 0x742d35Cc6634C0532925a3b844Bc454e4438f44e | 154       | 793         |
| ...                                        | ...       | ...         |


## 🚨 Dependencies

- Python 3.8+
- pandas, numpy (data processing)
- requests (API calls)
- jupyter (interactive analysis)