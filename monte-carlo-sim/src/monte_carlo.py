import numpy as np
from tqdm import trange


def simulate_prices(
        start_price: float,
        daily_returns: np.ndarray,
        num_days: int,
        num_simulations: int
) -> np.ndarray:
    simulations = np.zeros((num_days, num_simulations))
    simulations[0] = start_price

    mean = np.mean(daily_returns)
    std = np.std(daily_returns)

    for t in trange(1, num_days, desc="Running Monte Carlo"):
        random_returns = np.random.normal(mean, std, num_simulations)
        simulations[t] = simulations[t - 1] * (1 + random_returns)

    return simulations
