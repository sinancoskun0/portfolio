import numpy as np


def compute_daily_returns(prices: np.ndarray) -> np.ndarray:
    return np.diff(prices) / prices[:-1]


def summary_stats(simulated_prices: np.ndarray) -> dict:
    final_prices = simulated_prices[-1]

    return {
        "mean_final_price": float(np.mean(final_prices)),
        "median_final_price": float(np.median(final_prices)),
        "5th_percentile": float(np.percentile(final_prices, 5)),
        "95th_percentile": float(np.percentile(final_prices, 95)),
    }
