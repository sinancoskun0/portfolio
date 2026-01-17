import matplotlib.pyplot as plt
import numpy as np


def plot_simulations(simulations: np.ndarray, num_paths: int = 100):
    plt.figure(figsize=(10, 6))
    plt.plot(simulations[:, :num_paths], alpha=0.2)
    plt.title("Monte Carlo Stock Price Simulation")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.show()


def plot_distribution(simulations: np.ndarray):
    final_prices = simulations[-1]
    plt.figure(figsize=(8, 5))
    plt.hist(final_prices, bins=50)
    plt.title("Distribution of Final Prices")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.show()
