import numpy as np

from src.data_loader import load_price_data
from src.statistics import compute_daily_returns, summary_stats
from src.monte_carlo import simulate_prices
from src.visualization import plot_simulations, plot_distribution


CSV_PATH = "data/AAPL.csv"
NUM_DAYS = 252
NUM_SIMULATIONS = 10_000


def main():
    prices = load_price_data(CSV_PATH)
    returns = compute_daily_returns(prices.values)

    simulations = simulate_prices(
        start_price=prices.iloc[-1],
        daily_returns=returns,
        num_days=NUM_DAYS,
        num_simulations=NUM_SIMULATIONS
    )

    stats = summary_stats(simulations)

    for k, v in stats.items():
        print(f"{k}: {v:.2f}")

    plot_simulations(simulations)
    plot_distribution(simulations)


if __name__ == "__main__":
    main()
