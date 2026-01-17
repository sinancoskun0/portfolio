# Monte Carlo Stock Price Simulation

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![NumPy](https://img.shields.io/badge/NumPy-✔-informational?style=flat-square)
![Pandas](https://img.shields.io/badge/Pandas-✔-informational?style=flat-square)
![Matplotlib](https://img.shields.io/badge/Matplotlib-✔-informational?style=flat-square)
![Pytest](https://img.shields.io/badge/Pytest-✔-informational?style=flat-square)
![tqdm](https://img.shields.io/badge/tqdm-✔-informational?style=flat-square)

A simple, reproducible Monte Carlo simulation of stock prices using **real historical data stored locally**.

---

## Features

- Monte Carlo simulation using historical daily returns
- Real stock data loaded from CSV
- Summary stats (mean, median, percentiles)
- Visualizations of paths and final distribution
- Progress bar for long simulations (`tqdm`)
- Unit tests with `pytest`

---

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

