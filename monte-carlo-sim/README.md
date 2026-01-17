# 📈 Monte Carlo Stock Price Simulation

A Monte Carlo simulation of stock prices using real historical market data, focused on distributional outcomes, uncertainty, and risk.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?logo=matplotlib&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest&logoColor=white)
![tqdm](https://img.shields.io/badge/tqdm-Progress%20Bars-FFC107)

---

## 📊 Output

The simulation generates thousands of possible future price paths based on historical return statistics.

Key outputs:
- Simulated price paths over a fixed horizon
- Distribution of final prices
- Summary statistics (mean, median, tail percentiles)

Typical visualizations include:
- Overlaid Monte Carlo paths
- Histogram of terminal prices

---

## 🧠 Model Overview

### Data Source

- Real historical daily stock data
- Loaded from a local CSV (no APIs, no scraping)
- Only closing prices are required; additional fields are preserved for extensibility

### Return Model

Daily arithmetic returns are computed as: [ r_t = (P_t - P_{t-1}) / P_{t-1} ]


The simulation assumes returns are:
- Independent
- Identically distributed
- Normally distributed

Mean and standard deviation are estimated from historical data.

---

### Monte Carlo Process

For each simulation path:

1. Sample daily returns from `𝒩(μ, σ)`
2. Apply returns multiplicatively to price
3. Repeat for `T` trading days

[ P_t = P_{t-1} × (1 + r_t) ]


Thousands of paths are generated to approximate the future price distribution.

A progress bar (`tqdm`) is used to make long simulations observable and debuggable.

---

## 📈 Summary Statistics

After simulation, terminal prices are analyzed:

| Statistic | Description |
|---------|-------------|
| Mean | Expected final price |
| Median | 50th percentile outcome |
| 5th Percentile | Downside tail risk |
| 95th Percentile | Upside tail outcome |

These metrics are useful for:
- Scenario analysis
- Risk intuition
- Comparing model assumptions

---

## 🚀 Quick Start

### Installation

```bash
# From portfolio repository root
cd projects/monte-carlo-stock-sim

python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux / Mac

pip install -r requirements.txt



