import numpy as np
from src.monte_carlo import simulate_prices


def test_simulation_shape():
    returns = np.random.normal(0.001, 0.01, 100)
    sim = simulate_prices(100, returns, 50, 1000)
    assert sim.shape == (50, 1000)
